---
title: "Online DDL"
description: "MySQL/InnoDB mechanism that allows ALTER TABLE operations to run without blocking concurrent writes, with precise limits depending on the operation."
translationKey: "glossary_mysql_online_ddl"
aka: "MySQL Online DDL"
articles:
  - "/posts/mysql/enum-mysql-semplifica-o-complica"
---

**Online DDL** is the MySQL/InnoDB mechanism that allows many `ALTER TABLE` operations to run without blocking concurrent writes on the table. It was introduced in MySQL 5.6 and progressively expanded in later versions.

## How it works

MySQL automatically evaluates the requested operation and picks between three algorithms: `INSTANT` (metadata-only change, fraction of a second), `INPLACE` (modifies the table without copying it, supports parallel DML), `COPY` (full rebuild, blocks writes). The algorithm used depends on the type of ALTER and the MySQL version.

## What it's for

Drastically reducing downtime during schema maintenance on production databases. Operations like adding a trailing column, adding an index, modifying a default have become practically instant. Heavier operations (changing column type, rebuilding a primary index) still require a rebuild, but often with concurrency preserved.

## Watch out for

Online DDL isn't free: even `INPLACE` generates significant load on I/O and replication lag. On tables with hundreds of millions of rows, even "online" operations can produce hours of replica lag. Also, certain operations (e.g. modifying an ENUM column by inserting values in the middle) still fall into `ALGORITHM=COPY` and block writes. It's always worth explicitly specifying `ALGORITHM=INPLACE, LOCK=NONE` to be sure of the behaviour, and testing on a replica first.
