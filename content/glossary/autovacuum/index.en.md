---
title: "Autovacuum"
description: "PostgreSQL daemon that automatically runs VACUUM and ANALYZE on tables when the number of dead tuples exceeds a configurable threshold."
translationKey: "glossary_autovacuum"
aka: "Autovacuum Daemon"
articles:
  - "/posts/postgresql/vacuum-autovacuum-postgresql"
---

**Autovacuum** is a PostgreSQL daemon that automatically runs VACUUM and ANALYZE on tables when the number of dead tuples exceeds a threshold calculated as: `threshold + scale_factor × n_live_tup`. With defaults (threshold=50, scale_factor=0.2), on a table with 10 million rows it triggers after 2 million dead tuples.

## How it works

The daemon periodically checks `pg_stat_user_tables` and launches a worker for each table exceeding the threshold. The maximum number of simultaneous workers is controlled by `autovacuum_max_workers` (default 3). The `autovacuum_vacuum_cost_delay` parameter controls how much vacuum throttles itself to avoid overloading I/O.

## What it's for

It is the silent custodian that prevents tables from bloating due to dead tuple accumulation. It should never be disabled — that is the worst thing you can do to a production PostgreSQL. It should be configured per-table: high-traffic tables need low scale_factors (0.01-0.05) and reduced cost_delay.

## What can go wrong

With defaults, autovacuum is too conservative for high-traffic tables. 3 workers for dozens of active tables aren't enough. A 20% scale_factor on large tables generates millions of dead tuples before intervention. Per-table tuning with `ALTER TABLE ... SET (autovacuum_vacuum_scale_factor = 0.01)` is essential.
