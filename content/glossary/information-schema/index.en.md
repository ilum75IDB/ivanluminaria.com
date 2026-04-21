---
title: "information_schema"
description: "Read-only MySQL/MariaDB system schema exposing metadata about databases, tables, indexes, users and server state. Foundation for any assessment or structural analysis."
translationKey: "glossary_information_schema"
aka: "Information Schema, INFORMATION_SCHEMA"
articles:
  - "/posts/mysql/mysql-pre-upgrade-assessment"
---

**information_schema** is the SQL-standard virtual schema that MySQL and MariaDB expose as an introspection interface: it holds no application data, only metadata about server state (databases, tables, columns, indexes, users, privileges, session parameters).

## How it works

`information_schema` tables are views over the database's internal catalogs. The most commonly used are:

- `TABLES` — one row per table, with size, engine type, estimated row count
- `COLUMNS` — one row per column, with data type, nullability, collation
- `STATISTICS` — one row per index and included column, with estimated cardinality
- `SCHEMATA` — one row per database
- `PROCESSLIST` — active sessions (equivalent to `SHOW PROCESSLIST`)
- `INNODB_*` — metrics and status for the InnoDB engine

## What it's for

It's the starting point of any assessment: database sizing, identifying the largest tables, index audits, data-type analysis, checks for mixed collations. Many monitoring scripts and BI tools read `information_schema` to build state dashboards.

## Limitations to know

`data_length`, `index_length` and `table_rows` are **estimates** refreshed periodically by InnoDB and dependent on the last `ANALYZE TABLE`. On very volatile tables they can underestimate by 10-15%. For critical data (migration planning, capacity planning) it's good practice to cross-check with the physical size of the `.ibd` files (`du -sh /var/lib/mysql/<schema>/*.ibd`).
