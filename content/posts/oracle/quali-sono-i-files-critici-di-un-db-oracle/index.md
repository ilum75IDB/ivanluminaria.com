---
title: "ORA-00205 alle tre di notte: capire i file critici Oracle prima di averne bisogno"
date: 2099-12-31
draft: true
section: oracle
webo_status: da_approvare
webo_generated_at: 2026-06-07
---
## La chiamata delle tre di notte

Era una finestra di manutenzione pianificata su storage — il tipo di attività che di solito va liscia perché l'hai fatta decine di volte. Un grande gruppo farmaceutico italiano, sistemi Oracle 19c che gestiscono tracciabilità dei lotti e compliance regolatoria. Il team storage aveva completato il lavoro nei tempi previsti. Poi era arrivato il momento di riavviare l'istanza.

L'istanza non era ripartita.

Il messaggio nell'alert log era questo:

```text
ORA-00205: error in identifying control file
  '/u01/app/oracle/oradata/PHARMDB/control01.ctl'
```

Chi conosce la sequenza di startup Oracle sa già, leggendo quella riga, dove guardare e cosa chiedere al team storage. Chi non la conosce passa i successivi venti minuti a fare ipotesi nel buio — rete, listener, OS, permessi — prima di arrivare al punto reale.

Questo articolo parte da quella situazione. Non per raccontare un'impresa, ma perché è il contesto più onesto per spiegare perché certi file Oracle non sono "importanti": sono **necessari**. Senza di loro, il database non tenta nemmeno di avviarsi.

---

## La sequenza di startup: quando viene letto cosa

Prima di entrare nei singoli file, vale la pena capire la sequenza con cui Oracle avvia un'istanza. Non è un dettaglio accademico — è la mappa che permette di capire perché un file mancante blocca tutto il resto.

Oracle avvia un database in tre fasi distinte [1]:

**`NOMOUNT`** — Oracle alloca la SGA (System Global Area) e avvia i processi in background. Per farlo, legge il **parameter file** (SPFILE o PFILE). In questa fase Oracle non sa ancora nulla del database fisico: sa solo come configurare l'istanza in memoria.

**`MOUNT`** — Oracle legge il **control file**. In questa fase l'istanza "scopre" la struttura fisica del database: quali datafile esistono, dove si trovano, qual è la SCN corrente, qual è lo stato dei redo log. Solo dopo il MOUNT Oracle sa cosa sta gestendo.

**`OPEN`** — Oracle verifica la consistenza degli **online redo log files** e dei datafile, applica eventuale recovery se necessario, e apre il database agli utenti.

La conseguenza pratica è immediata: se il parameter file è corrotto o mancante, Oracle non arriva nemmeno al NOMOUNT. Se il control file è inaccessibile, l'istanza si ferma al MOUNT. Se i redo log sono corrotti, il blocco avviene in OPEN o durante le operazioni.

Conoscere questa sequenza significa sapere, leggendo un errore ORA, in quale fase si è fermato tutto — e quindi quale file cercare per primo.

---

## Il Parameter File: SPFILE e PFILE

Il parameter file è il punto di partenza assoluto. Prima ancora di toccare qualsiasi file su disco, Oracle lo legge per sapere come configurare l'istanza: quanta memoria allocare, dove si trovano i control file, qual è il nome del database, qual è la dimensione del blocco.

Esistono due varianti [2]:

**PFILE** (`init<SID>.ora`) — file di testo, modificabile con qualsiasi editor. Semplice da leggere, ma richiede un riavvio per applicare le modifiche. Utile in ambienti di sviluppo o come backup leggibile del parametro.

**SPFILE** (`spfile<SID>.ora`) — file binario, gestito da Oracle stesso. Permette modifiche a caldo con `ALTER SYSTEM SET` senza riavviare l'istanza. In produzione si usa quasi sempre lo SPFILE.

L'ordine di ricerca Oracle è preciso: cerca prima lo SPFILE nel path di default, poi il PFILE, poi un SPFILE con nome specifico se indicato. Su Linux/Unix il path standard è:

```bash
# SPFILE (default)
$ORACLE_HOME/dbs/spfilePHARMDB.ora

# PFILE (fallback)
$ORACLE_HOME/dbs/initPHARMDB.ora
```

Su Windows il path equivalente è `%ORACLE_HOME%\database\SPFILEPHARMD.ORA`.

Per verificare quale parameter file è attualmente in uso su un'istanza attiva:

```sql
-- Se il valore è vuoto, Oracle sta usando un PFILE
SHOW PARAMETER spfile;
```

Se `spfile` restituisce un valore, l'istanza usa lo SPFILE. Se il campo `VALUE` è vuoto, si sta usando un PFILE — informazione utile in fase di diagnostica.

**Perché è critico**: senza parameter file Oracle non sa nemmeno dove cercare il control file. Il parametro `control_files` che indica i path dei control file è contenuto proprio nello SPFILE o nel PFILE. Se questo file manca, l'errore tipico è `ORA-01078` (failure in processing system parameters) o `LRM-00109` (could not open parameter file).

---

## Il Control File: il registro centrale

Se il parameter file è il punto di partenza, il control file è il cuore dell'istanza. È un file binario che Oracle aggiorna continuamente durante il funzionamento, e contiene informazioni che nessun altro file può fornire [3]:

- Il nome del database (`db_name`)
- La lista di tutti i datafile con i rispettivi path e status
- La lista degli online redo log files
- La SCN (System Change Number) corrente — il "timestamp logico" del database
- Le informazioni di checkpoint
- Il catalogo dei backup RMAN (se si usa RMAN con il control file come repository)

Oracle non può montare il database senza il control file perché non ha modo di sapere quali datafile appartengono all'istanza, qual è il loro stato, e se il database è consistente. È una dipendenza strutturale, non una scelta di implementazione.

Per verificare i control file su un'istanza attiva [4]:

```sql
SELECT name FROM v$controlfile;
```

Su `oracle-node-01` con il SID `PHARMDB`, l'output atteso con una configurazione multiplexata è:

```text
NAME
--------------------------------------------------
/u01/app/oracle/oradata/PHARMDB/control01.ctl
/u02/app/oracle/fast_recovery_area/PHARMDB/control02.ctl
```

### Multiplexing: non un'opzione, una necessità

Oracle raccomanda di avere **almeno due copie del control file su path fisicamente separati**. Il motivo è semplice: se il control file è su un solo disco e quel disco ha un problema, il database non può aprirsi e il recovery diventa significativamente più complesso.

Il multiplexing si configura nel parameter file:

```text
control_files = '/u01/app/oracle/oradata/PHARMDB/control01.ctl',
                '/u02/app/oracle/fast_recovery_area/PHARMDB/control02.ctl'
```

Oracle scrive in modo sincrono su tutte le copie. Se una copia diventa inaccessibile, Oracle registra l'errore ma continua a funzionare con le copie rimanenti — fino a che almeno una copia è disponibile.

L'errore della notte farmaceutica, `ORA-00205`, indica esattamente che Oracle non riesce a identificare (leggere o verificare) il control file al path specificato. In quel caso specifico, il team storage aveva rimontato il filesystem `/u01` con permessi diversi dopo la manutenzione. Il control file era fisicamente intatto — semplicemente Oracle non riusciva a leggerlo.

---

## Gli Online Redo Log Files: il giornale delle transazioni

Gli online redo log files sono l'ultimo elemento della triade critica, e forse quello più sottile da capire.

Ogni modifica che avviene nel database Oracle — un `INSERT`, un `UPDATE`, una `DELETE` — viene prima scritta nei redo log, e solo successivamente (in modo asincrono) sui datafile. Questo meccanismo si chiama **write-ahead logging** ed è la base della durabilità delle transazioni: se il sistema crasha prima che i dati vengano scritti sui datafile, Oracle può ricostruire le modifiche leggendo i redo log.

Senza redo log, Oracle non può garantire la consistenza del database in caso di crash. Per questo motivo, se i redo log sono corrotti o mancanti, Oracle non apre il database [5].

### Struttura a gruppi e membri

I redo log sono organizzati in **gruppi**. Oracle scrive in modo circolare: riempie il gruppo 1, poi passa al gruppo 2, poi al gruppo 3, poi torna al gruppo 1 (sovrascrivendo). Ogni gruppo può contenere uno o più **membri** — copie identiche del log, su path diversi, per ridondanza.

```sql
-- Stato dei gruppi redo log
SELECT group#, members, status, bytes/1024/1024 AS mb
FROM v$log;

-- Path fisici dei membri
SELECT group#, member
FROM v$logfile
ORDER BY group#;
```

Un output tipico per `PHARMDB` con tre gruppi da 200MB ciascuno:

```text
GROUP#  MEMBERS  STATUS    MB
------  -------  --------  ---
     1        1  INACTIVE  200
     2        1  CURRENT   200
     3        1  INACTIVE  200
```

Lo status `CURRENT` indica il gruppo su cui Oracle sta scrivendo in questo momento. `INACTIVE` indica gruppi già ciclati e non più necessari per il recovery dell'istanza corrente. `ACTIVE` indicherebbe un gruppo ancora necessario per il recovery ma non più corrente.

I path fisici su `oracle-node-01`:

```bash
/u01/app/oracle/oradata/PHARMDB/redo01.log   # GROUP 1, 200MB
/u01/app/oracle/oradata/PHARMDB/redo02.log   # GROUP 2, 200MB
/u01/app/oracle/oradata/PHARMDB/redo03.log   # GROUP 3, 200MB
```

### Redo log online vs archived

Vale la pena chiarire la distinzione, anche se gli archived redo log non sono oggetto di questo articolo: gli **online redo log** sono i file attivi, quelli su cui Oracle scrive le transazioni in corso. Gli **archived redo log** sono copie dei gruppi già ciclati, create automaticamente se il database è in `ARCHIVELOG` mode. Per il backup e il point-in-time recovery servono entrambi — ma per l'avvio del database contano solo gli online redo log.

Gli errori tipici quando i redo log sono inaccessibili o corrotti:

```text
ORA-00313: open failed for members of log group 1 of thread 1
ORA-00312: online log 1 thread 1: '/u01/app/oracle/oradata/PHARMDB/redo01.log'
```

---

## Path standard e convenzioni OFA

Oracle raccomanda una convenzione di layout chiamata **OFA** (Optimal Flexible Architecture) che organizza i file dell'istanza in modo prevedibile. Seguirla non è obbligatorio, ma in produzione rende la vita significativamente più semplice — sia per la manutenzione ordinaria che per il recovery.

Tabella di riferimento rapido per `oracle-node-01` con SID `PHARMDB`:

| File | Path tipico Linux (OFA) | Comando di verifica |
|---|---|---|
| SPFILE | `/u01/app/oracle/product/19.0.0/dbhome_1/dbs/spfilePHARMDB.ora` | `SHOW PARAMETER spfile` |
| Control file 1 | `/u01/app/oracle/oradata/PHARMDB/control01.ctl` | `SELECT name FROM v$controlfile` |
| Control file 2 | `/u02/app/oracle/fast_recovery_area/PHARMDB/control02.ctl` | `SELECT name FROM v$controlfile` |
| Redo log group 1 | `/u01/app/oracle/oradata/PHARMDB/redo01.log` | `SELECT group#, member FROM v$logfile` |
| Redo log group 2 | `/u01/app/oracle/oradata/PHARMDB/redo02.log` | `SELECT group#, member FROM v$logfile` |
| Redo log group 3 | `/u01/app/oracle/oradata/PHARMDB/redo03.log` | `SELECT group#, member FROM v$logfile` |

**Nota su ASM**: in ambienti che usano Automatic Storage Management, i path fisici sono sostituiti da path logici del tipo `+DATA/PHARMDB/CONTROLFILE/current.260.1234567890`. Il concetto rimane identico — sono sempre gli stessi tre tipi di file critici — ma la gestione fisica è delegata ad ASM. Se lavori in un ambiente ASM, i comandi SQL di verifica restano gli stessi; cambiano solo i path nell'output.

---

## Mappa diagnostica: cosa blocca cosa

Quando un'istanza Oracle non parte, la prima domanda è: in quale fase si è fermata? La risposta è quasi sempre nell'alert log, e il codice di errore ORA indica direttamente quale file critico è coinvolto.

| File mancante/corrotto | Fase bloccata | Errore ORA tipico | Prima azione |
|---|---|---|---|
| SPFILE/PFILE | Pre-NOMOUNT | `ORA-01078`, `LRM-00109` | Verificare esistenza e permessi in `$ORACLE_HOME/dbs/` |
| Control file | MOUNT | `ORA-00205` | Verificare path in `control_files`, permessi filesystem, disponibilità copie multiplexate |
| Online redo log | OPEN | `ORA-00313`, `ORA-00312` | Verificare `v$logfile`, status gruppi in `v$log`, integrità fisica dei file |

Questa non è una guida al recovery — quello è un argomento separato, che richiede di distinguere tra control file corrotto e control file mancante, tra redo log CURRENT e redo log INACTIVE, tra recovery con RMAN e recovery manuale. È una **mappa diagnostica**: serve a non perdere tempo nelle direzioni sbagliate nelle prime fasi di un'emergenza.

In quella notte farmaceutica, `ORA-00205` aveva già detto tutto. Il control file era il problema, la fase era MOUNT, il passo successivo era verificare i permessi sul filesystem `/u01` — non chiamare il vendor di rete, non controllare il listener, non riavviare il server.

---

## Conoscere l'architettura prima di averne bisogno

La diagnosi rapida quella notte non è stata intuizione. È stata il risultato diretto di conoscere la sequenza di startup e sapere cosa legge Oracle in ciascuna fase.

Un DBA che conosce questi tre file sa cosa chiedere al team storage ("i permessi su `/u01` sono stati modificati durante la manutenzione?"), sa quali righe dell'alert log contano, sa in quale ordine escludere le ipotesi. Il valore non è "saper risolvere in emergenza" — è non perdere venti minuti a guardare nel posto sbagliato mentre un sistema di tracciabilità farmaceutica è fermo.

I tre file — SPFILE/PFILE, control file, online redo log — non sono concetti avanzati. Sono l'architettura minima di qualsiasi istanza Oracle. Conoscerli non richiede anni di esperienza: richiede di aver capito la sequenza di startup e il ruolo di ciascun componente.

Un possibile seguito naturale a questo articolo è il backup e il recovery di questi stessi file critici: come RMAN gestisce il restore del control file, come si ricrea uno SPFILE da un PFILE di emergenza, cosa succede quando il redo log CURRENT è corrotto e non si può semplicemente dropparlo. Ma quello è un capitolo separato.

---

## Fonti ufficiali

1. Oracle Database Concepts 19c — Startup and Shutdown: sequenza NOMOUNT/MOUNT/OPEN e ruolo dei file critici — `<TODO: scout URL esatto per Oracle 19c Concepts, capitolo "Starting Up a Database">`

2. Oracle Database Administrator's Guide 19c — Managing Initialization Parameters: SPFILE, PFILE, ordine di ricerca, `ALTER SYSTEM SET` — `<TODO: scout URL esatto per capitolo "Managing Initialization Parameters Using a Server Parameter File">`

3. Oracle Database Administrator's Guide 19c — [Managing the Online Redo Log](https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-the-online-redo-log.html) — gruppi, membri, status, `v$log`, `v$logfile`, errori ORA-00313/ORA-00312

4. Oracle Database Reference 19c — [V$CONTROLFILE](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/V-CONTROLFILE.html) — struttura e query di verifica dei control file

5. Oracle Database Reference 19c — [V$LOG](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/V-LOG.html) — colonne `GROUP#`, `MEMBERS`, `STATUS`, `BYTES`; interpretazione degli status CURRENT/ACTIVE/INACTIVE

6. oracle-base.com (Tim Hall) — `<TODO: scout URL specifico per "Oracle Database Startup and Shutdown" su oracle-base.com>` — sequenza di startup, errori comuni, esempi pratici

---

## Glossario candidato

- **SPFILE** (Oracle) — Server Parameter File: file binario letto da Oracle all'avvio che contiene i parametri di configurazione dell'istanza (`db_name`, `control_files`, `memory_target`, ecc.). Modificabile a caldo con `ALTER SYSTEM SET` senza riavviare il database.

- **Control File** (Oracle) — File binario aggiornato continuamente da Oracle che registra la struttura fisica del database: path di datafile e redo log, SCN corrente, informazioni di checkpoint. Indispensabile per la fase di MOUNT; va multiplexato su path fisicamente separati.

- **Online Redo Log** (Oracle) — File circolare che registra in sequenza tutte le modifiche apportate al database (redo entries) prima che vengano scritte sui datafile. Organizzato in gruppi con possibili membri multipli per ridondanza; base del meccanismo di recovery in caso di crash.

- **SCN** (System Change Number) — Numero sequenziale monotono crescente che Oracle usa per identificare un punto preciso nella vita del database. Presente nel control file e nei datafile; usato per determinare la consistenza e il punto di recovery.

- **OFA** (Optimal Flexible Architecture) — Convenzione di naming e layout dei path raccomandata da Oracle per organizzare i file di un'istanza (datafile, control file, redo log, backup) in modo prevedibile, manutenibile e portabile tra ambienti diversi.
