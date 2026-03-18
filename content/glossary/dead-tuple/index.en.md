---
title: "Dead Tuple"
description: "Obsolete row in a PostgreSQL table, marked as no longer visible after an UPDATE or DELETE but not yet physically removed from disk."
translationKey: "glossary_dead-tuple"
aka: "Dead Row"
articles:
  - "/posts/postgresql/vacuum-autovacuum-postgresql"
---

A **Dead Tuple** is a row in a PostgreSQL table that has been updated (UPDATE) or deleted (DELETE) but has not yet been physically removed. It remains in the data pages, occupying disk space and slowing down scans.

## How it works

When PostgreSQL executes an UPDATE, it does not overwrite the original row: it creates a new version and marks the old one as "dead." The old row remains physically in the data page until VACUUM cleans it up. Dead tuples are the price of the MVCC model — necessary to guarantee transactional isolation.

## What it's for

Dead tuples are a key indicator of table health. The `pg_stat_user_tables` view shows `n_dead_tup` and `last_autovacuum` — if dead tuples grow faster than autovacuum can clean, the table has a problem. A dead_tuple_percent above 20-30% is a warning sign.

## What can go wrong

On a table with 500,000 updates per day and autovacuum defaults (scale_factor 0.2), VACUUM triggers every 4 days. Meanwhile dead tuples accumulate, tables bloat, and queries slow down progressively — the "Monday fine, Friday disaster" pattern.
