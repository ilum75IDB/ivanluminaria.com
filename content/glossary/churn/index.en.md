---
title: "Churn"
description: "Measure of how much a database table changes after initial data insertion, in terms of UPDATEs and DELETEs. Determines the maintenance cost of indexes."
translationKey: "glossary_churn"
articles:
  - "/posts/postgresql/like-optimization-postgresql"
---

A table's **churn** is the measure of how much its data changes after insertion. A high-churn table undergoes frequent UPDATEs and DELETEs; a low-churn table is predominantly append-only (INSERT only).

## How it works

In PostgreSQL, every UPDATE creates a new row version (due to the MVCC model) and the old version becomes a dead tuple. DELETEs also create dead tuples. The higher the churn, the more work VACUUM and indexes must do to maintain performance. A GIN index on a high-churn table can significantly degrade write performance.

## What it's for

Evaluating churn before creating an index is essential to avoid solving a read problem by creating a write problem. On an append-only table (zero UPDATEs, zero DELETEs, zero dead tuples), a GIN index has minimal write impact. On a high-churn table, the same index could become a bottleneck.

## When to use it

Churn is analysed by checking table statistics: daily UPDATE and DELETE counts, dead tuples, VACUUM frequency. In PostgreSQL, `pg_stat_user_tables` provides these metrics. The decision to add a GIN or trigram index should always start from this analysis.
