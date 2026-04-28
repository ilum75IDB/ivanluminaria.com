---
title: "pg_stat_user_indexes"
description: "PostgreSQL system view that tracks how many times each index has been used by the planner — the primary tool for identifying useless indexes in production."
translationKey: "glossary_pg_stat_user_indexes"
aka: ""
articles:
  - "/posts/postgresql/postgresql-indici-quando-fanno-male"
---

`pg_stat_user_indexes` is a PostgreSQL system view that exposes usage statistics for all indexes on user tables (excluding system ones). For each index it keeps a count of how many times the planner has actually chosen it.

## How it works

The key column is `idx_scan`: it starts from zero at database boot (or at the last `pg_stat_reset()`) and increments by one each time the planner picks that index to execute a query. Other useful columns include:

- `idx_tup_read` — how many row pointers have been read from the index
- `idx_tup_fetch` — how many rows have actually been fetched from the table via the index
- `relname` — name of the table the index belongs to
- `indexrelname` — name of the index

## What it's for

It's the primary tool for identifying **useless indexes in production**. If an index has `idx_scan = 0` after weeks or months of activity, the planner has never found it useful for any query. It's a candidate for removal (after verifying it's not an index used only for uniqueness constraints or foreign keys).

## When to use it

Consult it as first diagnostic when you want to understand how much the indexes of a table are really worth, especially when there are many. Typical example:

```sql
SELECT relname, indexrelname, idx_scan,
       pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
WHERE relname = 'tablename'
ORDER BY idx_scan ASC;
```

Pair with `pg_stat_reset()` if you need to zero the statistics after a significant workload change.
