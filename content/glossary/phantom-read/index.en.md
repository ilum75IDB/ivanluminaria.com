---
title: "Phantom Read"
description: "Concurrency anomaly where a transaction reads a range twice and gets different results because another transaction inserted or deleted rows in between."
translationKey: "glossary_phantom_read"
aka: null
articles:
  - "/posts/mysql/mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb"
---

A **Phantom Read** occurs when a transaction executes the same range query twice and receives different result sets, because a concurrent transaction has inserted or deleted rows within that range in the meantime. The "phantom" label is apt: rows appear or disappear without the current transaction having touched them.

## How it works

The classic sequence involves two concurrent transactions:

```sql
-- Transaction A
BEGIN;
SELECT * FROM orders WHERE amount > 1000;
-- returns 5 rows

-- Transaction B (concurrently)
INSERT INTO orders (amount) VALUES (1500);
COMMIT;

-- Transaction A, same query
SELECT * FROM orders WHERE amount > 1000;
-- now returns 6 rows → phantom read
COMMIT;
```

Transaction A changed nothing, yet the result set differs. This is distinct from a **Non-Repeatable Read**, which involves modification of rows already read, not the addition or removal of rows within the scanned range.

## Isolation levels and prevention

`READ COMMITTED` allows phantom reads: each SELECT sees a snapshot current as of its own execution time. `REPEATABLE READ` — InnoDB's default — prevents them through **gap locks** and **next-key locks**, which lock index intervals and block concurrent INSERT statements within the read range. `SERIALIZABLE` provides the strongest guarantee by converting implicit SELECTs into blocking reads.

Choosing `READ COMMITTED` in high-concurrency workloads reduces the risk of gap-lock deadlocks but exposes the application to phantom reads — a trade-off that depends on the business logic requirements.
