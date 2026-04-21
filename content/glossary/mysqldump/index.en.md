---
title: "mysqldump"
description: "Logical backup utility included in every MySQL installation, producing a sequential SQL file to recreate schema and data."
translationKey: "glossary_mysqldump"
aka: "MySQL dump"
articles:
  - "/posts/mysql/mysqldump-mysqlpump-mydumper"
  - "/posts/mysql/mysql-pre-upgrade-assessment"
---

**mysqldump** is the logical backup utility included by default in every MySQL and MariaDB installation. It produces an SQL file containing all the statements (CREATE TABLE, INSERT) needed to fully rebuild a database's schema and data.

## How it works

mysqldump connects to the MySQL server and reads tables one at a time, generating the corresponding SQL statements as output. The operation is strictly single-threaded: one table after another, one row after another. The output file can be compressed externally (gzip, zstd) but the tool itself offers no native compression.

With the `--single-transaction` option, the dump runs within a transaction at REPEATABLE READ isolation level, which guarantees a consistent snapshot on InnoDB tables without acquiring write locks.

## What it's for

mysqldump is the standard tool for:

- Logical backup of small to medium databases
- Migrations between different MySQL versions
- Exporting individual tables or databases for transfer between environments
- Creating human-readable, inspectable dumps

## When it becomes a problem

On databases over 10-15 GB, the single-threaded dump becomes a bottleneck. A 60 GB database can require 3-4 hours for the dump and as many for the restore. The lack of parallelism is the structural limitation: there's no way to speed up the process other than switching to tools like mydumper.
