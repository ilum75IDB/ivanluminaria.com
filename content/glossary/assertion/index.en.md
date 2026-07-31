---
title: "ASSERTION"
description: "Declarative SQL integrity constraint that validates a predicate against the entire database state, spanning multiple tables simultaneously."
translationKey: "glossary_assertion"
aka: "Multi-table declarative constraint"
articles:
  - "/posts/oracle/articolo-oracle-assertions-in-oracle-26ai"
---

An ASSERTION is a declarative integrity constraint introduced by SQL-92 that expresses a boolean predicate over the entire database state. Unlike `CHECK` — which is scoped to a single row or at most a single table — an ASSERTION can span multiple tables and aggregations, and is violated whenever the predicate evaluates to `FALSE` after any DML or DDL operation.

## How it works

An ASSERTION is defined with `CREATE ASSERTION` and bound to a schema. The engine evaluates it at the end of each transaction (or, depending on the implementation, after each statement): if the predicate returns `FALSE`, the transaction is rejected with an automatic ROLLBACK.

```sql
CREATE ASSERTION max_orders_per_customer
CHECK (
  NOT EXISTS (
    SELECT customer_id
    FROM orders
    GROUP BY customer_id
    HAVING COUNT(*) > 1000
  )
);
```

The predicate can reference any table visible in the schema, using subqueries, aggregations, and joins. Enforcement is handled by the engine, not by the application layer.

## When to use it

ASSERTIONs cover business rules that cannot be expressed with `CHECK` or `FOREIGN KEY`: aggregate limits, cross-table invariants, temporal constraints spread across multiple entities. The cost is real: every transaction touching the referenced tables may trigger re-evaluation of the predicate, with a measurable performance impact in write-heavy workloads.

SQL-92 standardized them, but for decades no mainstream enterprise RDBMS implemented them natively. Oracle 23ai/26ai is the first production-grade engine at scale to do so.
