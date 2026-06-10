---
title: "SPFILE"
description: "SPFILE (Server Parameter File) is Oracle's binary configuration file read at startup, editable at runtime without restarting the database."
translationKey: "glossary_spfile"
aka: "Server Parameter File"
articles:
  - "/posts/oracle/quali-sono-i-files-critici-di-un-db-oracle"
---

The SPFILE is the binary file Oracle reads at startup to initialize instance parameters: `db_name`, `control_files`, `memory_target`, `sga_target`, and many others. Unlike its text-based predecessor PFILE (`init.ora`), the SPFILE cannot be edited manually with a text editor — changes go through SQL commands.

## How it works

At startup, Oracle looks for the SPFILE in a default location (`$ORACLE_HOME/dbs/spfile<SID>.ora` on Linux). If not found, it falls back to the PFILE. Parameter changes are made with `ALTER SYSTEM SET`, which writes directly to the binary file:

```sql
-- Persistent change (survives restart)
ALTER SYSTEM SET memory_target = 2G SCOPE = SPFILE;

-- In-memory only (lost on restart)
ALTER SYSTEM SET memory_target = 2G SCOPE = MEMORY;

-- Both in memory and in the file
ALTER SYSTEM SET memory_target = 2G SCOPE = BOTH;
```

The `SCOPE` parameter controls where the change is applied: `SPFILE`, `MEMORY`, or `BOTH`.

## Operational context

The SPFILE is the authoritative source for persistent instance configuration. It must be included in RMAN backups, which handles it natively. In RAC (Real Application Clusters) environments, a single shared SPFILE on ASM governs all nodes, with per-instance values settable via the `SID.*` prefix.

A common mistake is manually editing the binary file: the instance will fail to start. If the SPFILE becomes corrupted, restore it from an RMAN backup or recreate it from a PFILE using `CREATE SPFILE FROM PFILE`.
