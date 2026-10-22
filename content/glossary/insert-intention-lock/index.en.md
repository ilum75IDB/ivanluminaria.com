---
title: "Insert Intention Lock"
description: "Intention lock acquired by INSERT before writing into a gap. Compatible with other insert intention locks, blocked by existing gap locks."
translationKey: "glossary_insert_intention_lock"
aka: "Insert Intention Gap Lock"
articles:
  - "/posts/mysql/mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb"
---

An **Insert Intention Lock** is a special type of gap lock that InnoDB acquires whenever a transaction executes an `INSERT` into a gap between two index values. Multiple insert intention locks on the same gap are mutually compatible — concurrent inserts targeting the same interval can proceed in parallel — but any existing gap lock or next-key lock on that gap will block them.

## How it works

Before writing a new record, InnoDB places an insert intention lock on the target gap. If another transaction already holds a gap lock over the same range (for instance, from a `SELECT ... FOR UPDATE` on a range predicate), the `INSERT` waits until that lock is released.

```sql
-- Transaction A: acquires a gap lock on the interval (10, 20)
SELECT * FROM orders WHERE id BETWEEN 10 AND 20 FOR UPDATE;

-- Transaction B: tries to insert into the same interval, waits for A's gap lock
INSERT INTO orders (id, status) VALUES (15, 'new');
```

The compatibility between insert intention locks is by design: it allows high-concurrency inserts into the same gap without unnecessary serialization, as long as the inserted rows do not collide on the same key.

## Deadlocks from concurrent INSERTs

The most common deadlock pattern involving insert intention locks occurs when two transactions each acquire a gap lock — typically from a `SELECT ... FOR UPDATE` that returns no rows — and then both attempt to insert into the same gap. Each waits for the other to release its gap lock, creating a cycle that InnoDB detects and resolves by rolling back one of the transactions.

```sql
-- Typical deadlock sequence
-- T1: SELECT ... FOR UPDATE on gap → gap lock acquired
-- T2: SELECT ... FOR UPDATE on same gap → gap lock acquired
-- T1: INSERT into gap → waits for T2's gap lock
-- T2: INSERT into gap → waits for T1's gap lock → DEADLOCK
```

To diagnose this scenario, inspect the output of `SHOW ENGINE INNODB STATUS`: the relevant lock modes appear as `LOCK_MODE: X,GAP` and `LOCK_MODE: X,INSERT_INTENTION`.
