---
title: "CHECK constraint"
description: "Standard SQL constraint that restricts the values allowed in a column via a boolean expression. In MySQL it's only really enforced from version 8.0.16."
translationKey: "glossary_check_constraint"
aka: "CHECK constraint"
articles:
  - "/posts/mysql/enum-mysql-semplifica-o-complica"
  - "/posts/postgresql/enum-postgresql-paga-o-pesa"
  - "/posts/oracle/enum-oracle-workaround-fino-a-23ai"
---

The **CHECK constraint** is a standard SQL constraint that restricts the values allowed in a column or table via a boolean expression. When an `INSERT` or `UPDATE` would produce a value that violates the expression, the database rejects the operation.

## How it works

It's declared at column or table level in the `CREATE TABLE` or added later with `ALTER TABLE ADD CONSTRAINT`. The expression can be any valid boolean condition: `status IN ('NEW','ACTIVE','CLOSED')`, `price > 0`, `end_date >= start_date`. The constraint is evaluated on every write to the column.

## What it's for

Enforcing data integrity directly in the schema, without having to validate at application level. Particularly useful for:

- Restricting a field to a set of values (alternative to ENUM)
- Inter-column constraints (e.g. date coherence, sums that must match)
- Basic format validation (e.g. emails, tax codes)

## When to use it in MySQL

Mind the version: before **MySQL 8.0.16**, CHECK constraints were parsed and silently ignored. They've only been actually enforced since 8.0.16. This has surprised many developers migrating from PostgreSQL or Oracle, where CHECK has always worked.

Compared to ENUM, CHECK is more flexible (renaming a value is just an `ALTER CONSTRAINT`) but more verbose. Good for sets of 5-15 values that get touched occasionally, without the need for extra attributes.
