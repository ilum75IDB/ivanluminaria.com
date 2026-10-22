---
title: "PGA (Program Global Area)"
description: "PGA is the private memory area Oracle allocates per session. Misconfiguration silently degrades sort and hash join operations, making root cause analysis harder."
translationKey: "glossary_pga"
aka: "Program Global Area"
articles:
  - "/posts/oracle/ai-mostra-sintomo-board-chiede-causa"
---

The PGA (Program Global Area) is a private memory region that Oracle allocates for each server process or session. Unlike the SGA (System Global Area), which is shared across all sessions, the PGA is exclusive to its session: it holds the working memory for sort operations, hash joins, bitmap merges, and session-level variables.

## How it works

Oracle manages PGA memory either automatically (`PGA_AGGREGATE_TARGET`) or manually. In automatic mode, the database estimates available memory and distributes it across active sessions. When allocated PGA exceeds the target, Oracle spills data to disk (temp tablespace), causing a measurable performance drop.

```sql
-- Check current PGA configuration
SELECT name, value
FROM v$pgastat
WHERE name IN (
  'aggregate PGA target parameter',
  'aggregate PGA auto target',
  'total PGA inuse',
  'cache hit percentage'
);
```

The `WORKAREA_SIZE_POLICY` parameter controls whether management is `AUTO` or `MANUAL`. In manual mode, parameters such as `SORT_AREA_SIZE` and `HASH_AREA_SIZE` set per-session limits.

## Operational context

An undersized PGA causes frequent disk spills: queries with ORDER BY, GROUP BY, or hash joins slow down without standard alerts (CPU, aggregate I/O) clearly pointing to the cause. The degradation typically correlates with peaks in concurrent sessions rather than individual query regressions.

A PGA setting that was changed without a change log entry is one of the most elusive sources of performance regressions: symptoms surface in production, but the root cause traces back to a parameter change made weeks earlier — exactly the scenario where observability tooling alone is insufficient.
