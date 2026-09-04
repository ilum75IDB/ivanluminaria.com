---
categories:
- oracle
date: 2099-12-31
description: Strategia ibrida con transportable tablespaces e RMAN incremental per
  migrare 12 TB da Oracle 12c a 21c. Piano passo per passo, tempi reali, problemi
  nascosti.
draft: true
image: oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la.cover.jpg
seoTitle: 'Migrazione Oracle 12c → 21c: 12 TB in 4 ore di downtime'
tags:
- migration
- upgrade
- rman
- transportable-tablespaces
- oracle-21c
title: 'Oracle 12c → 21c su 12 TB: transportable tablespaces, RMAN incremental e la
  finestra del sabato notte'
translationKey: oracle_12c_21c_su_12_tb_transportable_tablespaces_rman_incremental_e_la
webo_generated_at: 2026-09-04
webo_status: da_approvare
---

## Il sabato notte che nessuno vuole

La richiesta era arrivata qualche settimana prima, in una di quelle riunioni dove i numeri vengono presentati come se fossero dettagli: "dobbiamo migrare il database Oracle da 12.2 a 21c, c'è una finestra di manutenzione il sabato notte, quattro ore". Dodici terabyte. Server con otto anni di vita, fuori supporto hardware. Il nuovo server già in rack, Oracle 21c installato — un CDB, perché in 21c non c'è altra scelta, e su questo torniamo fra poco.

Quattro ore per dodici terabyte.

Chi lavora con Oracle da un po' sa già dove sta il problema: non nel database, non nella versione, non nel nuovo hardware. Sta nella matematica. Un Data Pump su dodici terabyte, anche con parallelismo aggressivo e storage veloce, non finisce in quattro ore. Non finisce in otto. Probabilmente non finisce nel weekend.

Quello che segue è il ragionamento che ha portato a una strategia ibrida — transportable tablespaces cross-version più RMAN incremental — e i dettagli di cosa è successo davvero nelle quattro ore critiche. I numeri sono quelli reali, i comandi sono quelli usati, i problemi sono quelli che si trovano solo quando si è già dentro.

---

## Perché Data Pump non è la risposta a questa scala

Data Pump è lo strumento giusto per migrazioni fino a qualche centinaio di gigabyte, o per export/import selettivi di schemi specifici. Oltre quella soglia, i limiti diventano strutturali.

Su dodici terabyte, il problema principale è il throughput di I/O. Data Pump esporta i dati serializzando righe in formato proprietario Oracle, poi le reimporta ricostruendo segmenti, indici, statistiche. Anche con `PARALLEL=16` e storage NVMe su entrambi i lati, il throughput effettivo raramente supera i 3-4 GB/minuto in scenari reali (non benchmark). Dodici terabyte a 4 GB/minuto: cinquanta ore. Ottimisticamente.

C'è poi il problema dello spazio: serve un'area di staging che contenga l'intero export, più lo spazio sul target durante l'import. Con dodici terabyte di dati, si parla di venti-venticinque terabyte di spazio temporaneo necessario tra le due macchine.

L'ultimo problema è la finestra: Data Pump non è incrementale. Se l'export parte venerdì sera e il database continua a ricevere scritture, al termine dell'export i dati sono già parzialmente obsoleti. Non esiste un meccanismo nativo per sincronizzare le modifiche avvenute durante l'export.

---

## Le opzioni reali per migrazioni multi-terabyte

Quando Data Pump è fuori gioco, le alternative reali sono quattro [1]:

**RMAN Duplicate** — duplica il database completo via RMAN, inclusi tutti i file fisici. Richiede spazio doppio sul target (o quasi), ma è affidabile e ben documentato. Il problema: per dodici terabyte, anche la fase di copia iniziale richiede molte ore, e non risolve il problema della finestra breve.

**Transportable Tablespaces (TTS)** — copia i file datafile direttamente, senza serializzazione/deserializzazione. È il metodo più veloce per spostare grandi volumi perché il throughput è limitato solo dalla velocità del canale di trasferimento (rete, storage condiviso, nastro). Il vincolo storico era l'endianness: piattaforme diverse (es. Solaris SPARC → Linux x86) richiedevano una conversione. Tra due Linux x86_64, il problema non esiste [2].

**Data Guard come ponte** — si configura una standby database sulla nuova macchina, si lascia che la sincronizzazione avvenga via redo log (ore o giorni, senza impatto sul primario), poi si esegue un failover controllato nella finestra di manutenzione. Elegante, ma richiede che le versioni siano compatibili per il redo shipping — e tra 12c e 21c ci sono vincoli precisi.

**GoldenGate** — replica logica, massima flessibilità cross-version e cross-platform. Richiede licenza separata, setup non banale, e un periodo di warm-up per la sincronizzazione iniziale. Per una migrazione one-shot con finestra definita, è spesso sovradimensionato.

---

## La strategia scelta: TTS + RMAN incremental

La soluzione adottata combina due tecniche: transportable tablespaces per spostare la massa dei dati prima della finestra, e RMAN incremental backup per sincronizzare le modifiche accumulate nel frattempo.

L'idea di fondo è semplice: se non posso spostare dodici terabyte in quattro ore, sposto undici terabyte e mezzo nei giorni precedenti, e nelle quattro ore critiche sposto solo il delta.

Il piano si articola in tre fasi:

1. **Fase preparatoria** (giorni prima della finestra): backup RMAN level 0 trasportabile **a database aperto e in scrittura**, trasferimento sul nuovo server, restore come foreign datafile copy
2. **Fase di sincronizzazione** (giorni e ore prima della finestra): level 1 incrementali, sempre a database operativo, per ridurre progressivamente il gap
3. **Finestra di downtime** (quattro ore): tablespace in read-only, ultimo incrementale, plug-in dei metadati nella PDB, apertura

La differenza fra questo piano e quello che verrebbe istintivo — mettere le tablespace in read-only, copiarle con calma, poi allinearle — è tutta nel primo punto, ed è la ragione per cui la clausola `ALLOW INCONSISTENT` esiste.

---

## Pre-check: quello che si scopre prima di toccare qualcosa

Prima di muovere un byte, serve un'analisi di compatibilità. Tra Oracle 12.2 e Oracle 21c ci sono quasi dieci anni di versioni intermedie, e alcune cose sono cambiate in modo non retro-compatibile.

**Character set**: verificare che source e target usino lo stesso character set, o che il target sia un superset. Una migrazione TTS tra AL32UTF8 e WE8ISO8859P1 richiede conversione esplicita e non è banale.

```sql
-- Sul database sorgente (12c)
SELECT value FROM nls_database_parameters WHERE parameter = 'NLS_CHARACTERSET';
SELECT value FROM nls_database_parameters WHERE parameter = 'NLS_NCHAR_CHARACTERSET';
```

**Endianness**: su Linux x86_64 → Linux x86_64 non ci sono problemi. Su migrazioni cross-platform (es. AIX → Linux), serve `RMAN CONVERT TABLESPACE`.

```sql
-- Verifica platform
SELECT platform_name, endian_format FROM v$transportable_platform
WHERE endian_format = (SELECT endian_format FROM v$database);
```

**Architettura di destinazione**: è il vincolo che decide la forma di tutta la migrazione, e conviene scoprirlo prima di ordinare il server, non la settimana prima della finestra. **In Oracle 21c l'architettura non-CDB è desupportata**: multitenant è l'unica architettura supportata [3]. Un 12.2 non-CDB non diventa un 21c non-CDB, perché quel bersaglio non esiste più — diventa una **PDB dentro un CDB 21c**. Non è un dettaglio di packaging: cambia dove atterrano le tablespace, come si apre il database, e quali comandi si usano nella finestra.

**Componenti deprecati**: il report di pre-upgrade non si genera più con uno script SQL. Da Oracle 21c il Pre-Upgrade Information Tool (`preupgrade.jar`) non è più distribuito, e le sue funzioni sono confluite in **AutoUpgrade** [4]:

```bash
# Con la home 21c disponibile — sola analisi, non modifica nulla
java -jar $ORACLE_HOME_21C/rdbms/admin/autoupgrade.jar \
  -preupgrade "target_version=21,dir=/tmp/preupg" -mode analyze
```

Il report segnala oggetti invalidi, parametri obsoleti, componenti da rimuovere prima dell'upgrade. Tra i più comuni nel passaggio 12.2 → 21c: `SQLNET.ALLOWED_LOGON_VERSION` (deprecato), alcune viste di compatibilità, e le policy di audit — sull'auditing torniamo più avanti, perché è il punto su cui circola più disinformazione.

`-mode analyze` è a sola lettura: si può lanciare in produzione, in orario di lavoro, settimane prima. È la cosa che conviene fare per prima, ed è quella che quasi sempre si fa troppo tardi.

**Tablespace SYSTEM e SYSAUX**: non sono trasportabili. Restano sul sorgente; sul target il dizionario è quello della PDB, creato dal CDB.

---

## Il piano passo per passo

Il punto da cui dipende tutto: **le tablespace restano in lettura e scrittura fino all'ultimo passo**. È esattamente il motivo per cui esiste il backup incrementale `FOR TRANSPORT`: il read-only serve solo per il backup finale, quello che chiude la finestra. Chi mette le tablespace in read-only all'inizio, per copiarle con calma nei giorni precedenti, ha appena spostato il downtime — non lo ha ridotto: un'applicazione che non può scrivere è ferma, che il database sia aperto o no.

### Fase 1 — Copia iniziale a caldo (giorni prima)

Prima di tutto la self-containment: nessun oggetto nelle tablespace da trasportare deve dipendere da oggetti fuori da esse.

```sql
-- Sul sorgente
EXECUTE DBMS_TTS.TRANSPORT_SET_CHECK('DATA_01,DATA_02,IDX_01', TRUE);
SELECT * FROM transport_set_violations;
```

Se `transport_set_violations` è vuota si procede. Il backup level 0 si prende **a database aperto e in scrittura**, con `FOR TRANSPORT ALLOW INCONSISTENT` [1]: è la clausola che autorizza RMAN a produrre un backset trasportabile da tablespace non consistenti fra loro, che verranno riallineate dagli incrementali successivi.

```bash
rman target /
BACKUP INCREMENTAL LEVEL 0
  FOR TRANSPORT ALLOW INCONSISTENT
  TABLESPACE DATA_01, DATA_02, IDX_01
  FORMAT '/backup/rman/xtts_l0_%U';
```

Il backset viene trasferito sul nuovo server via `rsync` o storage replication. Con dodici terabyte su rete 10GbE il trasferimento richiede circa tre-quattro ore. **Nel frattempo il database sorgente lavora normalmente**: nessuna tablespace è in read-only, le applicazioni scrivono, e le modifiche che si accumulano sono esattamente il delta che gli incrementali recupereranno.

Sul target, i datafile si materializzano come *foreign datafile copy*:

```bash
# Sul target (CDB 21c, connesso alla PDB di destinazione)
rman target /
RESTORE FOREIGN TABLESPACE DATA_01, DATA_02, IDX_01 TO NEW
  FROM BACKUPSET '/backup/rman/xtts_l0_1_1';
```

### Fase 2 — Sincronizzazione incrementale

Nei giorni che separano la copia iniziale dalla finestra si eseguono uno o più level 1, sempre a database in scrittura. Ogni giro riduce il gap: il primo incrementale può valere qualche centinaio di gigabyte, l'ultimo prima della finestra tipicamente poche decine.

```bash
# Sul sorgente — database sempre operativo
BACKUP INCREMENTAL LEVEL 1
  FOR TRANSPORT ALLOW INCONSISTENT
  TABLESPACE DATA_01, DATA_02, IDX_01
  FORMAT '/backup/rman/xtts_l1_%U';
```

Sul target ogni backset si applica ai foreign datafile copy già presenti, **uno per volta e nell'ordine in cui è stato prodotto**:

```bash
# Sul target — un solo backupset per RECOVER
RECOVER FOREIGN DATAFILECOPY '/u02/oradata/pdb1/data_01.dbf',
                             '/u02/oradata/pdb1/data_02.dbf',
                             '/u02/oradata/pdb1/idx_01.dbf'
  FROM BACKUPSET '/backup/rman/xtts_l1_2_1';
```

Attenzione a una limitazione che non si scopre leggendo, ma sbattendoci contro: **non si possono applicare più backupset in un solo `RECOVER`**. Ogni incrementale è un comando a sé, in sequenza. Uno script che li accoda in un unico comando fallisce, e lo fa nel momento peggiore.

### Fase 3 — La finestra di quattro ore

Ore 23:00, sabato. Il sorgente viene chiuso alle applicazioni:

```sql
ALTER SYSTEM ENABLE RESTRICTED SESSION;
```

**Solo adesso** le tablespace vanno in read-only — è il passaggio che congela i dati e apre la finestra:

```sql
ALTER TABLESPACE data_01 READ ONLY;
ALTER TABLESPACE data_02 READ ONLY;
ALTER TABLESPACE idx_01 READ ONLY;
-- ripetere per tutte le tablespace applicative
```

L'ultimo incrementale si prende adesso, **senza** `ALLOW INCONSISTENT` (le tablespace ora sono consistenti) e con `DATAPUMP FORMAT`, che fa produrre a RMAN anche il dump dei metadati insieme al backset:

```bash
rman target /
BACKUP INCREMENTAL LEVEL 1
  FOR TRANSPORT
  DATAPUMP FORMAT '/backup/rman/xtts_meta.bck'
  TABLESPACE DATA_01, DATA_02, IDX_01
  FORMAT '/backup/rman/xtts_l1_final_%U';
```

Contiene solo le modifiche delle ultime ore — tipicamente pochi gigabyte. Trasferimento sul target e apply finale:

```bash
# Sul target
RECOVER FOREIGN DATAFILECOPY '/u02/oradata/pdb1/data_01.dbf',
                             '/u02/oradata/pdb1/data_02.dbf',
                             '/u02/oradata/pdb1/idx_01.dbf'
  FROM BACKUPSET '/backup/rman/xtts_l1_final_3_1';
```

Resta il plug-in dei metadati nella PDB di destinazione. Data Pump vuole un *directory object* — non un path del filesystem — e la lista completa dei datafile:

```sql
-- Sul target, dentro la PDB
CREATE DIRECTORY dump_dir AS '/backup/rman';
```

```bash
impdp system/***@pdb1 \
  DIRECTORY=dump_dir \
  DUMPFILE=tts_export.dmp \
  LOGFILE=tts_import.log \
  TRANSPORT_TABLESPACES=DATA_01,DATA_02,IDX_01 \
  TRANSPORT_DATAFILES='/u02/oradata/pdb1/data_01.dbf','/u02/oradata/pdb1/data_02.dbf','/u02/oradata/pdb1/idx_01.dbf'
```

Il `DUMPFILE` è quello prodotto sul sorgente con l'export dei metadati TTS, che si lancia dopo aver messo le tablespace in read-only:

```bash
# Sul sorgente, a tablespace già read-only
expdp system/*** \
  DIRECTORY=dump_dir \
  DUMPFILE=tts_export.dmp \
  LOGFILE=tts_export.log \
  TRANSPORT_TABLESPACES=DATA_01,DATA_02,IDX_01 \
  TRANSPORT_FULL_CHECK=Y
```

A questo punto le tablespace sono nella PDB, che si apre e si rimette in scrittura:

```sql
ALTER PLUGGABLE DATABASE pdb1 OPEN;
ALTER TABLESPACE data_01 READ WRITE;
ALTER TABLESPACE data_02 READ WRITE;
ALTER TABLESPACE idx_01 READ WRITE;
```

Nessun `dbupgrade` in questo percorso: il dizionario dati non viene migrato, perché è quello della PDB — creato già a livello 21c dal CDB che la ospita. È una differenza che vale la pena tenere a mente quando si confrontano i tempi con quelli di un upgrade in place, dove invece l'upgrade del dizionario è la fase che domina.

---

## Quello che i manuali non dicono

Quattro problemi che si trovano solo quando si è già dentro la finestra.

**Password file**: il formato in sé non cambia — `12.2` è il default sia in 12.2 sia in 21c. Quello che cambia è la tolleranza: in 21c il parametro `IGNORECASE` è desupportato e i password file sono sempre case-sensitive [6]. Un password file ereditato da un ambiente che conviveva con password case-insensitive smette di far entrare gli utenti amministrativi, e succede al primo `sqlplus sys as sysdba` da remoto — cioè nel momento peggiore. Si rigenera sul target prima dell'apertura:

```bash
orapwd file=$ORACLE_HOME/dbs/orapwCDB1 password=<sys_password> format=12.2
```

**Auditing, e cosa si legge in giro**: la versione che circola è "in 21c l'auditing tradizionale non c'è più". Non è così, e la differenza conta quando si pianifica. In 21c il default resta il **mixed mode** — unified auditing attivo insieme all'auditing tradizionale — esattamente come da 12c in poi; l'auditing tradizionale è **deprecato** in 21c e **desupportato** solo da 23c [5]. Il *pure* unified auditing non è un parametro: si ottiene rilinkando il binario Oracle con `uniaud_on` e riavviando l'istanza. Tradotto in pratica: la migrazione non obbliga a rifare le policy di audit quella notte, ma il conto arriva alla release dopo — e conviene mettere la conversione a piano, non scoprirla quando è obbligatoria.

**Auto-Indexing**: Oracle 21c ha Auto-Indexing abilitabile (era introdotto in 19c). Se non si vuole che Oracle inizi a creare indici automaticamente sul nuovo database, va disabilitato esplicitamente:

```sql
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE','OFF');
```

**Il CDB non è un'opzione da rimandare**: chi arriva da 12.2 tende a trattare multitenant come una decisione architetturale da prendere con calma, magari alla release successiva. In 21c quella calma non c'è: il non-CDB è desupportato, quindi la destinazione è una PDB e basta. La conseguenza operativa è che il CDB va creato e collaudato **prima** della finestra, con il suo `db_name`, i suoi parametri di memoria, i suoi servizi — e vanno riportati nella PDB gli oggetti che nel vecchio database vivevano fuori dalle tablespace trasportate: profili, ruoli, utenti, directory object, DB link, job dello scheduler. Non viaggiano col TTS, e sono la voce che più spesso si scopre mancante il lunedì mattina.

---

## I numeri della notte

La distinzione che conta è fra ciò che è successo **prima**, a database in produzione, e ciò che è successo **dentro** la finestra. Solo la seconda tabella è downtime.

**Fuori finestra — database aperto, applicazioni operative**

| Fase | Durata |
|---|---|
| Backup RMAN level 0 `FOR TRANSPORT ALLOW INCONSISTENT` | 1h 15min |
| Trasferimento backset (11,8 TB via rsync su 10GbE) | 3h 40min |
| `RESTORE FOREIGN TABLESPACE` sul target | 48 min |
| Level 1 intermedi dei giorni successivi + apply | 1h 05min |
| **Totale lavoro preparatorio** | **6h 48min** |

**Dentro la finestra — downtime applicativo**

| Fase | Durata |
|---|---|
| Restricted session + tablespace in read-only | 9 min |
| Ultimo level 1 `FOR TRANSPORT` + `DATAPUMP` (delta ~180 GB) | 22 min |
| Export metadati TTS sul sorgente | 12 min |
| Trasferimento delta + dump sul target | 25 min |
| `RECOVER FOREIGN DATAFILECOPY` finale | 18 min |
| `impdp` plug-in dei metadati nella PDB | 12 min |
| Apertura PDB + tablespace in read-write | 4 min |
| Ricreazione oggetti non trasportati (utenti, ruoli, DB link, job) | 35 min |
| Statistiche dizionario + ricompilazione oggetti invalidi | 45 min |
| Validazione e smoke test applicativo | 50 min |
| **Totale finestra di downtime** | **3h 52min** |

Otto minuti di margine sulle quattro ore. Non è molto, ma è stato sufficiente.

Vale la pena guardare le due tabelle insieme: il lavoro totale è stato quasi undici ore, di cui meno di quattro visibili all'utente. Non abbiamo reso veloce la migrazione — l'abbiamo spostata quasi tutta fuori dalla finestra. È l'unica cosa che questo metodo sa fare, ed è tutto ciò che serviva.

---

## Validazione: i controlli che non si saltano

Dopo l'apertura della PDB, la validazione non è opzionale. Quattro controlli nell'ordine giusto — tutti da eseguire **dentro la PDB**, non nel root del CDB, altrimenti si sta guardando il database sbagliato:

```sql
ALTER SESSION SET CONTAINER = pdb1;
```

**Oggetti invalidi**: il plug-in dei metadati può lasciare oggetti applicativi invalidi, tipicamente per dipendenze verso oggetti non ancora ricreati. `utl_recomp` li ricompila:

```sql
EXECUTE UTL_RECOMP.RECOMP_SERIAL();
-- oppure parallelo
EXECUTE UTL_RECOMP.RECOMP_PARALLEL(4);
```

**Violazioni del plug-in**: è il controllo specifico di questo percorso, e non ha equivalente in un upgrade in place. `PDB_PLUG_IN_VIOLATIONS` elenca ciò che il CDB ha trovato di incompatibile quando ha accolto la PDB — opzioni non installate, parametri sotto la soglia, componenti mancanti:

```sql
SELECT name, cause, type, status, message
FROM pdb_plug_in_violations
WHERE status <> 'RESOLVED'
ORDER BY time;
```

Le righe di tipo `ERROR` vanno risolte prima di dichiarare chiusa la migrazione; quelle `WARNING` vanno lette una per una, non archiviate in blocco.

**Statistiche optimizer**: le statistiche del dizionario vanno rigenerate. Le statistiche degli oggetti applicativi si possono importare dal sorgente o rigenerare:

```sql
EXECUTE DBMS_STATS.GATHER_DICTIONARY_STATS;
EXECUTE DBMS_STATS.GATHER_FIXED_OBJECTS_STATS;
```

**Verifica componenti**: tutti i componenti Oracle devono essere in stato `VALID`:

```sql
SELECT comp_name, version, status FROM dba_registry ORDER BY comp_name;
```

Qualsiasi componente in stato `INVALID` o `UPGRADED` (invece di `VALID`) richiede attenzione prima di dichiarare la migrazione completata. In una PDB appena popolata via TTS il registro riflette il CDB che la ospita: se qualcosa è invalido lì, il problema è del contenitore, non del trasporto.

---

## Quello che resta del runbook

La migrazione è andata. La PDB è in produzione da lunedì mattina, gli applicativi non si sono accorti di nulla — o quasi: un paio di query con hint obsoleti hanno richiesto revisione nei giorni successivi, perché l'optimizer 21c ha statistiche più accurate e sceglie piani diversi.

Il punto che vale la pena portarsi via non è la tecnica specifica — TTS più RMAN incremental è una strategia documentata, non un'invenzione. È il ragionamento che precede la scelta: capire perché Data Pump non funziona a quella scala, capire quali sono i vincoli reali (finestra, spazio, architettura di destinazione), e scegliere la combinazione di strumenti che li rispetta. Il vincolo che ha pesato di più non è stato nemmeno tecnico nel senso stretto: è stato scoprire per tempo che il non-CDB non esisteva più come destinazione. Scoprirlo tardi non allunga la finestra — cambia il progetto.

La parte più lunga non è stata la notte del sabato. È stata la settimana prima: i pre-check con AutoUpgrade, i test sul target con un subset di dati, la prova del plug-in su una PDB di collaudo, la verifica che ogni passo del runbook producesse l'output atteso. Quando si arriva alla finestra di quattro ore con un runbook già testato, le sorprese sono gestibili. Quando si arriva senza averlo testato, quegli otto minuti di margine diventano zero molto in fretta.

---

## Fonti ufficiali

1. Oracle Database Backup and Recovery User's Guide 21c — [Transporting Data Across Platforms](https://docs.oracle.com/en/database/oracle/oracle-database/21/bradv/rman-transporting-data-across-platforms.html) (`BACKUP … FOR TRANSPORT ALLOW INCONSISTENT`, `RESTORE FOREIGN TABLESPACE`, `RECOVER FOREIGN DATAFILECOPY`)
2. Oracle Database Administrator's Guide 21c — [Transporting Tablespaces Between Databases](https://docs.oracle.com/en/database/oracle/oracle-database/21/admin/transporting-data.html)
3. Oracle Database Upgrade Guide 21c — [Manual Non-CDB Release Upgrades to Multitenant Architecture](https://docs.oracle.com/en/database/oracle/oracle-database/21/upgrd/upgrade-scenarios-non-cdb-oracle-databases.html) (desupporto dell'architettura non-CDB)
4. Oracle Database Upgrade Guide 21c — [Using the Pre-Upgrade Information Tool](https://docs.oracle.com/en/database/oracle/oracle-database/21/upgrd/using-preupgrade-information-tool-for-oracle-database.html) (`preupgrade.jar` non più distribuito, funzioni confluite in AutoUpgrade)
5. Oracle Database Security Guide 21c — [Introduction to Auditing](https://docs.oracle.com/en/database/oracle/oracle-database/21/dbseg/introduction-to-auditing.html) (mixed mode di default, `uniaud_on` per il pure unified auditing)
6. Oracle Database Administrator's Reference 21c — [Creating and Populating Password Files](https://docs.oracle.com/en/database/oracle/oracle-database/21/ntqrf/creating-and-populating-password-files.html) (`format`, desupporto di `IGNORECASE`)

---

## Glossario
- **[Transportable Tablespaces (TTS)](/it/glossary/transportable-tablespaces/)** — tecnica Oracle che permette di spostare tablespace tra database copiando i datafile fisici e importando solo il metadata tramite Data Pump. Molto più veloce di un export/import completo su grandi volumi.

- **RMAN Incremental Backup** — backup RMAN che registra solo i blocchi modificati dall'ultimo backup di livello uguale o superiore. Level 0 è la base completa, level 1 è il delta. Usato in migrazione per sincronizzare il gap tra copia iniziale e finestra di downtime.

- **AutoUpgrade** — utility Java (`autoupgrade.jar`) che da Oracle 21c è lo strumento unico per analisi pre-upgrade, correzioni e upgrade vero e proprio. Con `-preupgrade … -mode analyze` produce a sola lettura il report che prima si otteneva con `preupgrade.jar`, non più distribuito.

- **Foreign datafile copy** — datafile che RMAN materializza sul database di destinazione a partire da un backset trasportabile, prima che le tablespace vengano agganciate. È l'oggetto su cui agiscono `RESTORE FOREIGN TABLESPACE` e `RECOVER FOREIGN DATAFILECOPY` nel trasporto incrementale.

- **Unified Auditing** — framework di auditing introdotto in 12c che consolida i log (database, fine-grained, SYSDBA) nella struttura `AUDSYS`. In 21c convive con l'auditing tradizionale in *mixed mode*, che resta il default; il *pure* unified auditing richiede il relink del binario con `uniaud_on`.

- **Auto-Indexing** — funzionalità Oracle (disponibile da 19c, configurabile in 21c) che analizza il workload e crea automaticamente indici invisibili, li valida, e li rende visibili se migliorano le performance. Va disabilitato esplicitamente se non desiderato in produzione.
