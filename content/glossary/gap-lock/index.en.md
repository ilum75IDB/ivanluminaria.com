---
title: "Gap Lock"
description: "InnoDB Gap Lock blocks an index range to prevent INSERT within that range. Active under REPEATABLE READ, disabled under READ COMMITTED."
translationKey: "glossary_gap_lock"
aka: "Gap Lock (InnoDB)"
articles:
  - "/posts/mysql/mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb"
---

A Gap Lock is an InnoDB locking mechanism that protects an **interval** between two index values without locking the records that bound that interval. Its primary purpose is to prevent other transactions from inserting rows into the protected range, preserving read consistency.

## How it works

When a transaction reads a range using `SELECT ... FOR UPDATE` or `SELECT ... LOCK IN SHARE MODE`, InnoDB may acquire a Gap Lock on the interval between the involved index values. No physical record is locked: the lock exists only on the "gap" between values.

```sql
-- Transaction A: reads rows with id between 10 and 20
SELECT * FROM orders WHERE id BETWEEN 10 AND 20 FOR UPDATE;

-- Transaction B: tries to insert id = 15 → blocked by the Gap Lock
INSERT INTO orders (id, status) VALUES (15, 'new');
```

Two Gap Locks on the same interval are **compatible with each other**: the conflict arises only with INSERT attempts targeting the protected range.

## Operational context

Gap Locks are active exclusively under the `REPEATABLE READ` isolation level (InnoDB default). Switching to `READ COMMITTED` causes InnoDB to release Gap Locks after each statement, reducing contention but exposing the transaction to non-repeatable reads and phantom reads.

In high-concurrency systems with frequent INSERT operations, Gap Locks are a common source of deadlocks: two transactions can hold overlapping Gap Locks and then block each other when attempting to insert. Diagnosing these scenarios requires analyzing the output of `SHOW ENGINE INNODB STATUS`.
