---
title: "Parallel DML"
description: "Oracle feature that distributes INSERT, UPDATE, DELETE and MERGE across multiple slave processes. Requires explicit session-level enablement to take effect."
translationKey: "glossary_parallel_dml"
aka: "Parallel DML (Oracle Parallel Execution)"
articles:
  - "/posts/data-warehouse/etl-oracle-da-4-ore-a-25-minuti-con-staging-tables-merge-e-parallel-dml"
---

Parallel DML is the Oracle mechanism that splits write operations — INSERT, UPDATE, DELETE, and MERGE — across multiple parallel slave processes coordinated by a single query coordinator. Unlike Parallel Query, which activates automatically on tables with a parallel degree set, Parallel DML requires explicit opt-in at the session level before any hints are honored.

## How it works

Enable it with a DDL statement on the current session:

```sql
ALTER SESSION ENABLE PARALLEL DML;
```

Only after this command do `/*+ PARALLEL(table, degree) */` hints take effect on DML statements. Without the session-level enablement, Oracle silently discards the hints — no error, no warning — making the issue hard to spot during performance troubleshooting.

```sql
INSERT /*+ PARALLEL(target_table, 8) */ INTO target_table
SELECT * FROM staging_table;
```

Each slave process handles a logical partition of the data. The COMMIT at the end consolidates all writes atomically. Until the COMMIT, the target table is not accessible to other DML sessions.

## When to use it

Parallel DML is the right tool for ETL loads in Data Warehouse environments where tens or hundreds of millions of rows must be processed within tight batch windows. The speedup scales with available I/O bandwidth and the parallelism degree configured on the table or specified in the hint.

Key constraints to keep in mind:

- Not applicable to tables with enabled triggers
- Incompatible with certain types of referential integrity constraints
- The session must not have any open DML transactions before enablement
