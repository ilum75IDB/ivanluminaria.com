---
title: "Partial Index"
description: "PostgreSQL index that covers only a subset of the table's rows, defined with WHERE in the CREATE INDEX. Reduces space and maintenance time."
translationKey: "glossary_indice_parziale"
aka: "Indice Parziale"
articles:
  - "/posts/postgresql/postgresql-indici-quando-fanno-male"
---

A **partial index** is a PostgreSQL index that covers only a subset of the table's rows, defined with a `WHERE` clause in the `CREATE INDEX`. Rows that don't satisfy the condition are not indexed and take no space in the index.

## How it works

The syntax is simple:

```sql
CREATE INDEX idx_active
ON orders (created_at)
WHERE status = 'active';
```

The index contains only the rows with `status = 'active'`. All others are ignored. The planner uses this index only for queries that include the same `WHERE status = 'active'` condition (or a more restrictive one).

## What it's for

It solves a very common scenario: most operational queries always filter by a condition (e.g. `active = true`, `archived = false`, `date > x`), and the rows that don't satisfy that condition are never searched. Indexing them is a waste.

Concrete benefits:

- **Space**: the index is smaller, sometimes a lot. On a table where 35% of rows are "active", the partial index takes 35% of the space.
- **Maintenance**: less work for VACUUM, less write-amplification on INSERT/UPDATE of excluded rows.
- **Performance**: the index is smaller to walk and tends to fit in cache more easily.

## When to use it

Use it when:

- Operational queries systematically filter on a binary condition
- The rows that don't satisfy the condition are many (>50%) and not relevant for the hot workload
- Queries on the other subset are rare and acceptable with a seq scan

Don't use it if queries filter on dynamic or variable conditions: the planner will never use the partial index.
