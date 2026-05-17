---
title: "Oracle major release"
description: "Main version of the Oracle Database server with significant feature changes and dedicated Premier support cycle. Numbering: 19c, 21c, 23ai, 26ai."
translationKey: "glossary_oracle_major_release"
aka: "Oracle Database release model"
articles:
  - "/posts/oracle/enum-oracle-19c-26ai-domini"
---

An **Oracle Database major release** is a main version of the product with significant feature changes, a dedicated Premier support cycle, and its own numbering. With each major release Oracle introduces **new SQL syntax, new data types, new engine operating modes**, and — periodically — raises the lower bound of supported compatibility versions.

## How the cycle works

Oracle alternates two kinds of major release:

- **Long-Term Release (LTS)** — extended Premier support (typically 5 years + 3 of extended). It's the reference version for critical enterprise systems, where upgrades are planned years in advance. **19c** (LTS, released 2019) and **23ai** (LTS, released 2024) are the recent LTS releases.
- **Innovation Release** — short support (typically 2 years of Premier, no extended). Meant for those who want to experiment with new features early and then consolidate on the next LTS. **21c** was the Innovation Release between 19c and 23ai.

## Why knowing the version matters

It determines **what you can write** in your SQL: `JSON Relational Duality`, `SQL Domain` and `Vector Search` exist from 23ai onwards; `ASSERTION`s will arrive with 26ai. It also determines what you **can no longer write**: features deprecated in earlier versions are removed at regular intervals in subsequent major releases. On the upgrade path from 19c to 23ai, the differences typically affect DDL, dictionary views, and a handful of system PL/SQL packages.

## The four releases that matter for a modern schema

| Release | Type | Year | What it brings on constraints and domains |
|---------|------|------|-------------------------------------------|
| **19c** | LTS | 2019 | Starting point: `CHECK` + lookup table |
| **21c** | Innovation | 2021 | Nothing substantial for value domains |
| **23ai** | LTS | 2024 | `SQL Domain`, `ALTER DOMAIN`, `Annotations` |
| **26ai** | LTS | 2026 (announced) | `ASSERTION` cross-table |
