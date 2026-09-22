---
title: "Hit ratio"
description: "Percentage of InnoDB page reads served from the Buffer Pool vs. total reads. Values below 990/1000 indicate excessive disk pressure."
translationKey: "glossary_hit_ratio"
aka: "Buffer Pool hit ratio"
articles:
  - "/posts/mysql/innodb-buffer-pool-dimensionamento-hit-ratio-e-warm-up-dopo-restart"
---

The hit ratio measures how many InnoDB page reads are satisfied directly from the Buffer Pool, without touching the disk. It is the primary indicator of how effectively the memory allocated to InnoDB is being used: a high value means the active working set fits in RAM; a low value means frequent physical I/O and higher latencies.

## How to read it

MySQL reports the hit ratio inside `SHOW ENGINE INNODB STATUS`, under the `BUFFER POOL AND MEMORY` section:

```
Buffer pool hit rate X / 1000
```

A value of `997 / 1000` means 997 out of every 1000 reads were served from memory. The widely accepted operational threshold is **990/1000**: dropping below it signals that the Buffer Pool is undersized relative to the active working set.

## Operational context

The hit ratio is particularly volatile after a MySQL restart: the Buffer Pool is cold and the first queries trigger cascading page faults, pushing the value well below 900/1000. InnoDB addresses this with automatic Buffer Pool dump and reload (`innodb_buffer_pool_dump_at_shutdown` / `innodb_buffer_pool_load_at_startup`), which significantly shortens the warm-up window.

A chronically low hit ratio is not always fixed by increasing `innodb_buffer_pool_size` alone. Inefficient queries performing full scans on large tables pollute the Buffer Pool with single-use pages, displacing hot data regardless of how much memory is available.
