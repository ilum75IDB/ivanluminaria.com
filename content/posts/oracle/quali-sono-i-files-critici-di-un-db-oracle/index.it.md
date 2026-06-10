---
title: "ORA-00205 alle tre di notte: capire i file critici Oracle prima di averne bisogno"
seoTitle: "ORA-00205: file critici Oracle 19c (SPFILE, control, redo log)"
description: "Diagnosi guidata di ORA-00205 in piena emergenza notturna: fase MOUNT, control file, SPFILE, redo log. Metodo pratico per i DBA Oracle reperibili."
date: "2026-07-14T08:03:00+01:00"
draft: false
translationKey: "quali_sono_i_files_critici_di_un_db_oracle"
tags: ["incident-response", "startup", "control-file", "oracle-19c"]
categories: ["oracle"]
image: "quali-sono-i-files-critici-di-un-db-oracle.cover.jpg"
webo_generated_at: 2026-06-07
webo_status: scheduled
---

## La chiamata

[3:08] Il telefono vibra sul comodino. È Paolo, DBA del cliente farmaceutico — Oracle 19c, tracciabilità lotti, compliance regolatoria. La finestra di manutenzione storage si era chiusa alle 2:30. Lui aveva provato lo startup. L'istanza non era ripartita.

Mi legge il messaggio dal cellulare, voce piatta ma con quella tensione sottile di chi sa che il sistema è fermo e non sa ancora perché:

```text
ORA-00205: error in identifying control file
  '/u01/app/oracle/oradata/PHARMDB/control01.ctl'
```

È la prima emergenza vera che gestisce da reperibile. Non è impreparato: conosce Oracle, sa usare i comandi, ha letto la documentazione del cliente. Il punto è che quella documentazione è scritta come reference, non come metodo. E in quel momento gli serve un metodo.

---

## La fase MOUNT

[3:09] La prima cosa che gli chiedo non è "hai controllato i permessi?" o "il listener è su?". Gli chiedo: "in quale fase di startup si è fermato Oracle?".

Non è una domanda retorica. È il punto di partenza di qualsiasi diagnosi su un'istanza che non parte.

Oracle avvia un database in tre fasi distinte [1]:

**`NOMOUNT`** — Oracle alloca la SGA e avvia i processi in background leggendo il **parameter file** (SPFILE o PFILE). In questa fase non conosce ancora il database fisico: sa solo come configurare l'istanza in memoria.

**`MOUNT`** — Oracle legge il **control file**. Qui l'istanza "scopre" la struttura fisica del database: quali datafile esistono, dove si trovano, qual è la SCN corrente, qual è lo stato dei redo log. Solo dopo il MOUNT Oracle sa cosa sta gestendo.

**`OPEN`** — Oracle verifica la consistenza degli **online redo log files** e dei datafile, applica eventuale recovery se necessario, e apre il database agli utenti.

La conseguenza pratica è diretta: se il parameter file è corrotto o mancante, Oracle non arriva nemmeno al NOMOUNT. Se il control file è inaccessibile, l'istanza si ferma al MOUNT. Se i redo log sono corrotti, il blocco avviene in OPEN.

Conoscere questa sequenza significa sapere, leggendo un codice ORA, in quale fase si è fermato tutto — e quindi quale file cercare per primo, senza ipotesi al buio.

Paolo ci pensa un secondo. "ORA-00205 è in MOUNT. Quindi è il control file."

Esatto.

---

## Il control file e il rimount

[3:11] Gli detto le tre verifiche da fare in sequenza, in quest'ordine:

**(a)** dammi il path esatto dal messaggio ORA-00205
**(b)** `ls -la` su quel path e dimmi proprietario e permessi
**(c)** confronta con il runbook pre-manutenzione che avevamo scritto insieme l'anno prima

Mentre Paolo apre il terminale, gli spiego perché il control file è il punto critico di quella fase.

Il control file è un file binario che Oracle aggiorna continuamente durante il funzionamento. Contiene informazioni che nessun altro file può fornire [3]:

- il nome del database (`db_name`)
- la lista di tutti i datafile con i rispettivi path e status
- la lista degli online redo log files
- la SCN (System Change Number) corrente — il "timestamp logico" del database
- le informazioni di checkpoint
- il catalogo dei backup RMAN, quando si usa RMAN con il control file come repository

Oracle non può montare il database senza control file: gli mancherebbe il modo di sapere quali datafile appartengono all'istanza, qual è il loro stato e se il database è consistente. È una dipendenza strutturale.

Per verificare i control file su un'istanza attiva [4]:

```sql
SELECT name FROM v$controlfile;
```

Su `oracle-node-01` con il SID `PHARMDB`, l'output con una configurazione multiplexata è:

```text
NAME
--------------------------------------------------
/u01/app/oracle/oradata/PHARMDB/control01.ctl
/u02/app/oracle/fast_recovery_area/PHARMDB/control02.ctl
```

Due copie, su path fisicamente separati. Il multiplexing non è un'opzione: se il control file vive su un solo disco e quel disco ha un problema, il database non si apre e il recovery diventa significativamente più complesso. Si configura nel parameter file:

```text
control_files = '/u01/app/oracle/oradata/PHARMDB/control01.ctl',
                '/u02/app/oracle/fast_recovery_area/PHARMDB/control02.ctl'
```

Oracle scrive in modo sincrono su tutte le copie. Se una diventa inaccessibile, registra l'errore e continua a funzionare con le copie rimanenti — fino a che almeno una è disponibile.

**Nota su ASM**: in ambienti che usano Automatic Storage Management i path fisici sono sostituiti da path logici del tipo `+DATA/PHARMDB/CONTROLFILE/current.260.1234567890`. Il concetto rimane identico — sono sempre gli stessi tre tipi di file critici — cambia solo la gestione fisica, delegata ad ASM. I comandi SQL di verifica sono gli stessi; cambia solo l'output.

[3:14] Paolo fa il `ls -la`. I permessi sono cambiati: prima della manutenzione il proprietario era `oracle:oinstall`, adesso è `root:root`. Oracle non può leggere il file.

Il control file era fisicamente intatto. Il team storage aveva rimontato il filesystem `/u01` con permessi diversi dopo la manutenzione, e Oracle non riusciva ad aprirlo.

Gli dico subito: "ok, chiamiamo storage. Non toccare nulla tu, niente `chmod` a mano." Non perché non sappia farlo — saprebbe — ma perché in un sistema di compliance regolatoria ogni modifica manuale fuori procedura diventa un problema documentale oltre che tecnico. Il fix deve passare dal team storage, con ticket aperto e tracciato.

Mentre aspettiamo che storage si colleghi, gli faccio notare una cosa: se il `ls -la` avesse mostrato il file intatto e accessibile, il passo successivo sarebbe stato risalire di una fase, al parameter file. Errore diverso, fase diversa: tipicamente `ORA-01078` (failure in processing system parameters) o `LRM-00109` (could not open parameter file), e in quel caso Oracle non sarebbe arrivato nemmeno al NOMOUNT.

Il parameter file è il punto di partenza assoluto: Oracle lo legge prima di qualsiasi altra cosa per sapere come configurare l'istanza in memoria, e soprattutto per sapere dove si trovano i control file. Il parametro `control_files` che indica i path è contenuto proprio lì.

Esistono due varianti [2]:

**PFILE** (`init<SID>.ora`) — file di testo, modificabile con qualsiasi editor. Richiede un riavvio per applicare le modifiche. Utile in ambienti di sviluppo o come backup leggibile dei parametri.

**SPFILE** (`spfile<SID>.ora`) — file binario, gestito da Oracle. Permette modifiche a caldo con `ALTER SYSTEM SET` senza riavviare l'istanza. In produzione si usa quasi sempre lo SPFILE.

L'ordine di ricerca Oracle è preciso: cerca prima lo SPFILE nel path di default, poi il PFILE. Su Linux/Unix:

```bash
# SPFILE (default)
$ORACLE_HOME/dbs/spfilePHARMDB.ora

# PFILE (fallback)
$ORACLE_HOME/dbs/initPHARMDB.ora
```

Per verificare quale parameter file è in uso su un'istanza attiva:

```sql
-- Se VALUE è vuoto, Oracle sta usando un PFILE
SHOW PARAMETER spfile;
```

Paolo prende nota. Nel nostro caso il parameter file era a posto — il problema era una fase più avanti — e il modello mentale ora è completo.

---

## Lo startup completo

[3:23] Storage applica `chmod 640` e ripristina `oracle:oinstall` come proprietario sui file di `/u01`. Paolo riavvia l'istanza.

[3:38] L'istanza supera il MOUNT. Poi si ferma in OPEN con un warning sui redo log.

Gli spiego cosa sta guardando.

Gli online redo log files sono l'ultimo elemento della triade critica. Ogni modifica che avviene nel database — un `INSERT`, un `UPDATE`, una `DELETE` — viene prima scritta nei redo log, e solo in seguito (in modo asincrono) sui datafile. Questo meccanismo si chiama **write-ahead logging**: se il sistema crasha prima che i dati vengano scritti sui datafile, Oracle può ricostruire le modifiche leggendo i redo log. Senza redo log, Oracle non può garantire la consistenza del database in caso di crash — e per questo, se sono corrotti o mancanti, il database non si apre [5].

I redo log sono organizzati in **gruppi**. Oracle scrive in modo circolare: riempie il gruppo 1, passa al 2, poi al 3, poi torna al gruppo 1. Ogni gruppo può contenere uno o più **membri** — copie identiche del log su path diversi, per ridondanza.

```sql
-- Stato dei gruppi redo log
SELECT group#, members, status, bytes/1024/1024 AS mb
FROM v$log;

-- Path fisici dei membri
SELECT group#, member
FROM v$logfile
ORDER BY group#;
```

L'output per `PHARMDB` con tre gruppi da 200MB:

```text
GROUP#  MEMBERS  STATUS    MB
------  -------  --------  ---
     1        1  INACTIVE  200
     2        1  CURRENT   200
     3        1  INACTIVE  200
```

`CURRENT` è il gruppo su cui Oracle sta scrivendo in quel momento. `INACTIVE` indica gruppi già ciclati, non più necessari per il recovery dell'istanza corrente. `ACTIVE` segnalerebbe un gruppo ancora necessario per il recovery ma non più corrente — uno stato che richiede attenzione prima di qualsiasi operazione sui log.

I path fisici su `oracle-node-01`:

```bash
/u01/app/oracle/oradata/PHARMDB/redo01.log   # GROUP 1, 200MB
/u01/app/oracle/oradata/PHARMDB/redo02.log   # GROUP 2, 200MB
/u01/app/oracle/oradata/PHARMDB/redo03.log   # GROUP 3, 200MB
```

Gli errori tipici quando i redo log sono inaccessibili o corrotti:

```text
ORA-00313: open failed for members of log group 1 of thread 1
ORA-00312: online log 1 thread 1: '/u01/app/oracle/oradata/PHARMDB/redo01.log'
```

In questo caso non era una criticità reale. Il rimount di `/u01` aveva toccato anche la directory dei redo log, e Oracle aveva registrato un warning durante il primo tentativo di apertura. Paolo verifica lo status dei gruppi con `v$log`, controlla i permessi dei file fisici: tutto a posto dopo il `chmod` applicato da storage. Il warning era già rientrato.

[3:42] Database OPEN. La tracciabilità lotti torna online.

---

## Scheda di riferimento

Paolo mi richiama subito dopo. "Ivan grazie davvero, da solo non ci sarei mai arrivato in tempo. Ho letto la documentazione del cliente ma è scritta come reference, non come metodo. Adesso ho capito la sequenza, e ho capito perché serve il runbook."

Gli dico di segnarsi due tabelle nel quaderno — quelle che avremmo dovuto mettere nel runbook fin dall'inizio.

**Path standard e convenzioni OFA**

Oracle raccomanda una convenzione di layout chiamata **OFA** (Optimal Flexible Architecture) che organizza i file dell'istanza in modo prevedibile. Seguirla non è obbligatorio, e in produzione rende la manutenzione ordinaria e il recovery significativamente più gestibili.

| File | Path tipico Linux (OFA) | Comando di verifica |
|---|---|---|
| SPFILE | `/u01/app/oracle/product/19.0.0/dbhome_1/dbs/spfilePHARMDB.ora` | `SHOW PARAMETER spfile` |
| Control file 1 | `/u01/app/oracle/oradata/PHARMDB/control01.ctl` | `SELECT name FROM v$controlfile` |
| Control file 2 | `/u02/app/oracle/fast_recovery_area/PHARMDB/control02.ctl` | `SELECT name FROM v$controlfile` |
| Redo log group 1 | `/u01/app/oracle/oradata/PHARMDB/redo01.log` | `SELECT group#, member FROM v$logfile` |
| Redo log group 2 | `/u01/app/oracle/oradata/PHARMDB/redo02.log` | `SELECT group#, member FROM v$logfile` |
| Redo log group 3 | `/u01/app/oracle/oradata/PHARMDB/redo03.log` | `SELECT group#, member FROM v$logfile` |

**Mappa diagnostica: cosa blocca cosa**

Quando un'istanza Oracle non parte, la prima domanda è: in quale fase si è fermata? La risposta è quasi sempre nell'alert log, e il codice ORA indica direttamente quale file critico è coinvolto.

| File mancante/corrotto | Fase bloccata | Errore ORA tipico | Prima azione |
|---|---|---|---|
| SPFILE/PFILE | Pre-NOMOUNT | `ORA-01078`, `LRM-00109` | Verificare esistenza e permessi in `$ORACLE_HOME/dbs/` |
| Control file | MOUNT | `ORA-00205` | Verificare path in `control_files`, permessi filesystem, disponibilità copie multiplexate |
| Online redo log | OPEN | `ORA-00313`, `ORA-00312` | Verificare `v$logfile`, status gruppi in `v$log`, integrità fisica dei file |

Questa non è una guida al recovery — quello è un argomento separato, che richiede di distinguere tra control file corrotto e control file mancante, tra redo log CURRENT e redo log INACTIVE, tra recovery con RMAN e recovery manuale. È una mappa diagnostica: serve a non andare nelle direzioni sbagliate nelle prime fasi di un'emergenza.

---

## La riflessione

Paolo non era impreparato perché incompetente. Conosceva la sintassi — sapeva cosa fa `SHOW PARAMETER spfile`, sapeva interrogare `v$controlfile`. Quello che non aveva ancora interiorizzato era la sequenza di startup come metodo diagnostico: quale file legge Oracle in ciascuna fase, e quindi quale file cercare per primo quando qualcosa non va.

La differenza tra venti minuti spesi su rete, listener e OS e tre verifiche dritte al punto non è esperienza accumulata negli anni. È avere un modello mentale della sequenza — NOMOUNT, MOUNT, OPEN — e sapere cosa mappa su cosa.

Il valore di quella chiamata non è stato risolvere il problema al posto suo. È stato trasferire quel modello in trenta minuti, con un caso reale davanti. Adesso Paolo sa cosa chiedere al team storage la prossima volta ("i permessi su `/u01` sono stati modificati durante la manutenzione?"), sa quali righe dell'alert log contano, sa in quale ordine escludere le ipotesi.

Il senior DBA che non viene più chiamato in piena notte ha investito in due cose: nel runbook scritto bene insieme al team del cliente, e nella capacità di guidare a distanza chi è on-call dando le tre verifiche giuste invece di fargliene fare trenta al buio.

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
