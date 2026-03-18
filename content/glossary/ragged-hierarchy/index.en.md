---
title: "Ragged hierarchy"
description: "A hierarchy where not all branches reach the same depth: some intermediate levels are missing."
translationKey: "glossary_ragged_hierarchy"
aka: "Unbalanced hierarchy, Gerarchia sbilanciata"
articles:
  - "/posts/data-warehouse/ragged-hierarchies"
---

A **ragged hierarchy** (also called unbalanced hierarchy) is a hierarchical structure where not all branches reach the same depth. Some intermediate levels are missing for certain entities.

## Concrete example

In a three-level hierarchy Top Group → Group → Client:

- Some clients have all three levels (complete hierarchy)
- Some clients have a Group but no Top Group
- Some clients have neither Group nor Top Group (direct clients)

The result is a structure with "holes" that causes problems in aggregation reports: NULL rows, split totals, incomplete drill-downs.

## Why it's a problem in the DWH

BI tools and SQL queries expect complete hierarchies to work correctly. A GROUP BY on a column with NULLs produces unexpected results: NULL rows are grouped separately, totals don't add up, and the same group can appear on multiple rows.

## How to solve it

The standard technique is **self-parenting**: an entity without a parent becomes its own parent. This balances the hierarchy upstream, in the ETL, eliminating NULLs from the dimension table. Additional flags (`is_direct_client`, `is_standalone_group`) allow distinguishing artificially balanced entities from those with a natural hierarchy.
