---
title: "Relay log"
description: "The relay log is the slave's local copy of the master's binlog in MySQL replication: the IO thread writes it, the SQL thread reads it to apply transactions."
translationKey: "glossary_relay_log"
aka: null
articles:
  - "/posts/mysql/replica-mysql-quando-lo-slave-resta-indietro-e-nessuno-se-ne-accorge"
---

The relay log is the binary file that a MySQL slave maintains locally as a copy of the events received from the master. It acts as a buffer between event reception and their actual application on the database: two separate threads handle each phase, and the relay log is the handoff point between them.

## How it works

MySQL replication on the slave relies on two independent threads:

- **IO thread**: connects to the master, reads the binlog, and writes events into the local relay log.
- **SQL thread**: reads the relay log and applies events (INSERT, UPDATE, DELETE, DDL) to the slave database.

This decoupling allows the slave to keep receiving events even when the SQL thread falls behind. Relay log files follow a naming convention such as `hostname-relay-bin.000001` and are rotated automatically.

```sql
-- Check relay log status on the slave
SHOW SLAVE STATUS\G
-- Relevant fields:
-- Relay_Log_File: current file being read by the SQL thread
-- Relay_Log_Pos: current position
-- Relay_Master_Log_File: corresponding master binlog file
-- Exec_Master_Log_Pos: position applied on the master
```

## Operational context

The relay log is central to diagnosing replication lag. When `Seconds_Behind_Master` grows, the relay log accumulates events not yet applied: the IO thread is ahead of the SQL thread. Monitoring relay log file sizes and the gap between `Read_Master_Log_Pos` and `Exec_Master_Log_Pos` helps pinpoint the bottleneck.

After a slave crash, MySQL uses the `relay-log.info` file to resume from the last applied position. With `relay_log_recovery = ON`, the relay log is regenerated from the master on restart, reducing the risk of corruption.
