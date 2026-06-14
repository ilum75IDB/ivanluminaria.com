---
title: "Data Catalog"
description: "Centralized inventory of organizational data assets with metadata, lineage, and search: makes governance navigable without technical intervention."
translationKey: "glossary_data_catalog"
aka: "Enterprise Data Catalog"
articles:
  - "/posts/data-warehouse/data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati"
---

A Data Catalog is an organized inventory of all data assets available in an organization: tables, views, datasets, reports, APIs, files. Each asset carries technical and business metadata, lineage, quality classifications, and a shared glossary. The goal is to make data findable and understandable without opening a ticket to the engineering team for every question.

## How it works

The catalog collects metadata from heterogeneous sources through connectors (relational databases, data lakes, BI tools, ETL pipelines). For each asset it exposes:

- **technical metadata**: schema, data type, cardinality, update frequency
- **business metadata**: owner, natural-language description, domain tags
- **lineage**: a graph showing where data originates and where it is consumed
- **data quality score**: aggregate metrics computed by upstream validation processes

Users search assets via full-text search or domain/tag navigation. Data stewards enrich entries with annotations and approvals.

## When to use it

A Data Catalog becomes necessary when the number of sources exceeds the capacity for manual documentation — typically beyond 20–30 active datasets — or when compliance requires end-to-end traceability (GDPR, HIPAA, SOX). It is also the natural entry point for data contracts: the catalog exposes a dataset's specifications, while the contract formalizes quality guarantees and SLAs.

Without a catalog, governance stays a rarely-updated Word document; with one, it becomes a live system queryable by anyone with access.
