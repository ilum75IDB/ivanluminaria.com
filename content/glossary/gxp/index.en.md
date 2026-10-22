---
title: "GxP"
description: "Collective term for Good Practice regulatory guidelines in pharma: mandates change control, documented testing, and formal Quality approval for any computerized system change."
translationKey: "glossary_gxp"
aka: "Good Practice (GMP, GLP, GCP, GDP)"
articles:
  - "/posts/oracle/latenza-wan-e-change-control-gxp-il-costo-reale-del-lift-and-shift"
---

GxP is a collective acronym covering the "Good Practice" regulatory guidelines that apply to pharmaceutical, biotechnology, and medical device industries. The "x" is a placeholder for the specific discipline: GMP (Manufacturing), GLP (Laboratory), GCP (Clinical), GDP (Distribution). Any computerized system that falls within GxP scope is subject to strict requirements for validation, data integrity, and change control.

## Regulatory scope

The two primary references for computerized systems are **EU GMP Annex 11** (Europe) and **21 CFR Part 11** (FDA, USA). Both require that every GxP computerized system be validated, that data integrity is maintained, and that changes are tracked via an audit trail. At the database level, this means schema version control, immutable logs, and backup procedures verified at documented intervals.

## Operational impact on change control

Any modification to a GxP system — DBMS upgrade, schema migration, configuration parameter change — must follow a formal change control process:

1. **Impact Assessment**: risk evaluation against the existing validated state.
2. **Documented testing**: IQ (Installation Qualification), OQ (Operational Qualification), PQ (Performance Qualification).
3. **Quality approval**: formal sign-off before release to production.

A lift-and-shift of an Oracle database to the cloud, for example, is never transparent in a GxP environment: the underlying infrastructure changes, and that reopens the validation cycle. Change control timelines — often 4 to 12 weeks — are the hidden cost that migration plans consistently underestimate.

## When the DBA becomes part of the regulatory process

In GxP environments, the DBA is not only responsible for performance and availability: they are an actor within the quality system. DDL statements executed in production must be pre-approved, backups must be tested at documented frequencies, and every anomaly must generate a deviation report. WAN latency or an unplanned failover are not just technical incidents — they can be regulatory events requiring formal investigation.
