---
title: "Parallel Replication"
description: "MySQL replication mode that applies binlog events using multiple worker threads, reducing slave lag via LOGICAL_CLOCK commit timestamp grouping."
translationKey: "glossary_parallel_replication"
aka: "Multi-threaded Replication (MTR)"
articles:
  - "/posts/mysql/replica-mysql-quando-lo-slave-resta-indietro-e-nessuno-se-ne-accorge"
---

Parallel Replication is the mode in which MySQL applies binlog events on the replica using multiple worker threads simultaneously, replacing the traditional single SQL thread. The goal is to reduce replication lag when the primary generates transactions faster than the replica can apply them sequentially.

## How it works

MySQL exposes two policies via `slave_parallel_type`:

- **`DATABASE`**: parallelizes transactions that touch different databases. Only effective when the workload is spread across multiple schemas.
- **`LOGICAL_CLOCK`**: uses commit timestamps recorded in the binlog to identify transactions that were executing concurrently on the primary and can therefore be applied in parallel on the replica without breaking consistency.

`LOGICAL_CLOCK` is the recommended mode in most scenarios. The number of workers is controlled by `slave_parallel_workers`.

```sql
-- Typical replica configuration
SET GLOBAL slave_parallel_type = 'LOGICAL_CLOCK';
SET GLOBAL slave_parallel_workers = 8;
```

## When to use it

Parallel Replication becomes relevant when the replica accumulates lag even though hardware is not saturated — the bottleneck is event serialization, not resources. It is particularly effective on OLTP workloads with many short, concurrent transactions on the primary.

There are limits: if the primary runs mostly serial transactions or heavy single-table writes, the gain is marginal. Increasing `slave_parallel_workers` beyond a certain threshold also introduces coordination overhead that can degrade performance rather than improve it. The optimal value must be determined empirically based on the actual workload profile.
