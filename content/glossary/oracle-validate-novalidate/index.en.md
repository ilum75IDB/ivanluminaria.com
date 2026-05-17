---
title: "VALIDATE / NOVALIDATE"
description: "Oracle modes for applying a constraint at creation or modification time: VALIDATE checks all existing rows, NOVALIDATE skips the check."
translationKey: "glossary_oracle_validate_novalidate"
aka: "Constraint validation modes (Oracle)"
articles:
  - "/posts/oracle/enum-oracle-19c-26ai-domini"
---

**`VALIDATE`** and **`NOVALIDATE`** are the two modes Oracle Database uses when applying a constraint (CHECK, FK, UNIQUE, NOT NULL, and from 23ai also `SQL DOMAIN`) at the moment the constraint itself is **created or modified**. The difference concerns only the **rows already present** in the table: anything inserted or updated afterwards is always checked by the engine.

## How it works

You specify it as a clause option on `CREATE TABLE`, `ALTER TABLE ADD CONSTRAINT`, `ALTER TABLE MODIFY` or `ALTER DOMAIN`. `VALIDATE` (default) does a **full scan** of the table to verify every row respects the constraint; if even one violates, the operation fails with `ORA-02293`. `NOVALIDATE` skips the scan and accepts the current state "as is": the constraint is marked as enforced going forward, but the data dictionary reports it as **not validated** (`STATUS = ENABLED NOVALIDATE` in `DBA_CONSTRAINTS`).

## When to use NOVALIDATE

Typically on **very large tables** during tight maintenance windows, where the validation scan would cost hours of blocking. You apply `NOVALIDATE`, guarantee integrity going forward, and do a follow-up cleanup via background batch script. Common in:

- Schema migration on historical tables with hundreds of millions of rows
- Adding a CHECK on a `status` column of a DWH fact table
- Converting old inline `CHECK`s to `SQL DOMAIN` across many tables (Oracle 23ai+)

## What to check afterwards

Once the constraint is `ENABLED NOVALIDATE`, the optimizer **does not use it to optimize queries** (e.g. to prune impossible conditions), because it has no guarantee that historical rows respect it. To recover the optimal plan, after cleaning up historical data, it's worth running `ALTER TABLE ... ENABLE VALIDATE CONSTRAINT` to bring the constraint back to a fully valid state.
