---
title: "CREATE TYPE AS ENUM"
description: "PostgreSQL DDL statement that creates an enumerated type as a first-class object, reusable across columns and modifiable via ALTER TYPE."
translationKey: "glossary_postgresql_create_type_enum"
aka: "PostgreSQL ENUM type"
articles:
  - "/posts/postgresql/enum-postgresql-paga-o-pesa"
---

`CREATE TYPE ... AS ENUM` is the PostgreSQL DDL statement that declares an enumerated type — a closed domain of allowed text values. Unlike MySQL, in PostgreSQL an ENUM is a **standalone data type**, not a decoration of a `VARCHAR` column.

## What it looks like

Basic syntax: `CREATE TYPE type_name AS ENUM ('value1','value2',...)`. Once created, the type can be used as the type of one or more columns (`status subscription_status`), as parameter type for functions and procedures, and in partial index declarations. Internally PostgreSQL stores each value as a 4-byte OID, preserving the positional ordering declared at `CREATE TYPE` time.

## What it's for

To enforce, at the schema level, the membership of a value to a closed set. It's stricter than a `CHECK` constraint because it defines a **type** — so the constraint travels with the column even across functions, views, and procedure parameters. Queries like `WHERE status = 'ACTIVE'` stay readable and fast, no JOIN with a lookup table required.

## When to use it

It's the right choice when the value set is **stable over time** (days of the week, binary states, technical polarities) and the semantics must be schema-controlled. Not recommended when the vocabulary evolves frequently or you need extra attributes (localised labels, display order, flags), because PostgreSQL has no native `ALTER TYPE DROP VALUE`: removing a value requires recreating the type and migrating the columns.
