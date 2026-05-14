---
title: "OID (Object Identifier)"
description: "Internal numeric identifier used by PostgreSQL to refer to system objects (tables, types, functions). Unsigned 4-byte integer managed by the engine."
translationKey: "glossary_postgresql_oid"
aka: "PostgreSQL OID, Object Identifier"
articles:
  - "/posts/postgresql/enum-postgresql-paga-o-pesa"
---

The **OID** (Object Identifier) is an internal numeric identifier PostgreSQL uses to refer to system objects: tables, data types, functions, schemas, roles. It's an unsigned 4-byte integer managed by PostgreSQL itself, distinct from the primary keys of user tables.

## How it works

Every system catalog object (e.g. `pg_class` for tables, `pg_type` for types, `pg_enum` for ENUM values) has an `oid` column acting as the unique identifier. OIDs are assigned automatically by the engine and used as keys in JOINs across system catalogs. PostgreSQL exposes several conversion functions (`oid::regclass`, `oid::regtype`, etc.) to obtain the human-readable name of an object from its OID.

## What it's for

To identify every database object uniquely and stably across dump-restore. For ENUM types, each value declared in `CREATE TYPE ... AS ENUM` is assigned an OID, which gets stored in the rows of the tables that use the type. This lets you keep the value in just 4 bytes while still tying it to the readable name and the positional ordering.

## When to use it

Rarely directly in applications — the OID is an implementation detail invisible to most queries. It becomes relevant when analysing system catalogs (`information_schema`, `pg_catalog`), when writing introspection or monitoring tooling, and when debugging the behaviour of complex types like ENUMs or domains.
