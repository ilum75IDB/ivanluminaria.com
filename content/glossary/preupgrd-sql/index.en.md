---
title: "preupgrd.sql"
description: "Oracle pre-upgrade script to run on the source instance: checks invalid objects, deprecated parameters, and compatibility issues before cutover."
translationKey: "glossary_preupgrd_sql"
aka: "Oracle Pre-Upgrade Information Tool"
articles:
  - "/posts/oracle/oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback"
---

`preupgrd.sql` is the pre-upgrade script shipped with Oracle 19c (and earlier releases under similar names). It runs against the **source** instance before any migration procedure begins, producing a text report that captures the database state relative to the target version's requirements.

## What it does

The script queries the data dictionary and internal views to detect:

- `INVALID` objects that could block the post-upgrade recompilation phase
- initialization parameters that are deprecated or removed in the target version
- obsolete features still active (e.g., `COMPATIBLE` mismatches, out-of-range `DB_BLOCK_SIZE`)
- timezone, character set, and optional component issues that cannot be migrated automatically

Output is written to `$ORACLE_BASE/cfgtoollogs/db_unique_name/preupgrade/` as plain text files and, in recent versions, as ready-to-run corrective SQL scripts.

```bash
sqlplus / as sysdba @$ORACLE_HOME/rdbms/admin/preupgrd.sql
```

## When to use it

`preupgrd.sql` should be run **weeks before** cutover, not on migration night. The DBA uses the report to plan remediation: recompiling invalid objects, removing obsolete parameters, updating optional components. In critical production environments — such as 8 TB financial databases — the report feeds directly into the rollback plan and maintenance window estimation.

## Operational notes

Oracle ships updated versions of the script with each PSU/RU. Before running it, confirm you are using the copy from the **target version's** `ORACLE_HOME`, not the source's: that is where the up-to-date validation logic resides.
