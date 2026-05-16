---
title: "Enumerations in Oracle: twenty years of workarounds, and the road that opened up with 23ai"
seoTitle: "Oracle SQL Domains 23ai: enum, CHECK, lookup tables"
description: "Oracle never had a native ENUM. CHECK constraints, lookup tables and SQL Domains 23ai: three roads, a real banking case, and what's coming with 26ai."
date: "2026-06-16T08:03:00+01:00"
draft: false
translationKey: "enum_oracle_workaround_fino_a_23ai"
tags: ["schema-design"]
categories: ["oracle"]
image: "enum-oracle-workaround-fino-a-23ai.cover.jpg"
---

The question is the same one we asked [for MySQL](/en/posts/mysql/enum-mysql-semplifica-o-complica/) and then [for PostgreSQL](/en/posts/postgresql/enum-postgresql-paga-o-pesa/): a `status` or `type` column with a closed set of values, and three roads ahead. The database changes, the philosophy changes, and what the database actually offers changes too. On Oracle, until recently, the first option of the other two parts was simply missing — the native ENUM type. For twenty years, modelling an enumeration in Oracle was an exercise in workarounds: two viable roads and a third that was never really an enumeration.

With 23ai, a structural answer arrived: **SQL Domains** [1]. They're worth a close look, because Oracle got there last but got there well — and meanwhile the "lookup table" culture that grew on the field hasn't lost its place.

---

## The three roads, in two lines each

We'll use a `transactions` table with a status that takes a closed set of values. Banking sector — Oracle's classic Italian territory, where a chart of accounts and a taxonomy of statuses are regulated, audited, rarely improvised.

**CHECK constraint**:

```sql
CREATE TABLE transactions (
  id      NUMBER PRIMARY KEY,
  amount  NUMBER(15,2) NOT NULL,
  status  VARCHAR2(20) NOT NULL,
  CONSTRAINT chk_status CHECK (status IN
    ('PENDING','AUTHORIZED','COMPLETED','REVERSED','REJECTED'))
);
```

Standard SQL approach. Oracle has enforced `CHECK` constraints for decades [2] — no surprises about constraint validity like MySQL had before 8.0.16. Simple, readable, and for small projects it solves the problem immediately. **On the performance side it's practically free**: validation costs a handful of microseconds at INSERT/UPDATE time, adds nothing to SELECT, and the optimizer can actually use the constraint to its advantage — a query with `WHERE status='X'` on a value not allowed by the `CHECK` returns immediately, without scanning a single block. The real price, on a real system, you discover later: the same value list gets replicated on every table with the same `status` column, and every change becomes an `ALTER TABLE` per table. We'll see why this matters.

**Lookup table with foreign key**:

```sql
CREATE TABLE transaction_statuses (
  code      VARCHAR2(20) PRIMARY KEY,
  label     VARCHAR2(100) NOT NULL,
  ordering  NUMBER,
  active    CHAR(1) DEFAULT 'Y' CHECK (active IN ('Y','N'))
);

CREATE TABLE transactions (
  id            NUMBER PRIMARY KEY,
  amount        NUMBER(15,2) NOT NULL,
  status_code   VARCHAR2(20) NOT NULL,
  CONSTRAINT fk_status
    FOREIGN KEY (status_code) REFERENCES transaction_statuses(code)
);
```

The "pure database" road and — not by chance — the dominant cultural choice in Oracle enterprise projects. One extra table, one extra JOIN, and in exchange an enumeration that is **a database object with a life of its own**: you can attach localized labels to it, display ordering, active/inactive flag, audit trail on `MODIFY` of the taxonomy, and business rules richer than a simple "allowed/not allowed" [3]. On the systems I've seen in banking, telco and Italian public sector over the past twenty years, **eight times out of ten the choice was this** — and with good reason.

**Pseudo-pattern (SUBTYPE, COLLECTION, type-object)**:

```sql
-- Discouraged as "enumeration" for a persistent column:
CREATE OR REPLACE TYPE transaction_status_t AS OBJECT (
  code VARCHAR2(20)
);
/
```

Oracle's `TYPE` constructs (PL/SQL SUBTYPE, SQL COLLECTION, type-object) are powerful, but **they are not ENUMs**. They don't give native validation on persisted values, they don't have a lookup mechanism readable through pure SQL, and the data dictionary doesn't see them as "taxonomy". They are an application-level abstraction tool, not a constraint mechanism. Anyone who has used them to simulate an ENUM has generally regretted it when the first business report asked "how many active statuses do we have?" — and they couldn't extract them from the table without a PL/SQL query.

---

## What changes compared to MySQL and PostgreSQL

If you come from the two previous parts of the miniseries, three things deserve to be kept in mind before writing your first `CREATE TABLE` on Oracle.

**No native ENUM type**. On MySQL you have `ENUM('A','B','C')` as a column type; on PostgreSQL you have `CREATE TYPE ... AS ENUM` as a standalone object. On Oracle, until 23ai, these two options simply didn't exist. Only `CHECK` and lookup tables remained.

**`CHECK` is fully enforced, has been for a long time**. Unlike pre-8.0.16 MySQL (where `CHECK` constraints were parsed and silently ignored), Oracle has validated `CHECK` constraints since before the millennium. A historical detail with real consequences: if you come from MySQL, here there's no doubt about their effectiveness.

**Deeply rooted lookup-table culture**. The Oracle community, given the type of customers it serves (banking, insurance, public sector, telco), has always preferred lookup tables to `CHECK`. Not out of dogma, but because in those contexts the evolution of the value set is frequent, audit is mandatory, label localization is a standard. The lookup table is a flexibility gym — `CHECK` is a promise of rigidity.

---

## When `CHECK` is enough

Staying within the pattern of the other two parts, the cases where `CHECK` on Oracle is really the right choice are few and specific:

- **Value sets that will never change**. Sign of a measure (`'POS','NEG','ZERO'`), days of the week, months of the year, accounting polarity (`'DEBIT','CREDIT'`)
- **Tables with a single reference to the set**. If the column exists in **one** table only, the price of `ALTER TABLE` to add a value is marginal
- **Small or monolithic projects**, where the value domain is clear in code and doesn't need to be exposed as "configuration" to UI

Outside these three scenarios, in my experience, `CHECK` ages poorly. I see the same pattern emerge during evolution: business asks to add a new value — say `'MANUAL_AUTHORIZATION'` for transactions requiring manual intervention — and you realize the string is replicated in 14 tables. Fourteen `ALTER TABLE`s, fourteen regression tests, fourteen release notes. The lookup table would have required an `INSERT`.

---

## The lookup-table culture in Oracle (and why there's a reason)

On a banking project some time ago — a payments platform, Oracle 19c, around 1,200 tables in the application schema, team distributed between Italy and Romania — the transaction status taxonomy had been modelled with two tables:

- `transaction_statuses` (code, label_it, label_en, ordering, active, group)
- `transaction_statuses_audit` (MODIFY trigger that kept history of who changed what)

No `CHECK`. A single FK to `transaction_statuses.code` on every status column — `transactions.status_code`, `transactions_history.status_code`, `movements.status_code`, and a dozen other tables in the reconciliation module.

It seemed like overthinking, until the day compliance asked to be able to "**freeze**" a status temporarily (e.g. `'REVERSED'`) during an audit, without removing it from the schema — no new rows with that value, but historical rows had to remain readable and queryable. With the lookup table it was an `UPDATE transaction_statuses SET active = 'N' WHERE code = 'REVERSED'` plus some application-level checks. **Three lines of code**. If we had had `CHECK` constraints with the inline string list in 18 tables, it would have been a week of work between DDL, regression tests and deploy window.

It's not a hero story — it's the story of an architectural choice made five years earlier by the design team, and a compliance request that found the schema already prepared for the question being asked. Oracle's lookup-table culture grew from hundreds of episodes like this.

---

## The arrival of SQL Domains in 23ai

With Oracle Database 23ai (released on engineered systems in April 2024 and then in wider availability) comes a construct that was missing: the **SQL Domain** [1]. It's the first time Oracle gives a structural answer to the problem of "centralizing the domain of a column as a database object".

```sql
CREATE DOMAIN transaction_status AS VARCHAR2(20)
  CONSTRAINT chk_transaction_status CHECK (VALUE IN
    ('PENDING','AUTHORIZED','COMPLETED','REVERSED','REJECTED'))
  DEFAULT 'PENDING'
  ANNOTATIONS (display 'Transaction Status',
               description 'Lifecycle state of a transaction');

CREATE TABLE transactions (
  id      NUMBER PRIMARY KEY,
  amount  NUMBER(15,2) NOT NULL,
  status  transaction_status NOT NULL
);
```

The `DOMAIN` is a data dictionary object (visible in `DBA_DOMAINS`), reusable on any column, and brings the whole package with it: base type, `CHECK` constraint, `DEFAULT`, and — an original Oracle feature, not present in PostgreSQL's `DOMAIN` — an **annotations** system that can be read by BI tools, reporting systems, and UI generation frameworks to derive display labels, descriptions, ordering, etc.

The strong point isn't the syntax — it's the **ALTER DOMAIN**.

---

## `ALTER DOMAIN`: the superpower that was missing

```sql
ALTER DOMAIN transaction_status
  CONSTRAINT chk_transaction_status CHECK (VALUE IN
    ('PENDING','AUTHORIZED','COMPLETED','REVERSED','REJECTED',
     'MANUAL_AUTHORIZATION'));
```

That single statement updates the constraint **for all columns using `transaction_status`** — across 18 tables, 50, doesn't matter. Oracle takes care of propagating the check, and of validating existing rows (with `VALIDATE` or `NOVALIDATE`, depending on how you want to handle the transition) [4].

It's what the lookup table already gave you at a logical level (a single place to change the allowed values), now brought to the **schema catalog** level, without requiring a JOIN, without requiring an extra table, and without the 4 bytes of OID of a numeric FK.

For anyone who has worked twenty years with Oracle, it's one of those features that makes you say: "**finally**". Not because the lookup table has lost its place — the domain doesn't replace the lookup when you need localized labels, dynamic display ordering or audit trails. It replaces it when you needed **only** centralized validation and defaults. And those cases are many.

---

## When to choose what, today

A pragmatic guide, in summary form:

| Case | Recommended road |
|------|--------------------|
| Fixed set, 1 table, value domain known and immutable | Inline `CHECK` constraint |
| Fixed set, **multiple** tables, on Oracle pre-23ai | Lookup table with FK |
| Fixed set, multiple tables, **on Oracle 23ai+** | `SQL DOMAIN` |
| Evolving set + localized labels + dynamic ordering + audit | Lookup table with FK (even on 23ai+) |
| Cross-table validation (e.g. sum of statuses = N) | Trigger today, `ASSERTION` (26ai, coming) tomorrow |

The lookup table **is not dead** with SQL Domains. It remains the right choice when the enumeration is a **business entity** — with its attributes, its evolution, its governance. The SQL Domain is the ideal complement when the enumeration is a **schema constraint** — a pure domain, without attributes, reused on many columns.

---

## What's coming with 26ai: Assertions

Oracle 26ai (announced as the next major release) brings — among other things — formal support for **`ASSERTION`s**: an SQL standard construct, on paper for decades and never truly implemented by any mainstream DBMS, that lets you express **cross-table** constraints. Constraints that today you have to code as triggers or application-level checks, with all the risks involved (forgotten triggers, transactions that bypass the constraint, race conditions with relaxed isolation levels).

A possible example:

```sql
CREATE ASSERTION at_least_one_active CHECK (
  (SELECT COUNT(*) FROM transaction_statuses WHERE active = 'Y') >= 1
);
```

The idea is that the database engine guarantees this constraint **at a transactional level** — no triggers, no application code, centralized validation. For lookup-table-managed enumerations, `ASSERTION`s open a new scenario: the integrity of the entire taxonomy (not just the single column) becomes expressible in DDL.

This is material we'll develop when 26ai is available in testing, on real workloads. For now, it's worth knowing it's coming and being ready — the design of a status taxonomy today can already take into account where cross-table constraints will live better tomorrow.

---

## The question I take away from the miniseries

Three databases, three philosophies, three roads — and a question that remains valid everywhere: **how stable is your value set?**

- If it's truly stable and local → `CHECK` (and on Oracle 23ai+ → `DOMAIN`).
- If it has its own attributes and governance → lookup table, on any DB.
- If it's a frequent evolution of "registry" values → lookup table, always.

The rest is detail of syntax and engine. What matters — and what I've learned in three decades of schema design, on customers ranging from a multi-country insurance group to a commercial Italian bank — is that **schema rigidity is paid for during evolution, and flexibility is paid for in integrity**. The choice is always where you want to pay the price. Oracle 23ai, finally, gives you another point at which to pay it — more convenient, in many cases, than before.

---

## Official sources

1. Oracle Database 23ai SQL Language Reference — [CREATE DOMAIN](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/CREATE-DOMAIN.html)
2. Oracle Database 19c SQL Language Reference — [constraint_clause (CHECK and other constraints)](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/constraint.html)
3. Oracle Database 19c Database Concepts — [Data Integrity (integrity constraints, foreign key, lookup pattern)](https://docs.oracle.com/en/database/oracle/oracle-database/19/cncpt/data-integrity.html)
4. Oracle Database 23ai SQL Language Reference — [ALTER DOMAIN](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/ALTER-DOMAIN.html)

---

## Glossary

- **[SQL Domain](/en/glossary/oracle-sql-domain/)** — Construct introduced in Oracle 23ai that lets you define a base type + constraints + default + annotations as a data dictionary object, reusable on many columns. Conceptual equivalent of PostgreSQL's `DOMAIN`, but richer in metadata features.
- **[CHECK constraint](/en/glossary/check-constraint/)** — SQL constraint that limits the allowable values in a column or row through a boolean condition. Validated by the database engine at INSERT or UPDATE time.
- **[Lookup table](/en/glossary/lookup-table/)** — Auxiliary table holding the set of allowed values for a categorization column, referenced via foreign key from the "main" tables. Allows runtime evolution of the value set without schema changes.
- **[ALTER DOMAIN](/en/glossary/oracle-alter-domain/)** — Oracle 23ai+ command that modifies the constraint of a `SQL DOMAIN` and propagates the change to all columns using the domain. Replaces multiple `ALTER TABLE` calls with a single operation.
- **[ASSERTION](/en/glossary/sql-assertion/)** — SQL standard construct (not yet implemented by almost any mainstream DBMS) to express cross-table constraints validated at the transactional level. Announced in Oracle 26ai.
