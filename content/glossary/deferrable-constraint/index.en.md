---
title: "DEFERRABLE constraint"
description: "An integrity constraint whose verification can be postponed to COMMIT instead of being checked after each DML statement. Useful for multi-step transactions."
translationKey: "glossary_deferrable_constraint"
aka: null
articles:
  - "/posts/oracle/articolo-oracle-assertions-in-oracle-26ai"
---

A DEFERRABLE constraint is an integrity or referential constraint whose enforcement can be delayed until the end of the transaction — at COMMIT time — rather than being triggered immediately after each DML statement. This allows a transaction to pass through temporarily inconsistent intermediate states, as long as full consistency is restored before the transaction closes.

## How it works

A constraint declared `DEFERRABLE` supports two operating modes:

- `INITIALLY IMMEDIATE` — enforced after every DML by default; can be deferred explicitly via `SET CONSTRAINT`.
- `INITIALLY DEFERRED` — deferred to COMMIT by default.

```sql
ALTER TABLE orders
  ADD CONSTRAINT fk_customer
  FOREIGN KEY (customer_id) REFERENCES customers(id)
  DEFERRABLE INITIALLY DEFERRED;

-- Within the transaction:
SET CONSTRAINT fk_customer DEFERRED;
INSERT INTO orders (id, customer_id) VALUES (1, 999); -- customer 999 doesn't exist yet
INSERT INTO customers (id) VALUES (999);              -- now it does
COMMIT;                                               -- constraint check passes
```

## When to use it

The canonical use case is loading data with circular dependencies or inserting rows linked by foreign keys in a non-deterministic order. It is also common in replication pipelines and ETL processes where record arrival order is not guaranteed.

**Key limitation**: a DEFERRABLE constraint is not an Assertion. It operates on individual rows or predefined inter-table relationships, but cannot express arbitrary cross-table predicates such as `CHECK (SELECT COUNT(*) FROM ...)`. For that level of expressiveness, Oracle 23ai introduces native SQL Assertions.
