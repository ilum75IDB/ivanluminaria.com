---
title: "Flashback Database"
description: "Oracle feature that rewinds an entire database to a prior point in time using flashback logs, faster than a full RMAN restore for pervasive logical errors."
translationKey: "glossary_flashback_database"
aka: "Oracle Flashback Database Recovery"
articles:
  - "/posts/oracle/oracle-flashback-recupero-dati-logici-senza-downtime-da-query-a-database"
---

Flashback Database is an Oracle feature that rewinds an entire database to a previous state without restoring datafiles from backup. Unlike a full RMAN restore, it relies on dedicated logs written continuously in the background, making recovery significantly faster when a logical error has already spread across many objects.

## How it works

Oracle continuously writes previous block images to **flashback logs** stored in the Fast Recovery Area (FRA). When a Flashback Database operation starts, the engine reads those logs backwards to the target point in time (or SCN) and applies the saved block images over the current ones.

The database must be in `MOUNT` mode:

```sql
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
FLASHBACK DATABASE TO TIMESTAMP (SYSTIMESTAMP - INTERVAL '2' HOUR);
ALTER DATABASE OPEN RESETLOGS;
```

`OPEN RESETLOGS` is mandatory: it resets the redo log sequence and makes the flashback point unreachable going forward.

## When to use it

Flashback Database is the right tool when a logical error — a `DELETE` without a `WHERE` clause, a failed migration, a batch job that corrupted data across dozens of tables — has already gone past the window where Flashback Table or Flashback Query would suffice.

Key constraints to keep in mind:

- `DB_FLASHBACK_RETENTION_TARGET` must be configured, and the FRA must have enough space to retain flashback logs for the desired window.
- Datafiles added after the flashback point are not recovered automatically and must be handled separately.
- After `RESETLOGS`, any standby databases in the Data Guard configuration need to be resynchronized.
