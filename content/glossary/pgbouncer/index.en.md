---
title: "PgBouncer"
description: "Lightweight connection pooler for PostgreSQL that reduces connection overhead by maintaining a small pool of real database connections shared across many clients."
translationKey: "glossary_pgbouncer"
aka: "PgBouncer (PostgreSQL Connection Pooler)"
articles:
  - "/posts/postgresql/pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600"
---

PgBouncer is a lightweight connection pooler for PostgreSQL, written in C with asynchronous I/O. It sits between clients and the database, maintaining a small pool of real connections to PostgreSQL and reusing them across many concurrent clients, eliminating the per-connection fork and authentication overhead.

## How it works

PgBouncer intercepts incoming connections and maps them onto a subset of already-open real connections to PostgreSQL. It supports three pooling modes:

- **Session pooling**: a real connection is assigned to the client for the entire session lifetime.
- **Transaction pooling**: the real connection is returned to the pool after each COMMIT or ROLLBACK. This is the most efficient mode but is incompatible with certain stateful features (server-side prepared statements, `SET LOCAL`, advisory locks).
- **Statement pooling**: connection released after every single statement. Rarely used in production.

Minimal configuration is done via a `.ini` file:

```ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
```

## When to use it

PgBouncer is the right tool when the number of client connections exceeds what PostgreSQL can sustain comfortably (typically beyond 200–300 active connections), or when stateless workloads such as workers or microservices open and close connections at high frequency. It does not replace proper connection management on the application side, but it mitigates the impact under heavy load.

In transaction pooling mode, parameters like `server_reset_query` and the handling of prepared statements require careful attention to avoid unexpected behaviour.
