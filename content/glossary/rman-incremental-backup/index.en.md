---
title: "RMAN Incremental Backup"
description: "Oracle RMAN backup strategy that copies only changed blocks since the last backup at the same or higher level. Level 0 is the base, level 1 is the delta."
translationKey: "glossary_rman_incremental_backup"
aka: "RMAN Incremental Backup (Oracle Recovery Manager)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

An RMAN Incremental Backup copies only the data blocks that have changed since the last backup at the same or a higher level, rather than duplicating entire datafiles. This significantly reduces both backup window and data volume, making it the standard approach for keeping large databases in sync during migrations.

## How it works

The mechanism relies on two levels:

- **Level 0**: functionally equivalent to a full backup, but serves as the base of the incremental chain. All blocks are copied.
- **Level 1**: copies only blocks modified after the most recent level 0 or level 1 backup.

RMAN tracks changed blocks through the **Change Tracking File** (when enabled), avoiding a full scan of every datafile on each run.

```bash
# Level 0 incremental backup (base)
rman target /
BACKUP INCREMENTAL LEVEL 0 DATABASE;

# Level 1 incremental backup (delta)
BACKUP INCREMENTAL LEVEL 1 DATABASE;

# Apply delta to an image copy
RECOVER COPY OF DATABASE WITH TAG 'incr_merge';
```

## When to use it

In migration scenarios — such as moving from Oracle 12c to 21c on a 12 TB database — the typical workflow is:

1. Take a level 0 backup (or an initial physical copy) on the source system.
2. Apply successive level 1 backups to narrow the data gap as the cutover window approaches.
3. At downtime, apply the final incremental and open the target database.

This pattern compresses final downtime to minutes regardless of database size. The main constraint is chain dependency: a level 1 backup cannot be applied without a valid level 0 in place.
