---
title: "Staging Table"
description: "Temporary table used as a landing area for raw data in an ETL pipeline, separating ingestion from transformation and final load."
translationKey: "glossary_staging_table"
aka: "Staging area, landing table"
articles:
  - "/posts/data-warehouse/etl-oracle-da-4-ore-a-25-minuti-con-staging-tables-merge-e-parallel-dml"
---

A staging table is an intermediate table that receives raw data from the source before any transformation or load into the final destination. It cleanly separates the three phases of an ETL process, making each phase independent, observable, and restartable after a failure.

## How it works

Data is first bulk-loaded into the staging table — often with referential integrity constraints disabled to maximise INSERT throughput — and only afterwards are quality checks, transformations, and the MERGE into target tables applied.

```sql
-- 1. Raw load into the staging table (no active constraints)
INSERT /*+ APPEND */ INTO stg_orders
SELECT * FROM ext_orders_source;

-- 2. Transform and MERGE into the target table
MERGE INTO orders tgt
USING stg_orders src
  ON (tgt.order_id = src.order_id)
WHEN MATCHED THEN UPDATE SET tgt.status = src.status
WHEN NOT MATCHED THEN INSERT (order_id, status) VALUES (src.order_id, src.status);
```

Processing data in bulk against the staging table instead of row-by-row dramatically reduces the number of COMMITs and the pressure on the redo log.

## When to use it

Staging tables are the right tool whenever data volume makes in-flight transformation during ingestion impractical. They are especially useful when:

- the ETL process must be restartable (simply re-run from the last TRUNCATE/INSERT on the staging table);
- the source system cannot tolerate slow queries or long-running transactions;
- you want to apply Parallel DML during the MERGE phase without locking the source.

The main trade-off is additional disk space and the latency introduced by the double write, which is acceptable in virtually all batch contexts.
