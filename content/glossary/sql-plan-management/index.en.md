---
title: "SQL Plan Management (SPM)"
description: "Oracle feature that stabilizes execution plans through approved baselines, preventing optimizer-driven performance regressions."
translationKey: "glossary_sql_plan_management"
aka: "SPM, SQL Plan Baseline"
articles:
  - "/posts/oracle/oracle-sql-plan-management-stabilizzare-i-piani-di-esecuzione-per-prevenire"
---

SQL Plan Management (SPM) is an Oracle Database feature that gives DBAs explicit control over which execution plans the optimizer is allowed to use for a given SQL statement. The core mechanism is the **SQL Plan Baseline**: a repository of verified, accepted plans that the optimizer must consult before adopting any newly generated plan.

## How it works

When SPM is enabled, the optimizer can still generate alternative plans, but marks them as unaccepted. A new plan enters production only after explicit acceptance — either manual or through automatic plan evolution — and only if it can be proven to perform at least as well as the existing baseline plan.

```sql
-- Load a plan from the Cursor Cache into the baseline
DECLARE
  l_plans PLS_INTEGER;
BEGIN
  l_plans := DBMS_SPM.LOAD_PLANS_FROM_CURSOR_CACHE(
    sql_id => 'abc123xyz',
    plan_hash_value => 987654321
  );
END;
/
```

Each baseline entry is identified by a `SQL_HANDLE` + `PLAN_NAME` pair and is stored in the `SYSAUX` tablespace, persisting independently of statistics changes or system parameter modifications.

## When to use it

SPM is the go-to tool when:

- a statistics refresh, an optimizer patch, or an Oracle upgrade introduces plan regressions on critical queries;
- a specific query's behavior must be frozen in environments with strict SLAs;
- migrating between Oracle versions and plan stability must be guaranteed during the transition window.

The main operational overhead is baseline lifecycle management: accumulated baselines need periodic review, otherwise legitimate optimizer improvements get blocked indefinitely.
