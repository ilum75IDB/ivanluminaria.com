---
title: "Hash Join"
description: "Hash Join — a join strategy optimized for large data volumes, based on a hash table built in memory."
translationKey: "glossary_hash_join"
aka: "Hash Join"
articles:
  - "/posts/postgresql/explain-analyze-postgresql"
---

**Hash join** is a join strategy designed for large data volumes. It works in two phases: first it builds a data structure in memory, then uses it to find matches efficiently.

## How it works

The database reads the smaller table (build side) and builds a hash table in memory, indexing rows by the join column. Then it scans the larger table (probe side) and for each row looks up the match in the hash table with an O(1) lookup.

The complexity is linear — proportional to the sum of rows in both tables, not the product as in a nested loop. No indexes are needed: the hash table temporarily replaces the index.

## When it's the right choice

The optimizer chooses hash join when both tables are large and there are no useful indexes, or when statistics indicate that the number of rows to combine is too high for an efficient nested loop. It's one of the most common strategies in data warehouses and reports that aggregate millions of rows.

## What can go wrong

The weak point is memory. The hash table must fit in `work_mem`: if the smaller table doesn't fit, the database writes batches to disk (batched hash join), with a significant performance degradation.

- **work_mem too low**: the hash table is split into batches on disk, multiplying I/O
- **Wrong estimates**: the optimizer picks the wrong table as build side because statistics report fewer rows than reality
- **Data skew**: if one value in the join column dominates most rows, one hash bucket becomes huge while the rest stay empty
