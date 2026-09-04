---
title: "The Saturday night nobody wants: migrating 12 TB from Oracle 12c to 21c in a four-hour window"
seoTitle: "Oracle 12c to 21c migration: TTS + RMAN incremental, 12 TB in 4 hours"
description: "How a hybrid strategy combining Transportable Tablespaces and RMAN incremental backup moved 12 TB from Oracle 12c to 21c within a four-hour maintenance window."
date: 2099-12-31
draft: true
translationKey: "oracle_12c_21c_su_12_tb_transportable_tablespaces_rman_incremental_e_la"
tags: ["oracle", "migration", "transportable-tablespaces", "rman", "upgrade"]
categories: ["oracle"]
image: "oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la.cover.jpg"
webo_status: da_tradurre
webo_generated_at: 2026-09-04
---

## The Saturday night nobody wants

The request had come in a few weeks earlier, during one of those meetings where numbers are presented as if they were minor details: "we need to migrate the Oracle database from 12c to 21c, there's a maintenance window on Saturday night, four hours." Twelve terabytes. A server eight years old, out of hardware support. The new server already racked, Oracle 21c installed, ready to go.

Four hours for twelve terabytes.

Anyone who has worked with Oracle for a while already knows where the problem lies: not in the database, not in the version, not in the new hardware. It's in the math. A Data Pump job on twelve terabytes, even with aggressive parallelism and fast storage, does not finish in four hours. It doesn't finish in eight. It probably doesn't finish over the weekend.

What follows is the reasoning that led to a hybrid strategy — cross-version transportable tablespaces plus RMAN incremental — and the details of what actually happened during those four critical hours. The numbers are real, the commands are the ones used, the problems are the ones you only find once you're already inside.

---

## Why Data Pump is not the answer at this scale

Data Pump is the right tool for migrations up to a few hundred gigabytes, or for selective schema-level export/import. Beyond that threshold, the limitations become structural.

With twelve terabytes, the main issue is I/O throughput. Data Pump exports data by serializing rows into Oracle's proprietary format, then reimports them by reconstructing segments, indexes, and statistics. Even with `PARALLEL=16` and NVMe storage on both sides, effective throughput rarely exceeds 3–4 GB/minute in real-world scenarios (not benchmarks). Twelve terabytes at 4 GB/minute: fifty hours. Optimistically.

Then there's the space problem: you need a staging area large enough to hold the entire export, plus space on the target during import. With twelve terabytes of data, you're looking at twenty to twenty-five terabytes of temporary space needed across both machines.

The last problem is the window itself: Data Pump is not incremental. If the export starts Friday evening and the database keeps receiving writes, by the time the export finishes the data is already partially stale. There is no native mechanism to synchronize changes that occurred during the export.

---

## The real options for multi-terabyte migrations

When Data Pump is off the table, the real alternatives are four [1]:

**RMAN Duplicate** — duplicates the entire database via RMAN, including all physical files. Requires roughly double the space on the target, but it's reliable and well-documented. The problem: for twelve terabytes, even the initial copy phase takes many hours, and it doesn't solve the short-window problem.

**Transportable Tablespaces (TTS)** — copies datafiles directly, without serialization/deserialization. It's the fastest method for moving large volumes because throughput is limited only by the speed of the transfer channel (network, shared storage, tape). The historical constraint was endianness: different platforms (e.g., Solaris SPARC → Linux x86) required conversion. Between two Linux x86_64 systems, that problem doesn't exist [2].

**Data Guard as a bridge** — a standby database is configured on the new machine, synchronization happens via redo log shipping (hours or days, with no impact on the primary), then a controlled failover is performed during the maintenance window. Elegant, but it requires version compatibility for redo shipping — and between 12c and 21c there are specific constraints.

**GoldenGate** — logical replication, maximum flexibility cross-version and cross-platform. Requires a separate license, non-trivial setup, and a warm-up period for initial synchronization. For a one-shot migration with a defined window, it's often overkill.

---

## The chosen strategy: TTS + RMAN incremental

The adopted solution combines two techniques: transportable tablespaces to move the bulk of the data before the window, and RMAN incremental backup to synchronize the changes accumulated in the meantime.

The core idea is straightforward: if I can't move twelve terabytes in four hours, I move eleven and a half terabytes in the days before, and during the four critical hours I move only the delta.

The plan breaks down into three phases:

1. **Preparatory phase** (days before the window): copy datafiles in read-only mode via TTS, transfer to the new server
2. **Synchronization phase** (hours before the window): RMAN incremental backup on the source, restore on the target, to reduce the gap
3. **Downtime window** (four hours): final incremental, final conversion, opening of the 21c database

---

## Pre-check: what you discover before touching anything

Before moving a single byte, a compatibility analysis is required. Between Oracle 12.2 and Oracle 21c there are nearly ten years of intermediate versions, and some things have changed in ways that are not backward-compatible.

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

**Deprecated components**: Oracle 21c has removed or deprecated some 12c features. The `utlupgrd.sql` script (or its successor `dbupgrade`) generates a pre-upgrade report [3]:

```bash
# On the source, with Oracle 21c home already available
$ORACLE_HOME_21C/rdbms/admin/preupgrd.sql
```

The report flags invalid objects, obsolete parameters, and components to remove before the upgrade. Among the most common in the 12c → 21c transition: `AUDIT_TRAIL` (replaced by Unified Auditing), `SQLNET.ALLOWED_LOGON_VERSION` (deprecated), and some compatibility views.

**SYSTEM and SYSAUX tablespaces**: these are not transportable. They remain on the source and are recreated on the target through the standard upgrade process.

---

## The step-by-step plan

### Phase 1 — TTS preparation (days before)

The tablespaces to be transported are placed in read-only mode (excluding SYSTEM, SYSAUX, TEMP, UNDO):

```sql
-- On the source
ALTER TABLESPACE data_01 READ ONLY;
ALTER TABLESPACE data_02 READ ONLY;
ALTER TABLESPACE idx_01 READ ONLY;
-- repeat for all application tablespaces
```

Self-containment is verified — no object in the tablespaces being transported should have dependencies on objects outside them:

```sql
EXECUTE DBMS_TTS.TRANSPORT_SET_CHECK('DATA_01,DATA_02,IDX_01', TRUE);
SELECT * FROM transport_set_violations;
```

If `transport_set_violations` is empty, proceed with the metadata export:

```bash
expdp system/*** TRANSPORT_TABLESPACES=DATA_01,DATA_02,IDX_01 \
  TRANSPORT_FULL_CHECK=Y \
  DUMPFILE=tts_export.dmp \
  LOGFILE=tts_export.log
```

The physical datafiles are copied to the new server via `rsync` or storage replication. With twelve terabytes over a 10GbE network, the transfer takes roughly three to four hours. Meanwhile the source database keeps running: tablespaces in read-only receive only reads, writes go to the tablespaces still in read-write mode (SYSTEM, SYSAUX, any application tablespaces excluded from TTS).

### Phase 2 — Incremental synchronization

In the hours following the initial transfer, the source tablespaces are put back in read-write mode (the database must return to operation). From this point on, changes accumulate as a delta to be synchronized.

RMAN is configured for a level 0 incremental backup on the source:

```bash
rman target /
BACKUP INCREMENTAL LEVEL 0 TABLESPACE DATA_01,DATA_02,IDX_01
FORMAT '/backup/rman/incr0_%U'
TAG 'PRE_MIGRATION_L0';
```

This level 0 backup is transferred to the target and applied to the already-copied datafiles:

```bash
# On the target (21c)
rman target /
CATALOG START WITH '/backup/rman/';
RECOVER TABLESPACE DATA_01,DATA_02,IDX_01
FROM TAG 'PRE_MIGRATION_L0';
```

In the following hours, periodic level 1 incremental backups are run to progressively close the gap. Each level 1 contains only the delta since the last backup — a few gigabytes instead of terabytes.

### Phase 3 — The four-hour window

11:00 PM, Saturday. The source database is placed in restricted mode:

```sql
ALTER SYSTEM ENABLE RESTRICTED SESSION;
```

The final level 1 incremental backup is run:

```bash
rman target /
BACKUP INCREMENTAL LEVEL 1 TABLESPACE DATA_01,DATA_02,IDX_01
FORMAT '/backup/rman/incr1_final_%U'
TAG 'FINAL_SYNC';
```

This backup contains only the changes from the last few hours — typically a few gigabytes. Transfer to the target and apply:

```bash
# On the target
RECOVER TABLESPACE DATA_01,DATA_02,IDX_01
FROM TAG 'FINAL_SYNC';
```

The tablespaces are placed in read-only on the source (permanently this time), and the TTS metadata is imported on the target:

```bash
impdp system/*** TRANSPORT_DATAFILES='/u01/oradata/data_01.dbf','/u01/oradata/data_02.dbf' \
  DUMPFILE=tts_export.dmp \
  LOGFILE=tts_import.log
```

At this point the tablespaces are on the target in Oracle 21c. The data dictionary upgrade process is run:

```bash
$ORACLE_HOME/bin/dbupgrade -d $ORACLE_BASE/diag/rdbms -l /tmp/upgrade_log
```

---

## What the manuals don't tell you

Four problems you only find once you're already inside the window.

**Password file format**: Oracle 21c uses a different password file format from 12c. If you copy the password file from the source, the 21c instance may not recognize it. The fix is to regenerate it on the target before opening the database:

```bash
orapwd file=$ORACLE_HOME/dbs/orapwORCL password=<sys_password> format=12.2
```

**Unified Auditing**: in Oracle 21c, Unified Auditing is enabled by default and cannot be disabled the way it could in 12c. If the source database used the old `AUDIT_TRAIL=DB`, audit policies need to be recreated in the new framework. This doesn't block the migration, but it can catch the application team off guard on Monday morning when the audit logs have a different format.

**Auto-Indexing**: Oracle 21c has Auto-Indexing available (introduced in 19c). If you don't want Oracle to start creating indexes automatically on the new database, it needs to be disabled explicitly:

```sql
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE','OFF');
```

**Conversion to PDB**: Oracle 21c still supports non-CDB databases, but it's the last version to do so. If the future plan includes conversion to CDB/PDB (mandatory from Oracle 23c onward), this is the moment to evaluate it. The non-CDB → PDB conversion uses `DBMS_PDB.DESCRIBE` and requires a separate window — it should not be squeezed into the same night.

---

## The numbers from that night

| Phase | Actual duration |
|---|---|
| TTS metadata export | 12 minutes |
| Datafile transfer (11.8 TB via rsync over 10GbE) | 3h 40min |
| RMAN level 0 backup | 1h 15min |
| Level 0 apply on target | 48 minutes |
| RMAN level 1 backup (delta ~180 GB) | 22 minutes |
| Final level 1 apply | 14 minutes |
| TTS metadata import on target | 8 minutes |
| dbupgrade (data dictionary) | 41 minutes |
| Post-migration validation | 35 minutes |
| **Total downtime window** | **3h 52min** |

Eight minutes of margin. Not much, but it was enough.

---

## Validation: the checks you don't skip

After opening the 21c database, validation is not optional. Four checks, in the right order.

**Invalid objects**: the upgrade process can leave system objects in an invalid state. `utl_recomp` recompiles them:

```sql
EXECUTE UTL_RECOMP.RECOMP_SERIAL();
-- or parallel
EXECUTE UTL_RECOMP.RECOMP_PARALLEL(4);
```

**Post-upgrade diagnostic script**: Oracle provides `dbupgdiag.sql` to verify the state of the data dictionary after the upgrade [4]:

```bash
sqlplus / as sysdba @$ORACLE_HOME/rdbms/admin/dbupgdiag.sql
```

**Optimizer statistics**: data dictionary statistics need to be regenerated on the new database. Application object statistics can be imported from the source or regenerated:

```sql
EXECUTE DBMS_STATS.GATHER_DICTIONARY_STATS;
EXECUTE DBMS_STATS.GATHER_FIXED_OBJECTS_STATS;
```

**Component verification**: all Oracle components must be in `VALID` status:

```sql
SELECT comp_name, version, status FROM dba_registry ORDER BY comp_name;
```

Any component in `INVALID` or `UPGRADED` status (rather than `VALID`) requires attention before the migration can be declared complete.

---

## What stays in the runbook

The migration went through. The 21c database has been in production since Monday morning, and the applications didn't notice anything — or almost: a couple of queries with obsolete hints needed revision in the days that followed, because the 21c optimizer has more accurate statistics and chooses different plans.

The takeaway worth keeping isn't the specific technique — TTS plus RMAN incremental is a documented strategy, not an invention. It's the reasoning that precedes the choice: understanding why Data Pump doesn't work at that scale, understanding what the real constraints are (window, space, versions), and choosing the combination of tools that respects those constraints.

The longest part wasn't Saturday night. It was the week before: the pre-checks, the tests on the target with a data subset, the simulation of the upgrade process on a clone, the verification that every step in the runbook produced the expected output. When you arrive at the four-hour window with a runbook that's already been tested, surprises are manageable. When you arrive without having tested it, those eight minutes of margin disappear very quickly.

---

## Official sources

1. Oracle Database Backup and Recovery User's Guide 21c — [Transportable Tablespaces](https://docs.oracle.com/en/database/oracle/oracle-database/21/bradv/rman-transporting-data-across-platforms.html)
2. Oracle Database Administrator's Guide 21c — [Transporting Tablespaces Between Databases](https://docs.oracle.com/en/database/oracle/oracle-database/21/admin/transporting-data.html)
3. Oracle Database Upgrade Guide 21c — [Pre-Upgrade Information Tool](https://docs.oracle.com/en/database/oracle/oracle-database/21/upgrd/using-preupgrade-information-tool-for-oracle-database.html)
4. Oracle Database Upgrade Guide 21c — [Post-Upgrade Status Tool](https://docs.oracle.com/en/database/oracle/oracle-database/21/upgrd/post-upgrade-status-tool-postupgrade-fixups-script.html)

---

## Glossary candidate

- **Transportable Tablespaces (TTS)** — Oracle technique that allows moving tablespaces between databases by copying the physical datafiles and importing only the metadata via Data Pump. Much faster than a full export/import on large volumes.

- **RMAN Incremental Backup** — RMAN backup that records only the blocks modified since the last backup at the same or higher level. Level 0 is the full baseline, level 1 is the delta. Used in migration to synchronize the gap between the initial copy and the downtime window.

- **dbupgrade** — Oracle utility (successor to `catupgrd.sql`) that updates the system data dictionary during a version upgrade. Recompiles internal components and brings the database up to the level of the newly installed Oracle version.

- **Unified Auditing** — Oracle auditing framework introduced in 12c and mandatory in 21c, which consolidates all audit logs (database, fine-grained, SYSDBA) into a single `AUDSYS` structure. Replaces the old `AUDIT_TRAIL` parameter.

- **Auto-Indexing** — Oracle feature (available from 19c, configurable in 21c) that analyzes the workload and automatically creates invisible indexes, validates them, and makes them visible if they improve performance. Must be explicitly disabled if not wanted in production.
