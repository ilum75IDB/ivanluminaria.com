---
title: "Transaction Pooling"
description: "Connection pooling mode where a backend is assigned to a client only for the duration of a transaction, maximizing reuse of real database connections."
translationKey: "glossary_transaction_pooling"
aka: "Transaction-level pooling"
articles:
  - "/posts/postgresql/pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600"
---

Transaction Pooling is the most aggressive pooling mode available in tools like PgBouncer: a physical connection to the PostgreSQL backend is assigned to a client only for as long as it takes to complete a single transaction. The moment a COMMIT or ROLLBACK is issued, the backend returns to the pool and becomes available to any other waiting client.

## How it works

From the client's perspective, the connection appears persistent. Under the hood, the pooler tracks transaction boundaries and reassigns the physical backend at each cycle. With 1000 connected clients and short-lived transactions, 20–50 real PostgreSQL connections can be sufficient.

The key PgBouncer setting is `pool_mode = transaction`, configurable globally or per database:

```ini
[databases]
mydb = host=127.0.0.1 port=5432 pool_mode=transaction
```

## When to use it and its limits

This is the standard choice for high-concurrency web applications — typically a backend with its own connection pool sitting behind PgBouncer, which in turn connects to PostgreSQL. It dramatically reduces the number of active backend processes, cutting memory usage and context switching overhead.

The trade-offs are concrete: any feature that relies on server-side session state — server-side prepared statements, `SET` session variables, advisory locks, `WITH HOLD` cursors — breaks under Transaction Pooling because the backend session changes between transactions. The solution is either to switch to Session Pooling for those workloads or to disable the incompatible features at the application layer.
