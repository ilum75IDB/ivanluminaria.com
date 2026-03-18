---
title: "Bloat"
description: "Dead space accumulated in a PostgreSQL table or index due to unremoved dead tuples, inflating disk size and degrading query performance."
translationKey: "glossary_bloat"
aka: "Table Bloat / Index Bloat"
articles:
  - "/posts/postgresql/vacuum-autovacuum-postgresql"
---

**Bloat** is the accumulation of dead space within a PostgreSQL table or index, caused by dead tuples not yet removed by VACUUM. A table with 50% bloat occupies twice the necessary space and forces sequential scans to read twice as many pages.

## How it works

Bloat is measured by comparing the actual table size with the expected size based on live rows. The `pgstattuple` extension provides the `dead_tuple_percent` field. Bloat above 20-30% is a warning sign; above 50% is an emergency.

## What it's for

Monitoring bloat is essential to understand whether autovacuum is keeping pace. The `pg_stat_user_tables` query with `n_dead_tup` and `last_autovacuum` is the first diagnostic tool. If bloat is out of control, `pg_repack` rebuilds the table online without prolonged exclusive locks — unlike `VACUUM FULL`.

## What can go wrong

Normal VACUUM reclaims dead tuple space but doesn't compact the table — fragmented space remains. If bloat reaches 50-70%, VACUUM alone isn't enough. The options are `VACUUM FULL` (exclusive lock, blocks everything) or `pg_repack` (online, but requires installation). The real solution is not getting there, with a well-configured autovacuum.
