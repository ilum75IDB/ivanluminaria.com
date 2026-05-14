---
title: "ALTER TYPE ADD VALUE"
description: "PostgreSQL command that appends a value to an existing ENUM. Metadata-only operation, transactional, no rebuild of the tables that use the type."
translationKey: "glossary_postgresql_alter_type_add_value"
aka: "PostgreSQL ENUM extension"
articles:
  - "/posts/postgresql/enum-postgresql-paga-o-pesa"
---

`ALTER TYPE ... ADD VALUE` is the PostgreSQL command that adds a new value to an existing enumerated type. It's one of the most common DDL changes on an ENUM, and one of the **main differences** from MySQL: in PostgreSQL it requires no rebuild of the tables that use the type.

## How it works

Syntax: `ALTER TYPE type_name ADD VALUE 'new_value' [BEFORE|AFTER 'other_value']`. Without the positional clause, the new value is appended at the end. With `BEFORE` or `AFTER`, it's inserted at the specified position, which affects the ordering used by `ORDER BY` on that column. Available since PostgreSQL 9.1; `BEFORE`/`AFTER` positioning landed with 9.6.

## What it's for

To extend the vocabulary of an ENUM without recreating the type. It's a **metadata-only** operation: PostgreSQL updates the `pg_enum` catalog without touching the tables that use the type, even if they hold billions of rows. It runs in milliseconds, inside a transaction, with rollback possible if something goes wrong during the deploy.

## When to use it

It's the natural lifecycle change for a PostgreSQL ENUM: new product, new channel, new business policy → a new value to add to the set. Unlike `ADD VALUE`, PostgreSQL **has no native `DROP VALUE`**: removing a value requires recreating the type from scratch and migrating the columns that use it. This asymmetry is the main operational limit of the ENUM type in PostgreSQL.
