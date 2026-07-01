---
categories:
- mysql
date: 2099-12-31
draft: true
image: articolo-mysql-saturazione-swap-su-innodb-cluster-3-nodi-analisi-e-fix-dei-param.cover.jpg
tags: []
title: 'Swap at 100% on InnoDB Cluster: when join_buffer_size multiplies the problem'
translationKey: articolo_mysql_saturazione_swap_su_innodb_cluster_3_nodi_analisi_e_fix_dei_param
webo_generated_at: 2026-07-01
webo_status: da_tradurre
---

```
---
title: "The Tuesday morning call: MySQL InnoDB Cluster, swap at 100%, and a 2 GB per-thread buffer"
seoTitle: "MySQL InnoDB Cluster: swap at 100% and join_buffer_size fix"
description: "A MySQL InnoDB Cluster grinding to a halt due to join_buffer_size set to 2 GB per thread. Diagnosis, rolling restart, and the math behind per-thread buffers."
tags: ["mysql", "innodb-cluster", "performance-tuning", "memory", "incident-response"]
---
```

## The Tuesday morning call

Tuesday morning, just after nine. Coffee still warm on the desk, the kind of day that feels like you might finally close out the things left hanging since Friday. Then the call came in.

On the other end: the infrastructure team at an Italian grocery retail chain. Their monitoring backend had become painfully slow, internal dashboards wouldn't load, some alerts weren't firing. One node in the MySQL cluster had essentially stopped. "We didn't touch anything, it just happened."

Under the hood there was an aggregation query, seemingly harmless. Something like:

```sql
SELECT itemid, MIN(clock), MAX(clock), COUNT(*)
FROM history_log
GROUP BY itemid;
```

On a table with 1.3 billion rows, no partitioning, no time filter, no `LIMIT`. The cluster's secondary node had started swapping aggressively, then stopped responding.

The context: this retail company runs a 3-node MySQL InnoDB Cluster as the backend for their internal monitoring platform — the one that keeps tabs on POS systems, warehouses, and store logistics. The nodes — `mysql-node-01`, `mysql-node-02`, `mysql-node-03` — handle the collection and querying of historical metrics. The `history_log` table is the heart of the system: every monitoring event lands there, accumulating over time with no active retention policy and no date-based partitioning.

When the query ran in production — someone was evidently trying to answer a business question about the full item history — the secondary node didn't have enough free RAM to sustain the full scan. The situation, though, didn't end with that one query. It was the underlying memory configuration that made the cluster structurally fragile against any non-trivial aggregated load.

## `free -h` and the first surprise

The first signal had come from the customer's monitoring dashboard, shared on the call a few minutes after the initial phone call: the swap graph on `mysql-node-01` and `mysql-node-02` showed a flat line at maximum for hours. On `mysql-node-03`, everything looked normal.

```bash
# mysql-node-01
              total        used        free      shared  buff/cache   available
Mem:           157Gi       155Gi       512Mi       1.2Gi       1.5Gi       400Mi
Swap:            6Gi         6Gi         0Bi

# mysql-node-02
              total        used        free      shared  buff/cache   available
Mem:           157Gi       150Gi       2.1Gi       1.1Gi       4.8Gi       1.2Gi
Swap:            6Gi         6Gi         0Bi

# mysql-node-03
              total        used        free      shared  buff/cache   available
Mem:           157Gi        21Gi       130Gi       0.3Gi       5.9Gi       134Gi
Swap:            6Gi       512Mi       5.5Gi
```

The difference between nodes was stark. `mysql-node-03` was the node that had received the least query load during that period — the "cold" secondary, so to speak. The first two were handling the main read/write traffic, and memory was exhausted.

`vmstat 1 5` confirmed it: swap actively in use, not just statically occupied.

```bash
# vmstat 1 5 on mysql-node-01
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 3  2 6291456  52428  18432 1572864  142  198  2840  3120 4821 9234 28  8 58  6  0
 2  1 6291456  48120  18432 1572864  156  212  3012  3340 5102 9876 31  9 54  6  0
```

`si` and `so` (swap-in and swap-out) actively running: the kernel was continuously moving pages between RAM and disk. With a relational database under load, this is the fastest way to irreversibly degrade performance.

## The math that didn't add up

Looking at the active configuration on the cluster, the parameter that jumped out immediately was this:

```sql
SHOW VARIABLES LIKE 'join_buffer_size';
-- join_buffer_size = 2147483648  (2 GB)

SHOW VARIABLES LIKE 'max_connections';
-- max_connections = 151

SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
-- innodb_buffer_pool_size = 133143986176  (124 GB)
```

`join_buffer_size` at 2 GB is a **per-thread** parameter, not global. Every MySQL connection executing a join without an index can allocate up to 2 GB of additional memory. With `max_connections = 151`, the theoretical allocation potential is:

```
2 GB × 151 connections = 302 GB
```

On machines with 157 GB of total RAM, of which 124 GB already committed to `innodb_buffer_pool_size`.

Obviously 302 GB doesn't get allocated all at once under normal conditions — per-thread buffers are only allocated when needed, and not all connections execute joins simultaneously. During an aggregated load spike, though, with full-scan queries on `history_log` running across multiple connections, even a fraction of that potential is enough to saturate available RAM.

`tmp_table_size` and `max_heap_table_size` were also oversized, contributing to pressure on in-memory temporary tables.

## What the `performance_schema` was saying

To understand which queries were actually consuming resources, querying `events_statements_summary_by_digest` gave the full picture:

```sql
SELECT
    DIGEST_TEXT,
    COUNT_STAR,
    SUM_ROWS_EXAMINED,
    SUM_CREATED_TMP_DISK_TABLES,
    SUM_NO_INDEX_USED,
    ROUND(SUM_TIMER_WAIT / 1e12, 2) AS total_wait_sec
FROM performance_schema.events_statements_summary_by_digest
WHERE SUM_NO_INDEX_USED > 0
   OR SUM_CREATED_TMP_DISK_TABLES > 0
ORDER BY SUM_ROWS_EXAMINED DESC
LIMIT 10;
```

The numbers that came back were significant [1]:

- Accumulated `Select_full_join`: up to **22,631,693** — joins executed without an index
- `Created_tmp_disk_tables`: over **200,000** — temporary tables spilled to disk because memory ran out

These weren't numbers from a single event. They were the result of weeks of poorly optimized queries accumulating silently, until a full scan on `history_log` tipped the system over the edge.

## The structure of `history_log` and the node with nowhere to go

```sql
SHOW CREATE TABLE history_log\G
-- Engine: InnoDB
-- Rows (approx): 1.312.847.203
-- Partitions: none
-- Indexes: PRIMARY KEY (id), KEY idx_itemid_clock (itemid, clock)

SELECT COUNT(*) FROM history_log;
-- 1312847203
```

The table had an index on `(itemid, clock)`, but the aggregation query that caused the crash didn't filter on `clock`. MySQL couldn't use the index efficiently for a `GROUP BY itemid` across the entire table — the execution plan chose a full scan, allocated temporary structures in memory, and when memory ran out, spilled everything to disk. On `mysql-node-02`, with swap already at 100%, there was no virtual disk space left: the node stopped [2].

Without date-based partitioning on `history_log`, any aggregation query over the full history is structurally dangerous. That's an architectural decision that needed to be addressed — and at the same time, not immediately. The urgent fix was on the memory parameters.

## The new values and the reasoning behind them

The intervention plan was straightforward. The per-thread parameters needed to be resized to reasonable values for the actual workload:

```ini
# my.cnf — applied changes
[mysqld]

# Per-thread buffers: from 2G down to 64M
join_buffer_size        = 64M
tmp_table_size          = 64M
max_heap_table_size     = 64M

# InnoDB redo log: increased capacity to reduce checkpoint frequency
innodb_redo_log_capacity = 8G

# InnoDB parameters kept unchanged
innodb_buffer_pool_size  = 124G   # already correctly sized for the dataset
innodb_buffer_pool_instances = 8  # unchanged
```

The decision to keep `innodb_buffer_pool_size` at 124 GB was deliberate: the buffer pool is global memory, not per-thread, and its sizing was correct relative to the active dataset size. Reducing it would have worsened I/O performance without addressing the root cause.

`join_buffer_size` at 64 MB is a standard value for mixed OLTP workloads. With 151 maximum connections, the allocation potential drops to:

```
64 MB × 151 = 9.6 GB
```

Added to the 124 GB buffer pool and OS overhead, this fits comfortably within the 157 GB available with enough headroom for spikes [3].

The `innodb_redo_log_capacity` at 8 GB (up from a lower previous value) reduces the frequency of InnoDB checkpoints, which under write-intensive workloads generate additional I/O — a secondary contributor to system pressure.

## The rolling restart and why it works on InnoDB Cluster

InnoDB Cluster with Group Replication allows nodes to be restarted in sequence without interrupting service, provided quorum is maintained [4]. With 3 nodes, one node can be taken offline at a time: the other two maintain quorum and continue serving requests.

The sequence applied, agreed on the phone with the customer's team:

```bash
# Step 1: restart mysql-node-03 (the node with minimal swap, lowest risk)
# Check cluster status before proceeding
mysqlsh -- cluster status

# On mysql-node-03: stop, update my.cnf, start
systemctl stop mysqld
# -- update /etc/my.cnf with new parameters --
systemctl start mysqld

# Wait for automatic rejoin to the cluster
# Verify: SECONDARY back ONLINE

# Step 2: restart mysql-node-02
# Step 3: restart mysql-node-01 (PRIMARY last)
# Before restarting PRIMARY: manual switchover if needed
mysqlsh -- cluster setPrimaryInstance mysql-node-02:3306
```

Restarting the PRIMARY node last is a precaution: if the PRIMARY is restarted while the other two aren't fully synchronized yet, Group Replication automatically elects a new PRIMARY — and it's cleaner to handle the switchover manually.

Total time for the operation: about 40 minutes from the first call, zero service interruptions for client applications. The store POS terminals never noticed.

## From 100% to 11%: the numbers after the fix

The swap graph in the hours following the rolling restart showed the expected curve: rapid drop on `mysql-node-01` and `mysql-node-02`, stabilizing around 10–11%.

```bash
# mysql-node-01 — 6 hours after the rolling restart
              total        used        free      shared  buff/cache   available
Mem:           157Gi       132Gi        18Gi       0.8Gi       6.2Gi        23Gi
Swap:            6Gi       672Mi       5.4Gi

# mysql-node-02
              total        used        free      shared  buff/cache   available
Mem:           157Gi       129Gi        21Gi       0.7Gi       6.8Gi        25Gi
Swap:            6Gi       614Mi       5.4Gi
```

CPU load had stabilized: the spikes tied to swap I/O were gone. `performance_schema` metrics showed a clear reduction in `Created_tmp_disk_tables` — not to zero, because some queries were still doing full scans, but the system was no longer under structural pressure.

`Select_full_join` kept accumulating: that metric requires work on queries and indexes, not just memory parameters. The cluster, though, was handling the load without saturating swap.

## What still needs to be done on `history_log`

The memory parameter fix was necessary and sufficient to stabilize the cluster in the short term. The structural root cause, though — a 1.3-billion-row table with no partitioning and no retention policy — remains open.

Recommended actions for the customer over the medium term:

**Date-based partitioning on `history_log`**

```sql
-- Target schema (to be applied with a planned migration)
ALTER TABLE history_log
    PARTITION BY RANGE (clock) (
        PARTITION p_2023 VALUES LESS THAN (UNIX_TIMESTAMP('2024-01-01')),
        PARTITION p_2024 VALUES LESS THAN (UNIX_TIMESTAMP('2025-01-01')),
        PARTITION p_2025 VALUES LESS THAN (UNIX_TIMESTAMP('2026-01-01')),
        PARTITION p_future VALUES LESS THAN MAXVALUE
    );
```

With partitioning, queries filtering on `clock` can use partition pruning and avoid a full scan of the entire table. The aggregation query that caused the crash, with a reasonable time filter, would become manageable [2].

**Active retention policy**

Define a retention window (e.g., 12 months) and implement a periodic purge procedure. On 1.3 billion rows, even a 6-month retention significantly reduces the active dataset.

**Query tuning**

Aggregation queries without a time filter on `history_log` should be treated as maintenance operations, not operational queries. They should run on dedicated replicas, during maintenance windows, with `MAX_EXECUTION_TIME` set.

```sql
-- Safe version of the offending query
SELECT /*+ MAX_EXECUTION_TIME(30000) */ itemid, MIN(clock), MAX(clock), COUNT(*)
FROM history_log
WHERE clock >= UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 30 DAY))
GROUP BY itemid;
```

## The basic rule that gets forgotten

The fix was what it was: correct diagnosis, reasonable values, rolling restart. No magic, no heroics — a call that lasted a few hours with a team that knew what they had on their hands, and a couple of outside eyes that checked the buffer math.

What stands out, looking back, is how often per-thread buffer configuration gets overlooked in favor of buffer pool sizing. `innodb_buffer_pool_size` is the parameter everyone looks at first — and rightly so, it's the most impactful one. Per-thread buffers like `join_buffer_size`, `sort_buffer_size`, and `read_buffer_size` have an insidious characteristic, though: they're allocated per connection, and their real memory impact depends on the number of concurrently active connections.

The formula is simple:

```
memory_per_thread × max_connections = maximum potential pressure
```

It needs to be calculated explicitly when sizing a MySQL server, and compared against available RAM net of the buffer pool and OS overhead. If the result exceeds physical RAM, the system is structurally fragile — not "might have issues under load," but **will have them**, when the right load comes along.

In this case, the right load was an aggregation query on a 1.3-billion-row table, on an ordinary Tuesday morning. It could have been anything else, at any other time.

## Official sources

1. MySQL 8.0 Reference Manual — [Performance Schema Statement Digests](https://dev.mysql.com/doc/refman/8.0/en/performance-schema-statement-digests.html)
2. MySQL 8.0 Reference Manual — [RANGE Partitioning](https://dev.mysql.com/doc/refman/8.0/en/partitioning-range.html)
3. MySQL 8.0 Reference Manual — [Memory Use in MySQL](https://dev.mysql.com/doc/refman/8.0/en/memory-use.html)
4. MySQL 8.0 Reference Manual — [InnoDB Cluster — Rolling Restart](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-innodb-cluster-working-with-cluster.html)

## Glossary
- **[join_buffer_size](/en/glossary/join-buffer-size/)** (MySQL) — Buffer allocated per thread for every join executed without an index. Unlike the buffer pool, it is allocated for each active connection: its total memory impact depends on the number of concurrent connections.

- **[innodb_buffer_pool_size](/en/glossary/group-replication/)** (MySQL/InnoDB) — Global parameter defining the size of InnoDB's main cache for data and indexes. The most impactful memory parameter in MySQL: typically sized at 70–80% of available RAM on dedicated servers.

- **Group Replication** (MySQL) — MySQL's built-in synchronous multi-master replication mechanism, the foundation of InnoDB Cluster. Guarantees consistency across nodes via a distributed consensus protocol; enables rolling restarts without quorum loss with 3+ nodes.

- **performance_schema** (MySQL) — System schema that collects real-time execution metrics: per-query-digest statistics, wait events, per-thread memory allocation. The foundation for performance diagnostics without external tooling.

- **rolling restart** — Sequential node restart procedure that keeps a cluster's service active throughout the operation. On a 3-node InnoDB Cluster, it allows configuration changes to be applied without downtime by restarting one node at a time while the others maintain quorum.
