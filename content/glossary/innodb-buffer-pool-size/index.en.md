---
title: "innodb_buffer_pool_size"
description: "MySQL global parameter that sets the InnoDB buffer pool size for data and index caching — the single most impactful memory setting on a MySQL server."
translationKey: "glossary_innodb_buffer_pool_size"
aka: "InnoDB Buffer Pool"
articles:
  - "/posts/mysql/articolo-mysql-saturazione-swap-su-innodb-cluster-3-nodi-analisi-e-fix-dei-param"
---

`innodb_buffer_pool_size` is the MySQL global parameter that controls how much RAM is reserved for the InnoDB Buffer Pool — the in-memory structure that caches data and index pages to reduce disk I/O. It is the single parameter with the greatest performance impact on a dedicated MySQL server.

## How it works

InnoDB manages the Buffer Pool as a pool of 16 KB pages (default). When a query accesses a row, InnoDB loads the corresponding page into the Buffer Pool; subsequent reads on the same page are served from RAM without touching the disk. Modified pages (dirty pages) are flushed to disk asynchronously by background threads.

The value is set in `my.cnf` or `my.ini`:

```ini
[mysqld]
innodb_buffer_pool_size = 12G
```

On servers with RAM ≥ 1 GB, MySQL also supports dynamic reconfiguration at runtime:

```sql
SET GLOBAL innodb_buffer_pool_size = 12884901888;
```

## Sizing and operational context

On servers dedicated to MySQL, the established rule of thumb is **70–80% of available RAM**. Leaving less than 20% free puts memory pressure on the operating system and, in the worst cases, triggers swap usage — causing severe performance degradation.

In a 3-node InnoDB Cluster, each node maintains its own independent Buffer Pool. Oversizing on machines where RAM is shared with other processes (monitoring agents, binlog servers, etc.) is a frequent cause of swap saturation.

Monitoring the **Buffer Pool hit rate** is the primary indicator to watch:

```sql
SELECT
  (1 - (Innodb_buffer_pool_reads / Innodb_buffer_pool_read_requests)) * 100
    AS hit_rate_pct
FROM information_schema.GLOBAL_STATUS
WHERE Variable_name IN ('Innodb_buffer_pool_reads','Innodb_buffer_pool_read_requests');
```

A hit rate below 95% under OLTP workloads signals an undersized Buffer Pool.
