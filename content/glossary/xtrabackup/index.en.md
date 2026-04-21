---
title: "xtrabackup"
description: "Hot physical backup tool for MySQL/MariaDB developed by Percona. Copies InnoDB files with the database running, handling in-flight transactions via the redo log."
translationKey: "glossary_xtrabackup"
aka: "Percona XtraBackup"
articles:
  - "/posts/mysql/mysql-pre-upgrade-assessment"
---

**xtrabackup** is the main open-source tool for hot physical backups of MySQL, MariaDB and Percona Server, developed and maintained by Percona. Unlike `mysqldump` and `mydumper` — which produce logical dumps — it copies InnoDB data files directly on the filesystem while the database is running, with no downtime required.

## How it works

The process has two phases:

1. **Backup**: `xtrabackup` copies the InnoDB `.ibd` files and simultaneously reads the redo log to record all changes that happen during the copy. The result is a set of data files + a redo log that represents an *inconsistent* state of the database (the files were copied at slightly different moments) but a *reconstructible* one.
2. **Prepare**: before restore, `xtrabackup --prepare` performs a crash recovery applying the redo log to the data files, bringing them to a consistent state.

## When it's the best choice

On datasets larger than ~100 GB, xtrabackup's backup time is typically 5-10x faster than `mysqldump` and 2-4x faster than `mydumper`, because it skips `INSERT` regeneration entirely. The advantage is even more pronounced during restore, where a binary copy + crash recovery takes minutes compared to hours for a logical restore.

It's the required choice when the maintenance window is tight, for pre-upgrade snapshots, and for lift-and-shift migrations to new storage.

## Constraints to know

- **MyISAM** tables are locked during their copy (FLUSH TABLES WITH READ LOCK): on databases with residual MyISAM this can cause application blocking for minutes
- The backup requires direct filesystem access on the MySQL server
- The restore requires replaying the redo log before the instance can start (`--prepare` phase)
