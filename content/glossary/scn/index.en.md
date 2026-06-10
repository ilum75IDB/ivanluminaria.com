---
title: "SCN"
description: "System Change Number: the monotonically increasing sequence Oracle uses to timestamp every COMMIT and guarantee consistency and point-in-time recovery."
translationKey: "glossary_scn"
aka: "System Change Number"
articles:
  - "/posts/oracle/quali-sono-i-files-critici-di-un-db-oracle"
---

The SCN (System Change Number) is Oracle's internal counter that orders every change made to the database. It grows strictly monotonically: each COMMIT receives a higher SCN than the previous one, making it possible to reconstruct the exact state of the database at any past point in time.

## How it works

Whenever a transaction issues a COMMIT, Oracle assigns a unique SCN and records it in the redo log, the control file, and the datafile headers. This value is the reference point for all consistency and recovery operations.

```sql
-- Read the current database SCN
SELECT CURRENT_SCN FROM V$DATABASE;

-- SCN recorded in a datafile header
SELECT NAME, CHECKPOINT_CHANGE# FROM V$DATAFILE;
```

During instance recovery, Oracle compares the SCN stored in the control file against the SCN in each datafile header to determine which blocks require redo and which are already consistent.

## Operational context

The SCN is central to three main scenarios:

- **Point-in-time recovery (PITR)**: a target SCN is specified and Oracle reapplies redo up to that exact point.
- **Flashback**: Flashback Query and Flashback Database use the SCN to navigate through data history.
- **Data Guard and replication**: the standby applies archived redo up to the SCN transmitted by the primary, ensuring synchronization.

The SCN has a theoretical maximum (tied to the 48-bit architecture in recent versions), but under normal conditions this is not an operational constraint. Abnormal situations of reduced SCN headroom can be monitored via `V$DATABASE_INCARNATION` and related MOS notes.
