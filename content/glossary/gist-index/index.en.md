---
title: "GiST Index"
description: "Generalized Search Tree — PostgreSQL index family for data with geometric, range or similarity structure, indispensable for spatial and range queries."
translationKey: "glossary_gist_index"
aka: "Generalized Search Tree"
articles:
  - "/posts/postgresql/postgresql-indici-quando-fanno-male"
---

**GiST** (*Generalized Search Tree*) is a family of PostgreSQL indexes designed for data that cannot be ordered linearly: geometries, ranges, similarity vectors, full-text. It's a balanced tree that organises data by hierarchical *bounding boxes* instead of lexicographic ordering.

## How it works

While a B-tree orders values from "minimum" to "maximum" and performs dichotomous search, GiST groups data into nested regions (bounding boxes). Each tree node represents a region containing all data in its children. When searching for a value, GiST discards entire regions with an overlap comparison — without descending into nodes that can't contain the result.

This structure can index:

- **Geometries**: points, polygons, lines (with PostGIS)
- **Ranges**: `int4range`, `tsrange`, `daterange` and other range types
- **Full-text**: `tsvector` vectors for text search
- **Similarity**: with extensions like `pg_trgm` for approximate searches

## What it's for

It solves "spatial" or range queries that a B-tree cannot handle:

- Find all points inside a box or radius
- Find all records whose range overlaps with another range
- Find texts similar to a query, even with typos
- Search by containment: `range1 @> range2` or `geom1 && geom2`

## When to use it

Use it with `CREATE INDEX ... USING GIST (column)`. It's the natural complement of GIN: GIN for array/JSONB containment, GiST for geometry/range/similarity. On high-churn tables it has write costs similar to GIN — so it should be evaluated case by case.
