---
title: "GIN Index"
description: "Generalized Inverted Index — PostgreSQL index type optimised for full-text search, trigram pattern matching and queries on arrays and JSONB."
translationKey: "glossary_gin-index"
aka: "Generalized Inverted Index"
articles:
  - "/posts/postgresql/like-optimization-postgresql"
---

A **GIN Index** (Generalized Inverted Index) is a PostgreSQL index type designed for indexing composite values: arrays, JSONB documents, text with trigrams and full-text searches. Unlike B-Tree, a GIN creates an inverted mapping: from each element (word, trigram, JSON key) to the records containing it.

## How it works

For each distinct value in the indexed data, GIN maintains a list of pointers to the rows containing that value. In the case of `pg_trgm`, text is decomposed into trigrams (3-character sequences) and each trigram is indexed. A `LIKE '%ABC%'` search is translated into a trigram intersection, avoiding sequential scanning.

## What it's for

GIN solves the "contains" search problem (`LIKE '%value%'`) on text columns, which with a B-Tree would require a sequential scan of the entire table. On tables with millions of rows, the difference is between seconds and milliseconds.

## When to use it

GIN is ideal on append-only tables or those with low churn (few UPDATEs/DELETEs), as the index maintenance cost is higher than B-Tree. Creation in production should use `CREATE INDEX CONCURRENTLY` to avoid write locks.
