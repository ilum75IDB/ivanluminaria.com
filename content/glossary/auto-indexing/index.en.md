---
title: "Auto-Indexing"
description: "Oracle feature (from 19c) that monitors SQL workload, creates invisible indexes, and promotes them automatically when performance improves."
translationKey: "glossary_auto_indexing"
aka: "Automatic Indexing (Oracle)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

Auto-Indexing is an Oracle 19c feature that hands index lifecycle management over to the database engine: workload analysis, experimental creation, validation, and promotion. Oracle 21c extended the configurability of this behavior with finer-grained controls.

## How it works

The process runs in three automatic phases:

1. **Analysis** — Oracle monitors the SQL workload through the Automatic Workload Repository (AWR) and identifies queries that could benefit from new indexes.
2. **Invisible creation** — Candidate indexes are created as `INVISIBLE`, meaning the optimizer ignores them under normal conditions.
3. **Validation and promotion** — Oracle runs internal tests comparing execution plans. If the index reduces cost, it is promoted to `VISIBLE`; otherwise it stays invisible or is dropped.

```sql
-- Check Auto-Indexing configuration
SELECT * FROM DBA_AUTO_INDEX_CONFIG;

-- Enable / disable explicitly
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE', 'IMPLEMENT');
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE', 'OFF');
```

## Operational context

Auto-Indexing targets OLTP environments with variable or hard-to-profile workloads. On production databases with stable schemas and already-tuned indexes, the risk is redundant indexes that increase INSERT/UPDATE/DELETE overhead and consume tablespace.

**Practical recommendation**: in critical production environments, run in `REPORT ONLY` mode first before switching to `IMPLEMENT`. Disable explicitly with `OFF` when the DBA owns the indexing strategy manually.

```sql
-- Report mode: analyzes but does not create indexes
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE', 'REPORT ONLY');

-- List automatically managed indexes
SELECT INDEX_NAME, STATUS, AUTO
FROM DBA_INDEXES
WHERE AUTO = 'YES';
```
