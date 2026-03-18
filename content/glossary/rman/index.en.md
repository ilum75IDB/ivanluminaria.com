---
title: "RMAN"
description: "Recovery Manager — Oracle's tool for database backup, restore and recovery, including creation of standby databases for Data Guard."
translationKey: "glossary_rman"
aka: "Recovery Manager"
articles:
  - "/posts/oracle/oracle-data-guard"
---

**RMAN** (Recovery Manager) is Oracle's native tool for database backup, restore and recovery. It is a command-line utility that manages all data protection operations in an integrated way with the database.

## What it does

- **Backup**: full, incremental, archived log only
- **Restore**: recovery of datafiles, tablespaces or the entire database
- **Recovery**: applying redo logs to bring the database to a specific point in time
- **Duplicate**: creating database copies, including standby databases for Data Guard

## RMAN and Data Guard

For standby database creation, RMAN allows `DUPLICATE ... FOR STANDBY FROM ACTIVE DATABASE` — a direct network copy from primary to standby, with no need for intermediate tape or disk backups. The command transfers all datafiles and controlfiles and configures them automatically for replication.

## Why RMAN over manual copies

RMAN understands the internal structure of the Oracle database: it knows which blocks have changed (for incrementals), which files are needed, how to apply redo. A manual file copy (with `cp` or `rsync`) does not guarantee consistency and requires the database to be shut down. RMAN can work with the database open, with minimal performance impact.
