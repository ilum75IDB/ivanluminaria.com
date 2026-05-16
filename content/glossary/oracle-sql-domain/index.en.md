---
title: "SQL Domain"
description: "Construct introduced in Oracle Database 23ai that defines a reusable domain (base type + CHECK + DEFAULT + annotations) as a data dictionary object."
translationKey: "glossary_oracle_sql_domain"
aka: "SQL Domain (Oracle 23ai)"
articles:
  - "/posts/oracle/enum-oracle-workaround-fino-a-23ai"
  - "/posts/oracle/enum-oracle-19c-26ai-domini"
---

The **SQL Domain** is a construct introduced in Oracle Database 23ai that lets you define a **reusable domain** for a column: a base type (e.g. `VARCHAR2(20)`), a `CHECK` constraint, a `DEFAULT` value, and optional **annotations** metadata — all encapsulated in a data dictionary object that can be reused on many different columns.

## How it works

You declare it with `CREATE DOMAIN name AS base_type ... CONSTRAINT chk_X CHECK (...) DEFAULT ... ANNOTATIONS (...)`. Once created, the domain is visible in `DBA_DOMAINS` and can be used as a column type in any `CREATE TABLE`. Oracle validates the domain's `CHECK` on every INSERT/UPDATE just as it would for an inline constraint.

## What it's for

Centralizing in one place the domain of a column, avoiding replication of the same value list (or same constraint) across dozens of tables. When the set evolves, a single `ALTER DOMAIN` propagates the change to all columns using the domain — no need to touch the `CREATE TABLE`s or run multiple `ALTER TABLE`s.

## What sets it apart from PostgreSQL DOMAIN

PostgreSQL's `DOMAIN` has existed for much longer but is more minimal: base type + constraints, no annotations system. Oracle added a metadata layer (`display`, `description`, ordering, etc.) that BI tools, reporting systems and UI generation frameworks can read to automatically derive labels, visual ordering, field descriptions.
