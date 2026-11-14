---
title: "Fixed Plan"
description: "Oracle execution plan marked FIXED=YES in a SQL Plan Baseline: the optimizer always selects it, regardless of any alternative plans found."
translationKey: "glossary_piano_fixed"
aka: "Fixed Plan (SQL Plan Baseline)"
articles:
  - "/posts/oracle/oracle-sql-plan-management-stabilizzare-i-piani-di-esecuzione-per-prevenire"
---

A **fixed plan** is an execution plan stored in a SQL Plan Baseline and marked with the attribute `FIXED = YES`. Unlike plans that are merely accepted (`ACCEPTED = YES`), a fixed plan has absolute priority: the Oracle optimizer always selects it for that SQL statement, even if it finds alternative plans with a lower estimated cost during compilation.

## How it works

When the optimizer processes a query, it checks whether a SQL Plan Baseline exists for that SQL signature. If the baseline contains at least one plan with `FIXED = YES`, the optimizer ignores every other plan — accepted or not — and uses only the fixed one.

A plan is marked as fixed via `DBMS_SPM`:

```sql
DECLARE
  v_result PLS_INTEGER;
BEGIN
  v_result := DBMS_SPM.ALTER_SQL_PLAN_BASELINE(
    sql_handle      => 'SQL_abc123def456',
    plan_name       => 'SQL_PLAN_abc123def456_1',
    attribute_name  => 'fixed',
    attribute_value => 'YES'
  );
END;
/
```

## When to use it

A fixed plan is the right tool when plan stability matters more than the optimizer's automatic tuning:

- **Post-upgrade regressions**: after an Oracle upgrade or a statistics refresh, pinning a known-good plan prevents the optimizer from choosing worse paths.
- **Critical production queries**: for statements with tight SLAs, any variability in the execution plan is unacceptable.
- **Environments with unstable statistics**: highly volatile tables can produce different plans after each statistics gather; a fixed plan eliminates that variability.

The main drawback is rigidity: if data characteristics change significantly (new indexes, partitioning, very different volumes), a fixed plan can become suboptimal with no way for the optimizer to self-correct. It should be monitored and reviewed on a regular basis.
