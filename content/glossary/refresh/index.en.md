---
title: "Refresh (MV)"
description: "Materialized View Refresh: COMPLETE (full recompute) or FAST (incremental via MV log). A key architectural choice affecting query freshness and system performance."
translationKey: "glossary_refresh"
aka: "Materialized View Refresh"
articles:
  - "/posts/data-warehouse/la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto"
---

A Refresh is the operation that brings a Materialized View back in sync with its underlying base tables. Without it, the MV is a static snapshot: fast to query, but increasingly stale as the source data changes.

## Refresh modes

Two main modes exist:

- **COMPLETE**: recomputes the entire MV from scratch. Simple to reason about, expensive on large datasets.
- **FAST**: applies only the changes tracked in an MV log (a change-tracking structure created on the base table). Requires the log to be present and imposes constraints on the MV query definition.

```sql
-- Complete refresh (Oracle)
EXEC DBMS_MVIEW.REFRESH('MV_REVENUE_DAILY', method => 'C');

-- Fast (incremental) refresh — requires MV log on the base table
EXEC DBMS_MVIEW.REFRESH('MV_REVENUE_DAILY', method => 'F');
```

On PostgreSQL, refresh is always COMPLETE (`REFRESH MATERIALIZED VIEW`), with the `CONCURRENTLY` option available to avoid blocking concurrent reads during the operation.

## Choosing the right mode

FAST refresh reduces update time but adds operational complexity: the MV log consumes storage, must be maintained, and not all query shapes are compatible — complex aggregations, `DISTINCT`, and correlated subqueries often rule it out. COMPLETE is universally applicable but does not scale well on tables with millions of rows.

Frequency matters just as much as mode: on-demand refresh, hourly scheduling, or automatic refresh ON COMMIT each carry very different implications for base table transaction throughput and data latency.
