---
title: "NOLOGGING"
description: "Oracle mode that suppresses redo log generation during bulk operations (CTAS, INSERT APPEND, ALTER TABLE MOVE), speeding up operations but requiring an immediate backup."
translationKey: "glossary_nologging"
articles:
  - "/posts/oracle/oracle-partitioning"
---

**NOLOGGING** is an Oracle mode that disables redo log generation during bulk load operations. Operations complete much faster, but the data is not recoverable via redo in case of a crash before a backup is taken.

## How it works

When a segment (table, index, partition) is in NOLOGGING mode, bulk operations like CTAS, `INSERT /*+ APPEND */` and `ALTER TABLE MOVE` do not write redo log for data blocks. On a 380 GB copy, this eliminates the generation of the same amount of redo, preventing archivelog area saturation and reducing times from days to hours.

## What it's for

NOLOGGING is essential for migration operations on large tables. Without NOLOGGING, a 380 GB CTAS would generate 380 GB of redo log, putting the system into archivelog mode for days. With NOLOGGING, the same operation completes in a few hours with minimal system impact.

## When to use it

Activate before the bulk operation and deactivate immediately after (`ALTER TABLE ... LOGGING`). An RMAN backup must be run immediately afterwards, because NOLOGGING segments are not recoverable with a restore from redo. Never leave NOLOGGING permanently active on production tables.
