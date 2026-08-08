---
categories:
- mysql
date: '2026-08-08'
description: 'A real MySQL 8.0.34→8.0.45 patching workflow: broken views blocking
  mysqldump, GTID warnings, replica role check, and RPM upgrade order on RHEL 8.'
draft: false
image: articolo-mysql-patching-mysql-8-0-dal-backup-alla-verifica-passo-per-passo.cover.jpg
seoTitle: 'MySQL 8.0 upgrade on RHEL 8: broken views, GTID, replica check'
tags:
- mysql
- upgrade
- mysqldump
- gtid
- replication
title: The ticket said 'update MySQL and shut down the service'
translationKey: articolo_mysql_patching_mysql_8_0_dal_backup_alla_verifica_passo_per_passo
webo_generated_at: 2026-08-08
webo_status: scheduled
---

## The ticket said "update MySQL and shut down the service"

The ticket arrived in the morning: update MySQL Community from 8.0.34 to 8.0.45 on an RHEL 8.3 server, then shut down the application service for a maintenance window. Four lines, no details.

"Looks simple" is the most dangerous phrase a DBA can think before touching a production system. Every time we've trusted that feeling, something unexpected turned up. This time was no different: broken views blocking the dump, GTID enabled, a configured-but-stopped replica that nobody could explain. Nothing dramatic — all manageable, as long as you handle things in the right order.

What follows is the real workflow, with the queries used and the errors encountered. Not the official MySQL documentation — that's on `dev.mysql.com` and everyone knows it. This is the field.

---

## How much space does this database actually take?

Before doing anything, understand what you're dealing with. The database in question was small — roughly 135 MB, 58 tables, a single application schema — and "small" doesn't mean "no surprises."

The `information_schema` queries I always run as a first step:

```sql
-- Total schema size
SELECT
    table_schema                                    AS schema_name,
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS size_mb,
    COUNT(*)                                        AS table_count
FROM information_schema.tables
WHERE table_schema NOT IN ('mysql','information_schema','performance_schema','sys')
GROUP BY table_schema
ORDER BY size_mb DESC;
```

```sql
-- Largest tables, with row estimate and reclaimable space
SELECT
    table_name,
    ROUND((data_length + index_length) / 1024 / 1024, 2) AS size_mb,
    table_rows                                            AS estimated_rows,
    data_free / 1024 / 1024                               AS free_mb
FROM information_schema.tables
WHERE table_schema = 'app_monitoring'
ORDER BY (data_length + index_length) DESC
LIMIT 10;
```

In this case the three largest tables were all monitoring tables: `event_log` (~43 MB, ~500K rows), `metric_snapshot` (~41 MB, ~320K rows), `alert_history` (~28 MB, ~290K rows). No BLOBs, no large TEXT columns — the dump was going to be fast.

I also check for BLOB or MEDIUMBLOB columns that could inflate timing:

```sql
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'app_monitoring'
  AND data_type IN ('blob','mediumblob','longblob','text','mediumtext','longtext')
ORDER BY table_name;
```

Zero results. Good. On to the backup.

---

## mysqldump stalls: error 1356 and the broken views

I launch the dump. Thirty seconds of silence, then:

```text
mysqldump: Got error: 1356: View 'app_monitoring.v_active_alerts' references
invalid table(s) or column(s) or function(s) or definer/invoker of view
lack rights to use them when using LOCK TABLES
```

The dump stopped on a view. It's not uncommon: someone modifies an underlying table — renames a column, drops it, changes its type — and the view referencing it becomes invalid without anyone noticing until a dump or a direct query against that view is attempted.

The first step is to map all invalid views in the schema. Not just the ones that return an explicit 1356 error — also those with `last_altered` or `created` NULL in `information_schema`, which often indicate corrupted or non-compilable objects [1]:

```sql
-- View metadata: definer, security_type, updatability
SELECT
    table_name     AS view_name,
    definer,
    security_type,
    is_updatable,
    check_option
FROM information_schema.views
WHERE table_schema = 'app_monitoring'
ORDER BY table_name;
```

```sql
-- Direct listing: views to iterate with SELECT * LIMIT 1 on each
-- (useful in a script for large schemas)
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'app_monitoring'
  AND table_type = 'VIEW';
```

In this case I found 6 problematic views: 2 with an explicit 1356 error, 4 with `created` NULL in `information_schema` — a sign that MySQL couldn't compile them at query time.

The strategy is to exclude them from the main dump and save only their DDL separately using `--force`, so their definitions aren't lost:

```bash
# Main dump without the broken views
mysqldump \
  --single-transaction \
  --routines \
  --triggers \
  --events \
  --ignore-table=app_monitoring.v_active_alerts \
  --ignore-table=app_monitoring.v_alert_summary \
  --ignore-table=app_monitoring.v_metric_daily \
  --ignore-table=app_monitoring.v_metric_hourly \
  --ignore-table=app_monitoring.v_event_open \
  --ignore-table=app_monitoring.v_event_closed \
  app_monitoring > /backup/app_monitoring_$(date +%Y%m%d_%H%M).sql

# DDL of the broken views (structure only, --force to avoid blocking)
mysqldump \
  --no-data \
  --force \
  app_monitoring \
  v_active_alerts v_alert_summary v_metric_daily \
  v_metric_hourly v_event_open v_event_closed \
  > /backup/app_monitoring_broken_views_$(date +%Y%m%d_%H%M).sql
```

The second dump with `--force` produces the DDL for the views even when they're invalid — useful for recreating them later, once the underlying tables are fixed. It doesn't solve the broken view problem, but at least there's a record of what was there.

---

## The GTID warning and when to use `--set-gtid-purged=OFF`

During the main dump, this warning appears:

```text
Warning: A partial dump from a server that has GTIDs will by default include
the GTIDs of all transactions, even those that changed suppressed parts of
the database. If you don't want to restore the GTIDs, pass
--set-gtid-purged=OFF. To make a complete dump, pass --all-databases
--triggers --routines --events.
```

GTIDs — *Global Transaction Identifiers* — are unique identifiers that MySQL assigns to every transaction when `gtid_mode=ON` [2]. They exist primarily for replication: each server tracks which GTIDs it has already executed, and replication uses that information to know where to resume.

The warning says: you're doing a partial dump (one schema, not `--all-databases`), and the dump will still include the full GTID set for the entire server. If you then import this dump onto another server, that server will think it has already executed all those transactions — a condition that can break a freshly configured replica.

In this case the dump is purely a pre-upgrade backup, not for replicating to another server. Adding `--set-gtid-purged=OFF`:

```bash
mysqldump \
  --single-transaction \
  --routines \
  --triggers \
  --events \
  --set-gtid-purged=OFF \
  --ignore-table=app_monitoring.v_active_alerts \
  [... other --ignore-table flags ...] \
  app_monitoring > /backup/app_monitoring_$(date +%Y%m%d_%H%M).sql
```

Practical rule: if the dump is for backup/restore on the same server or a standalone server, `--set-gtid-purged=OFF` is almost always the right call. If you're building a replica or doing point-in-time recovery on a GTID-enabled server, the situation is more involved — a topic for another article.

---

## Before shutting down: is this server a primary, a replica, or standalone?

Backup done. Now comes the step many people skip: understanding the server's role in the cluster before shutting it down.

Shutting down a primary without promoting a replica causes downtime. Shutting down a Galera node without checking quorum can corrupt the cluster. Even here, where the server appeared to be standalone, the check is mandatory.

Queries to run in order:

```sql
-- 1. Replica status (if this server replicates from someone)
SHOW REPLICA STATUS\G
```

```sql
-- 2. Source status (if this server has replicas)
SHOW BINARY LOG STATUS\G
SHOW REPLICAS\G
```

```sql
-- 3. Group Replication or InnoDB Cluster
SELECT * FROM performance_schema.replication_group_members;
```

```sql
-- 4. Key parameters
SHOW VARIABLES LIKE 'server_id';
SHOW VARIABLES LIKE 'read_only';
SHOW VARIABLES LIKE 'gtid_mode';
SHOW VARIABLES LIKE 'group_replication%';
```

Result in this case: `SHOW REPLICA STATUS` returns one row with `Replica_IO_Running: No` and `Replica_SQL_Running: No` — the replica had been configured but stopped a long time ago. `SHOW REPLICAS` returns zero rows. `replication_group_members` is empty. `server_id=1`, `read_only=OFF`.

Effectively a standalone server with the leftovers of a replication configuration that was never completed or had been abandoned. No risk of cascading downtime. We proceed.

---

## The RPM upgrade: all packages, in the right order

Stop the service:

```bash
systemctl stop mysqld
systemctl status mysqld   # confirm it's actually stopped
```

The most common mistake at this stage is upgrading only `mysql-community-server` and forgetting the dependent packages. On RHEL 8 with the MySQL Community repos, the packages to upgrade together are [3]:

```bash
# Check current version
rpm -qa | grep mysql | sort

# Upgrade all MySQL packages in one shot
dnf upgrade \
  mysql-community-server \
  mysql-community-client \
  mysql-community-libs \
  mysql-community-common \
  mysql-community-client-plugins \
  mysql-community-icu-data-files
```

Upgrading only `mysql-community-server` while leaving `mysql-community-libs` at the previous version produces linking errors on restart that aren't immediately obvious to diagnose. Better to upgrade everything together.

Restart and verify:

```bash
systemctl start mysqld
systemctl status mysqld

# Check version
mysql -u root -p -e "SELECT VERSION();"
```

```text
+-----------+
| VERSION() |
+-----------+
| 8.0.45    |
+-----------+
```

In MySQL 8.0, the internal schema upgrade — which in older versions required running `mysql_upgrade` manually — is automatic on first startup [4]. The server runs the necessary migrations and writes to the log:

```text
[System] [MY-013381] [Server] Server upgrade from '80034' to '80045' started.
[System] [MY-013381] [Server] Server upgrade from '80034' to '80045' completed.
```

If those two lines don't appear, something didn't go as expected. Always verify:

```bash
grep -i "upgrade" /var/log/mysqld.log | tail -5
```

---

## Post-upgrade checks: the fact that it started isn't enough

The server is up and showing the correct version. Not done yet.

```sql
-- Check system tables
CHECK TABLE mysql.user;
CHECK TABLE mysql.db;

-- Verify application tables are accessible
SELECT COUNT(*) FROM app_monitoring.event_log;
SELECT COUNT(*) FROM app_monitoring.metric_snapshot;

-- Check critical variables post-upgrade
SHOW VARIABLES LIKE 'gtid_mode';
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
SHOW VARIABLES LIKE 'max_connections';
```

The broken views existed before the upgrade and remain broken after — the upgrade doesn't fix them, obviously. They need to be addressed separately, once the application team has clarified which underlying tables changed and how.

One final check on the log for silent errors:

```bash
grep -i "error\|warning\|corrupt" /var/log/mysqld.log | grep -v "^#" | tail -20
```

In this case, all clean. Patching complete.

---

## A four-line ticket doesn't capture the complexity of the work

MySQL patching isn't complicated. The commands are few and the official documentation is solid. The hard part isn't executing the steps — it's knowing which questions to ask before you start.

How large is the database? Are there invalid objects? Does this server have a role in the cluster? Are GTIDs enabled and what does that mean for the dump? Every skipped question is a risk that materializes at the worst possible moment: during the maintenance window, with someone waiting.

The difference between a junior and a senior approach isn't in the commands — it's in the time spent before running them. The `information_schema` queries, the replica check, the post-upgrade log verification: all steps that seem redundant until they aren't.

The broken views in this case were already broken before the patching. The upgrade didn't create them — it just made them visible because someone tried to run a dump for the first time in months. That's the kind of discovery that pays back the time invested in a thorough pre-backup analysis: not to block the patching, but to avoid being caught off guard halfway through.

---

## Official sources

1. MySQL 8.0 Reference Manual — [INFORMATION_SCHEMA VIEWS Table](https://dev.mysql.com/doc/refman/8.0/en/information-schema-views-table.html)
2. MySQL 8.0 Reference Manual — [Replication with Global Transaction Identifiers](https://dev.mysql.com/doc/refman/8.0/en/replication-gtids.html)
3. MySQL 8.0 Reference Manual — [Installing MySQL on Linux Using the MySQL Yum Repository](https://dev.mysql.com/doc/refman/8.0/en/linux-installation-yum-repo.html)
4. MySQL 8.0 Reference Manual — [Upgrading MySQL](https://dev.mysql.com/doc/refman/8.0/en/upgrading.html)

---

## Glossary candidate

- **GTID** (MySQL) — *Global Transaction Identifier*: a unique identifier assigned to every transaction when `gtid_mode=ON`. Composed of `server_uuid:sequence_number`, it allows replication to track exactly which transactions have already been applied, independently of the binlog position.

- **mysqldump** — logical backup utility bundled with MySQL. Produces a SQL file with `CREATE` and `INSERT` statements to recreate the database. Suitable for small to medium-sized databases; for high volumes, tools like mydumper or physical backups with xtrabackup are preferred.

- **Invalid view** (MySQL) — a view whose SQL body references objects that no longer exist or are not accessible (renamed tables, dropped columns, revoked permissions). MySQL does not automatically invalidate views when the underlying table changes: the error surfaces only on first execution or during a dump.

- **`--single-transaction`** (mysqldump) — flag that opens a `REPEATABLE READ` transaction before the dump, guaranteeing consistency without acquiring locks on InnoDB tables. Not applicable to MyISAM tables, which require `--lock-tables`.

- **`replication_group_members`** (MySQL Performance Schema) — system table listing the active nodes in a Group Replication cluster, with state (`ONLINE`, `RECOVERING`, `UNREACHABLE`) and role (`PRIMARY`, `SECONDARY`). Empty on standalone servers or those using traditional replication.
