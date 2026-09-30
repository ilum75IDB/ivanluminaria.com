---
title: "Execution plan"
description: "Sequence of operations chosen by the SQL optimizer to run a query: scans, joins, sorts. Stale statistics silently degrade it, regardless of hardware."
translationKey: "glossary_piano_di_esecuzione"
aka: "Query execution plan, Query plan"
articles:
  - "/posts/project-management/il-preventivo-dell-upgrade-e-la-domanda-che-non-e-istintiva"
---

An execution plan is the step-by-step recipe the database engine follows to answer a SQL query. The optimizer evaluates multiple candidate strategies — which indexes to use, in what order to join tables, whether to sort before or after a join — and picks the one with the lowest estimated cost. The result is a tree of operators executed in sequence.

## How it works

The optimizer relies on **statistics** (value distribution, table cardinality, index selectivity) to estimate the cost of each candidate plan. On PostgreSQL the starting point is `EXPLAIN` or `EXPLAIN ANALYZE`:

```sql
EXPLAIN ANALYZE
SELECT o.id, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'pending';
```

The output shows each node (Seq Scan, Index Scan, Hash Join, Sort…), the estimated cost, and — with `ANALYZE` — the actual runtime and rows processed. The gap between estimated and actual rows is the first signal of stale statistics.

## When it becomes a problem

A degraded plan typically appears after:

- **bulk loads** that shift data distribution without a subsequent `ANALYZE`;
- **version upgrades**, where the optimizer changes its heuristics;
- **organic table growth** beyond the thresholds the plan was calibrated for.

The classic symptom is a query that ran in milliseconds and suddenly takes tens of seconds, with no change to application code. Adding hardware does not fix it: a Full Table Scan over 500 million rows is expensive regardless of available RAM. The remedy is refreshing statistics (`ANALYZE`, `UPDATE STATISTICS`, `DBMS_STATS`) and confirming the optimizer picks the expected plan.
