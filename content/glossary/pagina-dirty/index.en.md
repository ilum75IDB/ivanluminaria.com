---
title: "Dirty page"
description: "Buffer pool page modified in memory but not yet written to disk. A high and growing count signals that InnoDB's flush thread cannot keep up with incoming writes."
translationKey: "glossary_pagina_dirty"
aka: "Dirty buffer, unflushed page"
articles:
  - "/posts/mysql/innodb-buffer-pool-dimensionamento-hit-ratio-e-warm-up-dopo-restart"
---

In InnoDB's buffer pool, a **dirty page** is a 16 KB page that has been modified in memory — by an INSERT, UPDATE, or DELETE — but whose updated content has not yet been written back to the data file on disk. The on-disk version is therefore stale relative to the in-memory one.

## How it works

Every time a transaction modifies a row, InnoDB updates the corresponding page in the buffer pool and marks it as dirty. A background flush thread (`page_cleaner`) periodically writes dirty pages to the `.ibd` files using two main strategies:

- **Fuzzy checkpoint**: continuous, incremental flushing to keep the dirty page ratio below `innodb_max_dirty_pages_pct` (default 90%).
- **Adaptive flushing**: accelerates flushing when the redo log write rate approaches its capacity limit, preventing InnoDB from having to stall user writes to reclaim space.

```sql
-- Monitor dirty pages in real time
SELECT VARIABLE_NAME, VARIABLE_VALUE
FROM performance_schema.global_status
WHERE VARIABLE_NAME IN (
    'Innodb_buffer_pool_pages_dirty',
    'Innodb_buffer_pool_pages_total'
);
```

## Operational context

A stable, low dirty page count is normal. The warning sign is a **sustained, monotonically increasing count**: it means the flush thread cannot drain writes fast enough. Common causes include a buffer pool that is large relative to disk throughput, an `innodb_io_capacity` set too low, or a sudden spike in write load.

In the event of a crash, InnoDB uses the redo log to recover dirty pages that were never flushed. The more dirty pages exist at crash time, the longer crash recovery will take on restart.
