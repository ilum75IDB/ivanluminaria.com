---
title: "XTTS (Cross-Platform Transportable Tablespaces)"
description: "Oracle method for migrating multi-terabyte databases across versions with minimal downtime, using cyclic RMAN incremental backups."
translationKey: "glossary_xtts"
aka: "Cross-Platform Transportable Tablespaces"
articles:
  - "/posts/oracle/oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback"
---

XTTS (Cross-Platform Transportable Tablespaces) is the Oracle technique for moving tablespaces between different platforms and database versions — for example from Oracle 11gR2 on Linux x86 to Oracle 19c on OCI — by physically transporting datafiles rather than performing a logical export/import. For databases in the terabyte range, this approach reduces the final cutover downtime from days to a few hours.

## How it works

The process is structured in three distinct phases:

1. **RMAN level 0 backup** — a full copy of the source tablespace datafiles, transferred to the destination and restored.
2. **Cyclic incrementals (level 1)** — run multiple times in the weeks before cutover, progressively shrinking the delta between source and destination.
3. **Final cutover** — the last incremental is applied with the source tablespace in read-only mode; plugging it into the destination completes the migration.

```bash
# Example: generating the RMAN script for a level 0 backup
$ORACLE_HOME/perl/bin/perl xttdriver.pl --backup_to_dest \
  --tablespaces USERS,FINANCE \
  --level 0
```

The `xttdriver.pl` script (available on Oracle MOS) orchestrates backup, endian conversion, and file transfer.

## When to use it

XTTS is the right choice when:

- The database exceeds a few hundred GB and a Data Pump export would require unacceptable maintenance windows.
- The migration crosses major versions (e.g. 11g → 19c) or platforms with different endianness.
- The SLA mandates a maximum downtime measurable in hours, not days.

The main drawback is operational complexity: it requires precise coordination between source and destination DBAs, character set compatibility checks, and separate handling of non-transportable objects (sequences, synonyms, grants) that must be migrated independently via Data Pump.
