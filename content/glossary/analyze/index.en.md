---
title: "ANALYZE"
description: "The PostgreSQL command that updates table statistics used by the optimizer to choose the execution plan."
translationKey: "glossary_analyze"
tags: ["glossary"]
---

`ANALYZE` is the PostgreSQL command that collects statistics about data distribution in tables and stores them in the `pg_statistic` catalog (readable through the `pg_stats` view). The optimizer uses these statistics to estimate cardinality — how many rows each operation will return — and choose the most efficient execution plan.

The collected statistics include: most common values, distribution histograms, number of distinct values, and NULL percentage for each column. Without up-to-date statistics, the optimizer is forced to guess, and wrong estimates lead to disastrous execution plans — such as choosing a nested loop on millions of rows thinking there are only hundreds.

PostgreSQL runs ANALYZE automatically through autovacuum, but the default threshold (50 rows + 10% of live rows) can be too high for tables that grow rapidly. After bulk imports or significant changes in data distribution, a manual ANALYZE is the first diagnostic action to take.

## Related articles

- [EXPLAIN ANALYZE is not enough: how to really read a PostgreSQL execution plan](/en/posts/postgresql/explain-analyze-postgresql/)
