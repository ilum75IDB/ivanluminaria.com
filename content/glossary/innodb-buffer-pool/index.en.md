---
title: "InnoDB Buffer Pool"
description: "InnoDB's main memory area that caches data and index pages to minimize disk reads. Configured via innodb_buffer_pool_size."
translationKey: "glossary_innodb_buffer_pool"
aka: "InnoDB Buffer Pool (MySQL)"
articles:
  - "/posts/mysql/innodb-buffer-pool-dimensionamento-hit-ratio-e-warm-up-dopo-restart"
---

The InnoDB Buffer Pool is the central memory component of the InnoDB storage engine in MySQL. It acts as a shared cache for data pages and index pages: whenever a query reads or modifies a row, InnoDB loads the corresponding page into the buffer pool and keeps it in memory as long as possible. The larger the buffer pool relative to the active dataset, the less I/O reaches the disk.

## How it works

InnoDB manages the buffer pool using a modified LRU (Least Recently Used) algorithm split into a "young list" (recently accessed pages) and an "old list" (eviction candidates). When a requested page is not in memory, a **buffer pool miss** occurs and InnoDB reads it from disk. The ratio between hits and misses is the **buffer pool hit ratio**.

The primary parameter is `innodb_buffer_pool_size`. On servers dedicated to MySQL, it is typically set to 80% of available RAM:

```sql
-- Check the current size
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';

-- Change at runtime (MySQL 5.7.5+)
SET GLOBAL innodb_buffer_pool_size = 12884901888; -- 12 GB
```

## Operational context

The buffer pool is flushed on every server restart. MySQL supports **automatic warm-up** via `innodb_buffer_pool_dump_at_shutdown` and `innodb_buffer_pool_load_at_startup`, which serialize and restore the list of most-used pages. Without warm-up, the first hours after a restart show a low hit ratio and elevated latencies.

On systems where the dataset exceeds available RAM, monitoring the hit ratio via `SHOW ENGINE INNODB STATUS` or the `information_schema.INNODB_BUFFER_POOL_STATS` table is essential to determine whether a memory increase is justified.
