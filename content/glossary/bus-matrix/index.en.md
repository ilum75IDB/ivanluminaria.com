---
title: "Bus Matrix"
description: "Ralph Kimball's two-dimensional grid with business processes as rows and conformed dimensions as columns. An organizational alignment tool used before the physical design of the data warehouse."
translationKey: "glossary_bus_matrix"
aka: "Kimball Bus Matrix, Data Warehouse Bus Architecture"
articles:
  - "/posts/data-warehouse/bus-matrix-terreno-comune"
---

**Bus Matrix** is a design tool introduced by Ralph Kimball to explicitly align an organization's business processes with the shared analytical dimensions that will describe them in the data warehouse.

## What it looks like

A two-dimensional matrix:

- **Rows**: business processes (sales, returns, campaigns, invoicing, inventory movements, policy issuance, premium collection, etc.)
- **Columns**: candidate conformed dimensions (customer, product, time, geography, channel, employee, etc.)
- **Cells**: an X if that process uses that dimension

Reading the matrix vertically tells you how many fact tables touch a given dimension: the more X's, the more critical conformity is for that dimension.

## What it's for

The bus matrix generates no code, creates no tables and tunes no queries. It exists for one purpose: to force the stakeholders (IT, business, finance, marketing) to stare at the same sheet of paper and agree, explicitly, on what they mean by "customer", "product", "date". It's an organizational alignment exercise that precedes the physical design.

## When to do it

At the very start of the project, before any CREATE TABLE. Kimball recommends it as the first step of the DWH lifecycle. Doing it later, when data marts have already been built independently by departments, costs orders of magnitude more: you need governance workshops, after-the-fact matching processes, mapping tables (xrefs) and time to renegotiate existing definitions.

## Relationship with conformed dimensions

The bus matrix is the diagnostic tool, conformed dimensions are the solution. Wherever two processes share a dimension in the matrix, that dimension *must* be conformed — same key, same structure, same semantics — otherwise cross-process analyses will return inconsistent numbers.
