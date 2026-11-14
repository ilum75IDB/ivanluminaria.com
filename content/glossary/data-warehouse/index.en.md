---
title: "Data Warehouse (DWH)"
description: "A database system optimized for historical data analysis, aggregating information from heterogeneous operational sources with a focus on bulk reads and aggregations."
translationKey: "glossary_data_warehouse"
aka: "DWH, Enterprise Data Warehouse (EDW)"
articles:
  - "/posts/data-warehouse/la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto"
---

A Data Warehouse is a storage system designed to consolidate data from multiple operational sources — CRM, ERP, billing systems, application logs — into a single repository optimized for analysis. It does not replace transactional databases: it sits alongside them, reading data through ETL or ELT pipelines.

## How it works

The access pattern is the inverse of OLTP: few, large writes (batch or micro-batch) and a very high volume of reads scanning millions of rows. The schema is typically denormalized — star schema or snowflake schema — to minimize JOIN operations and maximize analytical query performance.

```sql
-- Typical analytical query on a telco DWH
SELECT
    d.month,
    r.region,
    SUM(f.revenue_eur)  AS total_revenue,
    COUNT(f.customer_id) AS active_customers
FROM fact_revenue f
JOIN dim_date    d ON f.date_id   = d.date_id
JOIN dim_region  r ON f.region_id = r.region_id
WHERE d.year = 2024
GROUP BY d.month, r.region
ORDER BY d.month, total_revenue DESC;
```

Materialized views are a common tool for pre-computing expensive aggregations and serving them with minimal latency.

## When to use it

A DWH is the right choice when analytical workloads start degrading the performance of operational systems, when historical data needs to be retained beyond what source systems keep, or when multiple heterogeneous sources must be queried in a unified way. It is not suited to scenarios requiring sub-second real-time data: in those cases, lambda or kappa architectures with a streaming layer are more appropriate.

## Notes

The distinction between a DWH and a Data Lake is primarily about structure: a DWH enforces a rigid schema at write time (schema-on-write), while a Data Lake accepts raw data and applies the schema at read time (schema-on-read). Many modern architectures combine both in the pattern known as Data Lakehouse.
