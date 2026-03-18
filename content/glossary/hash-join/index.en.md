---
title: "Hash Join"
description: "How hash join works and why it is the best choice for joins on large data volumes."
translationKey: "glossary_hash_join"
tags: ["glossary"]
---

Hash join is a join strategy designed for large data volumes. It works in two phases: first the database reads the smaller table and builds a hash table in memory, indexing rows by the join column. Then it scans the larger table and for each row looks up the match in the hash table with an O(1) lookup.

The advantage is that no indexes are needed and the complexity is linear — proportional to the sum of rows in both tables, not the product as in a nested loop. The downside is that it requires memory for the hash table: if the smaller table does not fit in `work_mem`, the database must write batches to disk (batched hash join), slowing down the operation.

The optimizer chooses hash join when both tables are large and there are no useful indexes, or when statistics indicate that the number of rows to combine is too high for an efficient nested loop. It is one of the most common strategies in data warehouses and reports that aggregate millions of rows.

## Related articles

- [EXPLAIN ANALYZE is not enough: how to really read a PostgreSQL execution plan](/en/posts/postgresql/explain-analyze-postgresql/)
