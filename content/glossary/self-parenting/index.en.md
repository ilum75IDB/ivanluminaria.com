---
title: "Self-parenting"
description: "A technique for balancing ragged hierarchies: an entity without a parent becomes its own parent."
translationKey: "glossary_self_parenting"
aka: "Hierarchical self-reference"
articles:
  - "/posts/data-warehouse/ragged-hierarchies"
---

**Self-parenting** is a dimensional modeling technique used to balance ragged hierarchies. The principle is simple: an entity that doesn't have an upper hierarchical level becomes its own parent at that level.

## How it works

In a three-level hierarchy Top Group → Group → Client:

- A Client without a Group uses its own name/ID as its Group
- A Group without a Top Group uses its own name/ID as its Top Group

The result is a dimension table with no NULLs in the hierarchical columns, with all levels always populated.

## Distinction flags

To preserve information about which entities were artificially balanced, flags are added to the dimension:

- `is_direct_client = 'Y'`: the client didn't have a Group in the source
- `is_standalone_group = 'Y'`: the Group didn't have a Top Group in the source

These flags allow the business to filter "real" top groups from promoted clients.

## Why in the ETL, not in the report

Self-parenting is applied once in the ETL, not in every single report. A report should do GROUP BY and JOIN, not decide how to handle missing levels. If the balancing logic is in the model, all reports benefit automatically.
