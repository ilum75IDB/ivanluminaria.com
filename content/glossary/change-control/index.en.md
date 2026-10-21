---
title: "Change Control"
description: "Formal GxP process for managing changes to hardware, software, and procedures: risk assessment, test protocol, documentation, and authoritative signatures."
translationKey: "glossary_change_control"
aka: "Change Management Process"
articles:
  - "/posts/oracle/latenza-wan-e-change-control-gxp-il-costo-reale-del-lift-and-shift"
---

Change control is the mandatory formal process in GxP-validated systems (Good Practice) that governs any modification to infrastructure, software, or operational procedures. In pharmaceutical, medical, and biotech regulated environments, implementing a change without an approved change control record constitutes a documented deviation with direct regulatory consequences.

## How It Works

The typical cycle consists of four sequential phases:

1. **Change request** — technical description of the proposed modification, rationale, and impacted systems.
2. **Risk assessment** — impact analysis on existing validation status (IQ/OQ/PQ), data integrity, and operational continuity.
3. **Test protocol** — definition of tests to be executed before go-live, with explicit acceptance criteria.
4. **Approval and implementation** — authoritative signatures from designated roles (QA, IT, business owner) and post-implementation documentation.

Each phase produces traceable artifacts that must be retained in the document management system for internal audits and regulatory inspections.

## Operational Context

Change control becomes a critical bottleneck in cloud migration projects (lift-and-shift) because each migrated component — database, middleware, operating system — may require a separate change request. In Oracle environments running GxP systems, even a minor patch update can trigger a full re-validation cycle if it affects already-qualified functionality. Average approval timelines in mid-size organizations range from 2 to 8 weeks for medium-risk changes — a factor that migration plans systematically underestimate.
