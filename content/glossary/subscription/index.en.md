---
title: "Subscription"
description: "PostgreSQL subscriber-side object that establishes the connection to the publisher and manages the logical replication lifecycle: initial snapshot, streaming, reconnection."
translationKey: "glossary_subscription"
aka: "PostgreSQL Logical Replication Subscription"
articles:
  - "/posts/postgresql/replica-logica-in-postgresql-scenari-d-uso-configurazione-e-monitoraggio"
---

**Subscription** is the object that, on the **subscriber** side (the target database), establishes the connection to the PostgreSQL publisher, specifies which publication to subscribe to, and manages the full lifecycle of logical replication: initial data snapshot, streaming of incremental changes, automatic reconnection on disconnect.

## How to create one

You declare it with `CREATE SUBSCRIPTION`, providing the connection to the publisher and the publication to consume:

```sql
CREATE SUBSCRIPTION my_sub
  CONNECTION 'host=pg-primary user=replica_user dbname=app'
  PUBLICATION my_pub;
```

On creation, an initial snapshot of the tables is taken, then continuous WAL streaming begins.

## State and monitoring

The `pg_stat_subscription` view exposes the state of every active subscription: current apply position, lag, last received event. It's the entry point for troubleshooting replication lag or stalls.

## Operational limits

A subscription **cannot** be natively paused/resumed before version 14 — it can only be disabled with `ALTER SUBSCRIPTION ... DISABLE`. On **conflicts** (row already present on the target, constraint violations) the stream stops and must be resolved manually before it resumes.
