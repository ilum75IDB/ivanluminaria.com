---
title: "Logical Replication Slot"
description: "Persistent PostgreSQL structure on the publisher that tracks WAL consumption position per subscriber. Protects against data loss in case of disconnection."
translationKey: "glossary_slot_di_replica_logica"
aka: "Slot di replica logica"
articles:
  - "/posts/postgresql/replica-logica-in-postgresql-scenari-d-uso-configurazione-e-monitoraggio"
---

A **logical replication slot** is a persistent structure on the PostgreSQL publisher that stores the WAL consumption position for each subscriber. It guarantees that no change is lost even if the subscriber disconnects temporarily: WAL segments are retained until they are consumed and acknowledged.

## Why it exists

Without a slot, PostgreSQL recycles WAL segments as soon as they're no longer needed for crash recovery — typically within minutes on active systems. A subscriber disconnected for an hour would find an unrecoverable gap, and the only way out would be re-initialising the subscription from snapshot. The slot solves this by keeping the WAL available.

## The orphaned slot risk

A slot that stops consuming (crashed subscriber, dropped without removing the slot first, interrupted migration) **keeps holding WAL indefinitely**, filling up the publisher's disk. It's the number-one cause of outages from logical replication in production.

## Essential monitoring

The `pg_replication_slots` view exposes `active` (in use?), `restart_lsn` (where it would resume from), and computing the delta between `pg_current_wal_lsn()` and `restart_lsn` gives you the retained WAL volume. On critical systems an alert is mandatory when the delta exceeds a threshold (say 10 GB) or when a slot stays `active = false` for too long. PostgreSQL 13 introduced `max_slot_wal_keep_size` as a safety cap.
