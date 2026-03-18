---
title: "Nested Loop"
description: "Nested Loop Join — the join strategy that scans the inner table for each row of the outer table, ideal for small datasets with an index."
translationKey: "glossary_nested_loop"
aka: "Nested Loop Join"
articles:
  - "/posts/postgresql/explain-analyze-postgresql"
---

**Nested loop** is the simplest join strategy: for each row in the outer table, the database looks for matching rows in the inner table. It works like a double nested `for` loop — hence the name.

## How it works

The optimizer picks one table as "outer" and one as "inner". For each row in the outer table, it performs a lookup in the inner table on the join column. If the inner table has an index on the join column, each lookup is a direct B-tree access. Without an index, each lookup becomes a full sequential scan.

## When it's the right choice

Nested loop is unbeatable when the outer table has few rows and the inner table has an index on the join column. A join on 100 outer rows with a B-tree index on the inner table is practically instantaneous: few iterations, direct access, minimal memory.

It's also the preferred strategy for dimension lookups in data warehouses, where a filtered fact table (few rows) is joined with an indexed dimension table.

## What can go wrong

It becomes a disaster when the optimizer picks it on large datasets by mistake — typically because statistics underestimate the row count. A nested loop on 2 million outer rows means 2 million lookups in the inner table. Without an index, each lookup is a full scan.

In these cases a hash join or merge join would be orders of magnitude faster. The root cause is almost always a wrong cardinality estimate: stale statistics or a `default_statistics_target` that's too low.
