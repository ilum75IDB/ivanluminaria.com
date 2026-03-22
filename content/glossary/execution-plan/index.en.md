---
title: "Execution Plan"
description: "The sequence of operations chosen by the database optimizer to resolve a SQL query."
translationKey: "glossary_execution_plan"
aka: "Query Plan"
articles:
  - "/posts/postgresql/explain-analyze-postgresql"
  - "/posts/postgresql/pg-stat-statements"
---

An **execution plan** is the sequence of operations the database chooses to resolve a SQL query. When you write a SELECT with JOINs, WHERE filters, and sorts, the optimizer evaluates dozens of possible strategies and picks one based on available statistics.

## How it works

The plan is represented as a tree of nodes: each node is an operation (scan, join, sort, aggregate) that receives data from its child nodes and passes it to its parent. In PostgreSQL you view it with `EXPLAIN` (estimated plan) or `EXPLAIN ANALYZE` (actual plan with real timings and row counts).

The optimizer decides for each node which strategy to use: sequential scan or index scan for table access, nested loop, hash join or merge join for joins, sort or hash for groupings.

## Why it matters

Correctly reading an execution plan is the most important skill for query tuning. Looking at the total time is not enough: you need to compare estimated rows against actual rows node by node, check buffer I/O, and identify where the optimizer made poor choices.

A wrong estimate on even a single node can cascade through the entire plan, turning a millisecond query into one that takes minutes.

## What can go wrong

The most common problems in execution plans:

- **Wrong cardinality estimates**: the optimizer thinks a table returns 100 rows when it actually returns 2 million
- **Wrong join type**: a nested loop chosen where a hash join was needed, due to stale statistics
- **Ignored index**: a sequential scan on a large table because statistics don't reflect the real data distribution
- **Disk spill**: sort or hash operations that don't fit in `work_mem` and end up writing to disk
