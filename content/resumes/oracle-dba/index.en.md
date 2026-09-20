---
title: "Oracle DBA & Performance Tuning Expert"
seoTitle: "Oracle DBA & Performance Tuning Expert"
description: "Ivan Luminaria, Oracle DBA & Performance Tuning Expert: 30 years administering mission-critical databases, RAC, Data Guard, Exadata, AWR/ASH and Oracle Cloud."
date: "2026-09-14"
lastmod: "2026-09-20"
draft: false
layout: "simple"
---

**[Download PDF]({{% staticurl "downloads/CV_Oracle_DBA_Ivan_Luminaria_202609_EN.pdf" %}})** | **[LinkedIn Profile](https://www.linkedin.com/in/ivanluminaria)**

> **One role, four pillars.** This profile is one of the four pillars of [Technical Leader for Mission-Critical Databases and Data Warehouses](/en/resumes/technical-leader/).

---

## Professional Profile

Hundreds of Oracle databases administered over three decades across banking, insurance, telco, public administration and postal — multi-node Exadata clusters, fact tables ingesting 800M+ records per day with SLAs under 500 ms, environments serving 20M+ end users. MySQL and PostgreSQL administration at enterprise scale. Analytical batches cut from 4 hours to under 30 minutes on Oracle OCI and Autonomous Database — no platform change. OCP from the days when they were rare. Oracle Italy trainer on SQL, PL/SQL, administration, performance tuning; twenty-five years of continuous mentoring of junior DBAs toward senior level.

What I see when a post-incident request lands: monitoring metrics green until forty minutes before. The vendor ticket closed as "unable to reproduce". The junior DBA who inherited the system from a senior gone at year-end and doesn't yet have the mental map to connect the dots. The causal chain almost always sits in the interplay between layers — application, database, storage, network — not inside a single layer. Tools show symptoms, not causes.

Post-Incident Root Cause Analysis on cases where the logs of the moment had been rotated or compressed badly: AWR and ASH history, OS and storage logs, change register. I've reconstructed causal chains the team thought were lost, and produced documents that went before the board without the senior DBA being pinned as the default answer. What I bring: a cross-layer method built on real systems. We don't look for culprits — we reconstruct what actually happened.

---

## Areas of engagement

- **Database Health Check** — structured assessment of performance, reliability, capacity and latent risks, with an evidence-based report and a prioritised roadmap.
- **Post-Incident Root Cause Analysis** — incident reconstruction on real data (AWR, ASH, wait events, application and infrastructure logs), separating causes, consequences and correlations.
- **Ongoing DBA leadership** — advanced tuning, upgrade and patching plans, HA/DR strategies, coordination with development and infrastructure teams.
- **Modernisation advisory** — evaluation of Oracle → PostgreSQL migrations, cloud database services and Autonomous Database moves, with cost/risk analysis independent from vendors.

---

## Key results

- **Several hundred Oracle databases** across 30 years, spanning administration, tuning, DWH, PL/SQL and project management.
- About **1,500 MySQL and PostgreSQL instances** administered today for **POSTE ITALIANE**.
- **30+ Oracle databases on Exadata** (3+5 nodes, **67+ instances**) on a telco engagement for **TIM (via Huawei)**, serving **20M+ prepaid mobile users**: up to **800M records per day**; critical queries **under 500 ms** under 24/7 on-call.
- Critical analytical batches cut **from 4 hours to under 30 minutes** on Oracle in OCI and Autonomous Database.
- **Surety DWH** (Atradius) across **4 European countries** (Italy, Spain, France, Northern Europe) supported at DBA layer: **60,000+ lines of PL/SQL** and full daily load in **under 2 hours**.
- ETL/ELT pipelines integrating **15+ heterogeneous sources** on datasets above **2 billion rows**.

---

## Core Skills

### Oracle Database Administration

- Oracle Database up to 23ai, Autonomous Database
- Exadata, RAC, Data Guard, GoldenGate (basic)

### Advanced performance tuning

- Analysis and diagnostics: AWR, ADDM, ASH, Statspack, SQL Trace, TKPROF, Explain Plan
- SQL tuning: complex queries, hints, SQL Profiles, SQL Plan Management (SPM)
- Instance tuning: memory (SGA/PGA), initialization parameters, wait event analysis
- Design for performance: indexing (B-tree, Bitmap, Function-based), partitioning (Range, List, Hash, Composite), compression

### HA/DR and security

- RMAN (backup, recovery, cloning), Data Guard, Flashback Technologies
- Oracle TDE, user and privilege management, auditing
- ASM (Automatic Storage Management), tablespace management

### Installation, patching, migrations

- New instance install, PSU/CPU/RU, version upgrades, cross-platform migrations

### Cloud

- Oracle Cloud Infrastructure (OCI): Compute, Storage, Networking, Database Services (VM DB, Bare Metal, Exadata CS, Autonomous Database)
- AWS Aurora PostgreSQL, Microsoft Azure Database environments

### Other databases and tools

- PostgreSQL (administration, tuning, partitioning, replication)
- MySQL (administration, replication, InnoDB optimisation)
- Oracle Enterprise Manager (OEM) Cloud Control, SQL Developer, SQL*Plus, Toad
- PL/SQL, SQL, Unix Shell scripting

---

## Professional Experience

### IDEA DB CONSULTING S.R.L. — Rome, Italy (Full Remote Europe)
**Founder · Senior Oracle DBA & Performance Tuning Expert** | 2022 – Present

- **SILICONDEV → POSTE ITALIANE** — Senior Database Consultant — MySQL & PostgreSQL DBA | Jul 2025 – Present:
  - Administration of about 1,500 MySQL and PostgreSQL instances across production, certification and development.
  - Performance monitoring, query tuning, replication management and capacity planning at enterprise scale.
- **GENERALI Insurance** — Oracle DBA & Tuning Expert | Feb 2024 – May 2025:
  - Administration and advanced tuning of Oracle databases from 500 GB to 8 TB for insurance-sector applications.
  - AWR/ADDM analysis, SQL optimisation, proactive bottleneck resolution.
- **ATRADIUS, Surety division** — Oracle DBA | 2022 – 2026:
  - DBA layer supporting the multi-country DWH (Italy, Spain, France, Northern Europe) — 60,000+ lines of PL/SQL ETL, full daily load under 2 hours in OCI.
- **Other Banking, Telco and payments clients**:
  - Critical analytical batches cut from 4 hours to under 30 minutes on Oracle in OCI and Autonomous Database.
  - ETL/ELT from 15+ heterogeneous sources on 2B+ rows; RMAN, OEM, patching; PostgreSQL DWH as cost-effective alternative to Oracle.

---

### FREELANCE / INDEPENDENT CONSULTANT — Rome, Italy (Full Remote Europe)
**Senior Oracle DBA & Performance Tuning Expert · DWH Architect** | 2013 – 2022

- **FAI SERVICE** — Oracle DBA | 2021 – 2023:
  - Administration and tuning of Oracle 19c in OCI supporting ETL and Oracle Analytics Cloud dashboards.
  - *(contract transitioned to IDEA DB CONSULTING from 2022 with contract novation)*
- **LISCOR → Finwave, Gruppo Lutech** — Oracle DBA in the financial sector | 2020 – 2023:
  - Advanced PL/SQL development and query optimisation for financial applications with millions of daily transactions.
  - *(contract transitioned to IDEA DB CONSULTING from 2022 with contract novation)*
- **NIMIS → Huawei → for TIM** — Senior Oracle DBA & Performance Tuning Expert | 2020 – 2022:
  - 30+ critical Oracle databases (67+ instances) on 3- and 5-node Exadata clusters.
  - Direct responsibility for advanced performance tuning: AWR/ADDM analysis, SQL optimisation, indexing, partitioning and compression; ingestion up to 800M records/day, SLAs under 500 ms.
  - Storage management (ASM) and Oracle TDE for data security; 24/7 on-call for critical incident resolution.
  - *(contract transitioned to IDEA DB CONSULTING from 2022 with contract novation)*
- **DatabTech, Milan** — Oracle DBA and DWH Architect for Allianz and Mediobanca | 2018 – 2021:
  - Migration of Oracle Data Integrator (ODI) projects from version 10g to 12c.
- **Other Banking, Insurance and Telco clients** | 2013 – 2018:
  - Oracle DBA and tuning services for banking, insurance and telco clients.
  - Complex SQL and instance tuning; RMAN backup and recovery; Oracle Data Guard HA/DR with switchover/failover procedures.
  - Small technical teams in migration and upgrade projects.

---

### AUSELDA AED GROUP S.P.A. — Rome, Italy
**Project Oracle DBA · Performance & Tuning Expert** (for the Public Administration) | 2009 – 2013

- Administration and optimisation of Oracle databases supporting Public Administration applications.
- SQL and ETL tuning for DWH systems; installation, patching and database security management.

---

### ORACLE ITALIA S.R.L. — Various offices, Italy & Madrid, Spain
**Oracle DBA · DWH Architect · SQL & PL/SQL Developer · Training Specialist** | 1999 – 2009

- Oracle DBA roles for enterprise clients Telco (TIM, Vodafone, TRE), Finance (Bank of Italy, Generali, RAS) and Pharma (Menarini) with progressively increasing responsibilities.
- International engagement on Vodafone Spain (Madrid).
- Training Specialist (2000-2001) on Oracle Database Administration and Performance & Tuning.

---

### ETNOTEAM S.P.A. · 1999 — S.EL.DAT. S.P.A. · 1997 – 1999
**Software Developer · Junior Oracle DBA** (for Telecom, Rover Italia)

---

## Education

- **Computer Engineering studies (Software Engineering)** | Roma Tre University, Rome | 1994 – 2000
- **Scientific High School Diploma** | Liceo Scientifico Isacco Newton / Manieri Copernico, Rome | 1988 – 1993
- **Advanced English (C1/C2)** | The British Council, Rome | 2003 – 2004
- Continuous learning: Scrum Agile and Project Management (Randstad / Forma.temp, 2024) · Data Wrangling with SQL (Coursera, UC Davis, 2021) · Advanced SQL for Query Tuning and Oracle 12c (LinkedIn Learning, 2020)

---

## Languages

- **Italian**: Native
- **English**: C1/C2 (Fluent, professional)
- **Spanish**: C1 (Fluent)
- **Romanian**: C1 (Fluent)
- **French**: A1/A2 (Basic)

---

## Soft Skills

- Methodical analysis of performance problems, down to the real cause
- Priority management and adherence to deadlines under operational pressure
- Clear, evidence-based technical communication
- Attention to detail and operational precision
- Continuous learning and technological adaptability

---

*I authorise the processing of my personal data pursuant to Art. 13 of EU Regulation 2016/679 (GDPR).*

Rome, September 2026

---

**[Download PDF]({{% staticurl "downloads/CV_Oracle_DBA_Ivan_Luminaria_202609_EN.pdf" %}})** | **[LinkedIn Profile](https://www.linkedin.com/in/ivanluminaria)** | **[Back to previous page](/en/resumes/)**
