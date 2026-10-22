---
title: "Session pooling"
description: "Pooling mode where a backend connection stays assigned to a client for the entire session: more compatible but less efficient than transaction pooling."
translationKey: "glossary_session_pooling"
aka: "Session-level pooling"
articles:
  - "/posts/postgresql/pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600"
---

In session pooling, a backend connection is reserved for a client from the moment it connects until it disconnects. This is the mode closest to a direct connection and offers the highest compatibility with features that rely on session state: `SET` variables, cursors, temporary tables, and named prepared statements.

## How it works

The pool manager (e.g. PgBouncer) assigns a backend connection to the client at login and keeps it exclusively reserved for the lifetime of that session. No other client can use it in the meantime, even if the client is idle.

PgBouncer configuration:

```ini
[pgbouncer]
pool_mode = session
```

The maximum number of simultaneous database connections therefore equals the number of active clients, which limits the efficiency gain compared to direct connections.

## When to use it

Session pooling is the right choice when the application relies on persistent session state: ORMs that issue `SET search_path`, drivers that use named prepared statements, or legacy code that expects session variables to survive across queries.

It is less efficient than transaction pooling because the backend remains occupied even during client idle periods. In high-concurrency scenarios, the main advantage over direct connections is reduced authentication overhead and fewer backend process forks — not true connection multiplexing.
