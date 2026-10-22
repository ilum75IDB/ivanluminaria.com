---
title: "max_connections"
description: "PostgreSQL parameter that sets the maximum number of simultaneous client connections. Each connection has a real cost in memory and OS scheduling overhead."
translationKey: "glossary_max_connections"
aka: "max_connections (PostgreSQL connection limit)"
articles:
  - "/posts/postgresql/pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600"
---

`max_connections` is the `postgresql.conf` parameter that defines how many client connections PostgreSQL will accept at the same time. It is not an arbitrary cap: each active connection spawns a dedicated backend process, carrying a fixed cost in shared memory allocation and operating system scheduling overhead.

## How it works

PostgreSQL uses a process-per-connection model: every connecting client triggers a forked backend process. `max_connections` sets the ceiling for those processes. Once the limit is reached, the server rejects new connections with an explicit error.

```sql
-- Check the current value
SHOW max_connections;

-- Count currently active connections
SELECT count(*) FROM pg_stat_activity;
```

Changing the parameter requires a server restart because it determines the initial shared memory layout — particularly for lock tables and per-process buffers.

## Operational context

A high `max_connections` value is not free: each slot reserves roughly 5–10 MB of shared memory even when the connection is idle. At 500 connections, that is several gigabytes reserved before a single query runs.

The recommended pattern is to keep `max_connections` low (typically 100–200 for OLTP workloads) and delegate multiplexing to a connection pooler such as PgBouncer in transaction pooling mode. This allows thousands of application clients to share a small number of real backend connections.

## Notes

Raising `max_connections` also requires revisiting `work_mem` and `shared_buffers`: available memory is divided across all active backend processes. Increasing the limit without accounting for the overall memory footprint leads to memory pressure or, in the worst case, an OS-level OOM kill.
