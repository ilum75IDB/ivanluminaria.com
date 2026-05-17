---
title: "Oracle 19c, 21c, 23ai, 26ai: the silent rewrite of value domains"
seoTitle: "Oracle 19c → 26ai: SQL Domains and Assertions in 7 years"
description: "Seven years of Oracle seen through enumerations: from 19c CHECK to 23ai SQL Domains, all the way to 26ai Assertions. An insurance migration story."
date: "2026-06-23T08:03:00+01:00"
draft: false
translationKey: "enum_oracle_19c_26ai_domini"
tags: ["schema-design"]
categories: ["oracle"]
image: "enum-oracle-19c-26ai-domini.cover.jpg"
---

Over the past seven years, Oracle has silently rewritten how **value domains** are modelled in a schema. Without loud announcements, without the fanfare that PostgreSQL and MySQL have built around their `ENUM`. Four major releases — 19c, 21c, 23ai, 26ai — and a trajectory that, viewed from above, tells a precise story: Oracle got there last, and got there with a different solution.

If you're looking for the horizontal view (Oracle vs MySQL vs PostgreSQL, the three roads compared side by side), it's in [this article from the miniseries](/en/posts/oracle/enum-oracle-workaround-fino-a-23ai/). Here we take the vertical lens instead: a single platform, seven years, four releases. What you had at your disposal in each period, what changes in what comes next.

---

## 19c (2019): the starting point

Oracle Database 19c, released in 2019, is still today the **long-term reference release** for many enterprise systems — banking, insurance, Italian public sector, where upgrade cycles are long and prudent. When this story begins, the tools available for modelling an enumeration were two, and neither was "elegant":

```sql
-- Option 1: inline CHECK (Oracle 19c)
CREATE TABLE policies (
  id          NUMBER PRIMARY KEY,
  number      VARCHAR2(20) NOT NULL,
  status      VARCHAR2(20) NOT NULL,
  CONSTRAINT chk_policy_status CHECK (status IN
    ('ISSUED','ACTIVE','SUSPENDED','EXPIRED','CANCELLED','REVERSED'))
);

-- Option 2: lookup table with FK (Oracle 19c)
CREATE TABLE policy_statuses (
  code      VARCHAR2(20) PRIMARY KEY,
  label     VARCHAR2(100) NOT NULL,
  ordering  NUMBER,
  active    CHAR(1) DEFAULT 'Y' CHECK (active IN ('Y','N'))
);

CREATE TABLE policies (
  id            NUMBER PRIMARY KEY,
  number        VARCHAR2(20) NOT NULL,
  status_code   VARCHAR2(20) NOT NULL,
  CONSTRAINT fk_status FOREIGN KEY (status_code)
    REFERENCES policy_statuses(code)
);
```

The `CHECK` is light, enforced by the engine at runtime and used even by the optimizer to **prune impossible conditions** [1] — but it's local to the column, and replicating the same constraint across twenty tables sharing the same domain is an exercise in patience (and code review discipline). The lookup table is the pure-database road, dominant in enterprise projects: an extra JOIN, but also an enumeration that becomes a **database object with a life of its own** — localized labels, display ordering, active/inactive flags, audit trail.

In 19c **this was everything**. No `CREATE TYPE ENUM` like PostgreSQL, no column-level `ENUM` like MySQL. For those coming from those two worlds, the sensation was: *"so there's nothing native?"*. Answer: no. There was `CHECK`, there was the lookup, and there were twenty years of accumulated craft on how to make them work together.

---

## 21c (2021): an innovation release that skips value domains

Oracle Database 21c — the "innovation release", arrived on Cloud in 2020 and on-premises in 2021 — brings big things: the **native JSON type** [2], **blockchain tables** and **immutable tables** for tamper-proof audit, **SQL Macros** for reusing SQL fragments, in-DB AutoML integration. It's a release full of new ideas.

But for those looking at the specific problem of modelling value domains, **21c brings nothing**. No `CREATE DOMAIN`, no rework of `CHECK`, no integrated meta-taxonomy in the data dictionary. The DBA's choice when migrating from 19c to 21c, on the enumeration topic, doesn't change: `CHECK` or lookup.

Still worth naming, because it marks a passage: Oracle was working on other things during those two years, and anyone hoping for an answer on the schema-domain front had to wait. **The wait lasted two years longer than expected**, and it ended with the numeric leap to 23ai — the first signal, not just nominal, that Oracle was about to change pace.

---

## 23ai (2024): SQL Domains, finally

April 2024, Oracle Database 23ai released on engineered systems (Exadata Cloud@Customer first, then wider availability). Among the dozens of new features — and there are many, from `JSON Relational Duality` to `AI Vector Search` — the construct that matters for our story is just one: the **SQL Domain** [3].

```sql
-- Oracle 23ai
CREATE DOMAIN policy_status AS VARCHAR2(20)
  CONSTRAINT chk_policy_status CHECK (VALUE IN
    ('ISSUED','ACTIVE','SUSPENDED','EXPIRED','CANCELLED','REVERSED'))
  DEFAULT 'ISSUED'
  ANNOTATIONS (
    display 'Policy Status',
    description 'Lifecycle state of an insurance policy',
    ordering 'ISSUED<ACTIVE<SUSPENDED<EXPIRED<CANCELLED<REVERSED'
  );

CREATE TABLE policies (
  id      NUMBER PRIMARY KEY,
  number  VARCHAR2(20) NOT NULL,
  status  policy_status NOT NULL
);

CREATE TABLE policy_history (
  policy_id    NUMBER,
  event_date   DATE,
  status       policy_status NOT NULL,
  CONSTRAINT fk_pol FOREIGN KEY (policy_id) REFERENCES policies(id)
);
```

Three things in this block are worth reading carefully.

**First**: the `DOMAIN` is a **data dictionary object**. You find it in `DBA_DOMAINS`, `USER_DOMAINS`, `ALL_DOMAINS`, with columns describing the base type, the constraint, the default. For the first time, on Oracle, the **enumeration exists as an entity in the schema catalog** without requiring a second lookup table. The design review that asked "where is it documented that `status` can only take these six values?" now has a direct answer.

**Second**: the `ANNOTATIONS`. They're key/value metadata pairs that BI tools, UI generation procedures and reporting frameworks can read via `USER_ANNOTATIONS_USAGE` to automatically derive display labels, field descriptions, presentation ordering. On PostgreSQL the `DOMAIN` has only type + constraint; Oracle here took an extra step, and it's a step you notice when a Power BI or Tableau report taps directly into the dictionary to build its semantic maps.

**Third**: a single `status` column of type `policy_status` can be used in **dozens of tables**, and in all of them the same constraint, same default, same annotations apply. What with `CHECK` required twenty `ALTER TABLE`s to modify, with `DOMAIN` requires a single `ALTER DOMAIN` [4].

---

## A concrete 19c → 23ai migration

The schema of an insurance company — multi-country, Surety sector — on Oracle 19c, around 1,800 tables in the application schema, and a policy status taxonomy replicated across **22 tables** of the contract management module. Every time compliance asked to add a new status (last time: `'UNDER_AML_REVIEW'` for a new regulatory policy) it was 22 `ALTER TABLE`s to plan, test, deploy in a night window.

The upgrade to 23ai was not done **for** this problem — it was done for other reasons (infrastructure consolidation, end of Premier support on 19c). But once on 23ai, the architecture team planned a small refactor: convert the policy status taxonomy into a single SQL Domain.

The steps, in summary:

```sql
-- 1) Create the domain with values already present in production
CREATE DOMAIN policy_status AS VARCHAR2(20)
  CONSTRAINT chk_policy_status CHECK (VALUE IN
    ('ISSUED','ACTIVE','SUSPENDED','EXPIRED','CANCELLED','REVERSED',
     'UNDER_AML_REVIEW'))
  DEFAULT 'ISSUED';

-- 2) On the main table, declare the domain on the existing column
ALTER TABLE policies MODIFY (status policy_status);

-- 3) Same for each of the 21 dependent tables
ALTER TABLE policy_history MODIFY (status policy_status);
ALTER TABLE policy_premiums MODIFY (status policy_status);
-- ... etc.

-- 4) Drop the old redundant inline CHECKs (the domain replaces them now)
ALTER TABLE policies        DROP CONSTRAINT chk_policy_status;
ALTER TABLE policy_history  DROP CONSTRAINT chk_status_history;
-- ... etc.
```

The 22 tables were migrated in a maintenance window of just over an hour — almost all the time was consumed by the **validation of existing rows** (`VALIDATE`, default in Oracle), which read every table to confirm that no historical value violated the domain constraint. For the largest tables (policy history, ~340 million rows) `NOVALIDATE` was chosen with a follow-up cleanup via batch: in production, integrity going forward was guaranteed by the domain, and historical data had already been checked with a pre-flight script.

The final result, after the refactor: a single line of DDL to modify the taxonomy. The next compliance request — there will be one, always — will cost an `ALTER DOMAIN`, not a week of planning.

It's not a heroic story. It's the story of a team that recognized an opportunity at the right time and took it — Oracle had finally given the tool, all that was left was to pick it up.

---

## 26ai (2026): ASSERTION and what's on the horizon

Oracle 26ai (announced as the next major release) brings to the table, among other things, **`ASSERTION`s**: an SQL standard construct on paper for decades, never truly implemented by any mainstream DBMS, that lets you express **cross-table** constraints validated at the transactional level by the database engine.

For our story, `ASSERTION`s are the piece that closes a circle. With the 23ai SQL Domain we solved the "same constraint on many columns" problem. With the 26ai `ASSERTION`s another possibility opens: constraints involving **multiple tables together**, guaranteed by the database without the intervention of a trigger or application-level check.

```sql
-- Example (indicative syntax based on SQL standard):
CREATE ASSERTION at_least_one_active_status CHECK (
  (SELECT COUNT(*) FROM policy_statuses WHERE active = 'Y') >= 1
);

CREATE ASSERTION history_consistent CHECK (
  NOT EXISTS (
    SELECT 1 FROM policies p
    LEFT JOIN policy_history h ON h.policy_id = p.id
    WHERE p.status = 'REVERSED' AND h.status IS NULL
  )
);
```

Such constraints today are written as triggers — with all the issues involved: triggers forgotten in subsequent deploys, transactions that bypass the check due to isolation levels, race conditions hard to diagnose. `ASSERTION`s would shift the responsibility to the engine. When 26ai is available in testing and on real workloads, it will be material to dig into — but the design of a taxonomy today can already take into account where cross-table constraints will live better tomorrow.

---

## What Oracle still doesn't have

There's one thing Oracle still doesn't offer today: a **native enumerated type** like PostgreSQL's (`CREATE TYPE ... AS ENUM`) or MySQL's (`ENUM(...)`). It's worth saying openly, because someone might be wondering.

The SQL Domain is **conceptually more powerful** than a traditional ENUM (it's a reusable constraint, not a "closed" type), but it's also **more verbose** to declare and has an indirection overhead in the data dictionary. For the simplest use case — a column in a single table, very small value set, no metadata — the inline `CHECK` is still more terse. Oracle 23ai, in other words, did not replace `CHECK`: it gave it a companion for when `CHECK` was no longer enough.

It's coherent with Oracle's philosophy: provide powerful and general tools, leaving the designer the responsibility of choosing the right level of abstraction. PostgreSQL and MySQL made the opposite choice — provide a ready-to-use specific type — and for many cases that choice is more immediate. They are two different cultures, both legitimate.

---

## The trajectory, viewed from late 2026

Seven years, four releases, and a line that from the outside looks continuous but seen from inside is made of pauses and bursts. The 19c was the starting point: two known roads and no third. The 21c brought other things, staying still on this terrain. The 23ai opened the **structural road** that had been missing for decades. The 26ai closes the circle on constraints that span the single table.

It's not a heroic story. Oracle arrived after PostgreSQL (which has `DOMAIN`s since the late '90s) and after MySQL (which has `ENUM`s forever). But when it arrived, it arrived with a different idea — more general, more integrated in the dictionary, more extensible via annotations — and that idea is becoming the standard way of modelling value domains on the new Oracle schemas I see being built in production today.

The question to take away, for those modelling enterprise schemas on Oracle: **no longer "which road do I take", but "when does the inline `CHECK` suffice, and when is it worth declaring a `DOMAIN`"**. The two options coexist, and knowing when to switch from one to the other is today the real discriminator.

---

## Official sources

1. Oracle Database 19c SQL Language Reference — [constraint_clause (CHECK and other constraints)](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/constraint.html)
2. Oracle Database 21c Database New Features Guide — [Innovation Release overview](https://docs.oracle.com/en/database/oracle/oracle-database/21/nfcoa/index.html)
3. Oracle Database 23ai SQL Language Reference — [CREATE DOMAIN](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/CREATE-DOMAIN.html)
4. Oracle Database 23ai SQL Language Reference — [ALTER DOMAIN](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/ALTER-DOMAIN.html)

---

## Glossary

- **[SQL Domain](/en/glossary/oracle-sql-domain/)** — Construct introduced in Oracle 23ai that defines a reusable domain (base type + CHECK + DEFAULT + annotations) as a data dictionary object. For the first time on Oracle, an enumeration exists in the schema catalog without requiring a lookup table.
- **[Annotations (Oracle 23ai)](/en/glossary/oracle-annotations/)** — Key/value metadata pairs attachable to schema objects (columns, domains, tables), readable via `USER_ANNOTATIONS_USAGE`. Used by BI and UI generation tools to automatically derive display labels, descriptions, ordering.
- **[VALIDATE / NOVALIDATE](/en/glossary/oracle-validate-novalidate/)** — Modes for applying an Oracle constraint at creation or modification time: `VALIDATE` reads all existing rows to check compliance (default), `NOVALIDATE` skips the check to avoid blocking large tables during maintenance windows.
- **[Oracle major release](/en/glossary/oracle-major-release/)** — Main version of the Database server with significant feature changes, dedicated Premier support cycle, and its own numbering (19c, 21c, 23ai, 26ai). Different from patch sets and intermediate release updates.
- **[ASSERTION](/en/glossary/sql-assertion/)** — SQL standard construct for expressing cross-table constraints validated at the transactional level by the database engine. Announced in Oracle 26ai.
