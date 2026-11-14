---
title: "Flashback Query"
description: "Oracle feature that queries a past state of the database using a timestamp or SCN, reading directly from undo segments without any restore."
translationKey: "glossary_flashback_query"
aka: "Oracle Flashback Query"
articles:
  - "/posts/oracle/oracle-flashback-recupero-dati-logici-senza-downtime-da-query-a-database"
---

Flashback Query is an Oracle Database feature that lets you run a `SELECT` against a past state of your data by specifying a point in time via timestamp or System Change Number (SCN). No backup restore or downtime is involved: historical data is read directly from undo segments.

## How it works

Oracle retains previous versions of data blocks in undo tablespaces for a configurable retention window (`UNDO_RETENTION`). Flashback Query uses this mechanism to reconstruct the view of data as it existed at a given moment.

```sql
-- Query using a timestamp
SELECT *
FROM orders AS OF TIMESTAMP (SYSTIMESTAMP - INTERVAL '2' HOUR)
WHERE status = 'CANCELLED';

-- Query using an SCN
SELECT *
FROM orders AS OF SCN 4521890;
```

The `AS OF` clause works on any `SELECT`, including queries with JOINs and subqueries.

## When to use it

Typical scenarios include recovering rows deleted or modified by mistake, auditing data before a problematic transaction, and checking what a table contained before a nightly batch run. The main constraint is undo availability: if `UNDO_RETENTION` is set too low or the undo tablespace is under pressure, Oracle may overwrite historical blocks before the configured window expires. For longer time ranges or row-level change history, Flashback Versions Query or Flashback Data Archive are the appropriate tools.
