---
title: "ENUM in PostgreSQL: when the choice pays off, and when it bites back"
seoTitle: "PostgreSQL ENUM vs CHECK vs lookup: the right choice"
description: "PostgreSQL ENUM vs CHECK vs lookup table: ALTER TYPE ADD VALUE is metadata-cheap, dropping a value costs a migration. Three paths, one real telco case."
date: "2026-06-09T08:03:00+01:00"
draft: false
translationKey: "enum_postgresql_paga_o_pesa"
tags: ["enum", "data-modeling", "schema-design", "alter-type", "check-constraint"]
categories: ["postgresql"]
image: "enum-postgresql-paga-o-pesa.cover.jpg"
---

The question is the same we faced [in MySQL](/en/posts/mysql/enum-mysql-semplifica-o-complica/): a `status` or `type` column with a closed set of values, and three roads in front of you — native enumerated type, CHECK constraint, lookup table. Change the database, and the philosophy changes too — along with the place where the price gets paid.

PostgreSQL has its own ENUM, declared as a standalone type with `CREATE TYPE ... AS ENUM` [1] [2]. It's designed differently from MySQL's: type-safe like a domain, transactional like every other piece of DDL, and with one detail that trips almost everyone at first — it's **case-sensitive**. If you come from MySQL it's uncomfortable; if you've always worked in PostgreSQL it feels natural.

Worth digging into properly, because PostgreSQL ENUM isn't "MySQL ENUM with different syntax". It's a different beast. Best understood on its own terms.

---

## The three roads, two lines each

We'll use the example of a `subscriptions` table with a status column drawn from a closed set of values.

**Native ENUM**:

```sql
CREATE TYPE subscription_status AS ENUM (
  'ACTIVE','SUSPENDED','TERMINATED','EXPIRED'
);

CREATE TABLE subscriptions (
  id      BIGINT PRIMARY KEY,
  status  subscription_status NOT NULL
);
```

In PostgreSQL the type is a **first-class object**: you create it once, reuse it on many columns, modify it with `ALTER TYPE`. Internally the column takes 4 bytes (an internal `OID`), the value is validated by the engine, and reads return the original string (case-sensitive).

**CHECK constraint**:

```sql
CREATE TABLE subscriptions (
  id      BIGINT PRIMARY KEY,
  status  VARCHAR(20) NOT NULL,
  CONSTRAINT chk_status 
    CHECK (status IN ('ACTIVE','SUSPENDED','TERMINATED','EXPIRED'))
);
```

Standard SQL approach. More verbose, in exchange more flexible (the `CHECK` expression can be arbitrarily complex). In PostgreSQL `CHECK` constraints have always been fully enforced [3] — none of the "silently ignored" behavior that haunted MySQL until 8.0.16.

**Lookup table with FK**:

```sql
CREATE TABLE subscription_statuses (
  code        VARCHAR(20) PRIMARY KEY,
  label       VARCHAR(100) NOT NULL,
  active      BOOLEAN DEFAULT TRUE
);

CREATE TABLE subscriptions (
  id            BIGINT PRIMARY KEY,
  status_code   VARCHAR(20) NOT NULL,
  CONSTRAINT fk_status 
    FOREIGN KEY (status_code) REFERENCES subscription_statuses(code)
);
```

The "pure-database" road. More tables, more JOINs, and in exchange more flexibility: extra attributes, localized labels, display ordering, runtime activation/deactivation [4].

---

## What changes vs MySQL: three things to know upfront

If you come from MySQL, three details deserve a pre-flight check before you write your first `CREATE TYPE`.

**Case-sensitive**. `'ACTIVE'` and `'active'` are two different values. In MySQL they were the same value — a design choice many found "convenient" and others found "slippery". PostgreSQL goes the other way: if you declared `'ACTIVE'`, you'll always have to write `'ACTIVE'`. Unnormalized queries fail with *invalid input value*. It's rigor, and once you get used to it you appreciate it; on day one it costs a few minutes.

**Real type safety, not simulated**. ENUM is a type, not a constraint on a `VARCHAR`. You can write a function that takes `subscription_status` as a parameter, and the engine will reject at parse-time any call with a free-form string. The same holds for procedures, views, partial indexes. In MySQL this kind of safety doesn't exist — `ENUM` is a decorated `VARCHAR` column.

**ALTER TYPE is nearly free (and transactional)**. Adding a value at the end of a PostgreSQL ENUM is a metadata operation [5]. No table rebuild, no prolonged write lock. And like every other PostgreSQL DDL, it's inside the transaction: if the commit fails, the ENUM stays as it was. This is the most tangible difference compared to MySQL, where `MODIFY COLUMN ENUM(...)` on a large table can keep you awake for an entire night.

---

## When ENUM is the right choice in PostgreSQL

The principle is the same as in MySQL, applied to PostgreSQL: **stable set of values, schema-controlled semantics**. When both ingredients are present, ENUM in PostgreSQL even has a few extra advantages compared to its MySQL cousin:

1. **End-to-end type safety**: ENUM is a type that travels across functions, procedures, foreign data wrappers. It's not just a column constraint; it's a coherence guarantee PostgreSQL applies to the whole SQL code stack
2. **Compact storage**: 4 bytes per row (the same as an `INT` foreign key), comparable to MySQL. On tables with hundreds of millions of rows it isn't the main driver; it remains consistent
3. **Cheap ALTER TYPE ADD VALUE**: the most common modification — adding a new value — costs practically nothing
4. **Transactional DDL**: adding a value inside a transaction that also includes the application code deployment is an atomicity guarantee very few other DBMS hand you

In a system where the domain really is closed and well defined, ENUM in PostgreSQL removes complexity and adds safety. One `CREATE TYPE`, one column, done.

---

## The real case: subscription statuses at a mobile operator

A few projects back, we found ourselves designing the data model for subscription management at a European mobile operator. PostgreSQL stack, millions of active SIMs, a `subscriptions` table with a `status` column read by virtually every billing query.

The first version had four statuses, well defined by the business: `ACTIVE`, `SUSPENDED`, `TERMINATED`, `EXPIRED`. ENUM was the natural choice:

```sql
CREATE TYPE subscription_status AS ENUM (
  'ACTIVE','SUSPENDED','TERMINATED','EXPIRED'
);

ALTER TABLE subscriptions
  ADD COLUMN status subscription_status NOT NULL DEFAULT 'ACTIVE';
```

For a year and a half it worked in silence. Type-safe, readable, performant. No lookup table to seed, no FK to maintain at deploy time. No one even remembered it was there — which is the best compliment you can pay a schema.

Then, as is normal, the product grew.

The first call came from the anti-fraud team: they needed to distinguish between `SUSPENDED_NONPAYMENT` and `SUSPENDED_VOLUNTARY`. Easy operation in PostgreSQL — and this is where the difference with MySQL really shows:

```sql
ALTER TYPE subscription_status ADD VALUE 'SUSPENDED_NONPAYMENT' AFTER 'SUSPENDED';
ALTER TYPE subscription_status ADD VALUE 'SUSPENDED_VOLUNTARY'  AFTER 'SUSPENDED_NONPAYMENT';
```

Two metadata `ALTER TYPE`s. Milliseconds. No rebuild, no significant locks on a `subscriptions` table holding tens of millions of rows. The same operation in MySQL, I remember, would have required a `MODIFY COLUMN ENUM(...)` with the entire table rewritten under Online DDL, and a DBA standing in front of a monitor.

A point in PostgreSQL's favor. For real.

Then, a few quarters later, the trouble began.

---

## The limits, stories from the field

PostgreSQL ENUM has limits. They aren't worse than MySQL's — they're **different**, and they show up at different points in the lifecycle.

**You can't drop a value natively**. Sounds like a small detail; it's the biggest limitation. If the business decides to retire the `EXPIRED` status (because in the new commercial model it gets absorbed into `TERMINATED`), PostgreSQL has no `ALTER TYPE DROP VALUE`. You need to:

1. Create a new type with the reduced set of values
2. Update every row of the table to migrate it to the new set
3. Change the column type (`ALTER COLUMN ... TYPE`)
4. Drop the old type

All of this, on a large table, is exactly the heavy migration that in MySQL you'd have paid to **add** a value — here you pay it to **remove** one. The symmetry is cute only on paper: in production, it's still a lot of load.

**Renaming a value is easy, even if transactional**. `ALTER TYPE ... RENAME VALUE 'X' TO 'Y'` has been available since PostgreSQL 10. Fast and clean operation. There's a subtlety though: the ALTER TYPE runs inside the transaction, yes, and if the rename happens while other sessions hold open transactions on that type, you may run into locks. On high-concurrency systems it's not as trivial as it looks.

**Position-based ordering**. As in MySQL, the order in which values were declared matters for `ORDER BY`. If you added `SUSPENDED_NONPAYMENT` `AFTER 'SUSPENDED'`, the order is consistent. But if you forget and run `ALTER TYPE ... ADD VALUE 'NEW_ONE'` without specifying position, the value goes to the end. Dashboard sorts can surprise you.

**GIN/GiST indexes don't treat it as text**. Could be an advantage or a problem depending on your use case; if you were planning full-text search on it, remember ENUM isn't `text`. It needs to be cast, and the cast sometimes prevents index use.

In the subscriptions system, two years in, the statuses had grown to eleven, and a "cleanup" request from the business — drop three, rename two — turned an apparently-trivial change into a weekend-long migration, with partial dump-restore of a few satellite tables that used the type. The price had arrived — just at a different point in the lifecycle than in MySQL.

---

## When to switch to CHECK or lookup

The red flags are the same as in MySQL — the database changes, the project logic doesn't:

1. **Values change often** — not just added, but renamed or retired. If the vocabulary is actively evolving, the schema isn't the right place to hold it
2. **You need extra attributes** — multilingual descriptions, short/long labels, display ordering, active flag. ENUM doesn't accommodate them
3. **Dozens of values and growing** — beyond 20-30, the `CREATE TYPE` becomes an unwieldy list

`CHECK` constraints in PostgreSQL are a clean middle ground: easier to modify than an ENUM (just an `ALTER TABLE ... DROP CONSTRAINT ... ADD CONSTRAINT ...`), less structured than a real lookup. Good for sets of 5-15 values that get touched every now and then.

For the subscription model, the first evolution wave (4 → 11 statuses) we digested with `ALTER TYPE ADD VALUE`. The second wave — the one asking for multiple removals and renames — was the cue to rewrite toward a lookup table. Not because ENUM had been "wrong" from the start. It was right for a small, stable domain, and it became inconvenient when the domain stopped being stable.

---

## Lookup table done well, with an ENUM inside

The pattern here is analogous to what we saw in MySQL, and — to a limited extent of surprise — an ENUM inside the lookup table makes sense in PostgreSQL too.

```sql
CREATE TYPE subscription_status_code AS ENUM (
  'ACTIVE','SUSPENDED','TERMINATED','EXPIRED'
);

CREATE TABLE subscription_statuses (
  id          SMALLSERIAL PRIMARY KEY,
  code        subscription_status_code NOT NULL UNIQUE,
  description TEXT NOT NULL,
  sort_order  SMALLINT NOT NULL DEFAULT 0,
  active      BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO subscription_statuses (code, description, sort_order) VALUES
  ('ACTIVE',     'Subscription active and operational',   10),
  ('SUSPENDED',  'Suspended, can be reactivated',         20),
  ('TERMINATED', 'Terminated by customer',                30),
  ('EXPIRED',    'Natural contract expiration',           40);

CREATE TABLE subscriptions (
  id        BIGINT PRIMARY KEY,
  status_id SMALLINT NOT NULL,
  CONSTRAINT fk_status 
    FOREIGN KEY (status_id) REFERENCES subscription_statuses(id)
);
```

The three benefits are the same we saw in MySQL:

**The master carries only the id**, not the code. Two bytes (`SMALLINT`) instead of the 4 bytes of the direct ENUM OID — on tables with hundreds of millions of rows it adds up to GBs saved.

**Code and description are attributes of the lookup, not the key**. Renaming the description of a status — switching "Suspended, can be reactivated" to "Temporary suspension, can be reactivated" — is an `UPDATE` on a single row. No ALTER TYPE, no migration on the master.

**Extra attributes cost nothing**: a short-description field, a linked table for translations, a `valid_from/valid_to` flag to manage statuses valid only in certain windows. All of this, with a "pure" ENUM on the master, was out of reach.

And on the ENUM inside the lookup, **every limit we listed above becomes irrelevant**: the `subscription_statuses` table has 11 rows, a rebuild on 11 rows is invisible, a migration is trivial. The "only these values are allowed" constraint comes for free, without writing a separate `CHECK`.

### Adding and retiring values on the lookup pattern

On the lookup pattern, the two "delicate" operations become lightweight.

**Adding a status** (`RESERVED`, because subscriptions can now be "reserved" before activation):

```sql
-- Extend the ENUM inside the lookup (metadata, milliseconds)
ALTER TYPE subscription_status_code ADD VALUE 'RESERVED' BEFORE 'ACTIVE';

-- Insert the new row
INSERT INTO subscription_statuses (code, description, sort_order, active) VALUES
  ('RESERVED', 'Subscription reserved, not yet active', 5, TRUE);
```

**Retiring a status** (`EXPIRED` absorbed into `TERMINATED`): here PostgreSQL has no `DROP VALUE`. But on a lookup of a handful of rows, recreating the type is a matter of seconds even in production:

```sql
-- 1. Migrate the lookup rows using the "old" value
UPDATE subscription_statuses SET code = 'TERMINATED' WHERE code = 'EXPIRED';
-- (Single row; under the FK the master keeps pointing to the same id)

-- 2. Create the new type with the updated vocabulary
CREATE TYPE subscription_status_code_v2 AS ENUM (
  'RESERVED','ACTIVE','SUSPENDED','TERMINATED'
);

-- 3. Change the column type on the lookup
ALTER TABLE subscription_statuses 
  ALTER COLUMN code TYPE subscription_status_code_v2 
  USING code::text::subscription_status_code_v2;

-- 4. Drop the old type
DROP TYPE subscription_status_code;
ALTER TYPE subscription_status_code_v2 RENAME TO subscription_status_code;
```

Four steps, all on a small table. The master `subscriptions` — the one with hundreds of millions of rows — is never touched. It keeps referencing `status_id`, and the FK always resolves to the right lookup row. **Referential integrity is anchored to the surrogate id**, not the ENUM code, and that's the key to the pattern.

---

## The golden rule

The takeaway from the subscriptions case — and it holds, identical, in PostgreSQL and in MySQL — is:

> If the values in the domain will never change, ENUM is the right choice. If they will change — even just "occasionally" — don't tie the vocabulary to the schema.

The difference between the two databases isn't in the rule. It's in **where the price falls** when the domain changes:

- **In MySQL**, adding a value in a specific position costs a table rebuild. Adding it at the end is cheap; it corrupts the ordering however.
- **In PostgreSQL**, adding is always cheap (even in a specific position). Removing or reorganizing is the heavy migration.

Understanding your use case means understanding **what kind of evolution the domain is likely to undergo**. Only additions? PostgreSQL ENUM is an ally. Additions and removals? Better a lookup table from day one.

---

## The cross-DB mini-series

This is the second installment of a mini-series on enumerations across different DBMS. The "ENUM or lookup?" question doesn't have a universal answer — it shifts shape from database to database. The first article, on MySQL, is here:

- **[ENUM in MySQL: when it makes your day, and when it ruins your week](/en/posts/mysql/enum-mysql-semplifica-o-complica/)** — the same question, a different philosophy, and the real case of a shipment tracking system

Upcoming installments:

- **Oracle** — `CHECK` constraints, the SQL Domains introduced in 23ai, and why Oracle arrived "late" to this theme
- **Oracle, vertical deep-dive** — how enumerations were modeled in 19c, what changed in 21c, 23ai and 26ai, all the way to the new Assertions

> 📖 **If you landed here first**: I'd recommend reading [the MySQL piece](/en/posts/mysql/enum-mysql-semplifica-o-complica/) too. Many of the patterns we walk through here — the three roads, the lookup table done well, the ENUM-inside-the-lookup — are introduced there. The comparison makes everything clearer.

------------------------------------------------------------------------

## Official Sources

1. PostgreSQL Documentation — [Enumerated Types](https://www.postgresql.org/docs/current/datatype-enum.html)
2. PostgreSQL Documentation — [`CREATE TYPE`](https://www.postgresql.org/docs/current/sql-createtype.html)
3. PostgreSQL Documentation — [Constraints (CHECK)](https://www.postgresql.org/docs/current/ddl-constraints.html)
4. PostgreSQL Documentation — [`CREATE TABLE` (FOREIGN KEY)](https://www.postgresql.org/docs/current/sql-createtable.html)
5. PostgreSQL Documentation — [`ALTER TYPE` (ADD VALUE)](https://www.postgresql.org/docs/current/sql-altertype.html)

------------------------------------------------------------------------

## Glossary

**[CREATE TYPE AS ENUM](/en/glossary/postgresql-create-type-enum/)** — PostgreSQL DDL statement that creates an enumerated type as a first-class object. Unlike MySQL, the type exists independently of the columns using it and can be reused across the schema.

**[ALTER TYPE ADD VALUE](/en/glossary/postgresql-alter-type-add-value/)** — PostgreSQL command that appends a value to an existing ENUM. Metadata-only operation, transactional, no table rebuild. Available since PostgreSQL 9.1, with `BEFORE`/`AFTER` positioning since 9.6.

**[OID (Object Identifier)](/en/glossary/postgresql-oid/)** — Numeric identifier used internally by PostgreSQL to reference system objects (tables, types, functions). For ENUMs, the value is stored as a 4-byte internal OID.

**[Type safety](/en/glossary/type-safety/)** — Property of a type system that prevents, at parse-time or compile-time, the use of incompatible values. ENUM in PostgreSQL is a standalone type, not a constraint on `VARCHAR`, which enables end-to-end type safety across functions and procedures.

**[Lookup table](/en/glossary/lookup-table/)** — Reference table linked via foreign key that stores the valid values of an enumeration, with optional descriptive attributes (label, ordering, active flag). The preferred pattern when the domain evolves over time.
