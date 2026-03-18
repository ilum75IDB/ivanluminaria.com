---
title: "Execution Plan"
description: "What an execution plan is and how the database optimizer decides the strategy for running a query."
translationKey: "glossary_execution_plan"
tags: ["glossary"]
---

An execution plan is the sequence of operations the database chooses to resolve a SQL query. When you write a SELECT with JOINs, WHERE filters, and sorts, the optimizer evaluates dozens of possible strategies — which index to use, which join type, what order to read the tables — and picks one based on available statistics.

In PostgreSQL you can view it with `EXPLAIN` (estimated plan only) or `EXPLAIN ANALYZE` (actual plan with real timings). The plan is represented as a tree of nodes: each node is an operation (scan, join, sort, aggregate) that receives data from its child nodes and passes it to its parent node.

Correctly reading an execution plan is the most important skill for query tuning. Looking at the total time is not enough: you need to compare estimated rows against actual rows node by node, check buffer I/O, and identify where the optimizer made poor choices.

## Related articles

- [EXPLAIN ANALYZE is not enough: how to really read a PostgreSQL execution plan](/en/posts/postgresql/explain-analyze-postgresql/)
