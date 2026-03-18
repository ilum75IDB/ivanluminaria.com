---
title: "pg_trgm"
description: "PostgreSQL extension providing functions and operators for trigram-based similarity search, enabling GIN indexes for LIKE with wildcards."
translationKey: "glossary_pg-trgm"
articles:
  - "/posts/postgresql/like-optimization-postgresql"
---

**pg_trgm** is a PostgreSQL extension that implements trigram-based searching — sequences of three consecutive characters extracted from text. It enables the use of GIN and GiST indexes to accelerate `LIKE '%value%'` and `ILIKE` searches, which would otherwise require sequential scans.

## How it works

The extension decomposes each string into trigrams: for example, "hello" becomes {"  h", " he", "hel", "ell", "llo", "lo "}. A GIN index with operator class `gin_trgm_ops` indexes these trigrams. When executing a `LIKE '%ell%'`, PostgreSQL searches for matching trigrams in the index instead of scanning the entire table.

## What it's for

pg_trgm solves one of the most common problems in PostgreSQL: "contains" searches on large text columns. Without pg_trgm, a `LIKE '%value%'` on a table with millions of rows requires a full scan. With pg_trgm and a GIN index, the same search uses the index and responds in milliseconds.

## When to use it

Activate with `CREATE EXTENSION IF NOT EXISTS pg_trgm` and create the index with `USING gin (column gin_trgm_ops)`. It is ideal on tables with low churn (few UPDATEs/DELETEs). Index creation should use `CONCURRENTLY` in production to avoid locks.
