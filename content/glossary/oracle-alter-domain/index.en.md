---
title: "ALTER DOMAIN"
description: "Oracle 23ai command that modifies a SQL Domain (CHECK constraint, DEFAULT, annotations) propagating the change to all columns using the domain."
translationKey: "glossary_oracle_alter_domain"
aka: "ALTER DOMAIN (Oracle 23ai)"
articles:
  - "/posts/oracle/enum-oracle-workaround-fino-a-23ai"
---

`ALTER DOMAIN` is the Oracle Database 23ai command that **modifies an existing SQL Domain** — the `CHECK` constraint, the `DEFAULT` value, the `ANNOTATIONS` — propagating the change to all columns that declared that domain as their type. It's what makes the SQL Domain a real alternative to a lookup table, not just a reusable `CHECK`.

## How it works

`ALTER DOMAIN domain_name CONSTRAINT chk_X CHECK (VALUE IN (...))` updates the domain's constraint. Oracle automatically finds all columns declared with `domain_name` (across any table and schema, subject to grants) and applies the new constraint. Existing rows can be validated (`VALIDATE`) or left as-is (`NOVALIDATE`), at the discretion of whoever manages the migration.

## What it's for

Replacing dozens of `ALTER TABLE`s with a single operation. When a column's domain is used across 20 tables and a new allowed value needs to be added, before 23ai you had to modify 20 distinct `CHECK`s — with `ALTER DOMAIN` it's a single statement. Same applies to changes to the `DEFAULT` or the `ANNOTATIONS`.

## How it differs from ALTER TABLE

`ALTER TABLE ... MODIFY CONSTRAINT` acts on a single constraint of a single table. `ALTER DOMAIN` acts on all columns, across all tables, that inherit the domain. It's the difference between a local operation and a schema-wide governance operation.
