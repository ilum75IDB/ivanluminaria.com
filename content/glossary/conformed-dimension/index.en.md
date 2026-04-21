---
title: "Conformed Dimension"
description: "A dimension shared across multiple data marts with the same structure, semantics and key. Enables consistent, additive cross-process analysis."
translationKey: "glossary_conformed_dimension"
aka: "Shared Dimension"
articles:
  - "/posts/data-warehouse/bus-matrix-terreno-comune"
---

**Conformed Dimension** is a dimension used in more than one fact table or data mart with the same structure, the same semantics and the same key. It's the cornerstone of Kimball's bus architecture.

## What "conforming" means

Conforming a dimension means agreeing on three elements:

- **Unique natural key**: which identifier represents the entity (tax code, customer code, product code, VAT number)
- **Shared attributes**: which columns are common to every data mart using the dimension (country, region, category, etc.)
- **Grain**: the level of detail of the dimension (one row per customer, not per segment)

Attributes specific to a single department can stay in local dimension tables, but they must not enter the conformed part of the dimension.

## What it's for

Without conformed dimensions, measures coming from different fact tables cannot be reliably compared. With conformed dimensions, a query that crosses sales and marketing campaigns on the same customer returns a consistent result because "customer" means the same thing in both processes.

## Physical implementation

A conformed dimension doesn't have to be a single shared physical table. It can be:

- **Replicated** across multiple schemas (a pragmatic choice when data marts live on different databases)
- **Centralized** in a dedicated schema (e.g. `dim_conformed`) with views or synonyms in the data marts
- **Virtualized** through data virtualization tools

What matters is that the three properties — structure, semantics, key — are identical in every copy.

## When governance is needed

Keeping conformity over time requires a governance committee with representatives from the departments using the dimension. Every change (a new attribute, a new dedup rule, a new acquisition channel) must be agreed upon and propagated in a coordinated way — otherwise conformed dimensions drift and the whole structure collapses.
