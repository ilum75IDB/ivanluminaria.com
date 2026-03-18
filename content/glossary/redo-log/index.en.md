---
title: "Redo Log"
description: "Log files where Oracle records every data change before writing it to the datafiles, ensuring recovery in case of failure."
translationKey: "glossary_redo_log"
aka: "Online Redo Log, Archived Redo Log"
articles:
  - "/posts/oracle/oracle-data-guard"
---

**Redo Log** is the mechanism by which Oracle records every data modification (INSERT, UPDATE, DELETE, DDL) before it is permanently written to the datafiles. It is the fundamental guarantee of transaction durability.

## How it works

Oracle writes changes to the online redo logs sequentially and continuously. Redo logs are organized in circular groups: when one group fills up, Oracle switches to the next. When all groups have been used, Oracle returns to the first (log switch).

## Online vs Archived

- **Online redo log**: the active files where Oracle writes in real time. They are circular and get overwritten
- **Archived redo log**: copies of online redo logs saved before overwriting. Required for point-in-time recovery and for Data Guard

The database's `ARCHIVELOG` mode enables automatic creation of archived logs. Without it, redo logs are overwritten and recovery is limited to the last full backup.

## Why they matter

Redo logs are the heart of Oracle recovery and replication. Without redo:

- Instance recovery after a crash is not possible
- Point-in-time recovery (media recovery) is not possible
- Data Guard cannot function (replication relies entirely on redo)
- Flashback database is not possible
