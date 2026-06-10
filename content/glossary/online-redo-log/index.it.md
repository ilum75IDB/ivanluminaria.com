---
title: "Online Redo Log"
description: "File circolare Oracle che registra ogni modifica al database prima della scrittura sui datafile: fondamento del recovery in caso di crash."
translationKey: "glossary_online_redo_log"
aka: "Redo Log, Online Redo Log Files"
articles:
  - "/posts/oracle/quali-sono-i-files-critici-di-un-db-oracle"
---

L'Online Redo Log è la struttura che Oracle usa per garantire la durabilità delle transazioni. Ogni modifica — INSERT, UPDATE, DELETE, DDL — genera una **redo entry** che viene scritta nel redo log *prima* di essere applicata ai datafile. In caso di crash, Oracle rilegge queste entry per riportare il database a uno stato consistente.

## Come funziona

I redo log sono organizzati in **gruppi** (almeno due, consigliati tre o più in produzione). Oracle scrive in modo circolare: riempie il gruppo attivo, poi esegue un **log switch** e passa al successivo. Ogni gruppo può contenere più **membri** (copie fisiche identiche su dischi diversi) per ridondanza.

Il processo **LGWR** (Log Writer) scarica il redo buffer in memoria sul log corrente in quattro situazioni: a ogni COMMIT, quando il buffer è pieno al 30%, ogni 3 secondi, o prima che **DBWR** scriva i dirty block.

```sql
-- Visualizzare lo stato dei gruppi di redo log
SELECT group#, members, bytes/1024/1024 AS mb, status
FROM v$log
ORDER BY group#;

-- Visualizzare i membri fisici
SELECT group#, member, status
FROM v$logfile
ORDER BY group#;
```

## Contesto operativo

Dimensionare correttamente i redo log è critico: gruppi troppo piccoli causano log switch frequenti, che degradano le performance e aumentano il carico su ARCH (il processo di archiviazione, se il database è in **ARCHIVELOG mode**). Gruppi troppo grandi allungano i tempi di recovery.

Un log switch ogni 15-30 minuti è generalmente considerato un buon punto di partenza. In ambienti con picchi di scrittura elevati (bulk load, ETL) è normale osservare switch più frequenti: in quel caso si aumenta la dimensione dei gruppi o si aggiungono gruppi.

Se un gruppo non può essere sovrascritto perché ARCH non ha ancora archiviato il log precedente, il database si blocca in attesa: è uno dei colli di bottiglia più comuni in produzione.
