---
title: "Oracle PL/SQL Developer"
seoTitle: "Oracle PL/SQL Developer & SQL Tuning"
description: "Ivan Luminaria, Oracle PL/SQL Developer & SQL Tuning Expert: 30 years developing, refactoring and optimising PL/SQL code for enterprise data-intensive apps."
date: "2026-09-14"
lastmod: "2026-09-20"
draft: false
layout: "simple"
---

**[Download PDF]({{% staticurl "downloads/CV_Oracle_PLSQL_Ivan_Luminaria_202609_EN.pdf" %}})** | **[LinkedIn Profile](https://www.linkedin.com/in/ivanluminaria)**

> **One role, four pillars.** This profile is one of the four pillars of [Technical Leader for Mission-Critical Databases and Data Warehouses](/en/resumes/technical-leader/).

---

## Professional Profile

PL/SQL has a peculiar trait among programming languages: it stays in production for decades, often passing through four or five generations of developers who hand it over to each other. The value of whoever writes it is measured in what those successors can still read, understand and modify.

When I teach PL/SQL, I like to define it as an **exception-oriented language**: the ability to handle system exceptions and to define custom ones, declaratively inside every block, is what lets the code survive scenarios that weren't foreseeable at the time of writing.

Row-by-row cursors that could be BULK COLLECT. DML that ignores the underlying partitioning. Dynamic SQL built with string concatenation when bind variables were right there. These are the writing details that multiply execution times — the difference between a 4-hour batch and a 30-minute one almost always sits in a few pages of code. And when 60,000 lines of code govern the insurance business of four European countries, what looked like legacy becomes the operational backbone: not code to rewrite, but an executable rulebook of how the business actually works.

ETL packages of over 60,000 lines for a multi-country DWH, full daily ingestion cut from over 4 hours to under 2 hours with BULK COLLECT/FORALL, partition-aware DML and query rewriting. Analytical batches cut from 4 hours to under 30 minutes on 2B+ row datasets. Packages handling millions of daily financial transactions. PL/SQL Hierarchical Profiler, SQL Trace, TKPROF. Oracle Italy trainer on SQL and PL/SQL. Twenty-five years of continuous mentoring of junior developers toward senior level in banking, insurance, telco, public administration and postal.

Beyond PL/SQL and SQL I can read, understand and modify other languages too — Unix Shell Script, Python, Java, C++, JavaScript, HTML, CSS, Pascal and Camel. Some I studied at university, others I picked up when the code around the database needed touching. I'm no guru in any of them; but when a piece of critical logic lives outside the database — in a shell script, in a Python service, in a frontend that calls PL/SQL procedures — reading the other side helps to understand where the problem really sits.

What I bring: PL/SQL your junior developers can read and maintain, targeted refactors that reduce technical debt without hasty rewrites, and the discipline to tell technical debt from business asset.

---

## Areas of engagement

- **PL/SQL development & code review** — packages for ETL logic, data-processing procedures, PL/SQL APIs, business logic; audit and refactor of legacy PL/SQL codebases.
- **PL/SQL & SQL performance tuning** — Hierarchical Profiler analysis, BULK COLLECT/FORALL patterns, partition-aware DML, execution-plan-driven rewrites.
- **ETL/ELT design in PL/SQL** — standardised loading templates with checkpoints, real-time logging, error recovery, monitoring dashboards.
- **Mentoring & knowledge transfer** — coaching junior developers on PL/SQL best practices, code standards, testable patterns.

---

## Key results

- **Several hundred Oracle databases** across 30 years, spanning PL/SQL development, tuning, DWH and administration.
- **60,000+ lines of PL/SQL** designed and maintained for the **Surety DWH** (Atradius) multi-country across **4 European countries** (Italy, Spain, France, Northern Europe); reusable templates and real-time load monitoring.
- Full daily ingestion **from 4+ hours to under 2 hours** through query rewriting, BULK COLLECT/FORALL and partition-aware DML.
- PL/SQL packages for financial transaction processing handling **millions of daily operations** across banking and insurance clients.
- Critical analytical batches cut **from 4 hours to under 30 minutes** on 2B+ row datasets.
- ETL/ELT pipelines integrating **15+ heterogeneous sources** into Oracle and Oracle Analytics Cloud dashboards.

---

## Core Skills

### Languages

- Advanced PL/SQL · advanced SQL (Dynamic SQL, analytic functions, CTEs)
- Unix Shell scripting

### PL/SQL Development

- Packages, procedures, functions, triggers
- Records, collections, object types · error/exception handling
- Bulk processing (FORALL, BULK COLLECT) · dynamic SQL (DBMS_SQL, EXECUTE IMMEDIATE)
- PL/SQL Hierarchical Profiler
- Interaction with tables, views, sequences, synonyms

### SQL Optimisation & Performance

- Execution-plan analysis (Explain Plan), SQL Trace, TKPROF
- SQL tuning techniques (Hints, query rewriting, indexes)
- Impact of database design on PL/SQL performance

### Oracle Database

- Oracle Database up to 23ai, Autonomous Database

### Related concepts

- Data Warehousing (ETL/ELT logic), data integration
- Relational and multidimensional modelling

### Development tools

- SQL Developer, Toad, SQL*Plus
- Git and GitHub for version control

### Cloud

- Oracle Cloud Infrastructure (OCI) — database services knowledge

---

## Professional Experience

### IDEA DB CONSULTING S.R.L. — Rome, Italy (Full Remote Europe)
**Founder · Senior Oracle PL/SQL Developer · DWH Architect** | 2022 – Present

- **SILICONDEV → POSTE ITALIANE** — Senior Database Consultant | Jul 2025 – Present:
  - Administration of about 1,500 MySQL and PostgreSQL instances across production, certification and development.
  - Query tuning, performance monitoring, replication management and capacity planning at enterprise scale.
- **GENERALI Insurance** — SQL & PL/SQL Optimization | Feb 2024 – May 2025:
  - Complex query optimisation and PL/SQL development on Oracle databases from 500 GB to 8 TB for insurance-sector applications.
  - Hierarchical Profiler analysis and SQL tuning to identify bottlenecks.
- **ATRADIUS, Surety division** — PL/SQL Developer | 2022 – 2026:
  - Over 60,000 lines of PL/SQL code (packages, procedures, functions) for the multi-country DWH (Italy, Spain, France, Northern Europe) consolidating insurance claims and credit data.
  - Reusable PL/SQL templates for loading procedures with checkpoints and real-time logging.
  - Batch performance optimisation (query rewriting, BULK COLLECT/FORALL, partition-aware DML): daily cycle reduced from 4+ hours to under 2 hours.
- **Other Banking, Telco and payments clients** — PL/SQL development:
  - PL/SQL business logic packages for banking-sector DWH applications on 2B+ row datasets.
  - PL/SQL and SQL optimisation with Hierarchical Profiler analysis to identify bottlenecks.

---

### FREELANCE / INDEPENDENT CONSULTANT — Rome, Italy (Full Remote Europe)
**Senior Oracle PL/SQL Developer & DBA · DWH Architect** | 2013 – 2022

- **FAI SERVICE** — PL/SQL Developer | 2021 – 2023:
  - ETL procedures in PL/SQL on Oracle 19c in OCI for billing statistics, customer segmentation and cost/revenue tracking.
  - PL/SQL modules feeding Oracle Analytics Cloud dashboards with aggregated financial KPIs.
  - *(contract transitioned to IDEA DB CONSULTING from 2022 with contract novation)*
- **LISCOR → Finwave, Gruppo Lutech** — PL/SQL Developer in the financial sector | 2020 – 2023:
  - PL/SQL packages for financial transaction processing handling millions of daily operations across banking and insurance clients.
  - *(contract transitioned to IDEA DB CONSULTING from 2022 with contract novation)*
- **NIMIS → Huawei → for TIM** — Senior Oracle DBA & Performance Expert (development focus) | 2020 – 2022:
  - Specialist support to development teams in PL/SQL and SQL optimisation for critical applications on Exadata (67+ instances).
  - Analysis and tuning of high-volume PL/SQL batch processes; PL/SQL scripts for monitoring and administration tasks.
  - *(contract transitioned to IDEA DB CONSULTING from 2022 with contract novation)*
- **DatabTech, Milan** — Oracle DBA and DWH Architect for Allianz and Mediobanca | 2018 – 2021:
  - Migration of Oracle Data Integrator (ODI) projects from version 10g to 12c, with PL/SQL development supporting the migrated mappings.
- **Other Banking, Insurance and Telco clients** | 2013 – 2018:
  - Custom PL/SQL solutions for various clients: packages for ETL logic, data-processing procedures, PL/SQL APIs.
  - Intensive PL/SQL and SQL optimisation to improve the performance of existing systems.
  - Training and mentoring of junior developers on PL/SQL best practices.

---

### AUSELDA AED GROUP S.P.A. — Rome, Italy
**Oracle PL/SQL Developer · DWH Specialist** (for the Public Administration) | 2009 – 2013

- Development of PL/SQL components for Data Warehousing systems and management applications for Public Administration.
- Evolutionary and corrective maintenance of PL/SQL code; ETL optimisation on PL/SQL and OWB.

---

### ORACLE ITALIA S.R.L. — Various offices, Italy & Madrid, Spain
**SQL & PL/SQL Developer · DWH Architect · DBA · Training Specialist** | 1999 – 2009

- Intensive PL/SQL development for DWH, BI and custom application projects for TIM, Vodafone (Italy and Spain), Bank of Italy, Generali, Menarini.
- Creation of PL/SQL packages for complex business logic and data-loading procedures (ETL) with Oracle Warehouse Builder.
- BI Reports and HTMLDB (Apex) interfaces with PL/SQL logic.
- Training Specialist (2000-2001) on Oracle SQL and PL/SQL (basic and advanced) courses.

---

### ETNOTEAM S.P.A. · 1999 — S.EL.DAT. S.P.A. · 1997 – 1999
**Web Developer · Oracle SQL & PL/SQL Developer · Junior DBA** (for Telecom, Rover Italia)

- Web portal and client-server development with strong Oracle backend interaction; SQL and PL/SQL for backend logic.

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

- Analytical approach and orientation to solving complex problems
- Writing clean, efficient and maintainable code
- Advanced debugging and troubleshooting skills
- Excellent understanding of functional and technical requirements
- Effective collaboration in development teams
- Attention to detail and software quality

---

*I authorise the processing of my personal data pursuant to Art. 13 of EU Regulation 2016/679 (GDPR).*

Rome, September 2026

---

**[Download PDF]({{% staticurl "downloads/CV_Oracle_PLSQL_Ivan_Luminaria_202609_EN.pdf" %}})** | **[LinkedIn Profile](https://www.linkedin.com/in/ivanluminaria)** | **[Back to previous page](/en/resumes/)**
