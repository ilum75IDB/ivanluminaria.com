---
title: "OLAP"
description: "Online Analytical Processing — processing oriented to multidimensional data analysis, typical of data warehouses."
translationKey: "glossary_olap"
aka: "Online Analytical Processing"
articles:
  - "/posts/data-warehouse/ragged-hierarchies"
---

**OLAP** (Online Analytical Processing) refers to a data processing approach oriented to multidimensional analysis: aggregations, drill-down, time comparisons, slice-and-dice on large volumes of historical data.

## OLAP vs OLTP

| Feature | OLAP | OLTP |
|---------|------|------|
| Purpose | Analysis and reporting | Operational transactions |
| Data model | Star schema, denormalized | 3NF, normalized |
| Typical query | Aggregations over millions of rows | Read/write of a few rows |
| Users | Analysts, management | Applications, operators |
| Updates | Batch (periodic ETL) | Real-time |

## OLAP operations

The fundamental OLAP analysis operations are:

- **Drill-down**: from aggregated level to detail
- **Drill-up** (roll-up): from detail to aggregated level
- **Slice**: select a "slice" of data by fixing one dimension (e.g. year 2025 only)
- **Dice**: select a sub-cube by specifying multiple dimensions
- **Pivot**: rotate analysis dimensions (rows ↔ columns)

## Implementations

- **ROLAP** (Relational OLAP): data stays in relational tables, aggregations are computed with SQL queries. This is the approach used in data warehouses with star schemas
- **MOLAP** (Multidimensional OLAP): data is pre-aggregated in multidimensional structures (cubes). Faster for queries but requires more space and build time
- **HOLAP** (Hybrid): combination of both approaches
