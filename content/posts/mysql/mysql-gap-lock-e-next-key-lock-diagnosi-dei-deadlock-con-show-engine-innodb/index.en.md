---
categories:
- mysql
date: '2026-11-03'
description: 'InnoDB gap locks and next-key locks explained on a real case: deadlocks
  on concurrent INSERTs, diagnosis with SHOW ENGINE INNODB STATUS, and when READ COMMITTED
  fixes everything.'
draft: false
image: mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb.cover.jpg
seoTitle: 'MySQL InnoDB gap locks and next-key locks: deadlock diagnosis'
tags:
- innodb
- locking
- deadlock
- isolation-level
- concurrency
title: 'MySQL gap locks and next-key locks: diagnosing and fixing deadlocks'
translationKey: mysql_gap_lock_e_next_key_lock_diagnosi_dei_deadlock_con_show_engine_innodb
webo_generated_at: 2026-10-21
webo_status: scheduled
---

## The Tuesday morning meeting

It was a Tuesday morning, and the meeting had started badly. On one side, the development team; on the other, the customer's DBA — a national postal and logistics operator running roughly fifteen hundred MySQL instances across as many nodes. The parcel tracking system was generating sporadic deadlocks on INSERTs, around three or four a day under normal load, many more during peak sorting periods.

The developers had brought the application logs: "the database is blocking our INSERTs for no reason." The DBA had brought the utilization graphs: "the queries are poorly written and doing range scans on enormous tables." Both were right about something. Both were wrong about the cause.

The problem was InnoDB's gap locks — a mechanism that most teams know by name but don't truly understand until they run into it in production.

## Record locks, gap locks, next-key locks: three different things

Before getting into the specific case, it's worth clarifying the terminology, because InnoDB uses three distinct lock types that are frequently confused.

A **record lock** locks a single row in the index. If you run `SELECT ... FOR UPDATE WHERE id = 42`, InnoDB places a record lock on the row with `id = 42`. Straightforward.

A **gap lock** locks an *interval* between two index values — the "gap" between two existing records — without locking the records themselves. If the index contains values 10, 20, 30, a gap lock on the interval (10, 20) prevents any other transaction from inserting a value into that interval. The key point: a gap lock doesn't block existing records, it blocks the space between them.

A **next-key lock** is the combination of the two: a record lock on the current record plus a gap lock on the interval preceding it. This is the default lock type InnoDB uses for index scans under `REPEATABLE READ`. If you do a range scan touching values 10, 20, 30, InnoDB places next-key locks on (-∞, 10], (10, 20], (20, 30], (30, +∞). You're locking not just the records you read, but all the gaps between them.

Why does InnoDB do this? To prevent **phantom reads** — the situation where a transaction reads a range twice and gets different results because another transaction inserted rows in between. Under `REPEATABLE READ`, the SQL standard requires this not to happen, and InnoDB enforces it by locking the gaps.

```sql
-- Example: this query under REPEATABLE READ
-- acquires next-key locks on the scanned interval
SELECT * FROM shipment_log
WHERE status = 'PENDING' AND created_at > '2024-01-15 08:00:00'
FOR UPDATE;
```

The problem arises when two transactions do range scans on overlapping intervals and then both try to INSERT into the same gap. Classic deadlock.

## Why REPEATABLE READ is the context where everything blows up

MySQL uses `REPEATABLE READ` as its default isolation level [1]. It's a historical choice tied to statement-based replication — under `READ COMMITTED`, certain binlog replication patterns could produce inconsistencies on the replica. With row-based replication (the default since MySQL 5.7.7) that concern is largely moot, but the default has stayed.

Under `REPEATABLE READ`, InnoDB must guarantee that a transaction always sees the same snapshot of the data for its entire duration. For plain reads (without `FOR UPDATE`) it uses MVCC — reading a historical version of the data without acquiring locks. But for locking reads (`SELECT ... FOR UPDATE`, `SELECT ... LOCK IN SHARE MODE`) and write operations, it has to use next-key locks to prevent phantoms.

The pattern generating deadlocks in the parcel tracking case looked like this:

1. Transaction A: searches for parcels in `PENDING` status within a certain time interval → acquires next-key locks on a range of the index
2. Transaction B: does the same on an overlapping range → acquires next-key locks on a partially overlapping range
3. Transaction A: tries to insert a new audit record → the record falls in the gap locked by B → waits
4. Transaction B: tries to insert a new audit record → the record falls in the gap locked by A → waits
5. InnoDB detects the cycle and kills one of the two transactions

There was nothing inherently wrong with the application code. The problem was the interaction between the access pattern (range scan + INSERT into the same gap) and the default isolation level.

## Diagnosis: SHOW ENGINE INNODB STATUS

When you suspect a deadlock in MySQL, the first tool is `SHOW ENGINE INNODB STATUS` [2]. The section to look at is `LATEST DETECTED DEADLOCK`, which shows the last deadlock InnoDB detected with full details: the transactions involved, the locks they held, the locks they were waiting for, and which transaction was chosen as the victim.

```sql
SHOW ENGINE INNODB STATUS\G
```

The output is verbose and needs careful reading. A simplified example of what you find in the deadlock section:

```text
------------------------
LATEST DETECTED DEADLOCK
------------------------
2024-01-16 09:23:41 0x7f8b4c001700
*** (1) TRANSACTION:
TRANSACTION 421938, ACTIVE 0 sec inserting
mysql tables in use 1, locked 1
LOCK WAIT 4 lock struct(s), heap size 1136, 2 row lock(s)
MySQL thread id 1842, OS thread handle 140234..., query id 98234 ...
INSERT INTO shipment_log (shipment_id, status, created_at)
VALUES (10045, 'PROCESSING', NOW())

*** (1) HOLDS THE LOCK(S):
RECORD LOCKS space id 312 page no 4 n bits 72 index idx_status_created
of table `tracking`.`shipment_log` trx id 421938 lock_mode X locks gap before rec

*** (1) WAITING FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS space id 312 page no 4 n bits 72 index idx_status_created
of table `tracking`.`shipment_log` trx id 421938 lock_mode X locks gap before rec insert intention waiting

*** (2) TRANSACTION:
TRANSACTION 421939, ACTIVE 0 sec inserting
...
*** (2) HOLDS THE LOCK(S):
RECORD LOCKS ... lock_mode X locks gap before rec

*** (2) WAITING FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS ... lock_mode X locks gap before rec insert intention waiting

*** WE ROLL BACK TRANSACTION (2)
```

The key phrases to look for: `lock_mode X locks gap before rec` (gap lock acquired) and `insert intention waiting` (INSERT waiting to enter a locked gap). When you see both in a deadlock, you're looking at exactly the gap lock / INSERT intention lock pattern.

Another useful tool, available since MySQL 5.6, is the `performance_schema.data_locks` table (or `information_schema.INNODB_LOCKS` in older versions):

```sql
-- MySQL 8.0+
SELECT
    r.trx_id AS waiting_trx,
    r.trx_mysql_thread_id AS waiting_thread,
    r.trx_query AS waiting_query,
    b.trx_id AS blocking_trx,
    b.trx_mysql_thread_id AS blocking_thread,
    b.trx_query AS blocking_query
FROM information_schema.INNODB_TRX b
JOIN information_schema.INNODB_TRX r
    ON r.trx_id != b.trx_id
JOIN performance_schema.data_locks dl
    ON dl.ENGINE_TRANSACTION_ID = r.trx_id
    AND dl.LOCK_STATUS = 'WAITING'
WHERE b.trx_id = dl.BLOCKING_ENGINE_TRANSACTION_ID;
```

## The case reconstructed step by step

The table involved had a structure similar to this:

```sql
CREATE TABLE shipment_log (
    id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    shipment_id BIGINT UNSIGNED NOT NULL,
    status      VARCHAR(20) NOT NULL,
    created_at  DATETIME NOT NULL,
    INDEX idx_status_created (status, created_at)
);
```

The application code, simplified, did the following within a single transaction:

```sql
-- Step 1: find recent records in PENDING status
SELECT id, shipment_id FROM shipment_log
WHERE status = 'PENDING'
  AND created_at > NOW() - INTERVAL 5 MINUTE
FOR UPDATE;

-- Step 2: update the status of the found records
UPDATE shipment_log SET status = 'PROCESSING'
WHERE id IN (...);

-- Step 3: insert an audit record
INSERT INTO shipment_log (shipment_id, status, created_at)
VALUES (?, 'PROCESSING', NOW());
```

The `FOR UPDATE` in step 1 was intentional — the team wanted to prevent two parallel workers from processing the same parcel. Reasonable. The problem is that `SELECT ... FOR UPDATE` with the condition `created_at > NOW() - INTERVAL 5 MINUTE` acquired next-key locks across the entire range of the `idx_status_created` index for `created_at` values in the last five minutes. And the INSERT in step 3 inserted a record with `created_at = NOW()` — exactly in the gap locked by the other concurrent transaction.

Two workers starting milliseconds apart would get stuck together, consistently.

## READ COMMITTED: when it's the right answer

The most direct solution, in this specific case, was to lower the isolation level to `READ COMMITTED` for those transactions [3]:

```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

Under `READ COMMITTED`, InnoDB doesn't use gap locks for reads. It uses only record locks on the rows actually found. The reason is that phantom reads are permitted in `READ COMMITTED` — each statement sees the data committed at the moment of its own execution, not at the start of the transaction. Without the need to prevent phantoms, gap locks aren't needed, and the deadlock pattern disappears.

The legitimate question is: is it safe? It depends on the context, and the trade-offs are worth spelling out explicitly.

`READ COMMITTED` is safe when:
- The application logic doesn't depend on the stability of a range between two reads within the same transaction (meaning you don't care if another transaction inserts rows in between)
- You're using row-based replication (the default since MySQL 5.7.7) — with statement-based replication, `READ COMMITTED` can produce inconsistencies on the replica in certain UPDATE/DELETE with subquery scenarios [4]
- Phantom reads are not a problem for the application's semantics

In the parcel tracking case, the answer to all three questions was yes. The worker didn't need a stable range — it needed to process the parcels available at that moment, not to guarantee that no other parcel had appeared in between. Replication was row-based. Phantom reads were irrelevant to the correctness of the system.

The change was made at the session level in the connection pool, not globally — a conservative choice that allowed `REPEATABLE READ` to remain the default for the rest of the system.

## Patterns for reducing deadlocks without changing the isolation level

`READ COMMITTED` isn't always the answer. When changing the isolation level isn't possible or desirable, other patterns can reduce the likelihood of deadlocks.

**Consistent access ordering.** Most classic deadlocks (not from gap locks) arise from transactions accessing the same resources in different orders. If transaction A locks table X first then Y, and transaction B does the reverse, a deadlock is almost guaranteed. Standardizing the order in which resources are accessed eliminates this class of problems.

**Smaller batch sizes.** Range scans over large intervals acquire gap locks over large intervals. Reducing the query's time window (from 5 minutes to 30 seconds, for example) reduces the width of the gap locks and the probability of overlap.

```sql
-- Instead of:
WHERE status = 'PENDING' AND created_at > NOW() - INTERVAL 5 MINUTE

-- Consider:
WHERE status = 'PENDING' AND created_at > NOW() - INTERVAL 30 SECOND
  AND created_at <= NOW() - INTERVAL 5 SECOND  -- avoid the most recent window
```

**Application-level retry logic.** Deadlocks in InnoDB are normal events, not anomalies. InnoDB always picks a victim and rolls back one of the transactions — the application needs to be ready to retry. A robust pattern uses retry with exponential backoff and a maximum number of attempts:

```python
import time
import random
import mysql.connector

def execute_with_retry(conn, fn, max_retries=3):
    for attempt in range(max_retries):
        try:
            return fn(conn)
        except mysql.connector.errors.DatabaseError as e:
            if e.errno == 1213 and attempt < max_retries - 1:
                # ER_LOCK_DEADLOCK — retry with backoff
                wait = (2 ** attempt) + random.uniform(0, 0.5)
                time.sleep(wait)
                continue
            raise
```

**Selective indexes on the lock column.** If `FOR UPDATE` is necessary, a more selective index reduces the number of rows (and gaps) involved in the scan. In this specific case, adding `shipment_id` to the index and filtering by a specific worker would have drastically reduced the width of the locked range.

## What remains after the meeting

The switch to `READ COMMITTED` at the session level eliminated the deadlocks within an hour of the deploy. Not magic — a direct consequence of understanding what was happening under the hood.

The most useful thing to come out of that week of analysis wasn't the fix itself, but the method: reading `SHOW ENGINE INNODB STATUS` carefully, understanding the difference between record locks and gap locks, and not assuming that MySQL's default is always the right choice for your use case. `REPEATABLE READ` is a conservative and correct choice in many contexts. In others — like concurrent workers doing range scans plus INSERTs — it's the direct cause of the problem.

The customer's DBA added deadlock monitoring to their alerting system — a periodic query on `information_schema.INNODB_METRICS` tracking the `lock_deadlocks` counter. The developers added retry logic. Both were necessary, and neither alone would have been enough.

## Official sources

1. MySQL Documentation — [InnoDB Transaction Isolation Levels](https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-isolation-levels.html)
2. MySQL Documentation — [SHOW ENGINE INNODB STATUS](https://dev.mysql.com/doc/refman/8.0/en/innodb-standard-monitor.html)
3. MySQL Documentation — [InnoDB Locking: Gap Locks](https://dev.mysql.com/doc/refman/8.0/en/innodb-locking.html#innodb-gap-locks)
4. MySQL Documentation — [Binary Logging Formats and READ COMMITTED](https://dev.mysql.com/doc/refman/8.0/en/binary-log-formats.html)

## Glossary
- **[Gap lock](/en/glossary/gap-lock/)** (InnoDB) — a lock that blocks an interval between two index values, without locking the records themselves. Prevents INSERTs into the locked interval. Active under `REPEATABLE READ`, absent under `READ COMMITTED`.

- **[Next-key lock](/en/glossary/gap-lock/)** (InnoDB) — a combination of a record lock on the current record and a gap lock on the interval preceding it. The default lock type for index scans under `REPEATABLE READ`; prevents phantom reads.

- **[Insert intention lock](/en/glossary/next-key-lock/)** (InnoDB) — an intention lock acquired by an INSERT before placing a record into a gap. Compatible with other insert intention locks on the same gap, but blocked by existing gap locks. The direct cause of deadlocks from concurrent INSERTs.

- **[REPEATABLE READ](/en/glossary/gap-lock/)** — the default isolation level in MySQL/InnoDB. Guarantees that a transaction always sees the same snapshot of the data for its entire duration; implemented via MVCC for reads and next-key locks for locking operations.

- **[Phantom read](/en/glossary/next-key-lock/)** — a concurrency anomaly where a transaction reads a range twice and gets different results because another transaction inserted or deleted rows in between. Prevented by `REPEATABLE READ` via gap locks; permitted under `READ COMMITTED`.
