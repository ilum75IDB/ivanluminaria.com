---
title: "ENUM (MySQL)"
description: "MySQL data type that allows a predefined set of string values, stored internally as a 1-2 byte numeric index."
translationKey: "glossary_mysql_enum"
aka: "MySQL ENUM type"
articles:
  - "/posts/mysql/enum-mysql-semplifica-o-complica"
---

**ENUM (MySQL)** is a data type that only allows a predefined set of string values, declared when the column is created. It's one of MySQL's characteristic features — few other mainstream DBMSes have a native enumerated type.

## How it works

When you declare `status ENUM('NEW','ACTIVE','CLOSED')`, MySQL assigns each value a numeric index: 'NEW'=1, 'ACTIVE'=2, 'CLOSED'=3. The integer index is stored on disk, not the string. Conversion happens at read time. Below 256 declared values ENUM uses 1 byte per row; between 256 and 65535, it uses 2 bytes.

## What it's for

ENUM offers three concrete advantages: compact storage (1-2 bytes instead of N characters of a VARCHAR), an "only these values allowed" constraint declared at schema level without needing a separate CHECK, and readable queries (`WHERE status = 'ACTIVE'`) with no JOIN against a lookup table.

## When to use it

It's the right call when the value domain is genuinely closed and stable over time: days of the week, fixed binary or ternary states, polarity, regulated transaction types. It also works perfectly inside a small lookup table (5-50 rows), where its limits become irrelevant.

## Limits to know

- **Case-insensitive**: `'ACTIVE'` and `'active'` are the same value (different behaviour from PostgreSQL)
- **Ordering by declaration position**, not alphabetical — an `ORDER BY` can produce surprising results
- **Modifying the ENUM** (inserting a value in the middle, renaming, reordering) requires a table rebuild, expensive on large tables
