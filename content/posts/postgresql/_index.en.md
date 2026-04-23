---
description: "PostgreSQL: architecture, performance and design insights on one of the most advanced and long-standing open source databases."
layout: "list"
title: "PostgreSQL"
image: "postgresql.cover.jpg"
---

I have seen PostgreSQL in production with `shared_buffers` set to 128MB on machines with 256GB of RAM — "because we kept the default". I have seen `autovacuum` turned off because "it was slowing the system down", and three months later a table of 500 million rows with 80% bloat and queries that never finished. I have seen streaming replicas silently broken for weeks, and we only realised it when the master went down and the failover did not kick in.

And I have seen the exact opposite: Postgres clusters handling thousands of concurrent connections, managing terabytes of data and surviving major upgrades without a minute of perceived downtime.

The difference is not in the code. It is in **whoever had the courage to touch the defaults rather than put up with them**.

------------------------------------------------------------------------

PostgreSQL is not just an open source database. It is the result of nearly four decades of academic and industrial evolution.

Born in 1986 at the University of Berkeley as an evolution of Ingres, the POSTGRES project introduced concepts that were ahead of their time: **extensibility, custom data types, rules and an advanced relational model**. In 1996 SQL support arrived and the name became PostgreSQL. The world, though, kept on calling it simply "Postgres". And that is perfectly fine.

After twenty years working on it, I have learned one thing: PostgreSQL **rewards those who study it and punishes those who leave it on defaults**. It is an engine designed to be tuned, not installed and forgotten. The assumptions from development get dismantled by the reality of production:

- **VACUUM and autovacuum** are not optional — they are like brushing your teeth
- **`shared_buffers`** at the default 128MB is only reasonable on a laptop
- **`work_mem`** set wrong, multiplied by active connections, will OOM you at the worst possible moment
- **Replicas** need active monitoring — streaming breaks silently
- **Extensions** can change catalog behaviour and block upgrades

------------------------------------------------------------------------

## 🔧 The parameters I never leave at default

When I take a Postgres cluster into production, there are five parameters I never leave on their out-of-the-box values. Not because the default is wrong in absolute terms, but because it is designed to run anywhere — and "anywhere" is never your production machine.

| Parameter | What it controls | How I set it |
|---|---|---|
| **`shared_buffers`** | Postgres's shared cache | Usually 25% of RAM — no more, the filesystem cache handles the rest |
| **`effective_cache_size`** | What the planner believes is in cache | 50-75% of RAM — allocates nothing, influences the optimizer's choices |
| **`work_mem`** | Memory for sorts and hashes per operation | Low (4-16MB) if there are many connections, high only for dedicated analytical workloads |
| **`autovacuum_*`** | Automatic cleanup of dead tuples | Never disabled. Tuned if needed (`naptime`, `cost_limit`) to be more aggressive on hot tables |
| **`wal_level` + `max_wal_senders`** | WAL detail, slots for replicas | `replica` or `logical` depending on the case, senders sized on real replicas plus headroom |

Five parameters. Twenty minutes of analysis. Months of performance problems avoided.

------------------------------------------------------------------------

## 📚 What I talk about here

Real stories and technical decisions on PostgreSQL in production. Architecture, VACUUM and bloat, parameter tuning, streaming and logical replication, upgrade strategies, backups with pg_basebackup and WAL archiving, extensions that actually help (and the ones you could have skipped).

No recipes out of a box. Just what I have seen work in real environments — postal, banking, public administration, telco — where Postgres runs thousands of instances in parallel and cannot afford approximations.

------------------------------------------------------------------------

Choosing PostgreSQL is not just choosing an open source database.

It is choosing an engine designed to be extended, analysed and understood — and accepting that, without a bit of study, the defaults will not take you very far.
