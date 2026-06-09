---
title: "Publication"
description: "PostgreSQL logical replication object that defines the set of tables (and rows, from 15) whose changes are made available to subscribers."
translationKey: "glossary_publication"
aka: "PostgreSQL Logical Replication Publication"
articles:
  - "/posts/postgresql/replica-logica-in-postgresql-scenari-d-uso-configurazione-e-monitoraggio"
---

**Publication** is a PostgreSQL logical replication object that defines a set of tables whose changes are made available for replication. It lives on the **publisher** (the source database) and can be consumed by one or more independent subscribers, each with its own subscription.

## How to create one

You declare it with `CREATE PUBLICATION`, listing the tables to include. From version 15 onward you can also add a `WHERE` clause to filter replicated rows:

```sql
CREATE PUBLICATION my_pub
  FOR TABLE customers, orders
  WHERE (status = 'active');
```

## What it doesn't carry

A publication transports **DML** changes (INSERT, UPDATE, DELETE, TRUNCATE) but **not DDL**: schema changes (ALTER TABLE, CREATE INDEX) must be applied manually on both sides of the replication, or via external orchestration tooling. **Sequences** are also not replicated by default.

## When to use

Typically for cross-version PostgreSQL migrations, CDC integration into a data warehouse, or selective replication of table subsets to staging nodes. A single publication can feed multiple subscribers in parallel, each at its own consumption pace.
