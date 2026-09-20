# Ivan Luminaria

<p class="role">Oracle PL/SQL Developer & SQL Performance Tuning Expert</p>
<p class="contact">Rome, Italy · (+39) 335 727 1217 · ivan.luminaria@gmail.com · linkedin.com/in/ivanluminaria · ivanluminaria.com</p>

## Profile

PL/SQL has a peculiar trait among programming languages: it stays in production for decades, often passing through four or five generations of developers who hand it over to each other. The value of whoever writes it is measured in what those successors can still read, understand and modify.

When I teach PL/SQL, I like to define it as an **exception-oriented language**: the ability to handle system exceptions and to define custom ones, declaratively inside every block, is what lets the code survive scenarios that weren't foreseeable at the time of writing.

Row-by-row cursors that could be BULK COLLECT. DML that ignores the underlying partitioning. Dynamic SQL built with string concatenation when bind variables were right there. These are the writing details that multiply execution times — the difference between a 4-hour batch and a 30-minute one almost always sits in a few pages of code. And when 60,000 lines of code govern the insurance business of four European countries, what looked like legacy becomes the operational backbone: not code to rewrite, but an executable rulebook of how the business actually works.

ETL packages of over 60,000 lines for a multi-country DWH, full daily ingestion cut from over 4 hours to under 2 hours with BULK COLLECT/FORALL, partition-aware DML and query rewriting. Analytical batches cut from 4 hours to under 30 minutes on 2B+ row datasets. Packages handling millions of daily financial transactions. PL/SQL Hierarchical Profiler, SQL Trace, TKPROF. Oracle Italy trainer on SQL and PL/SQL. Twenty-five years of continuous mentoring of junior developers toward senior level in banking, insurance, telco, public administration and postal.

Beyond PL/SQL and SQL I can read, understand and modify other languages too — Unix Shell Script, Python, Java, C++, JavaScript, HTML, CSS, Pascal and CaML. Some I studied at university, others I picked up when the code around the database needed touching. I'm no guru in any of them; but when a piece of critical logic lives outside the database — in a shell script, in a Python service, in a frontend that calls PL/SQL procedures — reading the other side helps to understand where the problem really sits.

What I bring: PL/SQL your junior developers can read and maintain, targeted refactors that reduce technical debt without hasty rewrites, and the discipline to tell technical debt from business asset.

## Areas of engagement

- **PL/SQL development & code review** — packages for ETL logic, data-processing procedures, PL/SQL APIs, business logic; audit and refactor of legacy PL/SQL codebases.
- **PL/SQL & SQL performance tuning** — Hierarchical Profiler analysis, BULK COLLECT/FORALL patterns, partition-aware DML, execution-plan-driven rewrites.
- **ETL/ELT design in PL/SQL** — standardised loading templates with checkpoints, real-time logging, error recovery, monitoring dashboards.
- **Mentoring & knowledge transfer** — coaching junior developers on PL/SQL best practices, code standards, testable patterns.

## Key results

- **Several hundred Oracle databases** across 30 years, spanning PL/SQL development, tuning, DWH and administration.
- **60,000+ lines of PL/SQL** designed and maintained for the **Surety DWH** (Atradius) multi-country across **4 European countries** (Italy, Spain, France, Northern Europe); reusable templates and real-time load monitoring.
- Full daily ingestion **from 4+ hours to under 2 hours** through query rewriting, BULK COLLECT/FORALL and partition-aware DML.
- PL/SQL packages for financial transaction processing handling **millions of daily operations** across banking and insurance clients.
- Critical analytical batches cut **from 4 hours to under 30 minutes** on 2B+ row datasets.
- ETL/ELT pipelines integrating **15+ heterogeneous sources** into Oracle and Oracle Analytics Cloud dashboards.

## Core expertise

- **Languages**: PL/SQL (advanced) · SQL (advanced, including Dynamic SQL, analytic functions, CTEs) · Unix Shell scripting
- **PL/SQL Development**: packages, procedures, functions, triggers · records, collections, object types · error/exception handling · bulk processing (FORALL, BULK COLLECT) · dynamic SQL (DBMS_SQL, EXECUTE IMMEDIATE) · PL/SQL Hierarchical Profiler · interaction with tables, views, sequences, synonyms
- **SQL Optimisation & Performance**: execution-plan analysis (Explain Plan), SQL Trace, TKPROF · SQL tuning techniques (Hints, query rewriting, indexes) · understanding the impact of database design on PL/SQL performance
- **Oracle Database**: Oracle Database up to 23ai, Autonomous Database
- **Related concepts**: Data Warehousing (ETL/ELT logic), data integration, relational and multidimensional modelling
- **Development tools**: SQL Developer, Toad, SQL*Plus · Git and GitHub for version control
- **Cloud**: Oracle Cloud Infrastructure (OCI) — database services knowledge

## Experience

### IDEA DB CONSULTING S.R.L. — Founder · Senior Oracle PL/SQL Developer & DWH Architect · 2022 – Present
- **SILICONDEV → POSTE ITALIANE** (Jul 2025 – present): Senior Database Consultant; ~1,500 MySQL and PostgreSQL instances across production, certification and development; query tuning, performance monitoring, replication management, capacity planning at enterprise scale.
- **GENERALI Insurance** (Feb 2024 – May 2025): SQL & PL/SQL optimization on 500 GB–8 TB Oracle databases for insurance applications; Hierarchical Profiler and SQL tuning to identify bottlenecks.
- **Atradius**, Surety division (2022 – 2026): **60,000+ lines of PL/SQL** (packages, procedures, functions) for the multi-country DWH (Italy, Spain, France, Northern Europe) consolidating insurance claims and credit data; reusable PL/SQL templates for loading procedures, checkpoints and real-time logging; batch cycle reduced from 4+ h to under 2 h with query rewriting, BULK COLLECT/FORALL and partition-aware DML.
- **Other Banking, Telco and payments clients**: PL/SQL business logic packages for banking-sector DWH applications on 2B+ row datasets; PL/SQL and SQL optimisation with Hierarchical Profiler analysis to identify bottlenecks and improve critical path execution.

### Freelance consultant — Senior Oracle PL/SQL Developer & DBA / DWH Architect · 2013 – 2022
- **FAI Service** (2021 – 2023): PL/SQL ETL on Oracle 19c in OCI for billing statistics, customer segmentation and cost/revenue tracking; PL/SQL modules feeding Oracle Analytics Cloud dashboards with aggregated financial KPIs. *(contract transitioned to IDEA DB CONSULTING from 2022 with contract novation)*
- **LISCOR → Finwave, Gruppo Lutech** (2020 – 2023): PL/SQL Developer in the financial sector; PL/SQL packages for financial transaction processing handling millions of daily operations across banking and insurance clients; advanced query optimisation and PL/SQL tuning for high-volume financial pipelines. *(contract transitioned to IDEA DB CONSULTING from 2022 with contract novation)*
- **NIMIS → Huawei → for TIM** (2020 – 2022): Senior Oracle DBA & Performance Expert (development focus); specialist support to development teams in PL/SQL and SQL optimisation for critical applications on Exadata (67+ instances); analysis and tuning of high-volume PL/SQL batch processes; PL/SQL scripts for monitoring and administration tasks. *(contract transitioned to IDEA DB CONSULTING from 2022 with contract novation)*
- **DatabTech, Milan** (2018 – 2021): Oracle DBA and DWH Architect for Allianz and Mediobanca; migration of Oracle Data Integrator (ODI) projects from version 10g to 12c, with PL/SQL development supporting the migrated mappings.
- **Other Banking, Insurance and Telco clients** (2013 – 2018): custom PL/SQL solutions for various clients — packages for ETL logic, data-processing procedures, PL/SQL APIs; intensive PL/SQL and SQL optimisation for existing systems; PL/SQL modules for extract-transform-load into DWH systems; training and mentoring on PL/SQL best practices.

### Earlier career · 1997 – 2013
- **Auselda AED Group** (2009 – 2013): PL/SQL developer and DWH specialist for the Italian public sector; PL/SQL evolutionary and corrective maintenance; ETL optimisation on PL/SQL and Oracle Warehouse Builder.
- **Oracle Italia** (1999 – 2009): intensive PL/SQL development for DWH, BI and custom applications for TIM, Vodafone (Italy and Spain), Bank of Italy, Generali, Menarini; PL/SQL packages for complex business logic and ETL with OWB; BI Reports and HTMLDB (Apex) with PL/SQL logic; PL/SQL trainer 2000 – 2001.
- **Etnoteam** (1999) and **S.EL.DAT.** (1997 – 1999): web portal and client-server development with strong Oracle backend interaction; SQL and PL/SQL backend logic; junior DBA activities.

## Education & languages

- Computer Engineering studies (Software Engineering), Roma Tre University, 1994 – 2000 · Scientific high school diploma, 1993 · Advanced English C1/C2, The British Council, 2003 – 2004
- Italian (native) · English C1/C2 · Spanish C1 · Romanian C1 · French A2

<p class="gdpr">I authorise the processing of my personal data pursuant to Art. 13 of EU Regulation 2016/679 (GDPR). Rome, September 2026.</p>
