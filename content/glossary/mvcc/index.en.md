---
title: "MVCC"
description: "Multi-Version Concurrency Control — PostgreSQL's concurrency model that maintains multiple row versions to ensure transactional isolation without exclusive locks on reads."
translationKey: "glossary_mvcc"
aka: "Multi-Version Concurrency Control"
articles:
  - "/posts/postgresql/vacuum-autovacuum-postgresql"
---

**MVCC** (Multi-Version Concurrency Control) is the concurrency model used by PostgreSQL to manage simultaneous data access. Every UPDATE creates a new row version and marks the old one as "dead"; every DELETE marks the row as no longer visible. Reads don't block writes and vice versa.

## How it works

Each transaction sees a consistent snapshot of the database at the moment it begins. Rows modified by other uncommitted transactions are invisible. This eliminates the need for exclusive locks on reads, enabling high concurrency — but generates "garbage" in the form of dead tuples that must be cleaned up by VACUUM.

## What it's for

MVCC is PostgreSQL's architectural trade-off: high concurrency without locks, at the price of having to manage cleanup of obsolete versions. It is a reasonable price — provided autovacuum is correctly configured to keep pace with the table modification rate.

## Why it matters

If VACUUM cannot keep up with the rate of dead tuple generation, tables bloat, sequential scans slow down, and indexes become inefficient. The classic pattern: Monday the database is fine, Friday it's a disaster.
