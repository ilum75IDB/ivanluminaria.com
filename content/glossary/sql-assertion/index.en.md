---
title: "ASSERTION"
description: "SQL standard construct to express cross-table constraints validated at transactional level by the database engine. Announced in Oracle 26ai."
translationKey: "glossary_sql_assertion"
aka: "SQL ASSERTION (cross-table constraint)"
articles:
  - "/posts/oracle/enum-oracle-workaround-fino-a-23ai"
  - "/posts/oracle/enum-oracle-19c-26ai-domini"
---

The **`ASSERTION`** is a construct defined by the SQL standard — since the 1990s — to express constraints that **span multiple tables**, validated directly by the database engine at the transactional level. On paper it's an elegant solution to problems that today are solved with triggers or application-level checks. In practice, up to 2026, no mainstream DBMS had truly implemented it. Oracle has announced it for 26ai.

## How it works (on paper)

`CREATE ASSERTION name CHECK (<condition>)` defines a condition that the database always guarantees to be true. Unlike a table `CHECK` (which evaluates a single row at INSERT/UPDATE time), an `ASSERTION` can reference **multiple tables**, do aggregations, count rows. Examples: "at least one row in `statuses_x` must have `active='Y'`", or "the sum of amounts in `order_line` cannot exceed the `total` in `order`".

## Why it took so long

Implementing `ASSERTION`s efficiently is hard. On every modification of the involved tables, the engine must revalidate the assertion — and doing so without serializing all transactions requires sophisticated mechanisms of incremental checking or cross-table locking. No vendor has ever found the winning formula. Oracle 26ai will be the first serious attempt on a major commercial DBMS.

## What changes for those who model enumerations

For lookup-table-managed taxonomies, `ASSERTION`s open a new scenario: constraints that today live as application triggers (e.g. "the taxonomy cannot be left without active statuses") will become expressible in DDL, validated at the transactional level, managed by the engine. This is material to be developed when the 26ai implementation is available in testing.
