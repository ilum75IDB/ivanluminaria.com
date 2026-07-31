---
title: "Universal predicate"
description: "SQL logical expression asserting a condition holds for every row in a set, expressed indirectly with NOT EXISTS (... WHERE NOT condition)."
translationKey: "glossary_predicato_universal"
aka: "Universal quantifier SQL"
articles:
  - "/posts/oracle/articolo-oracle-assertions-in-oracle-26ai"
---

A universal predicate asserts that a given condition holds for **every** row in a set. In formal logic this maps to the ∀ quantifier (for all). SQL has no native universal quantifier, so the pattern is built through double negation.

## How it works

The core equivalence is:

> "∀ x: P(x)" ≡ "¬∃ x: ¬P(x)"

In SQL:

```sql
-- "all orders for this customer have amount > 0"
SELECT c.id
FROM customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.id
      AND NOT (o.amount > 0)
);
```

The engine scans the correlated subset and returns the parent row only when no row violating the condition is found. If the inner set is empty, the predicate holds by vacuous truth.

## When to use it

The universal predicate appears in **relational constraint** scenarios:

- verifying that every detail row of a header satisfies a business rule (e.g., all invoice lines have a non-null tax code);
- implementing logical **assertions** in databases that lack native `CREATE ASSERTION` support (Oracle 23ai included);
- expressing relational division ("customers who purchased *every* product in a category").

Watch out for vacuous truth: when the subquery returns no rows, `NOT EXISTS` evaluates to `TRUE` by definition, which can produce false positives if the reference set is empty.
