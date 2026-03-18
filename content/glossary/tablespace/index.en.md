---
title: "Tablespace"
description: "Logical storage unit in Oracle that groups one or more physical datafiles. Enables organising, managing and optimising disk space for tables, indexes and partitions."
translationKey: "glossary_tablespace"
articles:
  - "/posts/oracle/oracle-partitioning"
---

A **Tablespace** is the logical unit of storage organisation in Oracle Database. Each tablespace comprises one or more physical datafiles on disk, and every database object (table, index, partition) resides in a tablespace.

## How it works

Oracle separates logical management (tablespace) from physical management (datafile). A DBA can create dedicated tablespaces for different purposes: one for active data, one for indexes, one for archive. This enables distributing I/O load across different disks and applying differentiated management policies (e.g. read-only for historical data).

## What it's for

In the partitioning context, tablespaces enable advanced lifecycle management strategies: moving old partitions to economical archive tablespaces, setting them to read-only to reduce backup load, and reclaiming active space without deleting data. An `ALTER TABLE MOVE PARTITION ... TABLESPACE ts_archive` is a DDL operation that takes less than a second.

## When to use it

Every Oracle installation uses tablespaces. Tablespace design becomes critical when managing tables of hundreds of GB with partitioning, because good distribution across separate tablespaces enables efficient incremental backups and data lifecycle management.
