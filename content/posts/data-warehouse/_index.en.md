---
title: "Data Warehouse"
date: "2026-03-10T08:03:00+01:00"
description: "Data Warehouse architecture in practice: dimensional modeling, hierarchies, ETL and loading strategies. When data is not just meant to work, but to drive decisions."
image: "data-warehouse.cover.jpg"
layout: "list"
---

I have seen data warehouses built on daily granularity because "the business is fine with that" — and become useless the very next day, when marketing asked for hourly conversion analysis. I have seen customer dimensions without historisation, overwriting the postal code every time someone moved — and last year's reports that no longer matched. I have seen ETL jobs reloading 200 million rows in full every night because nobody ever had the courage to redesign the delta.

And I have seen the exact opposite: small, well-modelled data marts, with the bus matrix properly drawn — answering questions nobody had thought to ask yet, without touching a single line of code.

The difference has never been the technology. It has always been **the model**.

------------------------------------------------------------------------

A data warehouse is not a database with bigger tables. It is **a different way of thinking about data** — oriented towards analysis, history, decisions.

In transactional databases the *present moment* is what counts: the order you are inserting, the current balance, the row you are updating. In a data warehouse what counts is the *journey*: what that customer looked like six months ago, how the product has changed over time, which version of the master data was valid when that contract was signed.

Almost always, a DWH that does not hold up can be spotted by these things:

- **wrong granularity** in the fact table — too coarse and you lose detail, too fine and you slow everything down
- **flat dimensions** with no SCD handling — lost history, impossible "as-was" analyses
- **unbalanced hierarchies** that break aggregations the moment the business asks for a drill-down
- **bus matrix never drawn** — data marts that do not talk to each other, the same entities modelled differently in every department
- **ETL designed as a copy** rather than as a transformation — transactional messiness arriving untouched in analytics

These are problems you cannot see in development. They blow up six months later, when the business asks for reports the model cannot support.

------------------------------------------------------------------------

## 📊 What I ask the business before touching the model

Before even drawing a fact table, there are five questions I put to the business. They are not optional — they are the difference between a data warehouse that lasts ten years and one that needs rewriting after two.

| Question | What I am trying to understand | Why it is critical |
|---|---|---|
| **What grain do you need the data at?** | Daily, hourly, single transaction | Always pick the finest useful grain — aggregating later is possible, disaggregating is not |
| **How far back in time?** | History required, analytical depth | Drives volumes, storage, partitioning and archiving strategies |
| **What happens when a master record changes?** | A customer moves, a product changes category | Determines the SCD type (1, 2, 3, 6) for each dimension |
| **Which hierarchies must it support?** | Drill-down, roll-up, alternative paths | Prevents ragged dimensions, unjustified snowflakes, slow joins on aggregates |
| **What latency is acceptable?** | Nightly batch, intraday, near real-time | It changes everything: ETL, model, infrastructure, cost |

Five questions. Twenty minutes of meeting. Weeks of rewrites avoided.

------------------------------------------------------------------------

## 📚 What I talk about here

Real stories of data warehouse design and restructuring in production. Dimensional modelling (Kimball read properly, not as slogans), slowly changing dimensions, bus matrix, hierarchies, incremental loading strategies and analytical performance.

No textbook recipes. Just solutions applied to real systems — insurance, finance, public administration, telco, postal — that serve real business decisions.

------------------------------------------------------------------------

A data warehouse is not built to contain data.

It is built to answer questions — and those questions, inevitably, change.
