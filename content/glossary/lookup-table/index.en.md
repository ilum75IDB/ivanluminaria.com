---
title: "Lookup table"
description: "Reference table linked via foreign key that stores the valid values of an enumeration, along with any descriptive attributes."
translationKey: "glossary_lookup_table"
aka: "Reference table"
articles:
  - "/posts/mysql/enum-mysql-semplifica-o-complica"
---

A **lookup table** is a reference table that stores the valid values of an enumerated domain, linked to the tables using it via a foreign key. It's the "pure-database" way to model an enumeration, an alternative to native types like ENUM or to CHECK constraints.

## What it looks like

The canonical schema has at least three columns: a surrogate `id` (typically `SMALLINT` or `TINYINT`) as the primary key, a textual `code` (the natural key, usually unique), and an extended `description`. Often you add attributes like `display_order` for visual sorting, `active` for soft-delete, and audit timestamps.

## What it's for

The main advantage over ENUM is flexibility: renaming a description is an `UPDATE` on one row, no migration or rebuild of the referencing table. You can add attributes (localised labels, order, flags) without touching child schemas. It's the right fit when values change over time or when you need metadata attached to them.

## When to use it

It's the right call when:
- Values get modified with some frequency (additions, renames, deactivations)
- You need extra attributes (translations, order, flags)
- You want to manage values at runtime without DDL (admin panels)
- The number of values grows over time, past 20-30

The price is the JOIN required in queries, but it's easily optimised with composite indexes and dedicated views.
