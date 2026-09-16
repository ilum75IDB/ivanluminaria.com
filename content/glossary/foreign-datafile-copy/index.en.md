---
title: "Foreign datafile copy"
description: "Datafile that RMAN materializes on the destination database from a transportable backupset, before the tablespaces are plugged in."
translationKey: "glossary_foreign_datafile_copy"
aka: "Foreign Datafile Copy (RMAN cross-platform transportable backup)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

A *foreign datafile copy* is the datafile that RMAN materializes on the destination database starting from a backupset produced with the `FOR TRANSPORT` clause, before the corresponding tablespaces are plugged into the target PDB. It is the intermediate object of the transportable backup mechanism — what makes it possible to apply RMAN incremental backups to datafiles that on the target do not yet belong to any registered tablespace.

## How it works

The typical flow is two-phase. First you generate the transportable backupset on the source, usually with the database open, using `ALLOW INCONSISTENT`:

```bash
# On the source
rman target /
BACKUP INCREMENTAL LEVEL 0
  FOR TRANSPORT ALLOW INCONSISTENT
  TABLESPACE DATA_01, DATA_02
  FORMAT '/backup/rman/xtts_l0_%U';
```

On the target, the backupset is restored as *foreign datafile copy* — not yet a tablespace, but a file already positioned in the target CDB's filesystem:

```bash
# On the target
RESTORE FOREIGN TABLESPACE DATA_01, DATA_02 TO NEW
  FROM BACKUPSET '/backup/rman/xtts_l0_1_1';
```

Each subsequent incremental is applied to the foreign datafile copy with `RECOVER FOREIGN DATAFILECOPY`, explicitly listing the physical paths of the target files:

```bash
RECOVER FOREIGN DATAFILECOPY '/u02/oradata/pdb1/data_01.dbf',
                             '/u02/oradata/pdb1/data_02.dbf'
  FROM BACKUPSET '/backup/rman/xtts_l1_2_1';
```

**Important operational limit**: each `RECOVER FOREIGN DATAFILECOPY` accepts only one backupset at a time. A script that tries to queue multiple backupsets in a single command will fail.

## When to use it

In cross-version Transportable Tablespaces (TTS) migrations combined with incremental backup — a pattern used to move terabyte-scale volumes when the downtime window is too tight for a full Data Pump. The foreign datafile copy is the "landing zone" that allows the incremental chain to be applied on the target while the source database stays writable, reducing final downtime to just the last delta apply plus the metadata plug-in.
