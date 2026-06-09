---
title: "WAL"
description: "Write-Ahead Log — sequential record of all changes to a PostgreSQL database, written before the data files. Foundation of durability, crash recovery, physical and logical replication."
translationKey: "glossary_wal"
aka: "Write-Ahead Log"
articles:
  - "/posts/postgresql/replica-logica-in-postgresql-scenari-d-uso-configurazione-e-monitoraggio"
---

The **WAL** (Write-Ahead Log) is the sequential record of all changes made to a PostgreSQL database: every INSERT, UPDATE, DELETE, DDL is written here **before** the changes are applied to the actual data files. It's the foundation of durability, crash recovery, physical replication, and logical replication.

## Why "Write-Ahead"

The rule is: a transaction is considered committed only once its WAL record has been `fsync`'d to disk. Even if the server crashes immediately afterwards, the data file can be reconstructed by replaying the WAL records from the last checkpoint. This guarantee lets PostgreSQL tolerate sudden crashes without database corruption.

## On-disk structure

WAL records are grouped into **segments** of 16 MB by default (configurable via `wal_segment_size`) in the `pg_wal/` directory. Each segment has a 24-character hexadecimal name (e.g. `000000010000000000000042`) encoding timeline + LSN offset — the **Log Sequence Number**, the monotonic position identifier in the WAL stream.

## Logical replication and WAL

PostgreSQL's logical replication **decodes** WAL records (originally in physical format) into per-row logical changes (INSERT/UPDATE/DELETE with column values) via the `pgoutput` plugin. It's this "logical decoding" step that lets subscribers apply changes onto tables with a different physical layout (e.g. PostgreSQL 13 → 15 with a changed tablespace). Without WAL there is no replication.
