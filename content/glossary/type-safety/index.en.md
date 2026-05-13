---
title: "Type safety"
description: "Property of a type system that prevents, at parse-time, the use of values incompatible with the declared type of a column, parameter or variable."
translationKey: "glossary_type_safety"
aka: "Type checking, strict typing"
articles:
  - "/posts/postgresql/enum-postgresql-paga-o-pesa"
---

**Type safety** is the property of a type system that prevents, at parse-time or compile-time, the use of values incompatible with the declared type. In a database context, it means the engine rejects operations that violate type constraints before even executing the query.

## How it works

When a column, function parameter or variable is declared with a specific type (e.g. `INTEGER`, a custom domain, an ENUM), the engine checks at parse time that every value assigned or compared is compatible. Operations that mix incompatible types without an explicit cast raise an error before execution, preventing bugs that would otherwise only show up at runtime.

## What it's for

To shift error detection from runtime to parse-time, reducing the risk of corrupt or inconsistent data in production. In PostgreSQL, for instance, an ENUM is a standalone type: a function that takes a `subscription_status` cannot be called with an arbitrary string. In MySQL, where ENUM is just a decoration of a `VARCHAR` column, this guarantee doesn't exist — the constraint is on the column, not on the type itself.

## When to use it

It's useful in any system where semantic data integrity matters more than ease of writing: billing, finance, customer records, any domain where an "out-of-domain" value is a business error rather than an acceptable variant. End-to-end type safety is one of PostgreSQL's hallmark traits and a major reason it gets picked for enterprise workloads.
