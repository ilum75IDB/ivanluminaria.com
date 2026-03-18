---
title: "B-Tree"
description: "Balanced tree data structure, the default index type in most relational databases. Efficient for equality and range searches, but unsuitable for LIKE with leading wildcard."
translationKey: "glossary_b-tree"
articles:
  - "/posts/postgresql/like-optimization-postgresql"
---

**B-Tree** (Balanced Tree) is the most common data structure for indexes in relational databases and is the default index type in PostgreSQL, MySQL and Oracle. It maintains data sorted in a balanced tree structure that guarantees logarithmic search times.

## How it works

A B-Tree organises keys in sorted nodes, with each node containing pointers to child nodes. Search starts from the root and descends to the leaves, halving the search space at each level. For a table with 6 million rows, a B-Tree typically requires 3-4 levels of depth, meaning 3-4 page reads to find a value.

## What it's for

B-Trees are optimal for equality searches (`WHERE col = 'value'`), ranges (`WHERE col BETWEEN x AND y`), sorting and prefix searches (`LIKE 'ABC%'`). They cannot however be used for searches with a leading wildcard (`LIKE '%ABC%'`), because the B-Tree ordering doesn't help find substrings at arbitrary positions.

## When to use it

B-Tree is the right choice for most indexes. When a "contains" search on text is needed, you must switch to a GIN index with the pg_trgm extension. The choice between B-Tree and GIN depends on the query type and the table's workload profile.
