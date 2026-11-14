---
title: "Materialized View (MV)"
description: "A pre-computed view stored physically on disk: queries read already-aggregated data without recalculating. Supported by Oracle, PostgreSQL, SQL Server."
translationKey: "glossary_materialized_view"
aka: "Materialized View"
articles:
  - "/posts/data-warehouse/la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto"
---

A Materialized View (MV) is a view whose result is computed once and stored physically on disk, unlike a regular view that re-executes its query on every access. Subsequent reads find data already available: no JOINs, no aggregations to recompute at runtime.

## How it works

The MV is created with a defining query; the engine executes that query and persists its result as if it were a table. Updates happen through a **refresh**: full (`COMPLETE`) or incremental (`FAST`/`INCREMENTAL`), depending on the RDBMS and the query structure.

```sql
-- PostgreSQL
CREATE MATERIALIZED VIEW mv_revenue_daily AS
SELECT
    date_trunc('day', event_ts) AS day,
    customer_id,
    SUM(amount)                 AS total_revenue
FROM fact_events
GROUP BY 1, 2;

-- Manual refresh
REFRESH MATERIALIZED VIEW mv_revenue_daily;
```

In Oracle, the refresh can be scheduled and supports `FAST` mode via materialized view logs. In SQL Server, the equivalent construct is an **Indexed View**.

## When to use it

MVs are the right tool when:

- the underlying query is expensive (aggregations over billions of rows, multi-table JOINs) and data changes infrequently or on a predictable schedule;
- you want to separate OLTP load from analytical load without duplicating the entire pipeline;
- a Data Warehouse or Data Mart requires pre-aggregated layers for dashboards and reports.

The main trade-off is **data latency**: between one refresh and the next, the MV can be stale. In contexts where freshness is critical (near-real-time), evaluate whether frequent refreshes negate the performance benefit.
