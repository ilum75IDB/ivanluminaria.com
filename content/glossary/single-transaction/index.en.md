---
title: "--single-transaction"
description: "mysqldump flag that opens a REPEATABLE READ transaction to export InnoDB data consistently, without acquiring table-level locks."
translationKey: "glossary_single_transaction"
aka: null
articles:
  - "/posts/mysql/articolo-mysql-patching-mysql-8-0-dal-backup-alla-verifica-passo-per-passo"
---

`--single-transaction` is a `mysqldump` option that opens a `REPEATABLE READ` transaction before the export begins. InnoDB's isolation guarantees a consistent snapshot of the data without blocking concurrent writes.

## How it works

At dump startup, MySQL implicitly issues `START TRANSACTION WITH CONSISTENT SNAPSHOT`. All subsequent reads happen within that single transaction, seeing data exactly as it was at the moment the snapshot was taken. Concurrent DML operations (INSERT, UPDATE, DELETE) continue uninterrupted because InnoDB isolates them through MVCC.

```bash
mysqldump --single-transaction --routines --events \
  -u root -p my_database > backup.sql
```

The resulting file contains a logically consistent dump, equivalent to a point-in-time snapshot.

## When to use it and limitations

`--single-transaction` is the standard choice for InnoDB databases in production: it avoids table-level locks that would stall applications. It does not apply to **MyISAM** or **MEMORY** tables, which have no transaction support. For those engines, `--lock-tables` is required, acquiring a shared lock for the entire duration of the dump.

When a schema contains mixed storage engines, the two flags are mutually exclusive: `--single-transaction` automatically disables `--lock-tables`. Non-transactional tables included in the dump may therefore be inconsistent relative to the InnoDB tables.

## Operational notes

For large dumps, the open transaction can accumulate significant undo log entries in InnoDB. Monitoring `innodb_history_list_length` during long backup operations is a sound practice to avoid pressure on the undo tablespace.
