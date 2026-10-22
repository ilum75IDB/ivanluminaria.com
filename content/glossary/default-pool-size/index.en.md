---
title: "default_pool_size"
description: "PgBouncer parameter defining the number of real PostgreSQL connections maintained per database/user pair, crucial for sizing the connection pool."
translationKey: "glossary_default_pool_size"
aka: null
articles:
  - "/posts/postgresql/pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600"
---

`default_pool_size` is a fundamental parameter in PgBouncer, a lightweight and high-performance connection pooler for PostgreSQL. This parameter determines the maximum number of *real* connections that PgBouncer maintains open to the PostgreSQL server for each unique combination of database and user. It is central to correctly sizing the connection pool and ensuring efficient resource management.

## What it does and how it works

PgBouncer acts as an intermediary between client applications and the PostgreSQL server. Instead of having PostgreSQL open a new connection for every client request, PgBouncer maintains a pool of pre-existing connections and reuses them. The `default_pool_size` parameter controls the size of this pool for each specific (database, user) pair.

For example, if `default_pool_size` is set to `20` and PgBouncer manages connections for `db1` with `user_a` and `db2` with `user_b`, it will maintain up to 20 connections for `(db1, user_a)` and another 20 for `(db2, user_b)`. This mechanism reduces the overhead of creating and closing connections, improving performance and scalability. The parameter applies regardless of the `pool_mode` (Session, Transaction, Statement).

Here's an example configuration in `pgbouncer.ini`:

```ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb
anotherdb = host=127.0.0.1 port=5432 dbname=anotherdb

[pgbouncer]
default_pool_size = 20
pool_mode = transaction
```

## Impact and sizing

Correctly sizing `default_pool_size` is crucial for the overall system performance:

*   **Value too low**: If the number of available connections in the pool is insufficient for concurrent requests, clients will have to wait for a connection to become free. This introduces latency, reduces throughput, and can cause bottlenecks.
*   **Value too high**: An excessive `default_pool_size` leads PgBouncer to open too many connections to PostgreSQL. This can overload the database server itself, consuming memory and CPU for connection management, and potentially nullifying the benefits of pooling.

Optimal sizing depends on various factors: the workload (number of queries per second, transaction duration), the number of concurrent clients, the `pool_mode` used (Transaction pooling generally allows for smaller, more efficient pools), and the hardware resources of the PostgreSQL server. It is advisable to monitor PgBouncer statistics (e.g., `SHOW STATS`, `SHOW POOLS`) to observe `waiting_clients` and pool utilization, and adjust the value based on actual needs.
