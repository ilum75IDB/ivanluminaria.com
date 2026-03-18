---
title: "Local Index"
description: "Oracle index partitioned with the same key as the table, where each table partition has its corresponding index partition. More maintainable than a global index."
translationKey: "glossary_local-index"
articles:
  - "/posts/oracle/oracle-partitioning"
---

A **Local Index** is an Oracle index created on a partitioned table, which is automatically partitioned with the same key and boundaries as the table. Each table partition has a corresponding index partition.

## How it works

When an index is created with the `LOCAL` clause, Oracle creates one index partition for each table partition. If the table has 100 monthly partitions, the index will have 100 corresponding partitions. DDL operations on a partition (DROP, TRUNCATE, SPLIT) invalidate only the corresponding index partition, not the entire index.

## What it's for

Local Index is the preferred choice for indexes on partitioned tables because it maintains partition independence. A `DROP PARTITION` takes less than a second and doesn't invalidate any other index. With a global index, the same operation would invalidate the entire index, requiring hours of rebuild.

## When to use it

Use when the index includes the partition key or when queries always filter on the partition column. For point lookups on non-partition columns (e.g. primary key), a global index is needed instead. The rule: local where possible, global only where necessary.
