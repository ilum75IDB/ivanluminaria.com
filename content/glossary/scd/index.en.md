---
title: "SCD"
description: "Slowly Changing Dimension — a data warehouse technique for tracking changes over time in dimension tables."
translationKey: "glossary_scd"
aka: "Slowly Changing Dimension"
articles:
  - "/posts/data-warehouse/scd-tipo-2"
---

**SCD** (Slowly Changing Dimension) refers to a set of techniques used in data warehousing to manage changes in dimension table data over time.

## Main types

- **Type 1**: overwrite the previous value. No history preserved
- **Type 2**: insert a new row with validity dates (start date, end date). Preserves full history
- **Type 3**: add a column for the previous value. Preserves only the last change

## Why it matters

In a transactional database, when a customer changes address you update the record. In a data warehouse this would mean losing history: all previous sales would appear associated with the new address.

SCD Type 2 solves this problem by maintaining one row for each version of the data, with validity dates that allow reconstructing the situation at any point in time.

## When to use it

The choice of type depends on the business requirement. If only the current value matters, Type 1 is sufficient. If the business needs accurate historical analysis — and in most real-world data warehouses it does — Type 2 is the standard choice.
