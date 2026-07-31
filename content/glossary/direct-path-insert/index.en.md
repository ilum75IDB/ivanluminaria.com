---
title: "Direct-path insert"
description: "Oracle data loading mode that bypasses the buffer cache and writes directly to datafiles using the /*+ APPEND */ hint."
translationKey: "glossary_direct_path_insert"
aka: "Direct-path insert (Oracle APPEND hint)"
articles:
  - "/posts/oracle/articolo-oracle-assertions-in-oracle-26ai"
---

Direct-path insert is an Oracle write mode that bypasses the buffer cache and places data directly into datafiles, above the segment's high-water mark. It is activated via the `/*+ APPEND */` hint on an `INSERT` statement and is typically used in bulk loading operations to reduce I/O overhead and the volume of redo generated.

## How it works

During a Direct-path insert, Oracle does not look for free blocks within the existing segment: it allocates new space beyond the high-water mark and writes directly to disk, skipping the buffer pool entirely. Redo generation is minimal (or zero in `NOLOGGING` mode), making the operation significantly faster than a conventional insert on large datasets.

```sql
INSERT /*+ APPEND */ INTO target_table
SELECT * FROM source_table;
COMMIT;
```

Until the COMMIT, the table is locked for writes by other sessions: no other process can insert rows into the same table during the transaction.

## When to use it and limitations

Direct-path insert is suited for ETL pipelines, bulk loads, and staging table population. It comes with several operational restrictions worth noting:

- **Integrity constraints**: `CHECK` and `NOT NULL` constraints are enforced, but foreign key constraints may need to be disabled or deferred to preserve performance.
- **Triggers**: `BEFORE/AFTER INSERT ROW` triggers are not fired in direct-path mode.
- **Assertions (Oracle 23ai+)**: behavior with Assertions must be verified case by case, as the validation mechanism differs from that of a conventional insert.

In environments where Assertions are active, explicit testing is required before adopting Direct-path insert in production.
