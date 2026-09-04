---
title: "MERGE"
description: "SQL statement that combines INSERT and UPDATE into a single atomic operation (upsert), removing the dual table-access pattern common in legacy ETL pipelines."
translationKey: "glossary_merge"
aka: "UPSERT, MERGE INTO"
articles:
  - "/posts/data-warehouse/etl-oracle-da-4-ore-a-25-minuti-con-staging-tables-merge-e-parallel-dml"
---

`MERGE` is a standard SQL statement (ISO/IEC 9075) that combines INSERT and UPDATE logic into a single atomic operation. The engine touches the target table once, compares each source row against its counterpart in the target, and decides on the fly whether to insert, update, or — where supported — delete.

## How it works

The basic syntax has three main clauses: `USING` (data source), `ON` (join condition), and `WHEN MATCHED` / `WHEN NOT MATCHED` (conditional actions).

```sql
MERGE INTO orders_dw tgt
USING staging_orders src
  ON (tgt.order_id = src.order_id)
WHEN MATCHED THEN
  UPDATE SET tgt.amount = src.amount,
             tgt.status = src.status
WHEN NOT MATCHED THEN
  INSERT (order_id, amount, status)
  VALUES (src.order_id, src.amount, src.status);
```

The entire operation is wrapped in a single transaction: either everything succeeds (implicit or explicit COMMIT), or nothing is written (automatic ROLLBACK on error).

## When to use it

`MERGE` is the natural fit for ETL/ELT pipelines loading incremental data into a data warehouse: the staging table carries new or changed rows, and `MERGE` applies them to the target without a preliminary SELECT to discriminate between INSERT and UPDATE candidates.

Compared to the legacy `SELECT → IF EXISTS → INSERT/UPDATE` pattern:

- **Eliminates the race condition** between read and write in concurrent environments.
- **Reduces round-trips** to the database.
- **Supports parallelization** (e.g., `PARALLEL DML` in Oracle) on partitioned tables.

The main drawback is portability: syntax differs across Oracle, SQL Server, PostgreSQL (which uses `INSERT ... ON CONFLICT`) and MySQL (`INSERT ... ON DUPLICATE KEY UPDATE`), making cross-vendor reuse difficult without an abstraction layer.
