---
title: "mysqlpump"
description: "Evolution of mysqldump introduced in MySQL 5.7 with table-level parallelism, deprecated by Oracle in MySQL 8.0.34."
translationKey: "glossary_mysqlpump"
aka: "MySQL pump"
articles:
  - "/posts/mysql/mysqldump-mysqlpump-mydumper"
---

**mysqlpump** is the logical backup utility introduced by Oracle in MySQL 5.7 as an evolution of mysqldump. The main difference is support for table-level parallelism and native output compression (zlib, lz4, zstd).

## How it works

mysqlpump can dump multiple tables simultaneously using parallel threads, configurable via `--default-parallelism`. Compression is applied directly during the dump without needing external pipes to gzip. It also supports selective dumping of MySQL users and accounts.

However, the parallelism operates only at the whole-table level: if a single table is much larger than the others, one thread drags on alone while the rest have already finished.

## The consistency problem

With parallelism enabled, mysqlpump does not guarantee consistency across different tables — tables exported by different threads may reflect different points in time. This is a critical limitation for production backups on relational databases with foreign keys.

## Current status

Oracle declared mysqlpump deprecated in MySQL 8.0.34 and removed it entirely in MySQL 8.4. For those seeking parallelism in logical backup, mydumper is the recommended alternative.
