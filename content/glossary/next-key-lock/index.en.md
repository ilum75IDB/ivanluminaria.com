---
title: "Next-key lock"
description: "InnoDB locking mechanism combining a record lock and a gap lock to prevent phantom reads under REPEATABLE READ index scans."
translationKey: "glossary_next_key_lock"
aka: "Next-key locking"
articles:
  - "/posts/mysql/mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb"
---

A **next-key lock** is InnoDB's default locking strategy during index scans under `REPEATABLE READ`. It combines a **record lock** on the current row with a **gap lock** on the open interval immediately preceding it, forming the half-open range `(previous_value, current_value]`.

## How it works

When a query acquires a next-key lock on a record with value `42`, it locks both the record `42` and the interval `(x, 42]`, where `x` is the immediately preceding value in the index. No other transaction can insert a value into that interval until the lock is released.

```sql
-- This SELECT under REPEATABLE READ acquires next-key locks
-- on every returned record and on the gaps between them
SELECT * FROM orders WHERE status = 'open' FOR SHARE;
```

On the record with the highest index value, InnoDB extends the next-key lock up to the internal `supremum` sentinel, covering all future values that could be inserted beyond the current maximum.

## When it applies

Next-key locks are active by default in `REPEATABLE READ` and ensure that re-reading the same query within the same transaction always returns identical results, preventing **phantom reads**. Under `READ COMMITTED`, gap locks are released after predicate evaluation, reducing contention at the cost of phantom read exposure.

Next-key locks are the most common source of deadlocks in applications that run concurrent INSERT and SELECT operations on the same index: two transactions can hold overlapping gap locks and block each other when both attempt an INSERT into the same interval.
