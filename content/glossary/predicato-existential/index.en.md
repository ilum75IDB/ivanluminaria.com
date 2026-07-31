---
title: "Existential Predicate"
description: "SQL logical expression that checks whether at least one row satisfies a condition, forming the basis of EXISTS and NOT EXISTS patterns."
translationKey: "glossary_predicato_existential"
aka: "Existential predicate, existence predicate"
articles:
  - "/posts/oracle/articolo-oracle-assertions-in-oracle-26ai"
---

An **existential predicate** is a logical expression that evaluates to `TRUE` if at least one row satisfies a given condition. In SQL, it underpins the `EXISTS` and `NOT EXISTS` operators, typically used inside correlated subqueries to verify the presence or absence of related data without explicitly retrieving it.

## How it works

The engine evaluates the correlated subquery row by row against the outer query. As soon as it finds the first matching row, it returns `TRUE` and stops scanning (short-circuit evaluation). This often makes it more efficient than a `JOIN` or an `IN` clause on large datasets.

```sql
-- Check that at least one active order exists for each customer
SELECT c.id, c.name
FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.id
      AND o.status = 'ACTIVE'
);
```

The `SELECT 1` inside the subquery is conventional: the projected value is irrelevant — only row existence matters.

## When to use it

The existential predicate is the natural pattern for implementing **"at least one" Assertions**: constraints or checks that require the guaranteed presence of at least one related record. In Oracle 23ai, where declarative Assertions are not yet exposed as native DDL objects, `EXISTS` inside triggers or check constraints is the standard operational substitute.

`NOT EXISTS` covers the complementary case — no row must satisfy the condition — useful for exclusion constraints or detecting gaps in time series.

One caveat: on uncorrelated subqueries or unindexed columns, cost can degrade to a full scan. Running `EXPLAIN PLAN` before deploying `EXISTS`-based queries against large tables is always advisable.
