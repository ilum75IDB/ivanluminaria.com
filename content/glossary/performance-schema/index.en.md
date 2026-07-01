---
title: "performance_schema"
description: "MySQL system schema collecting real-time execution metrics: query digests, wait events, and per-thread memory. The baseline for performance diagnostics without external tools."
translationKey: "glossary_performance_schema"
aka: "P_S (common abbreviation)"
articles:
  - "/posts/mysql/articolo-mysql-saturazione-swap-su-innodb-cluster-3-nodi-analisi-e-fix-dei-param"
---

`performance_schema` is a system database available in MySQL since version 5.5, designed to expose internal server execution metrics without requiring external tooling. Data is collected in memory through low-overhead instrumentation structures and updated in real time.

## How it works

The instrumentation engine intercepts internal events (queries, locks, I/O, memory allocations) and aggregates them into tables queryable via standard SQL. The main areas covered are:

- **Statement digests**: aggregated statistics per normalized query (`events_statements_summary_by_digest`)
- **Wait events**: waits on mutexes, I/O, locks (`events_waits_summary_global_by_event_name`)
- **Memory**: allocations per thread and per component (`memory_summary_by_thread_by_event_name`)

```sql
-- Top 10 queries by average latency
SELECT
    digest_text,
    count_star,
    ROUND(avg_timer_wait / 1e9, 2) AS avg_ms
FROM performance_schema.events_statements_summary_by_digest
ORDER BY avg_timer_wait DESC
LIMIT 10;
```

Granular enablement of instruments is controlled through the `setup_instruments` and `setup_consumers` tables: only the required categories can be activated to minimize workload impact.

## When to use it

`performance_schema` is the starting point for any MySQL performance analysis when external APM tools are unavailable. Typical scenarios:

- Identifying slow queries when the slow query log is not enabled
- Diagnosing contention on the InnoDB buffer pool or row-level locks
- Monitoring per-thread memory usage in environments with high concurrent connections (relevant in InnoDB Cluster setups)

**Key limitations**: data is volatile (reset on server restart), tables are not persisted to disk, and the overhead — while low — is measurable on workloads with very high frequency of short statements.
