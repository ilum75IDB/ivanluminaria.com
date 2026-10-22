---
categories:
- postgresql
date: '2026-11-17'
description: 12 microservices, 600 simultaneous connections, PostgreSQL on its knees.
  How PgBouncer cut real connections to 80 while improving throughput and stability.
  Transaction pooling, prepared statements, critical parameters.
draft: false
image: pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600.cover.jpg
seoTitle: 'PgBouncer: from 600 to 80 PostgreSQL connections without losing throughput'
tags:
- pgbouncer
- connection-pooling
- postgresql
- performance
- scalability
title: 'Six hundred connections and a Monday morning: PgBouncer from 600 to 80 PostgreSQL
  connections without losing throughput'
translationKey: pgbouncer_su_postgresql_transaction_pooling_parametri_critici_e_il_salto_da_600
webo_generated_at: 2026-10-22
webo_status: scheduled
---

## Six hundred connections and a Monday morning

The monitoring dashboard was showing numbers that didn't add up. A distributed application across twelve microservices, each configured with its own internal pool of fifty connections to PostgreSQL. On paper: fifty times twelve equals six hundred — but in production the instances scaled horizontally, and peak load pushed the total even higher.

PostgreSQL wasn't holding up. Queries that normally completed in a few milliseconds were waiting for free slots for tens of seconds. The server's load average was consistently above ten. Memory was nearly exhausted — not from data, but from PostgreSQL's own backend processes.

The team had already tried reducing the pools on the application side, but each microservice was developed by a different team, with its own dependencies and constraints. Coordinating a uniform reduction would have taken weeks. An infrastructure-level solution was needed.

That solution was PgBouncer.

## Why PostgreSQL struggles with hundreds of connections

Before understanding why PgBouncer helps, it's worth understanding why PostgreSQL suffers with many simultaneous connections — this isn't a configuration flaw, it's architecture.

PostgreSQL uses a **process-per-connection** model: each client connection is served by a separate OS process, with its own stack, its own private memory, and its own context-switch overhead. On Linux, each PostgreSQL backend typically occupies between 5 and 10 MB of private memory (plus shared memory). With six hundred active connections, that's 3–6 GB of RAM dedicated solely to backend processes — before a single query runs.

The problem compounds with **context switching**. The kernel scheduler has to manage hundreds of processes competing for CPU cores. When most of these processes are waiting on I/O or locks, the kernel spends time scheduling rather than doing useful work. The effect shows up in load average: a server with eight cores showing a load average of twelve or fifteen isn't doing twelve times the work — it's burning CPU cycles on scheduling overhead.

There's also the issue of **locks and statistics**. Every connection, even when idle, holds data structures in shared memory. With six hundred connections, operations like `VACUUM`, `ANALYZE`, and lock management become more expensive because they have to traverse larger structures.

PostgreSQL's `max_connections` parameter exists precisely for this reason: it's not an arbitrary limit, it's a safeguard against system collapse [1].

## What PgBouncer does and where it sits in the architecture

PgBouncer is a lightweight connection pooler that sits between clients (the microservices) and PostgreSQL. Clients connect to PgBouncer as if it were PostgreSQL — same port, same protocol. PgBouncer maintains a reduced pool of real connections to the database and reuses them across clients.

The key point is that PgBouncer is written in C, is single-threaded with asynchronous I/O (built on `libevent`), and handles thousands of client connections with minimal overhead. A single PgBouncer instance can comfortably handle a thousand client connections using a few tens of MB of RAM.

The resulting architecture looks like this:

```text
[Microservice A] ──┐
[Microservice B] ──┤                    ┌──────────────────┐
[Microservice C] ──┼──► [PgBouncer] ───►│  PostgreSQL      │
[Microservice D] ──┤    (port 5432)     │  (80 connections)│
[Microservice E] ──┘                    └──────────────────┘
  (600 client connections)
```

PgBouncer receives the six hundred client connections, but maintains only eighty real connections toward PostgreSQL. When a client sends a query, PgBouncer assigns an available backend connection, executes the query, and — depending on the pooling mode — releases that connection for other clients.

## Transaction pooling vs session pooling: the choice that changes everything

PgBouncer supports three pooling modes. The two relevant ones in production are **session pooling** and **transaction pooling**.

**Session pooling**: a backend connection is assigned to a client for the entire duration of its session. The backend is released only when the client disconnects. It's the most compatible mode — it works with everything — but offers the least savings: if a client holds a session open without issuing queries, the backend is still occupied.

**Transaction pooling**: a backend connection is assigned to the client only for the duration of a transaction. As soon as the transaction ends (COMMIT or ROLLBACK), the backend returns to the pool and can be assigned to another client. This is the mode that makes it possible to serve six hundred clients with eighty real backends, because in practice most clients are idle between transactions.

The choice between the two isn't trivial. Transaction pooling has important constraints:

- **Session variables** (`SET search_path`, `SET timezone`, etc.) don't persist across different transactions
- **Named prepared statements** don't work transparently (covered in the dedicated section below)
- **Session-level advisory locks** don't work
- `LISTEN/NOTIFY` is not supported in transaction pooling

Session pooling is safer, but requires clients to disconnect when they're not needed — something application-level connection pools already do. In that case, the savings are real but less dramatic.

In our situation, the microservices used a standard ORM without named prepared statements, without advisory locks, without `LISTEN/NOTIFY`. Transaction pooling was the right choice.

## Installation and basic configuration

On a recent Debian/Ubuntu distribution, installation is straightforward [2]:

```bash
apt install pgbouncer
```

Configuration lives in two files: `pgbouncer.ini` and `userlist.txt`.

### `pgbouncer.ini`

```ini
[databases]
; "appdb" is the name of the virtual database exposed by PgBouncer
; clients connect using this name
appdb = host=127.0.0.1 port=5432 dbname=appdb

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 5432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt

; pooling mode
pool_mode = transaction

; real connections to PostgreSQL per pool
default_pool_size = 80

; maximum client connections accepted by PgBouncer
max_client_conn = 1000

; reserve pool for traffic spikes
reserve_pool_size = 10
reserve_pool_timeout = 5

; idle server-side connection timeout
server_idle_timeout = 600

; logging
logfile = /var/log/pgbouncer/pgbouncer.log
pidfile = /var/run/pgbouncer/pgbouncer.pid

; statistics
stats_period = 60
```

### `userlist.txt`

The file contains credentials in the format `"username" "password_hash"`. PgBouncer supports MD5 hashes in PostgreSQL format (`md5` + md5(password + username)):

```text
"app_user" "md5a1b2c3d4e5f6..."
"pgbouncer_admin" "md5..."
```

To generate the correct hash:

```bash
echo -n "passwordusername" | md5sum
# prefix "md5" to the result
```

After configuration, start PgBouncer and verify it connects correctly:

```bash
systemctl start pgbouncer
systemctl enable pgbouncer

# verify admin connection
psql -h 127.0.0.1 -p 5432 -U pgbouncer pgbouncer
```

## From six hundred to eighty: the numbers before and after

After deploying PgBouncer in transaction pooling mode, the numbers shifted substantially. Some representative measurements collected in the first few weeks:

| Metric | Before | After |
|---|---|---|
| Real connections to PostgreSQL | 580–620 | 65–80 |
| RAM used by PG backends | ~4.2 GB | ~600 MB |
| Load average (8 cores) | 12–18 | 3–5 |
| Average query latency (p50) | 180 ms | 22 ms |
| p99 latency | 4.2 s | 310 ms |
| Connection timeouts | frequent | none |

The latency reduction isn't only due to less connection contention. With fewer active backend processes, the kernel does less context switching, PostgreSQL manages smaller data structures, and `VACUUM` manages to complete its cycles without being constantly interrupted. It's a cascade effect.

Overall throughput — queries per second — increased by roughly 40%, even though the number of real connections had been reduced by nearly an order of magnitude. This is the part that often surprises people: fewer connections doesn't mean less work done, it means less overhead per unit of work.

## Prepared statements and transaction pooling: untangling the knot

The most common issue when migrating to PgBouncer in transaction pooling mode involves **prepared statements**.

In PostgreSQL, named prepared statements (`PREPARE name AS ...`) are tied to the session. In transaction pooling, each transaction can end up on a different backend — so a prepared statement created in a previous transaction doesn't exist on the new backend.

The result is an error like:

```text
ERROR: prepared statement "s1" does not exist
```

There are three approaches to handle this:

**1. Use anonymous prepared statements (protocol-level)**

Modern drivers like `libpq`, `asyncpg`, `psycopg3`, and JDBC support prepared statements at the protocol level without an explicit name. PgBouncer handles these transparently in transaction pooling. If the framework uses this mechanism (most modern ORMs do), there's no issue.

**2. Disable prepared statements on the application side**

If the driver or ORM uses named prepared statements, the simplest fix is to disable them. In SQLAlchemy, for example:

```python
engine = create_engine(
    "postgresql+psycopg2://user:pass@pgbouncer-host/appdb",
    execution_options={"no_parameters": True},
    # or with psycopg2:
    connect_args={"options": "-c statement_timeout=30000"}
)
```

With JDBC and the PostgreSQL driver:

```text
jdbc:postgresql://pgbouncer-host/appdb?prepareThreshold=0
```

`prepareThreshold=0` tells the driver never to use server-side prepared statements.

**3. Use `DEALLOCATE ALL` between transactions**

Less elegant, but it works: configure PgBouncer with `server_reset_query = DEALLOCATE ALL` to clean up prepared statements when a backend returns to the pool. Note: this adds latency to every connection release.

In our case, the microservices were using SQLAlchemy with psycopg2 and named prepared statements. The fix was adding the `prepareThreshold=0` equivalent to the driver configuration — a two-line change per service, deployed in an afternoon.

## The critical parameters to understand before going to production

Three parameters in `pgbouncer.ini` deserve specific attention [3]:

**`default_pool_size`**: the number of real connections to PostgreSQL maintained by PgBouncer for each (database, user) pair. It's the most important parameter. How to size it? A rule of thumb: `num_cores * 2` as a starting point, then measure. With eight cores, start at sixteen and increase until you find the saturation point. In our case, eighty connections on a server with sixteen cores and NVMe SSDs was the sweet spot.

**`max_client_conn`**: the maximum number of client connections PgBouncer accepts in total. It must be greater than the number of connections the clients can open. If six hundred clients each open one connection, `max_client_conn` must be at least six hundred — better a thousand for headroom. When this limit is exceeded, PgBouncer rejects new connections: an explicit error is better than a silent timeout.

**`reserve_pool_size`** and **`reserve_pool_timeout`**: the reserve pool is a set of additional connections PgBouncer can open when the main pool is exhausted. If a client waits more than `reserve_pool_timeout` seconds for a connection, PgBouncer draws from the reserve pool. It's a safety net for spikes, not a structural solution: if the reserve pool is regularly depleted, `default_pool_size` needs to go up.

A frequently overlooked parameter is **`server_idle_timeout`**: how many seconds of inactivity before PgBouncer closes a backend connection. The default is six hundred seconds (ten minutes). In environments with highly variable traffic — heavy during the day, near-zero at night — lowering it to one hundred fifty or two hundred seconds reduces the number of idle connections PostgreSQL keeps open during low-activity hours.

## Reading the numbers: SHOW STATS and SHOW POOLS

PgBouncer exposes an administration console accessible by connecting to the virtual database `pgbouncer`:

```bash
psql -h 127.0.0.1 -p 5432 -U pgbouncer_admin pgbouncer
```

The most useful command for day-to-day monitoring is `SHOW STATS` [4]:

```sql
SHOW STATS;
```

```text
 database | total_xact_count | total_query_count | total_received | total_sent | total_xact_time | total_query_time | total_wait_time | avg_xact_count | avg_query_count | avg_recv | avg_sent | avg_xact_time | avg_query_time | avg_wait_time
----------+------------------+-------------------+----------------+------------+-----------------+------------------+-----------------+----------------+-----------------+----------+----------+---------------+----------------+---------------
 appdb    |        284721043 |         284721043 |   182043219872 | 9823041928 |    492831029183 |     492831029183 |      1823041928 |            312 |             312 |   199823 |    10782 |          1732 |           1732 |             6
```

The key columns: `avg_wait_time` (average wait time for a backend connection — if it exceeds a few milliseconds, the pool is too small) and `avg_xact_time` (average transaction duration).

`SHOW POOLS` displays the real-time state of the pools:

```sql
SHOW POOLS;
```

```text
 database | user     | cl_active | cl_waiting | sv_active | sv_idle | sv_used | sv_tested | sv_login | maxwait | maxwait_us | pool_mode
----------+----------+-----------+------------+-----------+---------+---------+-----------+----------+---------+------------+-----------
 appdb    | app_user |       412 |          0 |        78 |       2 |       0 |         0 |        0 |       0 |          0 | transaction
```

- `cl_active`: clients with an assigned backend connection
- `cl_waiting`: clients waiting for a backend connection — if this number is consistently > 0, the pool is saturated
- `sv_active`: busy backends
- `sv_idle`: free backends in the pool
- `maxwait`: maximum wait time for a client (in seconds) — the primary alarm indicator

For automated monitoring, these values are easily scraped by any metrics system. Prometheus has a dedicated exporter (`pgbouncer_exporter`) that exposes all `SHOW STATS` and `SHOW POOLS` metrics in scrape format [5].

## What remains after the deploy

PgBouncer isn't a magic solution and doesn't eliminate the need to design the data access layer properly. If queries are slow, PgBouncer won't speed them up. If the database has lock contention issues, PgBouncer won't fix them. What it does is remove a specific bottleneck — the overhead of managing connections — which in microservice architectures quickly becomes the dominant problem.

Looking back at the numbers, what stands out is how straightforward the diagnosis was: the server had enough memory for the data, enough CPU for the queries, enough I/O for the writes. It was suffering from the pure overhead of managing six hundred OS processes simultaneously. PgBouncer moved that problem outside PostgreSQL, where it can be handled far more efficiently.

One point worth keeping in mind for future architectures: in a system with many microservices, connection pooling shouldn't be an afterthought. It should be part of the initial design, alongside the load balancer or the service mesh. The cost of adding it later — coordinating teams, managing the migration, testing prepared statement compatibility — is real, even if ultimately manageable.

The team went on to add PgBouncer as a standard component in the deploy template for all new services. It's no longer a decision to make case by case.

## Official sources

1. PostgreSQL Documentation — [Connections and Authentication: max_connections](https://www.postgresql.org/docs/current/runtime-config-connection.html)
2. PgBouncer Documentation — [Installation](https://www.pgbouncer.org/install.html)
3. PgBouncer Documentation — [Configuration file pgbouncer.ini](https://www.pgbouncer.org/config.html)
4. PgBouncer Documentation — [Usage: SHOW commands](https://www.pgbouncer.org/usage.html)
5. prometheus-community — [pgbouncer_exporter](https://github.com/prometheus-community/pgbouncer_exporter)

## Glossary
- **[PgBouncer](/en/glossary/pgbouncer/)** — Lightweight connection pooler for PostgreSQL, written in C with asynchronous I/O. It sits between clients and the database, maintaining a reduced pool of real connections to PostgreSQL and reusing them across many clients.

- **[Transaction pooling](/en/glossary/pgbouncer/)** — Pooling mode in which a backend connection is assigned to the client only for the duration of a transaction. As soon as the transaction ends, the backend returns to the pool and becomes available for other clients. Allows serving many clients with few real connections.

- **[Session pooling](/en/glossary/transaction-pooling/)** — Pooling mode in which a backend connection remains assigned to a client for the entire duration of its session. More compatible than transaction pooling, but less efficient because the backend is occupied even when the client is idle.

- **[`max_connections`](/en/glossary/pgbouncer/)** (PostgreSQL) — Configuration parameter that limits the maximum number of simultaneous connections PostgreSQL accepts. It's not an arbitrary limit: it reflects the real cost in memory and scheduling overhead of each backend process.

- **[`default_pool_size`](/en/glossary/transaction-pooling/)** (PgBouncer) — Number of real connections to PostgreSQL maintained by PgBouncer for each (database, user) pair. It's the primary parameter for sizing the pool: too low causes wait times, too high brings the excessive-connections problem back to PostgreSQL.
