---
title: "mydumper"
description: "Open source logical backup tool for MySQL/MariaDB with true chunk-level parallelism, with parallel restore via myloader."
translationKey: "glossary_mydumper"
aka: "myloader"
articles:
  - "/posts/mysql/mysqldump-mysqlpump-mydumper"
  - "/posts/mysql/mysql-pre-upgrade-assessment"
---

**mydumper** is an open source logical backup tool for MySQL and MariaDB that implements true parallelism: not just across different tables, but also within the same table, splitting it into chunks based on the primary key.

## How it works

mydumper connects to the MySQL server, acquires a consistent snapshot with `FLUSH TABLES WITH READ LOCK` (or `--trx-consistency-only` to avoid global locks on InnoDB), then distributes the work among multiple threads. Each large table is broken into chunks — by default based on primary key ranges — and each chunk is exported by a separate thread.

The output is not a single SQL file but a directory with one file per table (or per chunk), plus metadata, schema, and stored procedure files.

## Restoring with myloader

mydumper's companion is `myloader`, which loads files in parallel while disabling foreign key checks and rebuilding indexes at the end. This approach makes the restore significantly faster compared to sequentially loading a single SQL file.

## When to use it

mydumper is the recommended choice for production databases over 10 GB where dump and restore speed is critical. On a 60 GB database with 8 threads, a dump that takes 3-4 hours with mysqldump completes in 20-25 minutes.
