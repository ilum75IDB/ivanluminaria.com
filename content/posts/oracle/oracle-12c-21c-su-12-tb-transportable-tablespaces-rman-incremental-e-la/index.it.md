---
title: "Oracle 12c → 21c su 12 TB: transportable tablespaces, RMAN incremental e la finestra del sabato notte"
seoTitle: "Migrazione Oracle 12c → 21c: 12 TB in 4 ore di downtime"
description: "Strategia ibrida con transportable tablespaces e RMAN incremental per migrare 12 TB da Oracle 12c a 21c. Piano passo per passo, tempi reali, problemi nascosti."
date: 2099-12-31
draft: true
translationKey: "oracle_12c_21c_su_12_tb_transportable_tablespaces_rman_incremental_e_la"
tags: ["migration", "upgrade", "rman", "transportable-tablespaces", "oracle-21c"]
categories: ["oracle"]
image: "oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la.cover.jpg"
webo_status: da_approvare
webo_generated_at: 2026-09-04
---

## Il sabato notte che nessuno vuole

La richiesta era arrivata qualche settimana prima, in una di quelle riunioni dove i numeri vengono presentati come se fossero dettagli: "dobbiamo migrare il database Oracle da 12c a 21c, c'è una finestra di manutenzione il sabato notte, quattro ore". Dodici terabyte. Server con otto anni di vita, fuori supporto hardware. Il nuovo server già in rack, Oracle 21c installato, pronto.

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

1. **Fase preparatoria** (giorni prima della finestra): copia dei datafile in modalità read-only via TTS, trasferimento sul nuovo server
2. **Fase di sincronizzazione** (ore prima della finestra): RMAN incremental backup sul sorgente, restore sul target, per ridurre il gap
3. **Finestra di downtime** (quattro ore): ultimo incremental, conversione finale, apertura del database 21c

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

**Componenti deprecati**: Oracle 21c ha rimosso o deprecato alcune feature di 12c. Lo script `utlupgrd.sql` (o il suo successore `dbupgrade`) genera un report di pre-upgrade [3]:

```bash
# Sul sorgente, con Oracle 21c home già disponibile
$ORACLE_HOME_21C/rdbms/admin/preupgrd.sql
```

Il report segnala oggetti invalidi, parametri obsoleti, componenti da rimuovere prima dell'upgrade. Tra i più comuni nel passaggio 12c → 21c: `AUDIT_TRAIL` (sostituito da Unified Auditing), `SQLNET.ALLOWED_LOGON_VERSION` (deprecato), e alcune viste di compatibilità.

**Tablespace SYSTEM e SYSAUX**: non sono trasportabili. Rimangono sul sorgente e vengono ricreati sul target tramite il processo di upgrade standard.

---

## Il piano passo per passo

### Fase 1 — Preparazione TTS (giorni prima)

Si mettono in read-only le tablespace da trasportare (escluse SYSTEM, SYSAUX, TEMP, UNDO):

```sql
-- Sul sorgente
ALTER TABLESPACE data_01 READ ONLY;
ALTER TABLESPACE data_02 READ ONLY;
ALTER TABLESPACE idx_01 READ ONLY;
-- ripetere per tutte le tablespace applicative
```

Si verifica la self-containment — nessun oggetto nelle tablespace da trasportare deve avere dipendenze su oggetti fuori da esse:

```sql
EXECUTE DBMS_TTS.TRANSPORT_SET_CHECK('DATA_01,DATA_02,IDX_01', TRUE);
SELECT * FROM transport_set_violations;
```

Se `transport_set_violations` è vuota, si procede con l'export del metadata:

```bash
expdp system/*** TRANSPORT_TABLESPACES=DATA_01,DATA_02,IDX_01 \
  TRANSPORT_FULL_CHECK=Y \
  DUMPFILE=tts_export.dmp \
  LOGFILE=tts_export.log
```

I datafile fisici vengono copiati sul nuovo server via `rsync` o storage replication. Con dodici terabyte su rete 10GbE, il trasferimento richiede circa tre-quattro ore. Nel frattempo il database sorgente continua a girare: le tablespace in read-only ricevono solo letture, le scritture vanno sulle tablespace ancora in read-write (SYSTEM, SYSAUX, eventuali tablespace applicative escluse dal TTS).

### Fase 2 — Sincronizzazione incrementale

Nelle ore successive al trasferimento iniziale, le tablespace sorgente vengono rimesse in read-write (il database deve tornare operativo). Da questo momento in poi, le modifiche si accumulano come delta da sincronizzare.

Si configura RMAN per backup incrementale level 0 sul sorgente:

```bash
rman target /
BACKUP INCREMENTAL LEVEL 0 TABLESPACE DATA_01,DATA_02,IDX_01
FORMAT '/backup/rman/incr0_%U'
TAG 'PRE_MIGRATION_L0';
```

Questo backup level 0 viene trasferito sul target e applicato ai datafile già copiati:

```bash
# Sul target (21c)
rman target /
CATALOG START WITH '/backup/rman/';
RECOVER TABLESPACE DATA_01,DATA_02,IDX_01
FROM TAG 'PRE_MIGRATION_L0';
```

Nelle ore successive, si eseguono backup incrementali level 1 periodici per ridurre progressivamente il gap. Ogni level 1 è solo il delta dall'ultimo backup — pochi gigabyte invece di terabyte.

### Fase 3 — La finestra di quattro ore

Ore 23:00, sabato. Il database sorgente viene messo in modalità restricted:

```sql
ALTER SYSTEM ENABLE RESTRICTED SESSION;
```

Si esegue l'ultimo backup incrementale level 1:

```bash
rman target /
BACKUP INCREMENTAL LEVEL 1 TABLESPACE DATA_01,DATA_02,IDX_01
FORMAT '/backup/rman/incr1_final_%U'
TAG 'FINAL_SYNC';
```

Questo backup contiene solo le modifiche delle ultime ore — tipicamente pochi gigabyte. Trasferimento sul target e apply:

```bash
# Sul target
RECOVER TABLESPACE DATA_01,DATA_02,IDX_01
FROM TAG 'FINAL_SYNC';
```

Le tablespace vengono messe in read-only sul sorgente (definitivamente questa volta), e si importa il metadata TTS sul target:

```bash
impdp system/*** TRANSPORT_DATAFILES='/u01/oradata/data_01.dbf','/u01/oradata/data_02.dbf' \
  DUMPFILE=tts_export.dmp \
  LOGFILE=tts_import.log
```

A questo punto le tablespace sono sul target in Oracle 21c. Si esegue il processo di upgrade del dizionario dati:

```bash
$ORACLE_HOME/bin/dbupgrade -d $ORACLE_BASE/diag/rdbms -l /tmp/upgrade_log
```

---

## Quello che i manuali non dicono

Quattro problemi che si trovano solo quando si è già dentro la finestra.

**Password file format**: Oracle 21c usa un formato di password file diverso da 12c. Se si copia il password file dal sorgente, l'istanza 21c potrebbe non riconoscerlo. La soluzione è rigenerarlo sul target prima dell'apertura:

```bash
orapwd file=$ORACLE_HOME/dbs/orapwORCL password=<sys_password> format=12.2
```

**Unified Auditing**: in Oracle 21c, Unified Auditing è abilitato per default e non disabilitabile come in 12c. Se il database sorgente usava il vecchio `AUDIT_TRAIL=DB`, le policy di audit vanno ricreate nel nuovo framework. Questo non blocca la migrazione, ma può sorprendere il team applicativo il lunedì mattina quando i log di audit hanno un formato diverso.

**Auto-Indexing**: Oracle 21c ha Auto-Indexing abilitabile (era introdotto in 19c). Se non si vuole che Oracle inizi a creare indici automaticamente sul nuovo database, va disabilitato esplicitamente:

```sql
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE','OFF');
```

**Conversione a PDB**: Oracle 21c supporta ancora i database non-CDB, ma è l'ultima versione a farlo. Se il piano futuro prevede la conversione a CDB/PDB (obbligatoria da Oracle 23c in poi), è il momento di valutarlo. La conversione non-CDB → PDB si fa con `DBMS_PDB.DESCRIBE` e richiede una finestra separata — non va infilata nella stessa notte.

---

## I numeri della notte

| Fase | Durata reale |
|---|---|
| Export TTS metadata | 12 minuti |
| Trasferimento datafile (11,8 TB via rsync su 10GbE) | 3h 40min |
| Backup RMAN level 0 | 1h 15min |
| Apply level 0 sul target | 48 minuti |
| Backup RMAN level 1 (delta ~180 GB) | 22 minuti |
| Apply level 1 finale | 14 minuti |
| Import TTS metadata sul target | 8 minuti |
| dbupgrade (dizionario dati) | 41 minuti |
| Validazione post-migrazione | 35 minuti |
| **Totale finestra di downtime** | **3h 52min** |

Otto minuti di margine. Non è molto, ma è stato sufficiente.

---

## Validazione: i controlli che non si saltano

Dopo l'apertura del database 21c, la validazione non è opzionale. Quattro controlli nell'ordine giusto.

**Oggetti invalidi**: il processo di upgrade può lasciare oggetti di sistema invalidi. `utl_recomp` li ricompila:

```sql
EXECUTE UTL_RECOMP.RECOMP_SERIAL();
-- oppure parallelo
EXECUTE UTL_RECOMP.RECOMP_PARALLEL(4);
```

**Script di diagnostica post-upgrade**: Oracle fornisce `dbupgdiag.sql` per verificare lo stato del dizionario dati dopo l'upgrade [4]:

```bash
sqlplus / as sysdba @$ORACLE_HOME/rdbms/admin/dbupgdiag.sql
```

**Statistiche optimizer**: le statistiche del dizionario dati vanno rigenerate sul nuovo database. Le statistiche degli oggetti applicativi si possono importare dal sorgente o rigenerare:

```sql
EXECUTE DBMS_STATS.GATHER_DICTIONARY_STATS;
EXECUTE DBMS_STATS.GATHER_FIXED_OBJECTS_STATS;
```

**Verifica componenti**: tutti i componenti Oracle devono essere in stato `VALID`:

```sql
SELECT comp_name, version, status FROM dba_registry ORDER BY comp_name;
```

Qualsiasi componente in stato `INVALID` o `UPGRADED` (invece di `VALID`) richiede attenzione prima di dichiarare la migrazione completata.

---

## Quello che resta del runbook

La migrazione è andata. Il database 21c è in produzione da lunedì mattina, gli applicativi non si sono accorti di nulla — o quasi: un paio di query con hint obsoleti hanno richiesto revisione nei giorni successivi, perché l'optimizer 21c ha statistiche più accurate e sceglie piani diversi.

Il punto che vale la pena portarsi via non è la tecnica specifica — TTS più RMAN incremental è una strategia documentata, non un'invenzione. È il ragionamento che precede la scelta: capire perché Data Pump non funziona a quella scala, capire quali sono i vincoli reali (finestra, spazio, versioni), e scegliere la combinazione di strumenti che rispetta quei vincoli.

La parte più lunga non è stata la notte del sabato. È stata la settimana prima: i pre-check, i test sul target con un subset di dati, la simulazione del processo di upgrade su un clone, la verifica che ogni passo del runbook producesse l'output atteso. Quando si arriva alla finestra di quattro ore con un runbook già testato, le sorprese sono gestibili. Quando si arriva senza averlo testato, quelle otto ore di margine diventano zero molto in fretta.

---

## Fonti ufficiali

1. Oracle Database Backup and Recovery User's Guide 21c — [Transportable Tablespaces](https://docs.oracle.com/en/database/oracle/oracle-database/21/bradv/rman-transporting-data-across-platforms.html)
2. Oracle Database Administrator's Guide 21c — [Transporting Tablespaces Between Databases](https://docs.oracle.com/en/database/oracle/oracle-database/21/admin/transporting-data.html)
3. Oracle Database Upgrade Guide 21c — [Pre-Upgrade Information Tool](https://docs.oracle.com/en/database/oracle/oracle-database/21/upgrd/using-preupgrade-information-tool-for-oracle-database.html)
4. Oracle Database Upgrade Guide 21c — [Post-Upgrade Status Tool](https://docs.oracle.com/en/database/oracle/oracle-database/21/upgrd/post-upgrade-status-tool-postupgrade-fixups-script.html)

---

## Glossario candidato

- **Transportable Tablespaces (TTS)** — tecnica Oracle che permette di spostare tablespace tra database copiando i datafile fisici e importando solo il metadata tramite Data Pump. Molto più veloce di un export/import completo su grandi volumi.

- **RMAN Incremental Backup** — backup RMAN che registra solo i blocchi modificati dall'ultimo backup di livello uguale o superiore. Level 0 è la base completa, level 1 è il delta. Usato in migrazione per sincronizzare il gap tra copia iniziale e finestra di downtime.

- **dbupgrade** — utility Oracle (successore di `catupgrd.sql`) che aggiorna il dizionario dati di sistema durante un upgrade di versione. Ricompila i componenti interni e porta il database al livello della nuova versione Oracle installata.

- **Unified Auditing** — framework di auditing Oracle introdotto in 12c e obbligatorio in 21c, che consolida tutti i log di audit (database, fine-grained, SYSDBA) in un'unica struttura `AUDSYS`. Sostituisce il vecchio parametro `AUDIT_TRAIL`.

- **Auto-Indexing** — funzionalità Oracle (disponibile da 19c, configurabile in 21c) che analizza il workload e crea automaticamente indici invisibili, li valida, e li rende visibili se migliorano le performance. Va disabilitato esplicitamente se non desiderato in produzione.
