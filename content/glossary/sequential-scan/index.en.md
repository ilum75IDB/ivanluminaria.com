---
title: "Sequential Scan"
description: "Read operation where PostgreSQL reads all blocks of a table without using indexes, efficient on small tables but problematic on large ones."
translationKey: "glossary_sequential-scan"
aka: "Seq Scan / Full Table Scan"
articles:
  - "/posts/postgresql/pg-stat-statements"
---

A **Sequential Scan** (Seq Scan) is the operation where PostgreSQL reads a table from start to finish, block by block, without using any index. It's PostgreSQL's equivalent of Oracle's Full Table Scan.

## When it's normal

On small tables (a few thousand rows), a sequential scan is often the most efficient choice. Reading an entire table sequentially is faster than index lookups when the table fits in a few pages. The optimizer chooses a sequential scan when it estimates it's cheaper than an index scan.

## When it's a problem

On large tables (millions of rows), a sequential scan to return few rows is a red flag. It means an appropriate index is missing or the table statistics are outdated and the optimizer is making wrong estimates. pg_stat_statements helps identify these situations by showing queries with the worst blocks read / rows returned ratio.

## How to diagnose it

EXPLAIN shows "Seq Scan on table" in the execution plan. If the subsequent filter discards most rows (rows removed by filter >> rows), an index on the filter column is almost certainly needed.
