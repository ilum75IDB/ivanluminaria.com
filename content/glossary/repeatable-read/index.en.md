---
title: "REPEATABLE READ"
description: "MySQL/InnoDB default isolation level: guarantees a consistent snapshot for the entire transaction duration via MVCC and next-key locks."
translationKey: "glossary_repeatable_read"
aka: "Repeatable Read Isolation Level"
articles:
  - "/posts/mysql/mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb"
---

REPEATABLE READ is the default isolation level in MySQL/InnoDB. A transaction running at this level always sees the same data snapshot from the moment of its first SELECT, regardless of how many changes other clients COMMIT in the meantime.

## How it works

InnoDB implements REPEATABLE READ on two separate tracks:

- **Non-locking reads (consistent read):** handled by MVCC. Each row maintains a version chain; the transaction reads the version valid at snapshot time, ignoring subsequent writes.
- **Locking reads and writes:** rely on physical locks. InnoDB applies **next-key locks** (record lock + gap lock) to prevent phantom rows from appearing between one `SELECT ... FOR UPDATE` and the next within the same transaction.

```sql
-- The transaction always sees the same snapshot
START TRANSACTION;
SELECT * FROM orders WHERE status = 'open';  -- snapshot fixed here
-- ... other operations ...
SELECT * FROM orders WHERE status = 'open';  -- identical result set
COMMIT;
```

## When to use it and trade-offs

REPEATABLE READ suits most OLTP workloads: balance checks, intra-transaction reports, multi-step operations that require stable data. The main cost is next-key locking, which widens the lock surface compared to READ COMMITTED and raises the risk of deadlocks on concurrent INSERTs. If the application does not need phantom-read protection, dropping to READ COMMITTED reduces contention.
