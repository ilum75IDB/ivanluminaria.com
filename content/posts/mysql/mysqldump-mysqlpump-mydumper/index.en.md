---
title: "mysqldump vs mysqlpump vs mydumper: the backup that keeps you up at night"
description: "A 60 GB database, a mysqldump that took three hours and blocked writes. I tested mysqlpump and mydumper on the same environment, with real dump and restore times. Here's what I found — and why choosing a backup tool is an architectural decision, not an operational one."
date: "2026-04-14T10:00:00+01:00"
draft: false
translationKey: "mysqldump_mysqlpump_mydumper"
tags: ["backup", "mysqldump", "mydumper", "restore", "mariadb"]
categories: ["mysql"]
image: "mysqldump-mysqlpump-mydumper.cover.jpg"
---

The call came on a Friday afternoon — because these things always happen on Fridays. The DBA from a logistics client messages me on Teams: "Last night's backup took three and a half hours. This morning users found the application sluggish at 8 AM. Can we talk?"

We could talk. In fact, we should have talked about this a while ago.

The setup was a classic: MySQL 8.0 on Rocky Linux, roughly 60 GB database, a business application with about thirty InnoDB tables, four or five of which were truly large — the orders table, the warehouse movements table, the tracking history. The backup ran every night via a mysqldump launched by cron at 2:00 AM. It had worked for years. The problem was that the database had grown in the meantime.

Three hours of mysqldump means three hours of `--lock-all-tables` — or in the best case three hours of a consistent transaction with `--single-transaction` that still holds an InnoDB snapshot open the entire time. And when the dump finishes at 5:00 AM and a test restore (which nobody ever did) would have taken another four hours, the backup window simply doesn't exist anymore.

---

## The real problem: mysqldump is single-threaded

The first thing to understand about {{< glossary term="mysqldump" >}}mysqldump{{< /glossary >}} is that it does one thing at a time. One table after another, one row after another, one SQL file as output. Period.

No parallelism. No native compression. No way to say "use 4 threads and get it done faster." It's a program born in 2000 — literally — and its design reflects an era when 60 GB was an unthinkable amount for a MySQL database.

The client's dump produced a 45 GB SQL file. A single monolithic file containing every table, every stored procedure, every trigger. To restore it, you just feed that file to `mysql` — but it took four hours, because the restore is sequential too.

```bash
# The classic backup — works, but scales terribly
mysqldump --single-transaction --routines --triggers --events \
  --all-databases > /backup/full_backup.sql
```

The paradox is that mysqldump has one enormous advantage: it's everywhere. It's included in every MySQL installation, requires nothing extra, produces readable SQL. If you need to move a 500-row table between two environments, it's perfect. If you need to back up a 60 GB production database — no.

I explained to the client that we had two alternatives: mysqlpump and mydumper. Two tools with different philosophies, different limitations, and performance that on paper promises a lot but in reality needs to be tested.

---

## mysqlpump: Oracle's unkept promise

{{< glossary term="mysqlpump" >}}mysqlpump{{< /glossary >}} arrived with MySQL 5.7 as the official evolution of mysqldump. The promise was clear: parallel dumping, native compression, user management. On paper, everything mysqldump was missing.

I set it up — actually, it was already there because it's included in the MySQL distribution — and ran a first test on the client's database:

```bash
mysqlpump --single-transaction --default-parallelism=4 \
  --compress-output=zlib --all-databases > /backup/full_backup.sql.zlib
```

The result? 48 minutes for the dump, versus three and a half hours with mysqldump. A significant improvement. But then I looked closer.

mysqlpump's parallelism works at the table level: if you have 4 threads, it dumps 4 tables simultaneously. The problem is that when you have one 30 GB table and three 50 MB tables, three threads finish in thirty seconds and then a single thread drags on for forty minutes on the big table. Parallelism is only as effective as your database is balanced — and production databases are never balanced.

But the more serious problem is something else. mysqlpump with `--single-transaction` does not guarantee consistent backup across different tables. The documentation itself says so, in a note that most people don't read:

> *mysqlpump does not guarantee consistency of the dumped data across tables when using parallelism. Tables dumped in different threads may be at different points in time.*

Read that sentence again. If you use parallelism — which is the only reason to use mysqlpump — you lose the consistency guarantee across tables. In a relational database. Where tables have foreign keys between them.

For a development or test environment, it might be fine. For a production backup that you might need to restore from in a disaster? No. Absolutely not.

Another note: Oracle declared mysqlpump **deprecated in MySQL 8.0.34** and removed it in MySQL 8.4. That tells you everything about Oracle's own confidence in this tool.

---

## mydumper: the tool that delivers on its promises

{{< glossary term="mydumper" >}}mydumper{{< /glossary >}} is an open source project born in 2009 from the MySQL community — specifically from the work of Domas Mituzas, Andrew Hutchings and later maintained by Max Bubenick. It's not an Oracle tool. It's not included in the MySQL distribution. It needs to be installed separately. But it does something that neither mysqldump nor mysqlpump can: true parallelism, at the chunk level within the same table.

```bash
# Installation on Rocky Linux / CentOS
yum install https://github.com/mydumper/mydumper/releases/download/v0.16.9-1/mydumper-0.16.9-1.el8.x86_64.rpm
```

mydumper takes a large table, splits it into chunks (by default based on the primary key), and assigns each chunk to a different thread. So that 30 GB table isn't dumped by a single thread — it's broken into pieces and downloaded in parallel.

The dump I ran on the client's database:

```bash
mydumper --threads 8 --compress --trx-consistency-only \
  --outputdir /backup/mydumper_full/ \
  --logfile /var/log/mydumper.log
```

22 minutes. Versus three and a half hours with mysqldump and 48 minutes with mysqlpump.

But mydumper's real advantage isn't just dump speed — it's restore speed. mydumper produces one file per table (or per chunk), and its companion `myloader` loads them in parallel:

```bash
myloader --threads 8 --directory /backup/mydumper_full/ \
  --overwrite-tables --compress-protocol
```

The restore that would have taken four hours with mysqldump took one hour and twenty minutes with myloader. On a 60 GB database. With eight threads.

---

## The numbers: testing on a real environment

I ran the tests on the client's actual server — not on a lab environment with NVMe drives and infinite RAM. Real server, real workload, SATA drives in RAID 10.

| Operation | mysqldump | mysqlpump (4 threads) | mydumper (8 threads) |
|-----------|-----------|----------------------|---------------------|
| **Dump** | 3h 25min | 48 min | 22 min |
| **Output size** | 45 GB (SQL) | 12 GB (compressed) | 9.8 GB (compressed) |
| **Restore** | ~4h (estimated) | ~3h (estimated) | 1h 20min |
| **Cross-table consistency** | Yes | No (with parallelism) | Yes |
| **Write locks** | No* | No* | No* |

*With `--single-transaction` on InnoDB.

A few notes on the numbers:
- The mysqldump and mysqlpump restore times are estimated because I didn't run the full test in production — too risky. The times are calculated from partial tests on a subset of tables
- mydumper's compression (`--compress`) uses zstd by default, which compresses better and faster than zlib
- myloader's restore disables foreign key checks and rebuilds indexes at the end, which dramatically speeds up loading

---

## Critical options you must never forget

Whatever tool you choose, there are options you must always include. I've seen them forgotten too many times, with consequences ranging from inconvenience to disaster.

### --single-transaction

Mandatory on InnoDB. Without this option, the dump acquires locks that block writes. With `--single-transaction`, the dump uses a transaction with REPEATABLE READ isolation level to get a consistent snapshot without blocking anyone.

Watch out: this only works on InnoDB tables. If you have MyISAM tables (and yes, in 2026 I still find them), those will be locked regardless.

### --routines --triggers --events

Stored procedures, triggers and scheduled events are not included in the dump by default. You need to ask for them explicitly. I've seen restores that "worked perfectly" — except all audit triggers were missing and the application was writing data with no tracking.

### --set-gtid-purged (MySQL) or --gtid (mydumper)

If you use GTID-based replication — and you should — the dump must handle GTIDs correctly. If it doesn't, restoring on a replica generates replication conflicts that will drive you crazy.

### Restore verification

This isn't an option — it's a practice. The backup you don't verify is the backup you don't have. I have a client who ran backups every night for three years. The day they needed to restore, they discovered the file had been corrupt since the week before. Three years of backups, zero restore tests.

```bash
# Minimal verification with mydumper: restore on test instance
myloader --threads 4 --directory /backup/mydumper_full/ \
  --host test-mysql-server --overwrite-tables

# Count rows from main tables
mysql -h test-mysql-server -e "
  SELECT table_name, table_rows
  FROM information_schema.tables
  WHERE table_schema = 'production_db'
  ORDER BY table_rows DESC LIMIT 10;"
```

---

## When to use what

After thirty years of databases, my rule is simple:

**mysqldump** — for databases under 5 GB, one-off migrations, single table dumps, development environments where speed isn't critical. It's the Swiss army knife: does everything, slowly, but it does it.

**mysqlpump** — I don't recommend it anymore. Deprecated by Oracle, no consistency guarantee with parallelism, and mydumper does everything mysqlpump promised but better. If you're using it, plan the migration to mydumper.

**mydumper/myloader** — for any production database over 10 GB. True parallelism, guaranteed consistency, fast restores. Requires a separate installation, but the time you save on the first backup more than pays for it.

---

## The complete strategy: not just logical backup

Something I always tell clients: logical backup (mysqldump, mydumper) is **one** component of the strategy, not the entire strategy.

For the logistics client we set up this scheme:

1. **mydumper every night** — full logical backup, 8 threads, zstd compression, 7-day retention
2. **Continuous binary log** — with `binlog_expire_logs_seconds` set to 7 days, for {{< glossary term="pitr" >}}point-in-time recovery{{< /glossary >}}
3. **Weekly Percona XtraBackup** — hot physical backup, for the fastest possible restore in case of total disaster
4. **Automated restore test** — a script that every Sunday restores the mydumper backup on a test instance and verifies row counts

Logical backup is convenient because it's portable — you can restore on any MySQL version, on any architecture. But for a 60 GB database, a physical backup with XtraBackup lets you restore in 15-20 minutes instead of an hour and a half. When the production database is down and the phone is ringing, that hour of difference matters.

The following Friday, the client's DBA messaged me on Teams again. But this time the message was different: "Backup finished in 23 minutes. No impact on users. Thanks."

You're welcome. But next time, don't wait until the backup takes three hours to ask for help.

------------------------------------------------------------------------

## Glossary

**[mysqldump](/en/glossary/mysqldump/)** — Logical backup utility included in every MySQL installation. Produces a sequential SQL file with all the statements needed to recreate schema and data. Single-threaded, reliable but slow on large databases.

**[mysqlpump](/en/glossary/mysqlpump/)** — Evolution of mysqldump introduced in MySQL 5.7, with support for table-level parallelism and native compression. Deprecated by Oracle in MySQL 8.0.34 due to consistency issues.

**[mydumper](/en/glossary/mydumper/)** — Open source logical backup tool for MySQL/MariaDB with true chunk-level parallelism. Splits large tables into pieces and exports them with multiple threads, with parallel restore via myloader.

**[PITR](/en/glossary/pitr/)** — Point-in-Time Recovery: a technique that combines a full backup with binary logs to bring the database to any specific point in time, not just the backup time.

**[GTID](/en/glossary/gtid/)** — Global Transaction Identifier: a unique identifier assigned to every transaction in MySQL, which simplifies replication management and transaction tracking between master and replica.
