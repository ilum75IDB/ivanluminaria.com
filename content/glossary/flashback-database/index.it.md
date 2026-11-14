---
title: "Flashback Database"
description: "Tecnica Oracle che riporta l'intero database a un punto nel tempo precedente usando i flashback logs, più rapida di un restore RMAN per errori logici pervasivi."
translationKey: "glossary_flashback_database"
aka: "Oracle Flashback Database Recovery"
articles:
  - "/posts/oracle/oracle-flashback-recupero-dati-logici-senza-downtime-da-query-a-database"
---

Flashback Database è una funzionalità Oracle che permette di riportare l'intero database a uno stato precedente nel tempo, senza dover ripristinare i datafile da backup. A differenza del restore RMAN, lavora su log dedicati scritti in avanti, il che rende l'operazione significativamente più rapida quando l'errore logico ha già propagato modifiche su molti oggetti.

## Come funziona

Oracle registra continuamente le immagini precedenti dei blocchi modificati nei **flashback logs**, archiviati nella Fast Recovery Area (FRA). Quando si avvia un Flashback Database, il motore legge questi log a ritroso fino al punto nel tempo (o SCN) desiderato, applicando le immagini precedenti ai blocchi correnti.

L'operazione richiede che il database sia in modalità `MOUNT`:

```sql
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
FLASHBACK DATABASE TO TIMESTAMP (SYSTIMESTAMP - INTERVAL '2' HOUR);
ALTER DATABASE OPEN RESETLOGS;
```

Il `OPEN RESETLOGS` è obbligatorio: azzera la sequenza dei redo log e rende il punto di flashback non più raggiungibile in avanti.

## Quando si usa

Flashback Database è lo strumento giusto quando un errore logico — un `DELETE` massivo senza `WHERE`, una migrazione andata storta, un batch che ha corrotto dati su decine di tabelle — ha già superato il tempo di reazione necessario per un Flashback Table o una Flashback Query.

Limiti da tenere presenti:

- Richiede che `DB_FLASHBACK_RETENTION_TARGET` sia configurato e che la FRA abbia spazio sufficiente per i flashback logs.
- Non recupera i datafile aggiunti dopo il punto di flashback: quelli vanno gestiti separatamente.
- Dopo `RESETLOGS`, gli standby database devono essere risincronizzati.
