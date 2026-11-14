---
categories:
- oracle
date: '2026-12-01'
description: 'How Oracle SPM turned a 45-minute financial report into a 3-minute run:
  diagnosing a suboptimal plan, loading a baseline, and preventing future regressions.'
draft: false
image: oracle-sql-plan-management-stabilizzare-i-piani-di-esecuzione-per-prevenire.cover.jpg
seoTitle: 'Oracle SQL Plan Management: stabilizing execution plans'
tags:
- oracle
- sql-plan-management
- performance-tuning
- optimizer
- oracle-19c
title: Pietro's morning and the report that 'has always been like this'
translationKey: oracle_sql_plan_management_stabilizzare_i_piani_di_esecuzione_per_prevenire
webo_generated_at: 2026-11-14
webo_status: scheduled
---

## Pietro's morning and the report that "has always been like this"

It was one of those rare mornings when the phone wasn't ringing. No alerts, no escalations, no panicked customer DBA on the line. Pietro, a junior who has been working with me for a few months on a project at a large Italian insurance group, had walked over to my desk with that slightly cautious curiosity juniors have when they sense the senior has a free moment.

"Can I ask you something about a query that's been bugging me?"

The query in question was the annual revenue report — one of those reports the management board runs every week to monitor income. It had been running for years. Forty-five minutes every time. The dev team knew. The PM knew. Management knew. It had become part of the landscape, like the hum of the air conditioning in the server room: present, accepted, ignored.

Pietro had found the query in the repository and noticed it didn't look particularly complex. Four tables, a few joins, an aggregate. Why did it take 45 minutes?

I answered the way I always do in these situations: "Let's pull the execution plan and see what the optimizer is doing."

I had no idea that teaching session was about to turn into an operational diagnosis.

## What the optimizer was doing under the hood

The query looked like this, simplified for readability:

```sql
SELECT
    c.customer_name,
    SUM(il.amount) AS total_revenue
FROM
    FINANCE.CUSTOMERS c
JOIN
    SALES.INVOICES i ON c.customer_id = i.customer_id
JOIN
    SALES.INVOICE_LINES il ON i.invoice_id = il.invoice_id
WHERE
    i.invoice_date BETWEEN TO_DATE('2025-01-01', 'YYYY-MM-DD')
                       AND TO_DATE('2025-12-31', 'YYYY-MM-DD')
GROUP BY
    c.customer_name
ORDER BY
    total_revenue DESC;
```

The tables involved were not small: `SALES.INVOICES` had around 150 million rows, `SALES.INVOICE_LINES` around 750 million, `FINANCE.CUSTOMERS` 5 million. The filter on `invoice_date` should have drastically reduced the dataset before the joins — but only if the optimizer had chosen the right path.

I pulled the current plan from the cursor cache:

```sql
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR(sql_id => '<sql_id>', format => 'ALLSTATS LAST'));
```

The plan showed a Hash Join on `SALES.INVOICES` and `SALES.INVOICE_LINES` with a Full Table Scan on both tables — before even applying the date filter. The optimizer was reading 750 million rows and then discarding most of them.

"Why is it doing that?" Pietro asked.

It's a fair question. The optimizer isn't stupid: it chose that plan because the statistics it had available led it to believe that was the most efficient path. The problem was that the statistics had changed — or more precisely, they had been updated in a non-representative way after a bulk collection run during a maintenance window, probably with partial data. The result: the optimizer was overestimating the selectivity of the `invoice_date` filter and underestimating the cost of a Full Table Scan on the large tables.

I cross-referenced with AWR snapshots [1] from the previous weeks:

```sql
SELECT
    snap_id,
    plan_hash_value,
    elapsed_time_total / executions_total AS avg_elapsed_us
FROM
    DBA_HIST_SQLSTAT
WHERE
    sql_id = '<sql_id>'
ORDER BY
    snap_id DESC;
```

The plan had changed about three weeks earlier. Before that point, the same query was running in under 4 minutes with a different plan — Nested Loops with an Index Range Scan on `SALES.INVOICES` (index on `invoice_date`) and a subsequent Index Scan on `SALES.INVOICE_LINES`. A far more efficient plan for this access pattern.

Pietro looked at the numbers in silence for a few seconds. "So the query isn't slow. It's the plan that's wrong."

Exactly.

## SQL Plan Management: the baseline as an anchor of stability

At this point I introduced SQL Plan Management [1], which is precisely the tool designed for situations like this.

The core idea is straightforward: Oracle maintains a repository of approved execution plans for each SQL statement, called a **SQL Plan Baseline**. When the optimizer generates a new plan for a query, it compares it against the baseline. If the new plan isn't in the baseline, it gets marked as "unaccepted" and isn't used automatically — even if the optimizer considers it better. Only plans explicitly accepted into the baseline are used in production.

This mechanism creates a clean separation between "the optimizer finds a new plan" and "the new plan goes to production." That separation is valuable: it gives you time to evaluate, test, and decide deliberately.

SPM operates on three core concepts:

- **SQL Plan Baseline**: the set of accepted plans for a specific SQL statement, identified by its `sql_id` or normalized text.
- **Accepted plan**: a plan in the baseline that the optimizer is allowed to use.
- **Candidate plan** (*unaccepted*): a plan the optimizer has found but that hasn't yet been verified and accepted.

The system parameter `OPTIMIZER_USE_SQL_PLAN_BASELINES` (default `TRUE`) controls whether the optimizer consults baselines. The parameter `OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES` [3] (default `FALSE`) controls whether Oracle automatically captures plans for repeated queries.

## Loading the good plan from the cursor cache

The optimal plan — the one with Nested Loops and Index Scan — was still in the cursor cache, associated with a `plan_hash_value` different from the current one. The goal was to load it into the baseline as an accepted plan.

The most direct method is `DBMS_SPM.LOAD_PLANS_FROM_CURSOR_CACHE` [2]:

```sql
DECLARE
    v_plans_loaded PLS_INTEGER;
BEGIN
    v_plans_loaded := DBMS_SPM.LOAD_PLANS_FROM_CURSOR_CACHE(
        sql_id          => '<sql_id>',
        plan_hash_value => <good_plan_hash_value>
    );
    DBMS_OUTPUT.PUT_LINE('Plans loaded: ' || v_plans_loaded);
END;
/
```

The function returns the number of plans loaded. The plan is inserted into the baseline with status `ACCEPTED = YES` — ready to be used by the optimizer.

To verify what's in the baseline:

```sql
SELECT
    sql_handle,
    plan_name,
    accepted,
    enabled,
    fixed,
    created,
    last_modified
FROM
    DBA_SQL_PLAN_BASELINES
WHERE
    sql_text LIKE '%FINANCE.CUSTOMERS%'
ORDER BY
    created DESC;
```

At this point we had two plans in the baseline: the good one (just loaded, `ACCEPTED = YES`) and the suboptimal one the optimizer had been using. The suboptimal plan wasn't in the baseline yet — it was simply the plan the optimizer was choosing freely in the absence of any constraints.

The next step was making sure the optimizer would use the good plan and not drift back to the bad one in the future.

## The evolution process: how SPM evaluates new plans

Before disabling the suboptimal plan, it's worth understanding how the evolution mechanism [1] works — because this is where SPM shows its real long-term value.

When the optimizer finds a plan not present in the baseline, it adds it as a candidate plan (*unaccepted*). That plan isn't used, but it's retained for later evaluation. The procedure `DBMS_SPM.EVOLVE_SQL_PLAN_BASELINE` [2] performs this evaluation: it runs the candidate plan in a controlled way and compares it against the current accepted plan. If the candidate is significantly more efficient (by default, at least 1.5% faster), it gets promoted to *accepted*.

```sql
SET SERVEROUTPUT ON
DECLARE
    v_report CLOB;
BEGIN
    v_report := DBMS_SPM.EVOLVE_SQL_PLAN_BASELINE(
        sql_handle  => '<sql_handle>',
        time_limit  => 60,   -- maximum seconds for the test
        verify      => 'YES',
        commit      => 'YES'
    );
    DBMS_OUTPUT.PUT_LINE(v_report);
END;
/
```

The parameter `verify => 'YES'` causes Oracle to actually execute the candidate plan to measure its performance. With `commit => 'YES'`, if the plan clears the threshold, it's automatically accepted.

In this specific case we didn't need automatic evolution — the good plan had already been loaded as accepted. But understanding the mechanism matters for cases where you're working with automatic capture (`OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES = TRUE`), where candidate plans accumulate and need to be periodically evaluated.

## Locking in the optimal plan and blocking future regressions

With the good plan in the baseline, we took one more step: marking it as `FIXED`. A fixed plan has absolute precedence — the optimizer always uses it, regardless of any other plan in the baseline or any new plans it might find.

```sql
DECLARE
    v_plans_modified PLS_INTEGER;
BEGIN
    v_plans_modified := DBMS_SPM.ALTER_SQL_PLAN_BASELINE(
        sql_handle  => '<sql_handle>',
        plan_name   => '<good_plan_name>',
        attribute_name  => 'fixed',
        attribute_value => 'YES'
    );
    DBMS_OUTPUT.PUT_LINE('Plans modified: ' || v_plans_modified);
END;
/
```

After this, we ran the query in the test environment. The plan the optimizer chose was the Nested Loops with Index Range Scan on `invoice_date`. Execution time: just under 3 minutes, down from 45.

The difference in the plan was stark: instead of reading the entire `SALES.INVOICE_LINES` table (750 million rows) with a Full Table Scan, the optimizer now accessed `SALES.INVOICES` first via the index on `invoice_date` — reducing the dataset to a few hundred thousand rows for the selected year — and then joined to `SALES.INVOICE_LINES` via an Index Scan on `invoice_id`. The filter was applied before the join, not after.

We left the suboptimal plan in the baseline with `ENABLED = NO` rather than deleting it, to preserve the history and have the option to re-enable it if needed. A conservative choice, but a sensible one in production.

## When to use SPM: scenarios and trade-offs

Pietro asked the right question at this point: "If it works this well, why don't we use it on every query?"

The honest answer is that SPM carries a management overhead that isn't trivial.

**Scenarios where SPM is particularly useful**:

- **Before and after an Oracle Database upgrade**: an upgrade can change optimizer behavior in significant ways. Loading baselines before the upgrade and verifying them afterward is an established practice.
- **After applying patches**: optimizer patches (included in PSUs/RUs) can alter plans. SPM lets you freeze critical plans before patching.
- **After a bulk statistics collection**: as in our case. A non-representative statistics collection can degrade dozens of queries simultaneously.
- **Critical queries with tight SLAs**: financial reports, nightly batch jobs, month-end closing queries — any query where a regression has a direct business impact.

**Trade-offs to consider**:

- Baselines need maintenance. If the table structure changes (new indexes, partitions, columns), the plans in the baseline may become suboptimal relative to the new structure. A periodic review process is necessary.
- With `OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES = TRUE` at the system level, candidate plans accumulate quickly. Without a regular evolution process, the baseline becomes an unmanageable archive.
- SPM is not a substitute for correct statistics. It's a stabilization tool, not an optimization tool. The good plan must exist and must be identified: SPM preserves it, it doesn't create it.

The strategy we adopted is selective: baselines only on identified critical queries, with a quarterly review. No automatic capture at the system level.

## The Monday morning report

In the days that followed, the revenue report started completing in around 3 minutes. No announcement, no heads-up to the dev team.

The first person to notice was one of the financial analysts, who wrote in the team chat: "The revenue report is already done? I usually kick it off and go grab a coffee."

The dev team asked what had changed. We walked them through the analysis, the suboptimal plan, the SPM mechanism. It was a useful conversation — not because the fix was complicated, but because it opened a discussion about managing critical queries proactively rather than reactively.

The management board noticed the improvement in the following weekly report. No heroics, no last-minute emergency. Just an analysis done on a quiet morning, triggered by a question from a curious junior.

Pietro, for his part, understood something that textbooks don't teach easily: that explaining a concept to someone forces you to look at it with fresh eyes. While I was walking him through the execution plan, I saw the slowness with the same freshness he did. Without that question, I probably would have opened another tab and moved on.

## What stays in the team runbook

After that morning, we added three practices to the team runbook:

1. **Quarterly review of SPM baselines** on critical queries — verifying that accepted plans are still optimal relative to the current table structure.
2. **AWR plan review** before and after every bulk statistics collection — comparing `plan_hash_value` for monitored queries.
3. **Pre-upgrade baseline loading procedure** — before any Oracle upgrade or patch, critical queries are identified and their current plans loaded into the baseline as a fallback.

SPM doesn't eliminate tuning work. It eliminates the surprise: that morning when you come into the office and find that a critical query has stopped performing the way it did yesterday, with no one having touched anything.

## Official sources

1. Oracle Database SQL Tuning Guide 19c — [Managing SQL Plan Baselines](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlad/managing-sql-plan-baselines.html)
2. Oracle Database PL/SQL Packages and Types Reference 19c — [DBMS_SPM](https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_SPM.html)
3. Oracle Database Reference 19c — [OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES.html)
4. Oracle-Base (Tim Hall) — [SQL Plan Management (SPM) in Oracle Database](https://oracle-base.com/articles/11g/sql-plan-management-11gr1)

## Glossary
- **[SQL Plan Management (SPM)](/en/glossary/sql-plan-management/)** — An Oracle Database feature that allows you to control and stabilize query execution plans through a repository of approved plans (baselines), preventing performance regressions caused by optimizer changes.

- **[SQL Plan Baseline](/en/glossary/awr/)** — The set of one or more accepted execution plans for a specific SQL statement, stored in the SPM repository. The optimizer only uses plans present in the baseline, ignoring alternative plans that haven't yet been verified.

- **[Fixed plan](/en/glossary/hash-join/)** (SPM) — An execution plan marked with attribute `FIXED = YES` in the SQL Plan Baseline. It has absolute precedence over all other plans in the baseline: the optimizer always selects it, regardless of any alternative plans it may find.

- **[AWR](/en/glossary/sql-plan-management/)** (Oracle) — Automatic Workload Repository: periodic snapshots of workload metrics, the foundation of AWR reports and ADDM. It preserves execution plan history via `DBA_HIST_SQLSTAT`, useful for identifying plan changes over time.

- **[Hash Join](/en/glossary/sql-plan-baseline/)** — A join algorithm used by the Oracle optimizer to combine two tables by building a hash table in memory from the smaller table and scanning the larger one. Efficient for large datasets without selective indexes; costly when applied before selective filters.
