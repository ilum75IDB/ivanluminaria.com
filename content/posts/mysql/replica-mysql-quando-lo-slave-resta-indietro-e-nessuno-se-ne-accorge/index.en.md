---
categories:
- mysql
date: 2099-12-31
description: Four hours of lag on a MySQL replica in a logistics system. How we diagnosed
  it, why Seconds_Behind_Master lies, and what actually fixed it.
draft: true
image: replica-mysql-quando-lo-slave-resta-indietro-e-nessuno-se-ne-accorge.cover.jpg
seoTitle: 'MySQL replica lag: GTID, parallel replication, pt-heartbeat'
tags:
- mysql
- replication
- gtid
- performance
- monitoring
title: 'The Monday morning report: four hours of MySQL replica lag'
translationKey: replica_mysql_quando_lo_slave_resta_indietro_e_nessuno_se_ne_accorge
webo_generated_at: 2026-08-08
webo_status: da_tradurre
---

## The Monday morning report

It was a Monday morning. The commercial manager of a large national postal and logistics operator had just opened the weekly shipment report and was staring at numbers that didn't add up. Friday afternoon deliveries were still showing as "in transit". Saturday's KPIs were at zero. Something was wrong, and the first hypothesis was a bug in the reporting application.

When we got in to look, there was no bug. There was something more subtle: the MySQL replica that ran all the reporting queries had accumulated four hours of lag behind the master. The data was there, correct, on the master — but the replica was still applying it hours behind. And no alert had fired.

Four hours of lag in a logistics system means operational decisions made on wrong numbers. It means the warehouse manager planned weekend shifts on data that didn't reflect reality. It means the urgent shipment prioritization system was working from a snapshot half a working day old.

This article explains how MySQL replication works under the hood, why its main monitoring tool is unreliable, and what we did to fix it — no magic, just profiling and a few architectural decisions.

---

## Binlog, relay log, and the two threads that don't talk enough

To understand why replication accumulates lag, you need to understand how it actually works. MySQL asynchronous replication relies on three main components: the **binary log** on the master, the **relay log** on the slave, and two threads that work in sequence.

The **IO thread** on the slave connects to the master and reads events from the binlog, writing them locally to the relay log. It's a sequential read, generally fast, rarely the bottleneck.

The **SQL thread** reads the relay log and applies events to the slave's local database. This is where the problem lies: in classic configuration, this thread is **single-threaded**. It applies one event at a time, in sequence. If the master has ten sessions writing in parallel, the slave applies them one after another.

```text
MASTER
  ├── session 1 → INSERT INTO spedizioni (...)
  ├── session 2 → UPDATE tracking SET stato = 'consegnato' WHERE ...
  ├── session 3 → INSERT INTO eventi_logistici (...)
  └── ... (N parallel sessions)
         │
         ▼ binlog (serialized)
SLAVE IO thread → relay log → SQL thread (single-threaded)
         ▼
  applies event 1, then event 2, then event 3...
```

The master writes in parallel, the slave applies in series. On a system under sustained load, this asymmetry is the primary cause of lag.

---

## Why Seconds_Behind_Master lies

The first thing you look at when you suspect lag is `SHOW SLAVE STATUS\G`. The `Seconds_Behind_Master` field looks like exactly what you need. It isn't.

```sql
SHOW SLAVE STATUS\G
-- ...
Seconds_Behind_Master: 14523
-- ...
```

Fourteen thousand seconds. Four hours. The number was there — but the problem is that this value is calculated in a way that makes it unreliable in several common scenarios.

`Seconds_Behind_Master` measures the difference between the timestamp of the event the SQL thread is **currently applying** and the current system time. If the SQL thread is stalled — because it's blocked on a lock, because it hit an error, because the relay log is exhausted and the IO thread hasn't received new events yet — the value stops updating or behaves unpredictably.

Even more insidious: if replication stops and then restarts, `Seconds_Behind_Master` can drop back to zero before the lag has actually been caught up, because the IO thread has flushed the relay log but the SQL thread hasn't finished applying it. The field reflects the SQL thread's state, not the real delay behind the master.

In practice, `Seconds_Behind_Master` is useful as a rough indicator, but not as a basis for alerting. [1]

**What to use instead**: with **GTID-based replication** enabled, you can calculate the real lag by comparing the set of transactions executed on the master (`gtid_executed` on the master) with those applied on the slave (`gtid_executed` on the slave). The difference — the number of pending transactions — is a far more reliable metric.

```sql
-- On the master
SELECT @@global.gtid_executed;

-- On the slave
SELECT @@global.gtid_executed;
-- The difference between the two sets is the real lag in transaction terms
```

With tools like Percona Toolkit's `pt-heartbeat`, you can measure lag even more precisely: the tool writes a timestamp to the master at regular intervals and measures how long it takes to appear on the slave. [2]

---

## The most common causes of slave lag

In this specific case, we identified three concurrent causes.

**1. Heavy unoptimized queries on the master**

The master ran a nightly bulk update: `UPDATE spedizioni SET stato_elaborazione = 'archiviato' WHERE data_spedizione < DATE_SUB(NOW(), INTERVAL 90 DAY)`. No index on `data_spedizione`. The query did a full table scan on a 180-million-row table, produced a single enormous binlog event, and the slave took 40 minutes to apply it — during which it applied nothing else.

**2. Single-threaded SQL thread under sustained load**

During peak hours (2 pm to 6 pm), the master received around 800 writes/second spread across dozens of parallel sessions. The SQL thread couldn't keep up: every hour of intense production added roughly 20–30 minutes of accumulated lag.

**3. Slow I/O on the slave**

The slave was on shared storage with other services. During peak hours, write latency climbed to levels that further slowed event application. The relay log was being written and read with latencies that multiplied the single-thread problem.

---

## GTID: why it's worth migrating now

The **Global Transaction ID** (GTID) is a unique identifier assigned to every transaction committed on the master. [3] Each transaction has a GTID in the format `source_id:transaction_id`, where `source_id` is the UUID of the master server.

```sql
-- Enable GTID on the master (requires restart or SET PERSIST on MySQL 8.0+)
SET PERSIST gtid_mode = ON;
SET PERSIST enforce_gtid_consistency = ON;

-- Verify the status
SHOW VARIABLES LIKE 'gtid_mode';
-- gtid_mode | ON
```

The advantages over binlog position-based replication are concrete:

- **Simpler failover**: with GTID, a new slave knows exactly where to resume without having to manually calculate the position in the binlog
- **Real lag monitoring**: as described above, comparing GTID sets is far more reliable than `Seconds_Behind_Master`
- **Missing transaction detection**: if a transaction was applied on the master but not on the slave, the gap is immediately visible in the GTID set

In the context of this project, the migration to GTID had already been planned but not yet executed. Having completed it before tackling the lag problem would have made diagnosis significantly faster.

---

## From single-thread to parallel replication

The solution to the SQL thread bottleneck is **parallel replication**, available in MySQL 5.7+ and MariaDB 10.0+. [4]

The basic idea: instead of applying events sequentially with a single thread, multiple worker threads apply transactions in parallel — while respecting consistency constraints.

MySQL offers two parallelization modes:

- **`DATABASE`**: transactions modifying different databases are applied in parallel. Simple, but useless if all writes go to the same database.
- **`LOGICAL_CLOCK`** (the right mode for most cases): uses commit timestamp information in the binlog to identify transactions that were executing concurrently on the master and can therefore be applied in parallel on the slave.

```sql
-- Configuration on the slave
STOP SLAVE SQL_THREAD;

SET GLOBAL slave_parallel_type = 'LOGICAL_CLOCK';
SET GLOBAL slave_parallel_workers = 8;
SET GLOBAL slave_preserve_commit_order = ON;

START SLAVE SQL_THREAD;
```

The `slave_preserve_commit_order = ON` parameter ensures that transactions are committed on the slave in the same order they were on the master — essential for read consistency. [4]

To get the most out of `LOGICAL_CLOCK`, the master should have `binlog_group_commit_sync_delay` configured to group more transactions into the same commit group. This slightly increases commit latency on the master, but significantly increases the parallelism available on the slave.

```sql
-- On the master: increase the group commit window
-- (value in microseconds, 1000 = 1ms)
SET GLOBAL binlog_group_commit_sync_delay = 1000;
SET GLOBAL binlog_group_commit_sync_no_delay_count = 10;
```

---

## What actually worked

We worked on three fronts in parallel, and the end result was a lag reduction from four hours to under thirty seconds under normal conditions.

**Front 1: parallel replication with 8 workers**

After enabling `LOGICAL_CLOCK` with 8 worker threads, the slave's throughput increased significantly. The accumulated lag dropped within a few hours. The customer's DBA had already evaluated this option previously but had run into internal resistance because "it had worked this way for years" — the crisis unblocked the conversation.

**Front 2: batch query optimization**

The nightly archival query was rewritten to operate in smaller batches, with an index added on `data_spedizione`:

```sql
-- Before: one enormous UPDATE
UPDATE spedizioni
SET stato_elaborazione = 'archiviato'
WHERE data_spedizione < DATE_SUB(NOW(), INTERVAL 90 DAY);

-- After: batches of 10,000 rows with a pause between each
-- (run by a Python script with loop + sleep)
UPDATE spedizioni
SET stato_elaborazione = 'archiviato'
WHERE data_spedizione < DATE_SUB(NOW(), INTERVAL 90 DAY)
  AND stato_elaborazione != 'archiviato'
LIMIT 10000;
```

```sql
-- Index added
ALTER TABLE spedizioni
ADD INDEX idx_data_elaborazione (data_spedizione, stato_elaborazione);
```

This eliminated the nightly lag spike: instead of a single 40-minute event, the slave applied thousands of small events spread over an hour, without ever stalling.

**Front 3: dedicated storage for the slave**

The slave was moved to dedicated storage with consistent write latencies. This alone wouldn't have solved the problem, but it eliminated the variability that made lag unpredictable during peak hours.

---

## Monitoring that doesn't lie

After resolving the lag, we built an alerting system that didn't rely on `Seconds_Behind_Master`.

The solution we adopted was Percona Toolkit's `pt-heartbeat`, configured to write a timestamp to the master every second and measure the delay on the slave:

```bash
# On the master: start the daemon that writes the heartbeat
pt-heartbeat \
  --user=monitor_user \
  --password=*** \
  --host=mysql-master-01 \
  --database=monitoring \
  --create-table \
  --daemonize \
  --update

# On the slave: measure the real lag
pt-heartbeat \
  --user=monitor_user \
  --password=*** \
  --host=mysql-replica-01 \
  --database=monitoring \
  --monitor \
  --master-server-id=1
```

The value returned by `pt-heartbeat --monitor` is the real lag in seconds, calculated from actual timestamps — not from binlog position or `Seconds_Behind_Master`.

We configured alerts on two thresholds:

- **Warning at 60 seconds**: notification to the team, no automatic action
- **Critical at 300 seconds (5 minutes)**: urgent notification + automatic blocking of reporting queries (temporary redirect to the master with read-only queries)

The automatic blocking was the most delicate part: better to return an explicit error to the user ("data temporarily unavailable, please try again in a few minutes") than to silently return data that's hours old.

---

## Four hours become thirty seconds

The four-hour lag was the visible symptom of three overlapping problems: single-thread architecture, an unoptimized batch query, shared storage. None of the three, on its own, would have caused four hours of delay — together, they amplified each other.

The most interesting part of this story isn't technical: it's that the problem had probably existed for months, and nobody had noticed because `Seconds_Behind_Master` wasn't being monitored systematically, and when it was checked manually it showed values that looked reasonable during low-activity hours.

Replica lag monitoring is not a nice-to-have. It's an operational metric that directly impacts the quality of the data the business uses to make decisions. If reporting queries run on a replica, the lag on that replica is an integral part of data quality — and should be treated as such, with alerts, thresholds, and a response plan.

`Seconds_Behind_Master` is a starting point, not an answer. `pt-heartbeat` or comparing GTID sets are far more reliable tools. And parallel replication, on MySQL 5.7+ with `LOGICAL_CLOCK`, is today the sensible default configuration for any replica under sustained load.

---

## Official sources

1. MySQL 8.0 Reference Manual — [Replication Slave Status Variables: Seconds_Behind_Master](https://dev.mysql.com/doc/refman/8.0/en/show-replica-status.html)
2. Percona Toolkit Documentation — [pt-heartbeat](https://docs.percona.com/percona-toolkit/pt-heartbeat.html)
3. MySQL 8.0 Reference Manual — [GTID-Based Replication](https://dev.mysql.com/doc/refman/8.0/en/replication-gtids.html)
4. MySQL 8.0 Reference Manual — [Replication with Multithreaded Appliers](https://dev.mysql.com/doc/refman/8.0/en/replication-threads-applier.html)

---

## Glossary
- **[Binlog](/en/glossary/binlog/)** (MySQL binary log) — sequential log of all data modifications on the MySQL master. The foundation of replication: the slave reads the binlog to know what to apply. Format: ROW, STATEMENT, or MIXED.

- **[Relay log](/en/glossary/gtid/)** — local copy of the master's binlog, written by the IO thread on the slave. The SQL thread reads the relay log to apply transactions. It's the buffer between event reception and application.

- **GTID** (Global Transaction Identifier) — unique identifier assigned to every transaction committed on a MySQL server. Format: `source_uuid:transaction_id`. Enables simplified failover and precise replica lag monitoring.

- **Parallel replication** — replication event application mode that uses multiple worker threads instead of a single SQL thread. In MySQL, `LOGICAL_CLOCK` mode identifies transactions that can be applied in parallel based on commit timestamps in the binlog.

- **pt-heartbeat** — Percona Toolkit tool that measures MySQL replica lag by writing timestamps to the master and comparing them with values read on the slave. More reliable than `Seconds_Behind_Master` for production alerting.
