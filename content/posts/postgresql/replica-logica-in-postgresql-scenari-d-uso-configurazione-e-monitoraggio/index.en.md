---
title: "Replica logica in PostgreSQL: le domande di un collega che chiariscono l'argomento"
date: 2099-12-31
draft: true
section: postgresql
webo_status: da_tradurre
webo_generated_at: 2026-06-08
---

## A job shadow that wasn't a lesson

Claudio was there to observe, not to learn in any formal sense. The job shadow was real work: a claims and policy management system running in production, a large Italian insurance group, and a concrete need to migrate from PostgreSQL 13 to PostgreSQL 15 without interrupting operations. In parallel, the fraud analysis team was waiting for a data feed into the data warehouse to power their models.

It wasn't the ideal context for explaining logical replication from scratch. Yet Claudio asked exactly the questions anyone would ask the first time — and answering those questions out loud, in a way that held up, made every choice I had already made in silence more solid.

This article follows that same sequence: first the questions, then the concepts, then the concrete configuration.

---

## Physical replication vs. logical replication: the opening dilemma

Claudio's first question came before we even opened a terminal: "Why aren't we using physical replication? Isn't that the standard approach?"

It's the right question. Physical replication — streaming replication — is the established choice for high availability and disaster recovery. It operates at the block level: the primary server streams WAL (Write-Ahead Log) segments to the replica, which applies them identically. The result is a byte-for-byte copy of the cluster. Straightforward to configure, reliable, well-documented [1].

Its limitation is the flip side of its strength: it replicates *everything*, in the same format, at the same PostgreSQL version. You can't replicate only certain tables. You can't replicate to a different engine version. You can't use the replica as a source for an external system that speaks a different protocol.

Logical replication operates at the row level, not the block level. The publisher decodes changes from the WAL and transmits them as logical operations — `INSERT`, `UPDATE`, `DELETE` — to one or more subscribers. This opens three possibilities that physical replication doesn't offer:

- replicating a subset of tables or rows
- replicating between different PostgreSQL versions (from version 10 onward, with limitations)
- feeding heterogeneous systems such as data warehouses or message brokers via Change Data Capture (CDC)

In our case, all three requirements were present at the same time.

---

## The three scenarios and Claudio's questions

### Cross-version migration with no downtime

"Can't I just run `pg_upgrade`?" Claudio asked, glancing at the documentation on the monitor beside him.

Yes, `pg_upgrade` works. But it requires taking the system offline, running the upgrade, verifying, and only then reopening traffic. With 100 million rows in `claim_events.claims` and 300 million in `claim_events.claim_details`, the downtime would have been in the range of hours — unacceptable for a system handling active claims settlements.

Logical replication allows a different approach: prepare the new PostgreSQL 15 cluster (`pg-claims-new-01`), feed it via subscription, and when the replication lag drops to seconds, execute the switchover. Downtime shrinks to the time needed to redirect connections — minutes, not hours.

### CDC integration toward the data warehouse

"Is it like a distributed trigger?" Claudio asked, with some satisfaction at the analogy.

No — and the difference is substantial. A trigger executes within the transaction, adds latency, and scales poorly at high volumes. Logical replication reads the WAL *after* the transaction has already been committed: no impact on the critical write path, no additional locks, no overhead on the publisher beyond WAL decoding.

For the fraud team, the requirement was to receive new claims submissions (`fraud_detection_audit.new_claims_for_analysis`) in near real time on `pg-dw-subscriber-01`. The dedicated publication `fraud_audit_pub` addressed exactly that requirement, without touching any application logic.

### Selective replication

"What if I only want data for active customers?" Claudio asked, already thinking about a future use case.

Here the answer is more nuanced. Logical replication lets you choose which tables to include in a publication. Starting with PostgreSQL 15, you can also add a `WHERE` clause to filter rows [2]. The main limitation involves DDL: schema changes are not replicated automatically — a point I return to in the monitoring section.

---

## Key concepts: publication, subscription, and replication slots

Before moving to configuration, three concepts worth pinning down.

**Publication** — defines *what* gets replicated on the publisher. It can include specific tables, all tables in a database (`FOR ALL TABLES`), or — from version 15 onward — sequences. Each publication has a name and can be referenced by multiple subscribers.

**Subscription** — defines *who* receives the data and *from where*. The subscription is created on the subscriber and specifies the connection string to the publisher and the name of the publication it subscribes to. At creation time, PostgreSQL performs an initial data copy (initial snapshot) and then streams subsequent changes.

**Logical replication slot** — the mechanism that guarantees persistence. The publisher retains the WAL segments needed until the subscriber has consumed them. This is essential for consistency, but it introduces a risk: if a subscriber disconnects for an extended period, WAL accumulates and the publisher's disk space can be exhausted. Monitoring slots is mandatory in production.

---

## Practical configuration

### Publisher: `pg-claims-primary-01` (PostgreSQL 13.10)

The most important parameter is `wal_level`, which must be set to `logical`. The other parameters size the resources for slots and workers.

```sql
-- On pg-claims-primary-01
ALTER SYSTEM SET wal_level = 'logical';
ALTER SYSTEM SET max_replication_slots = '10';
ALTER SYSTEM SET max_worker_processes = '10';
SELECT pg_reload_conf();
```

`wal_level = 'logical'` requires a server restart to take effect. The other parameters can be applied with `pg_reload_conf()`, but it's good practice to verify the effective values after the reload:

```sql
SHOW wal_level;
SHOW max_replication_slots;
```

After the restart, create the publications. For the migration, the main tables:

```sql
CREATE PUBLICATION claims_pub
  FOR TABLE insurance_policies.policies,
             claim_events.claims;
```

For the data warehouse integration, a separate dedicated publication:

```sql
CREATE PUBLICATION fraud_audit_pub
  FOR TABLE fraud_detection_audit.new_claims_for_analysis;
```

Separating publications by use case is a deliberate choice: it allows permissions, monitoring, and lifecycle to be managed independently.

**Replication user** — the subscriber connects with a dedicated user that must have the `REPLICATION` role and `SELECT` permissions on the published tables:

```sql
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD '...';
GRANT SELECT ON insurance_policies.policies TO replicator;
GRANT SELECT ON claim_events.claims TO replicator;
GRANT SELECT ON fraud_detection_audit.new_claims_for_analysis TO replicator;
```

Also verify that `pg_hba.conf` allows connections from the subscriber's IP with the appropriate authentication method (preferably `scram-sha-256`).

### Migration subscriber: `pg-claims-new-01` (PostgreSQL 15.3)

```sql
-- On pg-claims-new-01
ALTER SYSTEM SET max_worker_processes = '10';
SELECT pg_reload_conf();

CREATE SUBSCRIPTION claims_sub
  CONNECTION 'host=pg-claims-primary-01 port=5432 user=replicator password=...'
  PUBLICATION claims_pub;
```

At `CREATE SUBSCRIPTION` time, PostgreSQL starts the initial snapshot: it copies all existing rows from the published tables, then switches to streaming changes. With 150 million rows across `policies` and `claims`, this snapshot took several hours — scheduled during a low-activity window.

### Data warehouse subscriber: `pg-dw-subscriber-01` (PostgreSQL 15.3)

```sql
-- On pg-dw-subscriber-01
ALTER SYSTEM SET max_worker_processes = '5';
SELECT pg_reload_conf();

CREATE SUBSCRIPTION fraud_audit_sub
  CONNECTION 'host=pg-claims-primary-01 port=5432 user=replicator password=...'
  PUBLICATION fraud_audit_pub;
```

---

## Monitoring and troubleshooting

"How do I know if it's actually working?" — Claudio's most useful question of all.

### Replication lag

The `pg_replication_slots` view on the publisher shows the status of active slots and the volume of WAL being retained:

```sql
SELECT
  slot_name,
  active,
  pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS replication_lag_bytes
FROM pg_replication_slots
WHERE slot_type = 'logical';
```

A steadily growing `replication_lag_bytes` signals a subscriber under stress. If `active` is `false` and the lag keeps climbing, the slot is accumulating WAL without consuming it — a situation that needs prompt attention.

On the subscriber, `pg_stat_subscription` and `pg_stat_subscription_stats` show the apply status:

```sql
SELECT
  subname,
  subenabled,
  subconninfo,
  subslotname,
  substate,
  subbinary
FROM pg_subscription;

SELECT
  subid,
  relid,
  last_applied_lsn,
  last_received_lsn,
  pg_wal_lsn_diff(last_received_lsn, last_applied_lsn) AS apply_lag_bytes
FROM pg_stat_subscription_stats;
```

`apply_lag_bytes` measures the gap between what the subscriber has received and what it has actually applied. A stable, low value indicates a healthy system.

### Conflicts and primary keys

The most common conflict in logical replication is a primary key violation: the subscriber receives an `INSERT` for a row that already exists locally. This typically happens when the subscriber has pre-existing data that isn't aligned with the publisher.

PostgreSQL logs conflicts on the subscriber with messages like:

```
ERROR: duplicate key value violates unique constraint "claims_pkey"
```

Replication halts until the conflict is resolved. The options are: delete the conflicting row on the subscriber, or use `ALTER SUBSCRIPTION ... SKIP` to skip the problematic transaction (with a clear understanding of the consistency implications).

### DDL management

"If I add a column on the publisher, does the subscriber see it?" Claudio asked — and the answer required a pause.

No — not automatically. Logical replication carries data, not schema changes. If you add a `NOT NULL` column without a default on the publisher, replication breaks because the subscriber doesn't know where to put the value.

The correct procedure is:

1. Add the column on the subscriber before the publisher (with a default or as `NULL`)
2. Add the column on the publisher
3. Verify that replication resumes correctly

For frequent or complex schema changes, tools like `pg_logical` or dedicated CDC solutions (Debezium, pgoutput with external consumers) offer more sophisticated handling. In this project, DDL changes were infrequent and planned: the manual procedure was sufficient.

---

## Best practices and operational considerations

**WAL space** — set `max_slot_wal_keep_size` (available from version 13) to cap WAL accumulation when subscribers are inactive. Without this parameter, a disconnected subscriber can exhaust the publisher's disk space.

**Security** — always use `scram-sha-256` in `pg_hba.conf` for replication connections. Consider enforcing SSL by adding `sslmode=require` to the subscription connection string. Do not use the `postgres` superuser for replication.

**Orphaned slots** — a replication slot that is no longer in use but hasn't been dropped continues to retain WAL. Monitor `pg_replication_slots` periodically and remove stale slots with `SELECT pg_drop_replication_slot('slot_name')`.

**Tables without a primary key** — logical replication for `UPDATE` and `DELETE` operations requires a primary key or a configured replica identity (`REPLICA IDENTITY FULL` as an alternative, with a performance trade-off). Verify all tables before creating the publication.

**Final switchover** — in the migration scenario, the critical moment is the cutover: disable writes on the publisher (or redirect traffic), wait for the lag to reach zero, verify consistency, promote the new cluster. With lag monitored over the preceding days and stable below 500ms, the switchover took under three minutes.

---

## Closing

The system went to production without incident. There was no last-minute problem, no tense moment worth recounting. The new PostgreSQL 15 cluster took over traffic, the data warehouse kept receiving fraud detection data, and the insurance group got its upgrade with no maintenance window visible to users.

Claudio has a more concrete understanding of what he observed. I have a more articulate understanding of what I know — because I had to find the right words, not just the right commands. Explaining the difference between physical and logical replication to someone who doesn't know it means understanding it well enough to choose the right example, not just the technically accurate one.

Claudio's questions didn't change the technical choices. They made them more solid.

---

## Official sources

[1] PostgreSQL Documentation — [Logical Replication](https://www.postgresql.org/docs/current/logical-replication.html) — general concepts, architecture, differences from physical replication.

[2] PostgreSQL Documentation — [CREATE PUBLICATION](https://www.postgresql.org/docs/current/sql-create-publication.html) — full syntax, row filter options (PostgreSQL 15+), sequence handling.

[3] PostgreSQL Documentation — [CREATE SUBSCRIPTION](https://www.postgresql.org/docs/current/sql-create-subscription.html) — syntax, connection options, initial snapshot management.

[4] PostgreSQL Documentation — [Monitoring — pg_stat_replication_slots](https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-REPLICATION-SLOTS-VIEW) — system views for slot monitoring.

[5] PostgreSQL Documentation — [Replication Slots](https://www.postgresql.org/docs/current/warm-standby.html#STREAMING-REPLICATION-SLOTS) — slot mechanism, WAL accumulation risks, `max_slot_wal_keep_size`.

---

## Glossary candidate

**Publication** — a PostgreSQL object that defines the set of tables (and optionally rows, from version 15) whose changes are made available for logical replication. Created on the publisher with `CREATE PUBLICATION`, it can be referenced by multiple independent subscribers.

**Subscription** — a PostgreSQL object created on the subscriber that establishes the connection to the publisher, specifies the publication to subscribe to, and manages the replication lifecycle: initial snapshot, change streaming, automatic reconnection.

**Logical replication slot** — a persistent structure on the publisher that tracks the WAL consumption position for each subscriber. It guarantees that no change is lost during a temporary disconnection, at the cost of retaining WAL segments until they are consumed.

**WAL (Write-Ahead Log)** — a sequential log of all changes made to the PostgreSQL database, written before the changes are applied to the data files. It is the source from which logical replication extracts the operations to transmit to subscribers via the logical decoding process.

**CDC (Change Data Capture)** — a technique that intercepts and transmits, in near real time, data changes from a source system to target systems (data warehouses, message brokers, applications). PostgreSQL's logical replication implements CDC natively via the `pgoutput` protocol.
