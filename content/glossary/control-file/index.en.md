---
title: "Control File"
description: "Oracle binary file that records the physical database structure: datafile paths, redo logs, current SCN, and checkpoint info. Required for the MOUNT phase."
translationKey: "glossary_control_file"
aka: null
articles:
  - "/posts/oracle/quali-sono-i-files-critici-di-un-db-oracle"
---

The Control File is a small binary file kept continuously updated by Oracle. It holds the structural metadata of the database: datafile paths, redo log group paths, current SCN, and checkpoint information. Without it, the instance cannot progress past the MOUNT phase.

## What it records

Every time Oracle performs a CHECKPOINT or adds a file to the database structure, the Control File is updated synchronously. Key fields include:

- **Database name and DBID**
- **Path and status of each datafile** (online, offline, read-only)
- **Redo log group configuration**
- **Checkpoint SCN** — used during recovery to determine the consistency point
- **RMAN backup metadata** (when using Recovery Manager)

## Multiplexing and loss risk

Oracle allows — and recommends — keeping identical copies of the Control File on physically separate paths. The configuration is set via the `CONTROL_FILES` parameter:

```sql
ALTER SYSTEM SET CONTROL_FILES =
  '/u01/oradata/orcl/control01.ctl',
  '/u02/fast_recovery_area/orcl/control02.ctl'
SCOPE=SPFILE;
```

All copies are written in parallel on every update. If one copy is corrupted or missing, the database still starts using the valid copies. Losing **all** copies without a recent backup requires a complex manual recovery.

## Operational context

During startup, Oracle reads the Control File in the MOUNT phase to locate datafiles before opening them (OPEN phase). In a Data Guard environment, the standby Control File also holds synchronization metadata with the primary. In RMAN backups, the Control File (or a separate Catalog) acts as the central registry for all backup sets and image copies.
