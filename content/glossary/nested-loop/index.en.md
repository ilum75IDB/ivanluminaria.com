---
title: "Nested Loop (Join)"
description: "How nested loop join works and when the optimizer chooses it — or mistakenly chooses it."
translationKey: "glossary_nested_loop"
tags: ["glossary"]
---

The nested loop is the simplest join strategy: for each row in the outer table, the database looks for matching rows in the inner table. It works like a double nested for loop — hence the name.

It is the ideal choice when the outer table has few rows and the inner table has an index on the join column. In this scenario, the nested loop is unbeatable: few iterations, direct index access, minimal memory. A join on 100 outer rows with a B-tree index on the inner table is practically instantaneous.

It becomes a disaster when the optimizer picks it on large datasets by mistake — typically because statistics underestimate the row count. A nested loop on 2 million outer rows means 2 million lookups in the inner table, and without an index each lookup is a full scan. In these cases, a hash join or merge join would be orders of magnitude faster.

## Related articles

- [EXPLAIN ANALYZE is not enough: how to really read a PostgreSQL execution plan](/en/posts/postgresql/explain-analyze-postgresql/)
