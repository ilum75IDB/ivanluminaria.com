---
title: "Data Mart"
description: "A subset of the data warehouse focused on a single business process or functional area. Often built independently by a department."
translationKey: "glossary_data_mart"
aka: "Departmental Data Mart, Subject-Area Data Mart"
articles:
  - "/posts/data-warehouse/bus-matrix-terreno-comune"
---

**Data Mart** is a subset of a data warehouse focused on a single business process, a functional area (sales, marketing, finance) or a department. It typically holds one or a few fact tables and the dimensions related to them.

## Why data marts exist

In real organizations, a complete enterprise DWH takes years to build. Data marts are a pragmatic compromise: build first the piece a department needs now (e.g. a sales data mart for marketing) and integrate it with the others later. This is Kimball's bottom-up approach.

## The divergence risk

When multiple data marts are built independently by individual departments — often with different BI tools, on different source systems, on different timelines — the risk is that "customer" ends up meaning three different things across three data marts. Totals don't match, cross-department analysis becomes impossible or slow, and the CFO ends up with three versions of the truth.

## Conformed vs independent data marts

The critical difference is whether the data mart shares conformed dimensions or not:

- **Conformed data marts** (Kimball): share conformed dimensions (customer, product, time, geography) and can therefore be queried together consistently
- **Independent data marts**: built without shared governance, drift over time and generate the classic "three versions of the truth" problems

The bus matrix is the design tool that prevents the second scenario.

## When it makes sense

A data mart makes sense when:

- The functional scope is well-defined (one process, one department)
- Conformed dimensions are already available or will be built alongside
- The cost of a full enterprise DWH isn't justified
- You need fast time-to-value for a specific use case

It doesn't make sense as a "permanent isolated solution": either it's the first piece of an integrated strategy, or it turns into technical debt within a few years.
