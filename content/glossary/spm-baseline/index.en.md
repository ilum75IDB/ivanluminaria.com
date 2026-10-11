---
title: "SPM Baseline"
description: "Oracle SQL Plan Management baseline: freezes an approved execution plan for a query, preventing the Cost-Based Optimizer from switching to a less efficient one."
translationKey: "glossary_spm_baseline"
aka: "SQL Plan Management Baseline"
articles:
  - "/posts/oracle/oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback"
---

An SPM Baseline is an Oracle SQL Plan Management construct that pins a specific execution plan to a query. Once a plan is marked as an accepted baseline, the Cost-Based Optimizer (CBO) will use it exclusively — even if it finds an alternative plan with a lower estimated cost — until that alternative is explicitly accepted.

## How it works

Each plan is identified by a `SQL_HANDLE` (tied to the query text) and a `PLAN_NAME` (tied to the specific plan). Oracle maintains a SQL Plan History: new plans enter the history automatically but do not become baselines until explicitly accepted. Only `ACCEPTED` plans are eligible at runtime.

```sql
-- Load a baseline from the cursor cache for a specific query
DECLARE
  l_plans PLS_INTEGER;
BEGIN
  l_plans := DBMS_SPM.LOAD_PLANS_FROM_CURSOR_CACHE(
    sql_id => 'abc123xyz',
    plan_hash_value => 987654321
  );
END;
/

-- Check active baselines
SELECT sql_handle, plan_name, accepted, enabled, fixed
FROM   dba_sql_plan_baselines
WHERE  sql_text LIKE '%table_name%';
```

Setting `FIXED = YES` adds a harder lock: the CBO cannot consider any alternative plan regardless of new statistics or hints.

## When to use it

The most common scenario is a database upgrade (e.g., 11g R2 to 19c): plans validated in staging are captured and loaded as baselines before production go-live, so the new optimizer version cannot introduce regressions. It is also useful after a bulk statistics refresh or a structural change (new index, partitioning) that could destabilize critical queries.

The main drawback is maintenance overhead: baselines must be reviewed periodically. A plan frozen against a table that grows by an order of magnitude can become suboptimal over time.
