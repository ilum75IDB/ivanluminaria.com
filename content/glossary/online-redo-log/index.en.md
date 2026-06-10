---
title: "Online Redo Log"
description: "Oracle circular log files that record every database change before datafile writes, forming the foundation of crash recovery."
translationKey: "glossary_online_redo_log"
aka: "Redo Log, Online Redo Log Files"
articles:
  - "/posts/oracle/quali-sono-i-files-critici-di-un-db-oracle"
---

The Online Redo Log is the structure Oracle uses to guarantee transaction durability. Every change — INSERT, UPDATE, DELETE, DDL — generates a **redo entry** written to the redo log *before* being applied to the datafiles. After a crash, Oracle replays these entries to bring the database back to a consistent state.

## How it works

Redo logs are organized into **groups** (at least two; three or more recommended in production). Oracle writes in a circular fashion: it fills the active group, then performs a **log switch** and moves to the next one. Each group can hold multiple **members** — identical physical copies on separate disks — for redundancy.

The **LGWR** (Log Writer) background process flushes the in-memory redo buffer to the current log under four conditions: on every COMMIT, when the buffer reaches 30% capacity, every 3 seconds, or before **DBWR** writes dirty blocks.

```sql
-- Check redo log group status
SELECT group#, members, bytes/1024/1024 AS mb, status
FROM v$log
ORDER BY group#;

-- Check physical members
SELECT group#, member, status
FROM v$logfile
ORDER BY group#;
```

## Operational context

Sizing redo log groups correctly matters: groups that are too small cause frequent log switches, degrading performance and increasing load on ARCH (the archiver process, when the database runs in **ARCHIVELOG mode**). Groups that are too large extend recovery time.

One log switch every 15–30 minutes is a common baseline target. In high-write environments — bulk loads, ETL pipelines — more frequent switches are expected; the usual response is to increase group size or add more groups.

If a group cannot be overwritten because ARCH has not yet archived the previous log, the database stalls waiting for it. This is one of the most common production bottlenecks tied to redo log configuration.
