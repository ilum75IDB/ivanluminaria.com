---
title: "Query Rewriting"
description: "Oracle feature that transparently redirects queries on base tables to an equivalent Materialized View, with no changes required in application code."
translationKey: "glossary_query_rewriting"
aka: "Automatic Query Rewriting"
articles:
  - "/posts/data-warehouse/la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto"
---

Query Rewriting is a capability built into Oracle's query optimizer that intercepts SQL queries targeting base tables and transparently reroutes them to a Materialized View (MV) holding pre-computed results. The application layer is completely unaware of the substitution: it sends the same query as always and gets results back faster.

## How it works

When a MV is created or altered with `ENABLE QUERY REWRITE`, the optimizer is authorized to treat it as an alternative data source. Oracle checks that the MV is semantically equivalent to the incoming query — same aggregations, same columns, same filter logic — and, if the match holds, swaps the execution plan accordingly.

```sql
CREATE MATERIALIZED VIEW mv_daily_traffic
BUILD IMMEDIATE
REFRESH COMPLETE ON DEMAND
ENABLE QUERY REWRITE
AS
SELECT call_date, cell_id, SUM(duration_sec) AS total_duration
FROM fact_calls
GROUP BY call_date, cell_id;
```

After this definition, a query like `SELECT call_date, SUM(duration_sec) FROM fact_calls GROUP BY call_date` may be resolved by reading the MV instead of the base table, whenever the optimizer considers it advantageous.

## When to use it

Query Rewriting is most effective in Data Warehouses with heavy, repetitive analytical queries over the same aggregations. The critical prerequisite is MV **freshness**: if the MV data is stale relative to the base table, Oracle may choose not to use it — behavior controlled via the `QUERY_REWRITE_INTEGRITY` parameter. The session or system parameter `QUERY_REWRITE_ENABLED` must also be set. In environments with frequent or near-real-time refreshes, the benefit shrinks and the cost of refresh must be weighed against the read-time gain.
