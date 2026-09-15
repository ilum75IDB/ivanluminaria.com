---
title: "Buffer pool warm-up"
description: "Process of reloading hot pages into the InnoDB buffer pool after a restart, cutting cold-start time from hours to minutes."
translationKey: "glossary_buffer_pool_warm_up"
aka: "Buffer pool preloading"
articles:
  - "/posts/mysql/innodb-buffer-pool-dimensionamento-hit-ratio-e-warm-up-dopo-restart"
---

When MySQL restarts, the buffer pool is empty: every query must read from disk until the most-used pages are back in memory. Buffer pool warm-up is the process that accelerates this recovery, restoring hot pages before production traffic demands them.

## How it works

InnoDB can save the identifiers of pages resident in memory at shutdown and reload them on the next startup. Two system variables control the behavior:

```sql
-- Enable automatic dump at shutdown
SET GLOBAL innodb_buffer_pool_dump_at_shutdown = ON;

-- Enable automatic load at startup (set in my.cnf)
-- innodb_buffer_pool_load_at_startup = ON
```

The output file (`ib_buffer_pool`) contains `(tablespace_id, page_id)` pairs, not the actual data: it is lightweight, and the restore runs in the background without blocking incoming connections. The variable `innodb_buffer_pool_dump_pct` (default 25) limits the percentage of pages serialized, balancing completeness against dump time.

## When to use it

Warm-up is relevant in three main scenarios:

- **Planned restarts** (OS patching, MySQL upgrades): without warm-up, the hit ratio can stay below 50% for hours on instances with buffer pools in the tens of GB.
- **Replica failover**: a replica promoted to primary starts with a cold buffer pool; enabling dump/load on replicas as well reduces post-failover degradation.
- **Cloud environments with spot/preemptible instances**: frequent stop-start cycles make automatic warm-up nearly mandatory.

Load progress can be monitored in real time:

```sql
SHOW STATUS LIKE 'Innodb_buffer_pool_load_status';
```
