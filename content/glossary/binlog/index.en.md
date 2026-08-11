---
title: "Binlog"
description: "MySQL's Binary Log sequentially records every data change on the master: it is the foundation of master-slave replication and CDC pipelines."
translationKey: "glossary_binlog"
aka: "Binary Log"
articles:
  - "/posts/mysql/mysql-slave-lag-parallel-replication"
---

The Binlog (Binary Log) is the sequential log that MySQL maintains on the master to track every operation that modifies data. The slave reads it to know exactly what to replicate and in what order. Without the Binlog there is no replication, and without replication there is no high availability or disaster recovery on MySQL.

## How it works

Every COMMIT writes one or more events to the Binlog, depending on the format in use:

- **ROW**: records the actual rows changed (before/after image). More verbose, but fully deterministic.
- **STATEMENT**: records the SQL query as text. Compact, but non-deterministic functions (`NOW()`, `UUID()`) can cause divergence between master and slave.
- **MIXED**: MySQL automatically picks ROW or STATEMENT on a per-statement basis.

```sql
-- Check the active format
SHOW VARIABLES LIKE 'binlog_format';

-- Inspect events in a specific binlog file
SHOW BINLOG EVENTS IN 'mysql-bin.000042' LIMIT 20;
```

The slave tracks its current position in the Binlog via file name and offset (classic replication) or via GTID (Global Transaction Identifier), which makes failover significantly easier to manage.

## When it matters

The Binlog is active whenever replication is enabled, but it is also consumed by CDC tools such as Debezium to capture changes and feed streaming pipelines. It requires monitoring: a Binlog growing without being consumed by the slave is a direct indicator of replication lag. Retention is controlled via `binlog_expire_logs_seconds` (MySQL 8) or `expire_logs_days` (older versions).
