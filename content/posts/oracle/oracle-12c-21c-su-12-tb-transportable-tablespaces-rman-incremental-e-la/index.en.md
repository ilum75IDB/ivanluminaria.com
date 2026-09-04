---
title: "The Saturday night nobody wants: migrating 12 TB from Oracle 12.2 to 21c in a four-hour window"
seoTitle: "Oracle 12.2 to 21c migration: TTS + RMAN incremental, 12 TB in 4 hours"
description: "How to move 12 TB from Oracle 12.2 to 21c using transportable tablespaces and RMAN incremental backups — keeping downtime under four hours. Real numbers, real commands."
date: 2099-12-31
draft: true
translationKey: "oracle_12c_21c_su_12_tb_transportable_tablespaces_rman_incremental_e_la"
tags: ["oracle", "migration", "rman", "transportable-tablespaces", "multitenant"]
categories: ["oracle"]
image: "oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la.cover.jpg"
webo_status: da_tradurre
webo_generated_at: 2026-09-04
---

## The Saturday night nobody wants

The request had come in a few weeks earlier, at one of those meetings where numbers are presented as if they were minor details: "we need to migrate the Oracle database from 12.2 to 21c, there's a maintenance window on Saturday night, four hours." Twelve terabytes. A server eight years old, out of hardware support. The new server already racked, Oracle 21c installed — a CDB, because in 21c there is no other choice, and we'll come back to that shortly.

Four hours for twelve terabytes.

Anyone who has worked with Oracle for a while already knows where the problem is: not in the database, not in the version, not in the new hardware. It's in the math. A Data Pump export on twelve terabytes, even with aggressive parallelism and fast storage, does not finish in four hours. It doesn't finish in eight. It probably doesn't finish over the weekend.

What follows is the reasoning that led to a hybrid strategy — cross-version transportable tablespaces plus RMAN incremental — and the details of what actually happened during those four critical hours. The numbers are real, the commands are the ones we used, and the problems are the kind you only find once you're already inside.

---

## Why Data Pump is not the answer at this scale

Data Pump is the right tool for migrations up to a few hundred gigabytes, or for selective schema-level exports and imports. Beyond that threshold, the limitations become structural.

With twelve terabytes, the main issue is I/O throughput. Data Pump exports data by serializing rows into Oracle's proprietary format, then reimports them by rebuilding segments, indexes, and statistics. Even with `PARALLEL=16` and NVMe storage on both sides, effective throughput rarely exceeds 3–4 GB/minute in real-world scenarios (not benchmarks). Twelve terabytes at 4 GB/minute: fifty hours. Optimistically.

Then there's the space problem: you need a staging area large enough to hold the entire export, plus space on the target during import. With twelve terabytes of data, you're looking at twenty to twenty-five terabytes of temporary space needed across the two machines.

The last problem is the window itself: Data Pump is not incremental. If the export starts Friday evening and the database keeps receiving writes, by the time the export finishes the data is already partially stale. There is no native mechanism to synchronize changes that occurred during the export.

---

## The real options for multi-terabyte migrations

When Data Pump is off the table, the real alternatives are four [1]:

**RMAN Duplicate** — duplicates the entire database via RMAN, including all physical files. Requires nearly double the space on the target, but is reliable and well documented. The problem: for twelve terabytes, even the initial copy phase takes many hours, and it doesn't solve the short-window problem.

**Transportable Tablespaces (TTS)** — copies datafiles directly, without serialization or deserialization. It's the fastest method for moving large volumes because throughput is limited only by the speed of the transfer channel (network, shared storage, tape). The historical constraint was endianness: different platforms (e.g., Solaris SPARC → Linux x86) required explicit conversion. Between two Linux x86_64 systems, that problem doesn't exist [2].

**Data Guard as a bridge** — you configure a standby database on the new machine, let synchronization happen via redo log (hours or days, with no impact on the primary), then perform a controlled failover during the maintenance window. Elegant, but it requires version compatibility for redo shipping — and between 12c and 21c there are specific constraints.

**GoldenGate** — logical replication, maximum flexibility cross-version and cross-platform. Requires a separate license, non-trivial setup, and a warm-up period for initial synchronization. For a one-shot migration with a defined window, it's often overkill.

---

## The chosen strategy: TTS + RMAN incremental

The approach combines two techniques: transportable tablespaces to move the bulk of the data before the window, and RMAN incremental backups to synchronize the changes that accumulated in the meantime.

The underlying idea is simple: if I can't move twelve terabytes in four hours, I move eleven and a half terabytes in the days before, and during the four critical hours I move only the delta.

The plan breaks down into three phases:

1. **Preparatory phase** (days before the window): RMAN level 0 transportable backup **with the database open and writable**, transfer to the new server, restore as foreign datafile copy
2. **Synchronization phase** (days and hours before the window): level 1 incrementals, still with the database operational, to progressively close the gap
3. **Downtime window** (four hours): tablespaces read-only, final incremental, metadata plug-in into the PDB, open

The difference between this plan and the instinctive one — put the tablespaces read-only, copy them at leisure, then realign — is entirely in the first point, and it's the reason the `ALLOW INCONSISTENT` clause exists.

---

## Pre-check: what you discover before touching anything

Before moving a single byte, a compatibility analysis is required. Between Oracle 12.2 and Oracle 21c there are nearly ten years of intermediate releases, and some things have changed in ways that are not backward compatible.

**Character set**: verify that source and target use the same character set, or that the target is a superset. A TTS migration between AL32UTF8 and WE8ISO8859P1 requires explicit conversion and is not straightforward.

```sql
-- On the source database (12c)
SELECT value FROM nls_database_parameters WHERE parameter = 'NLS_CHARACTERSET';
SELECT value FROM nls_database_parameters WHERE parameter = 'NLS_NCHAR_CHARACTERSET';
```

**Endianness**: on Linux x86_64 → Linux x86_64 there are no issues. On cross-platform migrations (e.g., AIX → Linux), `RMAN CONVERT TABLESPACE` is required.

```sql
-- Check platform
SELECT platform_name, endian_format FROM v$transportable_platform
WHERE endian_format = (SELECT endian_format FROM v$database);
```

**Destination architecture**: this is the constraint that shapes the entire migration, and it's worth discovering before ordering the server — not the week before the window. **In Oracle 21c the non-CDB architecture is desupported**: multitenant is the only supported architecture [3]. A 12.2 non-CDB does not become a 21c non-CDB, because that target no longer exists — it becomes a **PDB inside a 21c CDB**. This is not a packaging detail: it changes where the tablespaces land, how the database is opened, and which commands you use during the window.

**Deprecated components**: the pre-upgrade report is no longer generated with a SQL script. As of Oracle 21c the Pre-Upgrade Information Tool (`preupgrade.jar`) is no longer distributed, and its functions have been absorbed into **AutoUpgrade** [4]:

```bash
# With the 21c home available — analysis only, modifies nothing
java -jar $ORACLE_HOME_21C/rdbms/admin/autoupgrade.jar \
  -preupgrade "target_version=21,dir=/tmp/preupg" -mode analyze
```

The report flags invalid objects, obsolete parameters, and components to remove before the upgrade. Among the most common in the 12.2 → 21c path: `SQLNET.ALLOWED_LOGON_VERSION` (deprecated), some compatibility views, and audit policies — we'll come back to auditing shortly, because it's the area where the most misinformation circulates.

`-mode analyze` is read-only: you can run it in production, during business hours, weeks in advance. It's the thing you should do first, and it's almost always done too late.

**SYSTEM and SYSAUX tablespaces**: not transportable. They stay on the source; on the target the data dictionary belongs to the PDB, created at 21c level by the CDB that hosts it.

---

## The plan, step by step

The point everything depends on: **the tablespaces stay read-write until the very last step**. That's exactly why the `FOR TRANSPORT` incremental backup exists: read-only is needed only for the final backup, the one that closes the window. Anyone who puts the tablespaces read-only at the start — to copy them at leisure over the preceding days — has just moved the downtime, not reduced it: an application that can't write is down, whether the database is open or not.

### Phase 1 — Hot initial copy (days before)

First, self-containment: no object in the tablespaces being transported can depend on objects outside them.

```sql
-- On the source
EXECUTE DBMS_TTS.TRANSPORT_SET_CHECK('DATA_01,DATA_02,IDX_01', TRUE);
SELECT * FROM transport_set_violations;
```

If `transport_set_violations` is empty, proceed. The level 0 backup is taken **with the database open and writable**, using `FOR TRANSPORT ALLOW INCONSISTENT` [1]: this clause authorizes RMAN to produce a transportable backupset from tablespaces that are not mutually consistent — they will be realigned by subsequent incrementals.

```bash
rman target /
BACKUP INCREMENTAL LEVEL 0
  FOR TRANSPORT ALLOW INCONSISTENT
  TABLESPACE DATA_01, DATA_02, IDX_01
  FORMAT '/backup/rman/xtts_l0_%U';
```

The backupset is transferred to the new server via `rsync` or storage replication. With twelve terabytes over a 10GbE network, the transfer takes roughly three to four hours. **Meanwhile the source database operates normally**: no tablespace is read-only, applications are writing, and the changes accumulating are exactly the delta that the incrementals will recover.

On the target, the datafiles materialize as *foreign datafile copies*:

```bash
# On the target (21c CDB, connected to the destination PDB)
rman target /
RESTORE FOREIGN TABLESPACE DATA_01, DATA_02, IDX_01 TO NEW
  FROM BACKUPSET '/backup/rman/xtts_l0_1_1';
```

### Phase 2 — Incremental synchronization

In the days between the initial copy and the window, one or more level 1 backups are taken, always with the database writable. Each pass closes the gap: the first incremental may cover a few hundred gigabytes, the last one before the window typically just a few tens.

```bash
# On the source — database always operational
BACKUP INCREMENTAL LEVEL 1
  FOR TRANSPORT ALLOW INCONSISTENT
  TABLESPACE DATA_01, DATA_02, IDX_01
  FORMAT '/backup/rman/xtts_l1_%U';
```

On the target, each backupset is applied to the foreign datafile copies already present, **one at a time and in the order they were produced**:

```bash
# On the target — one backupset per RECOVER
RECOVER FOREIGN DATAFILECOPY '/u02/oradata/pdb1/data_01.dbf',
                             '/u02/oradata/pdb1/data_02.dbf',
                             '/u02/oradata/pdb1/idx_01.dbf'
  FROM BACKUPSET '/backup/rman/xtts_l1_2_1';
```

One limitation worth flagging — the kind you discover by running into it, not by reading the manual: **you cannot apply multiple backupsets in a single `RECOVER`**. Each incremental is its own command, in sequence. A script that chains them into one command will fail, and it will do so at the worst possible moment.

### Phase 3 — The four-hour window

11:00 PM, Saturday. The source is closed to applications:

```sql
ALTER SYSTEM ENABLE RESTRICTED SESSION;
```

**Only now** do the tablespaces go read-only — this is the step that freezes the data and opens the window:

```sql
ALTER TABLESPACE data_01 READ ONLY;
ALTER TABLESPACE data_02 READ ONLY;
ALTER TABLESPACE idx_01 READ ONLY;
-- repeat for all application tablespaces
```

The final incremental is taken now, **without** `ALLOW INCONSISTENT` (the tablespaces are now consistent) and with `DATAPUMP FORMAT`, which causes RMAN to also produce a metadata dump alongside the backupset:

```bash
rman target /
BACKUP INCREMENTAL LEVEL 1
  FOR TRANSPORT
  DATAPUMP FORMAT '/backup/rman/xtts_meta.bck'
  TABLESPACE DATA_01, DATA_02, IDX_01
  FORMAT '/backup/rman/xtts_l1_final_%U';
```

This contains only the changes from the last few hours — typically a few gigabytes. Transfer to the target and final apply:

```bash
# On the target
RECOVER FOREIGN DATAFILECOPY '/u02/oradata/pdb1/data_01.dbf',
                             '/u02/oradata/pdb1/data_02.dbf',
                             '/u02/oradata/pdb1/idx_01.dbf'
  FROM BACKUPSET '/backup/rman/xtts_l1_final_3_1';
```

What remains is plugging the metadata into the destination PDB. Data Pump requires a *directory object* — not a filesystem path — and the full list of datafiles:

```sql
-- On the target, inside the PDB
CREATE DIRECTORY dump_dir AS '/backup/rman';
```

```bash
impdp system/***@pdb1 \
  DIRECTORY=dump_dir \
  DUMPFILE=tts_export.dmp \
  LOGFILE=tts_import.log \
  TRANSPORT_TABLESPACES=DATA_01,DATA_02,IDX_01 \
  TRANSPORT_DATAFILES='/u02/oradata/pdb1/data_01.dbf','/u02/oradata/pdb1/data_02.dbf','/u02/oradata/pdb1/idx_01.dbf'
```

The `DUMPFILE` is the one produced on the source with the TTS metadata export, which is run after the tablespaces are read-only:

```bash
# On the source, tablespaces already read-only
expdp system/*** \
  DIRECTORY=dump_dir \
  DUMPFILE=tts_export.dmp \
  LOGFILE=tts_export.log \
  TRANSPORT_TABLESPACES=DATA_01,DATA_02,IDX_01 \
  TRANSPORT_FULL_CHECK=Y
```

At this point the tablespaces are in the PDB, which is opened and put back in read-write:

```sql
ALTER PLUGGABLE DATABASE pdb1 OPEN;
ALTER TABLESPACE data_01 READ WRITE;
ALTER TABLESPACE data_02 READ WRITE;
ALTER TABLESPACE idx_01 READ WRITE;
```

There is no `dbupgrade` in this path: the data dictionary is not migrated, because it belongs to the PDB — already created at 21c level by the CDB that hosts it. That distinction is worth keeping in mind when comparing timings with an in-place upgrade, where dictionary upgrade is the dominant phase.

---

## What the manuals don't tell you

Four problems you only find once you're already inside the window.

**Password file**: the format itself doesn't change — `12.2` is the default in both 12.2 and 21c. What changes is the tolerance: in 21c the `IGNORECASE` parameter is desupported and password files are always case-sensitive [6]. A password file inherited from an environment that relied on case-insensitive passwords will lock out administrative users, and it happens on the first `sqlplus sys as sysdba` from a remote host — meaning at the worst possible moment. Regenerate it on the target before opening:

```bash
orapwd file=$ORACLE_HOME/dbs/orapwCDB1 password=<sys_password> format=12.2
```

**Auditing, and what you read online**: the version that circulates is "in 21c traditional auditing is gone." That's not accurate, and the difference matters when you're planning. In 21c the default remains **mixed mode** — unified auditing active alongside traditional auditing — exactly as it has been since 12c; traditional auditing is **deprecated** in 21c and **desupported** only from 23c onward [5]. *Pure* unified auditing is not a parameter: you get it by relinking the Oracle binary with `uniaud_on` and restarting the instance. In practical terms: the migration does not force you to redo audit policies that night, but the bill arrives at the next release — and it's worth putting the conversion on the roadmap rather than discovering it when it becomes mandatory.

**Auto-Indexing**: Oracle 21c has Auto-Indexing available (introduced in 19c). If you don't want Oracle to start creating indexes automatically on the new database, disable it explicitly:

```sql
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE','OFF');
```

**The CDB is not a decision you can defer**: anyone coming from 12.2 tends to treat multitenant as an architectural decision to make at leisure, maybe at the next release. In 21c that leisure doesn't exist: non-CDB is desupported, so the destination is a PDB, full stop. The operational consequence is that the CDB must be created and validated **before** the window, with its own `db_name`, memory parameters, and services — and the objects that in the old database lived outside the transported tablespaces must be recreated in the PDB: profiles, roles, users, directory objects, DB links, scheduler jobs. They don't travel with TTS, and they're the item most often discovered missing on Monday morning.

---

## The numbers from that night

The distinction that matters is between what happened **before**, with the database in production, and what happened **inside** the window. Only the second table is downtime.

**Outside the window — database open, applications running**

| Phase | Duration |
|---|---|
| RMAN level 0 backup `FOR TRANSPORT ALLOW INCONSISTENT` | 1h 15min |
| Backupset transfer (11.8 TB via rsync over 10GbE) | 3h 40min |
| `RESTORE FOREIGN TABLESPACE` on the target | 48 min |
| Intermediate level 1 backups over subsequent days + apply | 1h 05min |
| **Total preparatory work** | **6h 48min** |

**Inside the window — application downtime**

| Phase | Duration |
|---|---|
| Restricted session + tablespaces read-only | 9 min |
| Final level 1 `FOR TRANSPORT` + `DATAPUMP` (delta ~180 GB) | 22 min |
| TTS metadata export on the source | 12 min |
| Delta + dump transfer to the target | 25 min |
| Final `RECOVER FOREIGN DATAFILECOPY` | 18 min |
| `impdp` metadata plug-in into the PDB | 12 min |
| PDB open + tablespaces read-write | 4 min |
| Recreation of non-transported objects (users, roles, DB links, jobs) | 35 min |
| Dictionary statistics + invalid object recompilation | 45 min |
| Validation and application smoke test | 50 min |
| **Total downtime window** | **3h 52min** |

Eight minutes of margin against the four-hour limit. Not much, but enough.

It's worth looking at both tables together: the total work was nearly eleven hours, of which fewer than four were visible to users. We didn't make the migration fast — we moved almost all of it outside the window. That's the only thing this method does, and it was all that was needed.

---

## Validation: the checks you don't skip

After the PDB opens, validation is not optional. Four checks in the right order — all to be run **inside the PDB**, not in the CDB root, otherwise you're looking at the wrong database:

```sql
ALTER SESSION SET CONTAINER = pdb1;
```

**Invalid objects**: the metadata plug-in can leave application objects invalid, typically due to dependencies on objects not yet recreated. `utl_recomp` recompiles them:

```sql
EXECUTE UTL_RECOMP.RECOMP_SERIAL();
-- or parallel
EXECUTE UTL_RECOMP.RECOMP_PARALLEL(4);
```

**Plug-in violations**: this is the check specific to this path, with no equivalent in an in-place upgrade. `PDB_PLUG_IN_VIOLATIONS` lists what the CDB found incompatible when it accepted the PDB — uninstalled options, parameters below threshold, missing components:

```sql
SELECT name, cause, type, status, message
FROM pdb_plug_in_violations
WHERE status <> 'RESOLVED'
ORDER BY time;
```

Rows of type `ERROR` must be resolved before declaring the migration complete; `WARNING` rows should be read one by one, not dismissed wholesale.

**Optimizer statistics**: dictionary statistics need to be regenerated. Application object statistics can be imported from the source or regenerated:

```sql
EXECUTE DBMS_STATS.GATHER_DICTIONARY_STATS;
EXECUTE DBMS_STATS.GATHER_FIXED_OBJECTS_STATS;
```

**Component verification**: all Oracle components must be in `VALID` status:

```sql
SELECT comp_name, version, status FROM dba_registry ORDER BY comp_name;
```

Any component in `INVALID` or `UPGRADED` status (rather than `VALID`) requires attention before declaring the migration complete. In a PDB freshly populated via TTS, the registry reflects the CDB that hosts it: if something is invalid there, the problem belongs to the container, not to the transport.

---

## What stays in the runbook

The migration went through. The PDB has been in production since Monday morning, and the applications didn't notice — or almost: a couple of queries with obsolete hints needed revision in the days that followed, because the 21c optimizer has more accurate statistics and picks different plans.

The takeaway worth carrying forward is not the specific technique — TTS plus RMAN incremental is a documented strategy, not an invention. It's the reasoning that precedes the choice: understanding why Data Pump doesn't work at that scale, understanding what the real constraints are (window, space, destination architecture), and choosing the combination of tools that respects them. The constraint that weighed most wasn't even technical in the strict sense: it was discovering early enough that non-CDB no longer existed as a destination. Discovering it late doesn't extend the window — it changes the project.

The longest part wasn't Saturday night. It was the week before: pre-checks with AutoUpgrade, tests on the target with a data subset, a trial plug-in on a staging PDB, verifying that every step in the runbook produced the expected output. When you arrive at a four-hour window with a runbook already tested, surprises are manageable. When you arrive without having tested it, those eight minutes of margin disappear very quickly.

---

## Official sources

1. Oracle Database Backup and Recovery User's Guide 21c — [Transporting Data Across Platforms](https://docs.oracle.com/en/database/oracle/oracle-database/21/bradv/rman-transporting-data-across-platforms.html) (`BACKUP … FOR TRANSPORT ALLOW INCONSISTENT`, `RESTORE FOREIGN TABLESPACE`, `RECOVER FOREIGN DATAFILECOPY`)
2. Oracle Database Administrator's Guide 21c — [Transporting Tablespaces Between Databases](https://docs.oracle.com/en/database/oracle/oracle-database/21/admin/transporting-data.html)
3. Oracle Database Upgrade Guide 21c — [Manual Non-CDB Release Upgrades to Multitenant Architecture](https://docs.oracle.com/en/database/oracle/oracle-database/21/upgrd/upgrade-scenarios-non-cdb-oracle-databases.html) (non-CDB architecture desupport)
4. Oracle Database Upgrade Guide 21c — [Using the Pre-Upgrade Information Tool](https://docs.oracle.com/en/database/oracle/oracle-database/21/upgrd/using-preupgrade-information-tool-for-oracle-database.html) (`preupgrade.jar` no longer distributed, functions absorbed into AutoUpgrade)
5. Oracle Database Security Guide 21c — [Introduction to Auditing](https://docs.oracle.com/en/database/oracle/oracle-database/21/dbseg/introduction-to-auditing.html) (mixed mode by default, `uniaud_on` for pure unified auditing)
6. Oracle Database Administrator's Reference 21c — [Creating and Populating Password Files](https://docs.oracle.com/en/database/oracle/oracle-database/21/ntqrf/creating-and-populating-password-files.html) (`format`, `IGNORECASE` desupport)

---

## Glossary candidate

- **Transportable Tablespaces (TTS)** — Oracle technique for moving tablespaces between databases by copying the physical datafiles and importing only the metadata via Data Pump. Much faster than a full export/import at large volumes.

- **RMAN Incremental Backup** — an RMAN backup that records only the blocks changed since the last backup at the same or higher level. Level 0 is the full baseline, level 1 is the delta. Used in migration to synchronize the gap between the initial copy and the downtime window.

- **AutoUpgrade** — Java utility (`autoupgrade.jar`) that from Oracle 21c is the single tool for pre-upgrade analysis, fixes, and the upgrade itself. With `-preupgrade … -mode analyze` it produces a read-only report previously generated by `preupgrade.jar`, which is no longer distributed.

- **Foreign datafile copy** — a datafile that RMAN materializes on the destination database from a transportable backupset, before the tablespaces are plugged in. It is the object on which `RESTORE FOREIGN TABLESPACE` and `RECOVER FOREIGN DATAFILECOPY` operate during incremental transport.

- **Unified Auditing** — auditing framework introduced in 12c that consolidates logs (database, fine-grained, SYSDBA) into the `AUDSYS` structure. In 21c it coexists with traditional auditing in *mixed mode*, which remains the default; *pure* unified auditing requires relinking the binary with `uniaud_on`.

- **Auto-Indexing** — Oracle feature (available from 19c, configurable in 21c) that analyzes the workload and automatically creates invisible indexes, validates them, and makes them visible if they improve performance. Must be explicitly disabled if not wanted in production.
