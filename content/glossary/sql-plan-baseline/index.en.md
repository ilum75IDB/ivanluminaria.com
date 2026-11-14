---
title: "SQL Plan Baseline"
description: "Set of accepted execution plans for a specific SQL statement, stored in Oracle's SPM repository to ensure execution plan stability."
translationKey: "glossary_sql_plan_baseline"
aka: "SPM Baseline, Plan Baseline"
articles:
  - "/posts/oracle/oracle-sql-plan-management-stabilizzare-i-piani-di-esecuzione-per-prevenire"
---

A SQL Plan Baseline is a collection of one or more approved execution plans for a specific SQL statement, managed by the Oracle **SQL Plan Management (SPM)** component. When a baseline is active, the optimizer selects only from the plans it contains — even if it identifies seemingly more efficient alternatives during compilation.

## How it works

At parse time, the optimizer compares the generated plan against those stored in the baseline. If the plan is already marked `ACCEPTED = YES`, it is used immediately. If it is new, it is added to the baseline with status `NOT ACCEPTED` and held in quarantine until a DBA — or the automated plan evolution process — verifies and promotes it.

```sql
-- Manually loading a baseline from the Cursor Cache
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

## When to use it

Baselines are the primary tool for **preventing plan regressions** after database upgrades, statistics refreshes, or structural index changes. They are preferable to inline hints because they require no changes to application code and are managed entirely at the DBA level. The main limitation is that each baseline is tied to a specific `SQL_ID`: any variation in the query text — including whitespace or letter case — produces a different `SQL_ID` and requires a separate baseline.
