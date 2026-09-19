---
title: "Data Warehouse Architect"
seoTitle: "Data Warehouse Architect Oracle/PostgreSQL"
description: "Ivan Luminaria, Data Warehouse Architect Oracle/PostgreSQL: 30 years designing DWH solutions, Kimball dimensional modelling, ETL pipelines and analytical architectures."
date: "2026-09-14"
lastmod: "2026-09-20"
draft: false
layout: "simple"
---

**[Download PDF]({{% staticurl "downloads/CV_DWH_Architect_Ivan_Luminaria_202609_EN.pdf" %}})** | **[LinkedIn Profile](https://www.linkedin.com/in/ivanluminaria)**

> **One role, four pillars.** This profile is one of the four pillars of [Technical Leader for Mission-Critical Databases and Data Warehouses](/en/resumes/technical-leader/).

---

## Professional Profile

Most of the times I've been called to "design a new DWH", the existing DWH was fine. It just needed to be understood. Thirty years of Oracle, the last fifteen as a DWH Architect — I've learned the bottleneck is almost never the platform.

What I see right away when a proposal for a new platform lands on the table: the partition strategy never revisited after five years of growth. The PL/SQL ETL running serial when it could run parallel. The materialized view no one has refreshed since the schema change in 2019. It's the details that pile up, not the technologies that age out.

Analytical batches cut from 4 hours to under 30 minutes on Oracle OCI and Autonomous Database — no hardware change, only working on design and execution plans. Atradius Surety: DWH consolidating 4 EU countries, 60,000+ lines of PL/SQL, full daily ingestion under 2 hours. GENERALI: insurance DWH 500 GB–8 TB. TIM (via Huawei): 30+ Oracle databases on Exadata, 800M records/day, SLAs under 500 ms. ODI 10g→12c migration for Allianz and Mediobanca — never from scratch, always in continuity. Kimball, Inmon, star/snowflake, SCD, bus matrix. Long-standing Oracle Italy trainer on SQL, PL/SQL, tuning. What I bring: an independent second opinion before you sign a six-figure proposal, a method that starts from the data the system already records (AWR, ASH, wait events, execution plans), and the discipline to say "your current system can still hold — here's how".

---

## Areas of engagement

- **Data Warehouse design** — dimensional modelling, star and snowflake schemas, Slowly Changing Dimensions, bus matrix, source-to-target mapping.
- **ETL/ELT design and optimisation** — PL/SQL pipelines, Oracle Data Integrator, migration of legacy Oracle Warehouse Builder projects, cross-source integration.
- **DWH performance tuning** — partitioning strategies, compression, materialised views, query rewriting, execution plan analysis.
- **Modernisation and migration** — assessment of Oracle-based DWHs toward PostgreSQL alternatives, cloud DWH platforms (OCI, AWS, Azure).

---

## Key results

- **Several hundred Oracle databases** across 30 years, with focus on DWH design, ETL/ELT and administration.
- **Surety DWH** (Atradius) consolidating **4 European countries** (Italy, Spain, France, Northern Europe): **60,000+ lines of PL/SQL**, full daily load in **under 2 hours**, real-time monitoring of loading stages.
- DWH design on datasets exceeding **2 billion rows** with integration of **15+ heterogeneous sources**.
- Snowflake data model on Oracle Analytics Cloud with ETL on Oracle 19c in OCI for billing statistics, customer segmentation, portfolio and cost/revenue tracking.
- Critical analytical batches cut **from 4 hours to under 30 minutes** on Oracle in OCI and Autonomous Database.
- PostgreSQL DWH designed as **cost-effective alternative** to Oracle for banking and Telepass-related workloads.

---

## Core Skills

### DWH methodologies

- Multidimensional data modelling (Kimball, Inmon)
- Star Schema, Snowflake Schema, Slowly Changing Dimensions (SCD Type 1/2/3), Bus Matrix design

### Oracle stack

- Oracle Database up to 23ai, Exadata, RAC, Data Guard, Autonomous Database (ADB)
- Performance Tuning (AWR, ADDM, SQL Tuning Advisor), Storage Management (ASM), Backup & Recovery (RMAN), Oracle TDE

### PostgreSQL

- PostgreSQL 14+, Query Optimization, Table Partitioning
- `pg_stat_statements`, PgBouncer, logical replication, VACUUM/Autovacuum tuning

### Cloud

- Oracle Cloud Infrastructure (OCI): Compute, Storage, Networking, Database Services, Autonomous Database
- AWS Aurora PostgreSQL, Microsoft Azure Database environments

### ETL/ELT and Business Intelligence

- ETL pipelines in PL/SQL, Unix Shell scripting
- Oracle Data Integrator (ODI), Oracle Warehouse Builder (OWB, legacy projects)
- Oracle Analytics Cloud (OAC): Semantic Model Designer, dashboards and reports

### Languages, systems and cross-cutting

- Advanced SQL, advanced PL/SQL, Unix Shell scripting
- Linux (RHEL, CentOS, Oracle Linux), Unix, Windows Server
- Project Management (Agile/Scrum), team leadership up to 7 people, technical training

---

## Professional Experience

### IDEA DB CONSULTING S.R.L. — Rome, Italy (Full Remote Europe)
**Founder · Data Warehouse Architect · Oracle & PostgreSQL Expert** | 2022 – Present

- **SILICONDEV → POSTE ITALIANE** — Senior Database Consultant | Jul 2025 – Present:
  - Administration of about 1,500 MySQL and PostgreSQL instances across production, certification and development.
  - Performance monitoring, query tuning, replication management and capacity planning at enterprise scale.
- **GENERALI Insurance** — PM DWH Lead | Feb 2024 – May 2025:
  - Technical coordination on the insurance-sector Data Warehouse on Oracle databases from 500 GB to 8 TB.
  - Direct client interface for requirements, scope definition and solution presentation.
- **ATRADIUS, Surety division** — DWH Architect | 2022 – 2026:
  - Unified Oracle Data Warehouse consolidating data from 4 European countries (Italy, Spain, France, Northern Europe) from heterogeneous sources (Oracle, SQL Server, external files).
  - Modelling of core business domains (client portfolio, policies, contracts, billing, claims, claim transactions).
  - Over 60,000 lines of PL/SQL, loading framework with checkpoints and real-time logging; full daily load in under 2 hours.
- **Other Banking, Telco and payments clients** — DWH design and architecture:
  - Kimball/Inmon DWH architectures on datasets above 2 billion rows, integration of 15+ heterogeneous sources.
  - Critical analytical batches cut from 4 hours to under 30 minutes on Oracle in OCI and Autonomous Database.
  - PostgreSQL DWH as a cost-effective alternative to Oracle with partitioning strategies and query optimisation.

---

### FREELANCE / INDEPENDENT CONSULTANT — Rome, Italy (Full Remote Europe)
**Oracle DBA · Performance Tuning · DWH Architect** | 2013 – 2022

- **FAI SERVICE** — DWH Architect & Oracle DBA | 2021 – 2023:
  - Snowflake data model on Oracle Analytics Cloud, ETL on Oracle 19c in OCI, dashboards for billing, segmentation and portfolio.
  - *(contract transitioned to IDEA DB CONSULTING from 2022 with contract novation)*
- **LISCOR → Finwave, Gruppo Lutech** — Oracle DBA and DWH development in the financial sector | 2020 – 2023:
  - Advanced PL/SQL development and query optimisation for financial applications with millions of daily transactions.
  - *(contract transitioned to IDEA DB CONSULTING from 2022 with contract novation)*
- **NIMIS → Huawei → for TIM** — Oracle DBA and DWH Architect | 2020 – 2022:
  - Telco DWH architecture on 30+ critical Oracle databases (67+ instances on Exadata clusters) supporting over 20 million prepaid mobile users.
  - Fact tables ingesting up to 800 million traffic records per day, advanced partitioning and compression strategies, SLAs under 500 ms; ASM and Oracle TDE.
  - *(contract transitioned to IDEA DB CONSULTING from 2022 with contract novation)*
- **DatabTech, Milan** — Oracle DBA and DWH Architect for Allianz and Mediobanca | 2018 – 2021:
  - Migration of Oracle Data Integrator (ODI) projects from version 10g to 12c.
- **Other Banking, Insurance and Telco clients** | 2013 – 2018:
  - Data Warehouses on Oracle and PostgreSQL platforms, with Kimball/Inmon modelling.
  - ETL/ELT pipelines handling up to 500 million rows per load cycle.
  - Oracle Data Guard configurations for high availability and disaster recovery.
  - Teams of 3–7 people in distributed multicultural contexts, iterative Agile approach, budgets in the €100K – €500K range.

---

### AUSELDA AED GROUP S.P.A. — Rome, Italy
**Data Warehouse Architect · Performance & Tuning Expert · Oracle Project DBA** (for the Public Administration) | 2009 – 2013

- Kimball/Inmon DWH design and modelling for Public Administration entities.
- ETL/ELT development, complex SQL optimisation, Oracle Warehouse Builder product specialist.

---

### ORACLE ITALIA S.R.L. — Various offices, Italy & Madrid, Spain
**Data Warehouse Architect · Oracle DBA · SQL & PL/SQL Developer · Training Specialist** | 1999 – 2009

- Data Warehouses for Telco clients (TIM, Vodafone, TRE), Finance (Bank of Italy, Generali, RAS) and Pharma (Menarini), with Kimball/Inmon modelling and ETL on Oracle Warehouse Builder.
- International engagement on Vodafone Spain (Madrid).
- Training Specialist (2000-2001) on SQL, PL/SQL, Oracle DBA and Performance & Tuning.

---

### ETNOTEAM S.P.A. · 1999 — S.EL.DAT. S.P.A. · 1997 – 1999
**Web and Software Developer · Junior Oracle DBA** (for Telecom, Rover Italia)

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

- Cross-layer reading of complex situations, down to the real cause
- Translation between technical and business levels, for teams and management
- Coordination of distributed teams, on-site and full remote
- Mentoring and knowledge transfer
- Priority management under operational pressure
- Clear, evidence-based technical communication

---

*I authorise the processing of my personal data pursuant to Art. 13 of EU Regulation 2016/679 (GDPR).*

Rome, September 2026

---

**[Download PDF]({{% staticurl "downloads/CV_DWH_Architect_Ivan_Luminaria_202609_EN.pdf" %}})** | **[LinkedIn Profile](https://www.linkedin.com/in/ivanluminaria)** | **[Back to previous page](/en/resumes/)**
