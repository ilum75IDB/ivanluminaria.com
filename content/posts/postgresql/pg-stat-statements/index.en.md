---
title: "pg_stat_statements: the first thing to install on any PostgreSQL"
description: "A production PostgreSQL running for two years without pg_stat_statements. When we activated it, three queries consumed 80% of resources — each fixable with a single index. How to install, query and read the results of PostgreSQL's most important diagnostic extension."
date: "2026-04-21T10:00:00+01:00"
draft: false
translationKey: "pg_stat_statements"
tags: ["monitoring", "performance", "pg_stat_statements", "diagnostics", "tuning"]
categories: ["postgresql"]
image: "pg-stat-statements.cover.jpg"
---

The ticket said: "The database has been slow for a few days, but we don't know which query is the problem."

PostgreSQL 15 in production, a business application for a manufacturing company with about four hundred users. The server had 64 GB of RAM, 16 cores, NVMe drives — more than adequate hardware for the workload. Yet the application response times had climbed from 200 milliseconds to 2-3 seconds, and the trend was worsening.

The first thing I asked the DBA was: "Show me the pg_stat_statements output."

Silence. Then: "We don't have it enabled."

Two years of production. Four hundred users. No query diagnostic tool installed. It's like driving at night without headlights — as long as the road is straight you don't notice anything, but at the first curve you end up in the ditch.

---

## What pg_stat_statements does

{{< glossary term="pg-stat-statements" >}}pg_stat_statements{{< /glossary >}} is a PostgreSQL extension — included in the official distribution but not active by default — that tracks execution statistics for all SQL queries that pass through the server.

For each query, it records:

- How many times it was executed (`calls`)
- How much total time it consumed (`total_exec_time`)
- How much time on average per execution (`mean_exec_time`)
- How many rows it returned (`rows`)
- How many blocks it read from disk (`shared_blks_read`) and from cache (`shared_blks_hit`)

Queries are normalized: literal values are replaced with `$1`, `$2`, etc. This means `SELECT * FROM users WHERE id = 42` and `SELECT * FROM users WHERE id = 99` are the same query for pg_stat_statements. That's exactly what you want — you care about the pattern, not individual values.

---

## Installation: five minutes that change everything

Installation requires a modification to `postgresql.conf` and a service restart. There's no way around the restart — the extension must be loaded as a shared library at process startup.

```ini
# postgresql.conf
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.max = 10000
pg_stat_statements.track = all
```

The `pg_stat_statements.max` parameter defines how many distinct queries are tracked. The default is 5000, but on databases with many different queries it's worth raising it. `pg_stat_statements.track` set to `all` also tracks queries executed inside PL/pgSQL functions — without this parameter, queries in stored procedures aren't recorded.

After the restart:

```sql
CREATE EXTENSION pg_stat_statements;
```

From this moment on, every query that passes through the server is tracked. No need to touch the application, no need to modify queries, nothing. It's completely transparent.

The overhead? Negligible. I've benchmarked on various environments and the impact is in the range of 1-2% additional CPU. On any production database, it's a cost that pays for itself at the first diagnosed problem.

---

## The three queries eating the server

Back to the client. After the restart with the extension active, I waited 24 hours to collect a representative sample of the workload. Then I ran the query I always run first:

```sql
SELECT
    substring(query, 1, 80) AS query_truncated,
    calls,
    round(total_exec_time::numeric, 2) AS total_time_ms,
    round(mean_exec_time::numeric, 2) AS mean_time_ms,
    rows,
    round((100 * total_exec_time / sum(total_exec_time) OVER ())::numeric, 2) AS percentage
FROM pg_stat_statements
WHERE userid != (SELECT usesysid FROM pg_user WHERE usename = 'postgres')
ORDER BY total_exec_time DESC
LIMIT 20;
```

This query sorts all tracked queries by total time consumed and shows the percentage of the total. It's the starting point — it tells you immediately where the database's time goes.

The result was striking:

| # | Query (truncated) | Calls | Total time | Mean time | % |
|---|------------------|-------|------------|-----------|---|
| 1 | `SELECT o.*, c.name FROM orders o JOIN customers c ON...` | 847,000 | 1,240,000 ms | 1.46 ms | 42% |
| 2 | `SELECT p.*, s.qty FROM products p LEFT JOIN stock s...` | 312,000 | 680,000 ms | 2.18 ms | 23% |
| 3 | `SELECT * FROM audit_log WHERE created_at > $1 AND...` | 28,000 | 440,000 ms | 15.71 ms | 15% |

Three queries. 80% of the database's total time.

The first was executed 847,000 times in 24 hours — roughly ten times per second. The average time was low (1.46 ms) but the volume made it the most expensive overall. A missing index on the join column of the `customers` table.

The second had a LEFT JOIN doing a sequential scan on the `stock` table — 2 million rows, every time. An index on the join column brought the mean_time from 2.18 ms to 0.12 ms.

The third was the one that worried me most. 15 milliseconds average on an audit table with 50 million rows. The query filtered by `created_at` and `action_type`, but the existing index was only on `created_at`. A composite index `(created_at, action_type)` solved the problem.

Three indexes. Twenty minutes of work. The application's average response time dropped from 2.3 seconds to 180 milliseconds.

---

## The diagnostic queries I always use

After years of use, I have a set of queries I run regularly. I'm sharing them because they're the ones I wish I'd had when I started with PostgreSQL.

### Top queries by total time

That's the query I showed above. It tells you where the database's time goes. I use it as the first step in any diagnostic session.

### Top queries by average time

```sql
SELECT
    substring(query, 1, 80) AS query_truncated,
    calls,
    round(mean_exec_time::numeric, 2) AS mean_time_ms,
    round(total_exec_time::numeric, 2) AS total_time_ms,
    rows
FROM pg_stat_statements
WHERE calls > 100
ORDER BY mean_exec_time DESC
LIMIT 20;
```

This complements the first. It finds individually slow queries — ones that might be executed few times but each takes seconds. The `calls > 100` filter avoids picking up one-off queries that aren't representative.

### Queries with the most disk I/O

```sql
SELECT
    substring(query, 1, 80) AS query_truncated,
    calls,
    shared_blks_read AS disk_blocks,
    shared_blks_hit AS cache_blocks,
    round(
        100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0), 2
    ) AS cache_hit_ratio
FROM pg_stat_statements
WHERE shared_blks_read > 1000
ORDER BY shared_blks_read DESC
LIMIT 20;
```

This is essential for understanding which queries are hammering the disk. A `cache_hit_ratio` below 90% on a frequent query is a red flag — it means the data doesn't fit in `shared_buffers` and every execution reads from the filesystem.

### Queries with the worst rows returned / blocks read ratio

```sql
SELECT
    substring(query, 1, 80) AS query_truncated,
    calls,
    rows AS rows_returned,
    shared_blks_hit + shared_blks_read AS total_blocks,
    round(rows::numeric / nullif(shared_blks_hit + shared_blks_read, 0), 4) AS efficiency
FROM pg_stat_statements
WHERE calls > 50
  AND (shared_blks_hit + shared_blks_read) > 0
ORDER BY efficiency ASC
LIMIT 20;
```

This finds queries that read many blocks to return few rows — the classic sign of a sequential scan where an index scan should be used. An efficiency near zero on a frequent query is almost always a missing index.

---

## Resetting statistics: when and why

pg_stat_statements statistics are cumulative from the last reset. If the server has been up for six months, you're looking at a six-month average — which might hide a recent problem.

```sql
SELECT pg_stat_statements_reset();
```

When to reset? It depends on the situation:

- **After an application deploy**: queries change, old data is no longer useful
- **After a tuning intervention**: you want to see the effect of the new indexes, not the average with the "before"
- **Periodically**: some teams do a weekly or monthly reset and save the data to a history table before resetting

An approach I often use is saving a snapshot before the reset:

```sql
CREATE TABLE pgss_snapshot AS
SELECT now() AS snapshot_time, *
FROM pg_stat_statements;

SELECT pg_stat_statements_reset();
```

This gives you the history and fresh statistics.

---

## pg_stat_statements + EXPLAIN: the complete workflow

pg_stat_statements tells you *which* query is the problem. EXPLAIN tells you *why* it's a problem. Using them together is the most powerful diagnostic workflow PostgreSQL offers.

The process I follow is always the same:

1. **Identify the top queries** with pg_stat_statements (by total time, average time, or I/O)
2. **Copy the normalized query** and replace `$1`, `$2` with real values
3. **Run EXPLAIN (ANALYZE, BUFFERS)** to see the execution plan
4. **Look for red flags**: sequential scans on large tables, nested loops with many rows, on-disk sorts
5. **Intervene**: create an index, rewrite the query, update statistics with ANALYZE

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT o.*, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.created_at > '2026-01-01';
```

The important thing is the cycle: after the intervention, reset pg_stat_statements, wait a few hours, and verify that the query has actually improved in real numbers — not just in the EXPLAIN.

---

## Why it's not enabled by default

A question I get often: if pg_stat_statements is so useful, why doesn't PostgreSQL enable it by default?

The answer is philosophical rather than technical. PostgreSQL has a culture of minimalism — the core does the database, everything else is an extension. The overhead of pg_stat_statements is negligible, but the project prefers not to impose anything. It's the same reason `shared_buffers` defaults to 128 MB — a ridiculous value for any production use, but the project doesn't want to presume how much hardware you have.

The practical consequence is that every PostgreSQL installation should be explicitly configured. And pg_stat_statements should be the first line on the post-installation checklist — before tuning shared_buffers, before configuring autovacuum, before everything else.

Without pg_stat_statements you're flying blind. You can tune all you want, but you're guessing where to intervene.

---

## The day after

The day after creating the three indexes, I checked pg_stat_statements again. The workload distribution had changed completely. The three queries that previously consumed 80% of the time were now at 12% — and the most expensive query had become a report that ran once a day and nobody had ever complained was slow.

The DBA asked me: "But why didn't anyone tell us to install this extension?"

The answer is that pg_stat_statements isn't a secret. It's in the official documentation, it's in every performance tuning tutorial, it's recommended by every PostgreSQL DBA I know. But if you don't install it, you don't know what you don't know. And if you don't know what you don't know, everything seems to work — until it doesn't.

Five minutes of installation. Twenty minutes of analysis. Three indexes. A database that went from "slow for a few days" to "the fastest we've ever had" — which really just means "as fast as it should have been from the start."

------------------------------------------------------------------------

## Glossary

**[pg_stat_statements](/en/glossary/pg-stat-statements/)** — PostgreSQL extension that collects execution statistics for all SQL queries: times, counts, rows returned and blocks read. Essential tool for performance diagnostics.

**[shared_buffers](/en/glossary/shared-buffers/)** — PostgreSQL's shared memory area that serves as a cache for data blocks read from disk. The most important memory tuning parameter, with a default of 128 MB that's almost always inadequate for production.

**[Execution Plan](/en/glossary/execution-plan/)** — Sequence of operations (scan, join, sort) that the database chooses to resolve an SQL query. Viewed with EXPLAIN and EXPLAIN ANALYZE.

**[Sequential Scan](/en/glossary/sequential-scan/)** — Read operation where PostgreSQL reads all blocks of a table from start to finish without using indexes. Efficient on small tables, problematic on large tables when only a subset of rows is needed.

**[ANALYZE](/en/glossary/postgresql-analyze/)** — PostgreSQL command that collects statistics about data distribution in tables, used by the optimizer to choose the execution plan.
