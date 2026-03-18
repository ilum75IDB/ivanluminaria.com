---
title: "CTAS"
description: "Create Table As Select — Oracle technique for creating a new table populated with query results, used for migrations and restructuring of large tables."
translationKey: "glossary_ctas"
aka: "Create Table As Select"
articles:
  - "/posts/oracle/oracle-partitioning"
---

**CTAS** (Create Table As Select) is an Oracle SQL command that creates a new table and populates it in a single operation with the results of a SELECT. It is the standard technique for migrating data from one structure to another on large tables.

## How it works

The command combines DDL and DML: it creates the table with the structure derived from the SELECT and inserts the data in a single pass. With the `PARALLEL` hint and `NOLOGGING` mode, copying hundreds of GB can complete in a few hours. After the copy, the original table is renamed, the new one takes its place, and downtime is limited to the few seconds of the rename.

## What it's for

CTAS is essential when restructuring a table without being able to use `ALTER TABLE` directly — for example, adding partitioning to an existing table with billions of rows. It allows working on the new structure while the system is live on the old one.

## When to use it

Used for migrations to partitioned tables, reorganising fragmented data, and creating table copies with different structures. In production, it should always be combined with `NOLOGGING` (to reduce redo logs) and followed by an immediate RMAN backup.
