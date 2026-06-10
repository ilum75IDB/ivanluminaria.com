---
title: "Control File"
description: "File binario Oracle che registra la struttura fisica del database: datafile, redo log, SCN e checkpoint. Indispensabile per la fase di MOUNT."
translationKey: "glossary_control_file"
aka: null
articles:
  - "/posts/oracle/quali-sono-i-files-critici-di-un-db-oracle"
---

Il Control File è un file binario di piccole dimensioni mantenuto costantemente aggiornato da Oracle. Contiene i metadati strutturali del database: path dei datafile, path dei redo log group, SCN corrente e informazioni di checkpoint. Senza di esso, l'istanza non può superare la fase di MOUNT.

## Cosa registra

Ogni volta che Oracle esegue un CHECKPOINT o aggiunge un file alla struttura del database, il Control File viene aggiornato in modo sincrono. I campi principali includono:

- **Database name e DBID**
- **Path e stato di ogni datafile** (online, offline, read-only)
- **Configurazione dei redo log group**
- **SCN di checkpoint** — usato durante il recovery per determinare il punto di coerenza
- **RMAN backup metadata** (se si usa Recovery Manager)

## Multiplexing e rischio di perdita

Oracle consente — e raccomanda — di mantenere copie identiche del Control File su path fisicamente separati. La configurazione avviene nel parametro `CONTROL_FILES`:

```sql
ALTER SYSTEM SET CONTROL_FILES =
  '/u01/oradata/orcl/control01.ctl',
  '/u02/fast_recovery_area/orcl/control02.ctl'
SCOPE=SPFILE;
```

Tutte le copie vengono scritte in parallelo a ogni aggiornamento. Se una copia è corrotta o mancante, il database si avvia comunque usando le copie valide. La perdita di **tutte** le copie senza un backup recente richiede un recovery manuale complesso.

## Contesto operativo

Durante lo startup, Oracle legge il Control File nella fase MOUNT per localizzare i datafile prima di aprirli (fase OPEN). In un ambiente Data Guard, il Control File dello standby contiene anche i metadati di sincronizzazione con il primary. Nei backup RMAN, il Control File (o un Catalog separato) è il registro centrale di tutti i backup set e image copy.
