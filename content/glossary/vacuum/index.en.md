---
title: "VACUUM"
description: "PostgreSQL command that reclaims space occupied by dead tuples, making it reusable for new inserts without returning it to the operating system."
translationKey: "glossary_vacuum"
aka: "PostgreSQL VACUUM"
articles:
  - "/posts/postgresql/vacuum-autovacuum-postgresql"
---

**VACUUM** is the PostgreSQL command that reclaims space occupied by dead tuples and makes it available for new inserts. It does not return space to the operating system, does not reorganize the table, and does not compact anything — it marks pages as rewritable.

## How it works

`VACUUM table` scans the table, identifies dead tuples no longer visible to any transaction, and marks their space as reusable. It is a lightweight operation that does not block writes and can run in parallel with normal queries. `VACUUM FULL` instead physically rewrites the entire table with an exclusive lock — to be used very rarely and only in emergencies.

## What it's for

Without VACUUM, tables with heavy UPDATE and DELETE traffic accumulate dead tuples that occupy disk space and slow down sequential scans. VACUUM is the essential cleanup mechanism that balances the cost of PostgreSQL's MVCC model.

## Why it matters

Autovacuum runs VACUUM automatically, but with PostgreSQL defaults it may trigger too infrequently on high-traffic tables. On a table with 10 million rows, the default waits for 2 million dead tuples before acting — enough to visibly degrade performance.
