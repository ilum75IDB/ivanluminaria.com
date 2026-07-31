---
categories:
- oracle
date: 2099-12-31
description: Oracle 26ai introduces CREATE ASSERTION, the cross-table declarative
  constraint SQL-92 promised for decades. Syntax, comparison with triggers, and real
  insurance use cases.
draft: true
image: articolo-oracle-assertions-in-oracle-26ai.cover.jpg
seoTitle: 'Oracle 26ai CREATE ASSERTION: cross-table constraints explained'
tags:
- oracle-26ai
- integrity-constraints
- assertions
- sql-standard
- oracle-23ai
title: 'Three triggers, a nightly job, and 1,247 orphaned policies: Oracle 26ai Assertions
  explained'
translationKey: articolo_oracle_assertions_in_oracle_26ai
webo_generated_at: 2026-07-31
webo_status: da_tradurre
---

## Three triggers, a nightly job, and 1,247 orphaned policies

It was a routine batch migration — or so it seemed. A large Italian insurance group was consolidating historical data from a legacy system: a few million rows across `polizze` and `beneficiari`, a Saturday night maintenance window, a script tested in staging. To speed up the load, the team had temporarily disabled triggers on both tables. Standard procedure, documented in the runbook.

The problem surfaced Sunday morning, when the nightly reconciliation job finished its 45-minute run across 2.1 million policies and produced a report with 1,247 anomalous rows: policies in `ATTIVA` (active) status with no associated beneficiary. A direct violation of a critical business rule — "every active policy must have at least one beneficiary with a combined share equal to 100%" — that the system was supposed to guarantee at all times.

The rule was implemented with three coordinated triggers: an `AFTER INSERT OR UPDATE` on `polizze` that checked for the presence of beneficiaries whenever the status became `ATTIVA`, an `AFTER DELETE` on `beneficiari` that verified the linked policy wouldn't be left orphaned, and a third `AFTER UPDATE` on `beneficiari` that recalculated the shares. Plus the nightly job as a safety net for cases that slipped through — and something always slipped through, especially during batch operations with triggers disabled.

Detection time: roughly 18 hours. Manual correction time: half a working day. Actual cost: low, fortunately. But the question that stayed on the table after the incident was the right one: is there a way to express this rule at the schema level, so that no DML operation — batch or otherwise — can bypass it?

With Oracle 26ai, the answer is yes.

## SQL-92 was right, but nobody had listened

The SQL standard has defined `CREATE ASSERTION` since 1992. The idea is straightforward: an integrity constraint shouldn't be limited to a single row or a single table — it should be able to express predicates over the entire state of the database. The original standard syntax is:

```sql
CREATE ASSERTION constraint_name CHECK (boolean_condition)
```

where `boolean_condition` can involve subqueries, aggregations, and joins across different tables. Semantically, the constraint is satisfied when the condition is `TRUE` or `UNKNOWN`; it is violated when it is `FALSE`.

The problem is that no mainstream RDBMS had ever implemented this feature completely. PostgreSQL doesn't have it. MySQL doesn't have it. SQL Server doesn't have it. The reasons are well known: evaluating a predicate that spans multiple tables carries a potentially high cost, and the right moment to evaluate it — after each individual DML statement, or at the end of the transaction? — opens non-trivial implementation questions. The result: for thirty years, the feature remained in the standard document without landing in any product.

Oracle 23ai (later renamed 26ai in the subsequent release) is the first mainstream enterprise RDBMS to bring it to production [1]. This is a choice with precise conceptual weight: it signals that Oracle is taking SQL standard compliance seriously on features that other vendors have ignored, and that the relational model — with its declarative constraints — is still the direction of development, not a legacy to manage.

The fundamental distinction from an ordinary `CHECK` constraint is this: a `CHECK` evaluates a predicate on the columns of the current row, at the time of insertion or update. An `ASSERTION` evaluates a predicate over the entire contents of the involved tables, after every DML operation that could make it false. They are different tools for different problems.

## `CREATE ASSERTION` in Oracle 26ai: the syntax

Taking the insurance project schema as a reference, the two tables are:

```sql
-- Schema ins_core on oracle-node-01
CREATE TABLE polizze (
    id            NUMBER PRIMARY KEY,
    numero        VARCHAR2(20) NOT NULL,
    stato         VARCHAR2(10) CHECK (stato IN ('BOZZA','ATTIVA','SCADUTA','ANNULLATA')),
    data_inizio   DATE NOT NULL,
    data_fine     DATE
);

CREATE TABLE beneficiari (
    id            NUMBER PRIMARY KEY,
    id_polizza    NUMBER NOT NULL REFERENCES polizze(id),
    nome          VARCHAR2(100) NOT NULL,
    quota_pct     NUMBER(5,2) NOT NULL CHECK (quota_pct > 0 AND quota_pct <= 100)
);
```

The constraint that the three triggers were trying to enforce can be expressed like this:

```sql
-- Every ACTIVE policy must have at least one beneficiary
CREATE ASSERTION ins_core.polizza_ha_beneficiario CHECK (
    NOT EXISTS (
        SELECT 1 FROM ins_core.polizze p
        WHERE  p.stato = 'ATTIVA'
        AND    NOT EXISTS (
                   SELECT 1 FROM ins_core.beneficiari b
                   WHERE  b.id_polizza = p.id
               )
    )
);
```

This is the classic existential pattern: "there is no active policy for which no beneficiary exists." The double negation is the standard SQL way to express "for every X there must be at least one Y," and Assertions finally make this declarable at the schema level [2].

The second constraint — shares must sum to 100 — uses an aggregation pattern:

```sql
-- Beneficiary shares for every ACTIVE policy must sum to 100
CREATE ASSERTION ins_core.quote_beneficiari_complete CHECK (
    NOT EXISTS (
        SELECT b.id_polizza
        FROM   ins_core.beneficiari b
        JOIN   ins_core.polizze p ON p.id = b.id_polizza
        WHERE  p.stato = 'ATTIVA'
        GROUP BY b.id_polizza
        HAVING SUM(b.quota_pct) <> 100
    )
);
```

This second pattern is the one that is simply impossible to express with traditional `CHECK` constraints: the condition involves an aggregation across different rows of the same table, filtered by a join with another table.

To remove an Assertion:

```sql
DROP ASSERTION ins_core.polizza_ha_beneficiario;
```

The Oracle 26ai documentation also provides for temporarily disabling an Assertion with `DISABLE` and re-enabling it with `ENABLE`, analogously to traditional constraints [1]. This point is relevant for maintenance operations — but, as we'll see, it is also precisely the critical point to handle with care.

## Why pre-26ai alternatives were not equivalent

It's worth being precise about this, because the temptation to say "you can do it with triggers too" is real — and technically true, but it hides important differences.

| Mechanism | Declarative | Survives bulk load | Readable from schema | Evaluation cost |
|---|---|---|---|---|
| `CHECK` constraint | ✅ | ✅ | ✅ | Low (single row) |
| `AFTER` trigger | ❌ | ❌ (can be disabled) | ❌ | Medium (per row) |
| `DEFERRABLE` constraint | ✅ | Partial | ✅ | Low-medium |
| Materialised view + `WITH CHECK OPTION` | Partial | ❌ | Partial | High (refresh) |
| **ASSERTION** | ✅ | ✅ (if not disabled) | ✅ | Medium-high (cross-table) |

The `CHECK` constraint is declarative and readable, but cannot contain subqueries that reference other tables — a well-known and documented limitation [3]. Oracle enforces this explicitly: a `CHECK` that attempts a `SELECT` on another table raises an error at creation time.

`AFTER INSERT/UPDATE/DELETE` triggers work, but they are procedural. They don't appear in the schema definition in a readable way; they can be disabled with `ALTER TABLE DISABLE ALL TRIGGERS` or `ALTER TABLE ... DISABLE TRIGGER name`; in complex DML with non-trivial firing orders they can produce unexpected results. The incident with 1,247 orphaned policies is exactly the consequence of this fragility.

`DEFERRABLE` constraints handle temporality — they allow deferring verification to the end of the transaction rather than after each individual statement — but they don't express cross-table predicates. They are useful for multi-step DML (insert the parent row, then the children, verify the foreign key only at commit), not for constraints that span different tables [3].

Materialised views with `WITH CHECK OPTION` are a creative approximation: create a view that exposes violations, add a constraint on the view. It's not a constraint in the strict sense, it has refresh costs, and its behavior in concurrency scenarios is less predictable.

## When it makes sense to use them, and when it doesn't

Assertions are not free. The evaluation cost is real: every DML operation on a table involved in an Assertion may require executing the verification subquery. On tables with high-frequency DML — millions of inserts per second, OLTP systems with critical latency — this overhead needs to be measured before adopting the feature in production.

Cases where Assertions make sense:

- **Stable business rules**: if the predicate changes rarely, the cost of `DROP/CREATE` is acceptable. If the rule changes every sprint, triggers are more flexible.
- **Moderate DML frequency**: normal transactional systems, not high-throughput ingestion pipelines.
- **Predicates involving aggregations or cross-table existence**: exactly the cases that `CHECK` constraints don't cover.
- **Environments where schema readability is critical**: audits, compliance, onboarding of new DBAs — having the constraint declared in the schema is a concrete documentation advantage.

Cases to avoid or evaluate carefully:

- **Bulk load with direct-path insert**: `INSERT /*+ APPEND */` in Oracle bypasses the buffer cache and writes directly to datafiles. The behavior of Assertions in this scenario — whether they are evaluated, when, with what granularity — needs to be verified in the specific environment [4]. Don't assume the behavior is identical to conventional insert.
- **Tables with very high-frequency DML**: the evaluation cost multiplies with every operation. Measure first.
- **A feature still maturing**: Oracle 26ai is a recent release. Assertions are a new feature, and behavior in edge cases — high concurrency, partial rollbacks, concurrent DDL operations — needs to be tested in the target environment before adopting in production [4].

One point worth emphasizing: an Assertion can also be disabled, with `DISABLE`. This means the maintenance operation problem doesn't disappear — it shifts. The difference from triggers is that disabling an Assertion is an explicit DDL operation, visible in the system catalog, much harder to do "by accident" in a migration script. It's not absolute protection, but it's a more robust guardrail.

## Recurring patterns: the recipe book

Three patterns cover the majority of cross-table integrity constraints encountered in practice.

**"At least one" pattern** — every row in table A must have at least one corresponding row in B:

```sql
-- Every ACTIVE policy must have at least one beneficiary
CREATE ASSERTION ins_core.polizza_ha_beneficiario CHECK (
    NOT EXISTS (
        SELECT 1 FROM ins_core.polizze p
        WHERE  p.stato = 'ATTIVA'
        AND    NOT EXISTS (
                   SELECT 1 FROM ins_core.beneficiari b
                   WHERE  b.id_polizza = p.id
               )
    )
);
```

**"Constrained sum" pattern** — an aggregation over rows of B, grouped by A's key, must satisfy a condition:

```sql
-- Beneficiary shares for every ACTIVE policy must sum to 100
CREATE ASSERTION ins_core.quote_beneficiari_complete CHECK (
    NOT EXISTS (
        SELECT b.id_polizza
        FROM   ins_core.beneficiari b
        JOIN   ins_core.polizze p ON p.id = b.id_polizza
        WHERE  p.stato = 'ATTIVA'
        GROUP BY b.id_polizza
        HAVING SUM(b.quota_pct) <> 100
    )
);
```

**"All must" pattern** — every row in A must satisfy a condition involving B (variant with negated condition):

```sql
-- Every open claim must reference a policy in ACTIVE status
-- (example with additional sinistri table)
CREATE ASSERTION ins_core.sinistro_su_polizza_attiva CHECK (
    NOT EXISTS (
        SELECT 1 FROM ins_core.sinistri s
        JOIN   ins_core.polizze p ON p.id = s.id_polizza
        WHERE  s.stato = 'APERTO'
        AND    p.stato <> 'ATTIVA'
    )
);
```

These three patterns, combined, cover the vast majority of cross-table integrity constraints that in pre-26ai systems ended up in triggers. The syntax is more verbose than a simple `CHECK` constraint, but it is declarative, readable, and lives in the schema.

## The connection to article #88 and Oracle's direction

Those who read the article on Oracle's evolution from 19c to 26ai will remember that Assertions were mentioned in the final section as one of the most significant features of the new release — but without going deeper. This article is that deeper dive.

In the broader context of Oracle's roadmap, Assertions fit into a precise trend: bringing the product closer to full compliance with the SQL standard, on features that had remained theoretical for decades. JSON Relational Duality, True Cache, and Assertions share this characteristic — they are responses to real needs that the relational model had already theorized, but that products had never fully implemented.

This isn't nostalgia for relational purism. It's recognizing that some ideas from the relational model — declarative constraints above all — have concrete practical value that the industry has underestimated for years, delegating to triggers and application logic what should have lived in the schema.

## The constraint that doesn't break because there's no code to break

Three coordinated triggers, a 45-minute nightly job, and 1,247 orphaned policies found 18 hours after the incident. Not a disaster — a situation that was managed, corrected, documented. But the ongoing maintenance cost of those three triggers is real: every change to the business logic requires updating the procedural code, testing it, coordinating firing orders, and remembering to re-enable them after every batch operation.

An Assertion is not a magic wand. It has an evaluation cost, it has limitations in bulk load scenarios, and it's a new feature on an Oracle release that isn't yet in production everywhere. Before adopting it in a critical system, it's worth testing the specific behavior in the target environment — particularly for the DML patterns actually used in production, not just the standard cases.

The conceptual point, though, is solid: code that isn't written doesn't break. A constraint declared in the schema is visible, readable, and hard to bypass by accident. A trigger is procedural code that lives in a separate place, gets disabled with a single statement, and requires whoever runs the batch migration to know it exists and that it matters.

Moving the business rule to the right place — the schema — is a design choice, not just a technical one. Oracle 26ai's Assertions make this choice possible for the first time in a declarative way on a mainstream enterprise RDBMS. Worth understanding, even for those who won't be migrating to 26ai next week.

## Official sources

1. Oracle Database 23ai — `CREATE ASSERTION` syntax and semantics — `<TODO: scout fonte ufficiale per "CREATE ASSERTION Oracle 23ai/26ai documentation">`
2. Oracle Database 23ai New Features Guide — Integrity Constraints — `<TODO: scout fonte ufficiale per "Oracle 23ai New Features Guide — Integrity Constraints">`
3. Oracle Database SQL Language Reference — [Constraint Clauses](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/constraint.html) — covers `CHECK`, `DEFERRABLE`, existing integrity constraints (URL to verify for 26ai version)
4. Oracle Database 26ai Release Notes — GA vs preview status of Assertions, known limitations — `<TODO: scout fonte ufficiale per "Oracle 26ai Release Notes">`
5. ISO/IEC 9075 SQL Standard, SQL-92 — original definition of `CREATE ASSERTION` — `<TODO: scout riferimento pubblico accessibile per SQL-92 CREATE ASSERTION>`

## Glossary
- **[ASSERTION](/en/glossary/predicato-existential/)** (Oracle 26ai / SQL standard) — declarative integrity constraint that expresses a predicate over the entire state of the database, potentially involving multiple tables. Defined in SQL-92, implemented for the first time in a mainstream enterprise RDBMS with Oracle 23ai/26ai.

- **[Existential predicate](/en/glossary/assertion/)** (SQL) — logical expression asserting the existence of at least one row satisfying a condition. In SQL typically expressed with `EXISTS` or `NOT EXISTS` in a correlated subquery; the base pattern for "at least one" Assertions.

- **[Universal predicate](/en/glossary/predicato-existential/)** (SQL) — logical expression asserting that a condition holds for all rows in a set. In SQL expressed indirectly with `NOT EXISTS (... WHERE NOT condition)`, because SQL has no native universal quantifier.

- **DEFERRABLE constraint** (Oracle / SQL standard) — integrity constraint whose verification can be postponed to the end of the transaction rather than after each individual DML statement. Useful for multi-step DML, but not equivalent to an Assertion: it does not express cross-table predicates.

- **Direct-path insert** (Oracle) — data loading mode that bypasses the buffer cache and writes directly to datafiles, activated with the `/*+ APPEND */` hint. Interacts with integrity constraints differently from conventional insert; behavior with Assertions must be verified case by case.
