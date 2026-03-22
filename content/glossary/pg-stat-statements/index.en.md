---
title: "pg_stat_statements"
description: "PostgreSQL extension that collects execution statistics for all SQL queries, an essential tool for performance diagnostics."
translationKey: "glossary_pg-stat-statements"
aka: "pgss"
articles:
  - "/posts/postgresql/pg-stat-statements"
---

**pg_stat_statements** is a PostgreSQL extension — included in the official distribution but not active by default — that tracks execution statistics for all SQL queries that pass through the server. Queries are normalized (literal values replaced with parameters) to group executions of the same pattern.

## How it works

The extension requires loading as a shared library at server startup via the `shared_preload_libraries` parameter. Once active, it records for each query: execution count, total and average time, rows returned, blocks read from disk and from cache. The `pg_stat_statements.max` parameter controls how many distinct queries are tracked (default 5000).

## What it's for

It's the primary tool for identifying the most expensive queries on a PostgreSQL server. Sorting by `total_exec_time` immediately gives the ranking of queries consuming the most resources. Combined with EXPLAIN ANALYZE, it enables a complete diagnostic workflow: pg_stat_statements identifies the problem, EXPLAIN explains the cause.

## When to use it

It should be active on any production PostgreSQL installation. The overhead is negligible (1-2% CPU). Without pg_stat_statements, any performance tuning activity is based on guesswork rather than data.
