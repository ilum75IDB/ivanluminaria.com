---
categories:
- data-warehouse
date: '2026-12-09'
description: How Materialized Views turned a slow DWH prototype into a credible reporting
  system for a major telco operator. Selection criteria, refresh strategies, and measurable
  results.
draft: false
image: la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto.cover.jpg
seoTitle: 'Materialized Views in DWH: analytical performance in Telco'
tags:
- materialized-views
- data-warehouse
- performance-tuning
- oracle
- postgresql
title: 'The demo that couldn''t wait: Materialized Views in a Telco DWH'
translationKey: la_demo_che_non_poteva_aspettare_materialized_views_e_un_dwh_telco_sotto
webo_generated_at: 2026-11-14
webo_status: scheduled
---

## The demo that couldn't wait

It was a project we shouldn't have been doing. Not in the sense that it was wrong — it was exactly the kind of work we enjoyed — but in the sense that nobody had commissioned it. The consulting team had decided to build a Data Warehouse prototype for a large mobile telco operator we'd been working with for months, convinced that detailed reporting on customers and call traffic could open up new commercial conversations. An internal bet, funded with unbilled hours and a fair amount of enthusiasm.

The idea was straightforward: bring the client's marketing team a dashboard showing traffic patterns, geographic distribution of calls, segmentation by contract type. Data they already had, but couldn't read in aggregated form. We had access to the source systems, we had the experience, we had something to prove.

What we hadn't calculated properly was the scale.

The call detail records — CDRs — were accumulating at roughly 500 GB per month. Years of historical data, tens of millions of rows for each monthly period. When we started building reports on top of these tables, reality made itself felt in a fairly direct way: colleagues testing the queries came back with long faces and discouraging numbers. One hour and forty-five minutes for a monthly aggregation. Three minutes to load the main dashboard. The PM, who had believed in the project from the start, had stopped asking enthusiastic questions and started asking worried ones.

The demo was scheduled. It couldn't be moved.

## When the engine stalls on volume

The problem wasn't a bug. It was structural — and it's worth understanding why, because it's the same problem you run into in any analytical environment that grows without a pre-aggregation strategy.

Reporting queries on a DWH have a specific characteristic: they aggregate large volumes of historical data to produce summary results. A query that calculates monthly traffic per customer, for example, potentially has to read millions of rows, apply aggregation functions, and join against the customer master table. The database performs this work every single time someone opens the report.

A typical query against our schema looked like this:

```sql
SELECT
    cm.REGION,
    cm.ID_CUSTOMER,
    cm.NAME,
    cm.SURNAME,
    SUM(cdr.CALL_DURATION_SEC) / 60.0  AS TOTAL_DURATION_MIN,
    COUNT(cdr.ID_CDR)                  AS TOTAL_CALLS,
    AVG(cdr.COST)                      AS AVG_COST_PER_CALL
FROM
    call_detail_records cdr
    JOIN customer_master cm ON cdr.ID_CUSTOMER = cm.ID_CUSTOMER
WHERE
    cdr.CALL_DATE >= TRUNC(ADD_MONTHS(SYSDATE, -1), 'MM')
    AND cdr.CALL_DATE <  TRUNC(SYSDATE, 'MM')
GROUP BY
    cm.REGION,
    cm.ID_CUSTOMER,
    cm.NAME,
    cm.SURNAME
ORDER BY
    cm.REGION,
    TOTAL_DURATION_MIN DESC;
```

The execution plan showed exactly what we expected: a full scan on `call_detail_records` for the selected month, a hash join with `customer_master`, then the aggregation. With 500 GB of monthly CDR data and indexes that offered little help on such broad date-range queries, the response time was what it was.

Adding indexes would have helped marginally. Partitioning by date would have reduced the volume scanned, but we didn't have time to redesign the schema before the demo. We needed something that shifted the work outside the query itself.

## Experience finding its moment

It wasn't a sudden insight. I proposed Materialized Views because I'd already used them in other contexts — on Oracle, in financial reporting environments — and I knew the pattern fit well with what we were trying to do.

A Materialized View is, in essence, a query whose results are computed once and stored physically on disk as if they were a table. When an application queries the MV, it recalculates nothing: it reads already-aggregated data. The difference from a standard view is exactly this: a regular view is a query definition that executes every time; an MV is a pre-computed result that gets refreshed periodically.

Oracle has supported Materialized Views for a long time, with sophisticated refresh options and automatic query rewriting [1][2]. PostgreSQL introduced them in version 9.3 with a more streamlined syntax but equally effective [3]. In both cases, the principle is the same: shift the computational cost from read time to refresh time.

In our context, this was exactly the right trade-off. Historical data didn't change. Last month's reports were static. We could pre-compute everything once — or at most once a day — and serve results in milliseconds.

## Ideal candidates and scenarios where it doesn't make sense

Not every query is a good candidate for a Materialized View. Before implementing, we did a quick mapping of access patterns.

Ideal candidates share a few characteristics:

**Frequent aggregations on stable historical data.** If the same aggregation runs dozens of times a day against data that changes little or not at all, the cost of periodic refresh is easily justified by the savings on reads. Monthly CDR reports were the perfect case: data from the previous month never changes; current-month data only changes as new records arrive.

**Complex joins between large tables.** The join between `call_detail_records` and `customer_master` was expensive because it involved millions of rows. Pre-computing it in the MV meant the dashboard never had to execute that join again.

**Reports with tolerable data latency.** If marketing is fine with reports updated every hour, or even nightly, an MV with a scheduled refresh is the natural solution. If you need real-time consistency — a bank balance, a live inventory level — MVs add complexity without solving the problem.

Cases where it **doesn't** make sense:

- Data that changes continuously and requires immediate consistency
- Queries that run rarely (refresh cost outweighs the benefit)
- Small source tables where the original query is already fast
- OLTP scenarios where the write latency of the refresh is unacceptable

In our DWH, the distinction was clear: historical data was a perfect fit for MVs; current-day data could stay on direct queries.

## Refresh, consistency, and the hidden cost

The part that requires the most attention isn't creating the MV — it's managing the refresh. This is where the architectural decisions that actually matter get made.

Oracle offers two main modes [2]:

- **`REFRESH COMPLETE`**: recomputes the entire MV from scratch. Simple, reliable, expensive on large volumes. Suitable when source data changes in ways that can't be tracked incrementally.
- **`REFRESH FAST`**: incremental update based on *materialized view logs*, structures that track changes to the source tables. Much more efficient, but requires that the base tables have logs enabled and that the MV query respects certain constraints.

PostgreSQL [3] supports only full refresh (`REFRESH MATERIALIZED VIEW`), with the `CONCURRENTLY` option that allows updating the MV without blocking reads — provided a unique index exists on the MV itself.

In our case we chose a pragmatic approach: nightly full refresh for MVs on historical data, executed via an internal scheduler during low-activity hours. The load on the source system during refresh was concentrated in an acceptable time window, and morning reports found data already ready.

The Oracle configuration for automatic refresh looked like this:

```sql
-- Job creation for scheduled refresh (Oracle DBMS_SCHEDULER)
BEGIN
    DBMS_SCHEDULER.CREATE_JOB(
        job_name        => 'REFRESH_MV_MONTHLY_TRAFFIC',
        job_type        => 'PLSQL_BLOCK',
        job_action      => 'BEGIN DBMS_MVIEW.REFRESH(''MV_MONTHLY_TRAFFIC_SUMMARY'', ''C''); END;',
        start_date      => TRUNC(SYSDATE + 1) + INTERVAL '2' HOUR,
        repeat_interval => 'FREQ=DAILY; BYHOUR=2; BYMINUTE=0',
        enabled         => TRUE,
        comments        => 'Nightly refresh of monthly traffic MV for marketing reporting'
    );
END;
/
```

One detail worth highlighting: a full refresh on a large MV temporarily blocks queries against that MV (in Oracle, unless you use `ATOMIC_REFRESH => FALSE`). Scheduling the refresh at the right time isn't a secondary operational detail — it's part of the design.

## The reports come back to life

The MV that solved the main problem aggregated monthly traffic by customer and region:

```sql
CREATE MATERIALIZED VIEW mv_monthly_traffic_summary
BUILD IMMEDIATE
REFRESH COMPLETE ON DEMAND
AS
SELECT
    cm.REGION,
    cm.ID_CUSTOMER,
    cm.NAME,
    cm.SURNAME,
    TRUNC(cdr.CALL_DATE, 'MM')          AS CALL_MONTH,
    SUM(cdr.CALL_DURATION_SEC) / 60.0   AS TOTAL_DURATION_MIN,
    COUNT(cdr.ID_CDR)                   AS TOTAL_CALLS,
    AVG(cdr.COST)                       AS AVG_COST_PER_CALL
FROM
    call_detail_records cdr
    JOIN customer_master cm ON cdr.ID_CUSTOMER = cm.ID_CUSTOMER
GROUP BY
    cm.REGION,
    cm.ID_CUSTOMER,
    cm.NAME,
    cm.SURNAME,
    TRUNC(cdr.CALL_DATE, 'MM');

-- Index for the dashboard's most frequent queries
CREATE INDEX idx_mv_monthly_region_month
    ON mv_monthly_traffic_summary (REGION, CALL_MONTH);
```

The numbers after the first refresh were what we'd hoped for. The monthly aggregation query that had taken 45 seconds dropped to 2 seconds — and those 2 seconds were almost entirely network latency and application rendering, not database processing. The marketing dashboard load time went from 3 minutes to around 10 seconds.

The PM saw the results on a test screen the afternoon before the demo. He didn't say much. He nodded, asked whether we were sure the data was correct, and when we confirmed that yes, it was the same data as before, just pre-aggregated, he said "good" and closed his laptop.

That's the kind of silent approval that counts more than any compliment.

## Beyond the demo: the value that stays

The demo went well. The client's marketing team engaged with the reports, asked questions about the data, wanted to know whether it was possible to add filters by contract type and geographic area. Nobody commented on the speed — and that was exactly the right outcome. When a system works as it should, users don't think about the infrastructure. They think about the data.

The implicit objection that had been hanging over the project — "we already have the data, why should we invest in a separate DWH?" — dissolved the moment the marketing team saw patterns they hadn't been able to see before. Not because the data was new, but because it was accessible in a different way. Aggregated, navigable reporting changes the kind of questions you can ask.

Materialized Views weren't the answer to everything. The DWH still needed work: handling incremental updates, historicizing master data, managing exceptions in the CDRs. But they had solved the problem that was blocking the project at that specific moment, and they had established an architectural principle we'd use as a foundation for the rest of the development: pre-compute what is stable, keep dynamic only what must be.

The project didn't stay a prototype. In the months that followed, it became a contract.

## What stays in the notebook

The most useful lesson from this story isn't about Materialized Views themselves. It's about the moment when a technical tool becomes relevant.

MVs weren't new to any of us. They were a tool we knew, had used in other contexts, knew to work in certain scenarios. The value wasn't in the invention — it was in the recognition: this problem, at this moment, with these time constraints, gets solved this way.

There are situations where the right solution is the one you already know, not the one you're trying to learn. Knowing when to apply what you already have in the toolkit is a skill built over years and projects, not tutorials.

The PM gave trust and room to implement something that wasn't in the original plan. The team worked together to verify data correctness after the refresh. The client's DBA checked the impact on the source system during the nightly refresh window and gave the go-ahead. Nobody saved anything alone — it worked out because the right people did the right things at the right time.

The technical notebook grows this way: not with new solutions, but with contexts where old solutions still work.

## Official sources

1. Oracle Database SQL Language Reference 19c — [CREATE MATERIALIZED VIEW](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/CREATE-MATERIALIZED-VIEW.html) — full syntax, `REFRESH FAST/COMPLETE`, `ON COMMIT`, `BUILD IMMEDIATE/DEFERRED` options
2. Oracle Database Data Warehousing Guide 19c — [Basic Materialized Views](https://docs.oracle.com/en/database/oracle/oracle-database/19/dwhsg/basic-materialized-views.html) — concepts, DWH usage strategies, query rewriting
3. PostgreSQL Documentation — [Materialized Views](https://www.postgresql.org/docs/current/rules-materializedviews.html) — `CREATE MATERIALIZED VIEW`, `REFRESH MATERIALIZED VIEW`, `CONCURRENTLY` option

## Glossary
- **[Materialized View (MV)](/en/glossary/materialized-view/)** — A pre-computed view stored physically on disk. Contains the result of a query executed in advance; subsequent reads access already-aggregated data without recalculating. Supported by Oracle, PostgreSQL, SQL Server, and other RDBMS.

- **[Refresh (MV)](/en/glossary/materialized-view/)** — The process of updating a Materialized View's data to reflect changes in the base tables. Can be complete (full recomputation) or incremental (only changes tracked in MV logs). Frequency and mode are architectural choices with direct performance implications.

- **[Call Detail Record (CDR)](/en/glossary/refresh/)** — A record describing a single phone call: customer identifier, date, duration, call type, cost. In telco systems, CDRs are the primary operational data and accumulate in very high volumes (hundreds of GB per month for mid-sized operators).

- **[Query Rewriting](/en/glossary/materialized-view/)** — An Oracle feature that automatically intercepts a query against base tables and redirects it to an equivalent Materialized View, without any changes to application code. Enabled with `ENABLE QUERY REWRITE` in the MV definition.

- **[Data Warehouse (DWH)](/en/glossary/refresh/)** — A database system optimized for historical data analysis, aggregating information from multiple operational sources. Unlike OLTP systems, it prioritizes large-scale reads and aggregations over frequent, point-in-time writes.
