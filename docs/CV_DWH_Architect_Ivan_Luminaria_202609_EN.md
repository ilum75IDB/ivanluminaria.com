# Ivan Luminaria

<p class="role">Data Warehouse Architect · Oracle & PostgreSQL Expert</p>
<p class="contact">Rome, Italy · (+39) 335 727 1217 · ivan.luminaria@gmail.com · linkedin.com/in/ivanluminaria · ivanluminaria.com</p>

## Profile

Most of the times I've been called to "design a new DWH", the existing DWH was fine. It just needed to be understood. Thirty years of Oracle, the last fifteen as a DWH Architect — I've learned the bottleneck is almost never the platform.

What I see right away when a proposal for a new platform lands on the table: the partition strategy never revisited after five years of growth. The PL/SQL ETL running serial when it could run parallel. The materialized view no one has refreshed since the schema change in 2019. It's the details that pile up, not the technologies that age out.

Analytical batches cut from 4 hours to under 30 minutes on Oracle OCI and Autonomous Database — no hardware change, only working on design and execution plans. Atradius Surety: DWH consolidating 4 EU countries, 60,000+ lines of PL/SQL, full daily ingestion under 2 hours. GENERALI: insurance DWH 500 GB–8 TB. TIM (via Huawei): 30+ Oracle databases on Exadata, 800M records/day, SLAs under 500 ms. ODI 10g→12c migration for Allianz and Mediobanca — never from scratch, always in continuity. Kimball, Inmon, star/snowflake, SCD, bus matrix. Long-standing Oracle Italy trainer on SQL, PL/SQL, tuning. What I bring: an independent second opinion before you sign a six-figure proposal, a method that starts from the data the system already records (AWR, ASH, wait events, execution plans), and the discipline to say "your current system can still hold — here's how".

## Areas of engagement

- **Data Warehouse design** — dimensional modelling, star and snowflake schemas, Slowly Changing Dimensions, bus matrix, source-to-target mapping.
- **ETL/ELT design & optimisation** — PL/SQL-based pipelines, Oracle Data Integrator, Oracle Warehouse Builder legacy migration, cross-source integration.
- **DWH performance tuning** — partitioning strategies, compression, materialised views, query rewriting, execution plan analysis.
- **Modernisation & migration** — assessment of Oracle-based DWHs toward PostgreSQL alternatives, cloud DWH platforms (OCI, AWS, Azure).

## Key results

- **Several hundred Oracle databases** across 30 years, with focus on DWH design, ETL/ELT and administration.
- **Surety DWH** (Atradius) consolidating **4 European countries** (Italy, Spain, France, Northern Europe): **60,000+ lines of PL/SQL**, full daily load **under 2 hours**, real-time monitoring of loading stages.
- DWH design on datasets exceeding **2 billion rows** with 15+ heterogeneous source integrations.
- Snowflake schema on Oracle Analytics Cloud with ETL on Oracle 19c in OCI for billing statistics, customer segmentation, portfolio and cost/revenue tracking.
- Critical analytical batches cut **from 4 hours to under 30 minutes** on Oracle OCI and Autonomous Database.
- PostgreSQL DWH designed as **cost-effective alternative** to Oracle for banking and Telepass-related workloads.

## Core expertise

- **DWH Methodologies**: multidimensional data modelling (Kimball, Inmon) · Star Schema, Snowflake Schema · Slowly Changing Dimensions (SCD Type 1/2/3) · Bus Matrix design
- **Oracle Database**: Oracle up to 23ai · Exadata · RAC · Data Guard · Autonomous Database (ADB) · performance tuning (AWR, ADDM, SQL Tuning Advisor) · ASM · RMAN · TDE
- **PostgreSQL**: PostgreSQL 14+ · query optimisation · table partitioning · pg_stat_statements · PgBouncer · logical replication · VACUUM/autovacuum tuning
- **ETL/ELT Tools**: PL/SQL pipelines · Unix Shell scripting · Oracle Data Integrator (ODI) · Oracle Warehouse Builder (OWB, legacy)
- **BI & Reporting**: Oracle Analytics Cloud (OAC) — Semantic Model Designer, reports, dashboards
- **Cloud Platforms**: Oracle Cloud Infrastructure (OCI) · AWS Aurora PostgreSQL · Azure Database
- **Languages & OS**: SQL (advanced) · PL/SQL · Unix Shell scripting · Linux (RHEL, CentOS, Oracle Linux), Unix, Windows Server
- **Other**: project management (Agile/Scrum), team leadership up to 7 people, technical training

## Experience

### IDEA DB CONSULTING S.R.L. — Founder · DWH Architect · Oracle & PostgreSQL Expert · 2022 – Present
- **SILICONDEV → POSTE ITALIANE** (Jul 2025 – present): Senior Database Consultant; ~1,500 MySQL and PostgreSQL instances across production, certification and development; performance monitoring, query tuning, replication management, capacity planning at enterprise scale.
- **GENERALI Insurance** (Feb 2024 – May 2025): PM DWH Lead; technical coordination on insurance-sector Data Warehouse on 500 GB–8 TB Oracle databases; direct client interface on requirements, scope and solutions.
- **Atradius**, Surety division (2022 – 2026): unified Oracle DWH consolidating claims, credit, policies, contracts and billing data from **4 European countries** (Italy, Spain, France, Northern Europe); heterogeneous sources (Oracle, MS SQL Server, flat files) integrated into a single model; entire data model and ETL layer (**60,000+ lines of PL/SQL**) with real-time load monitoring; full daily ingestion under 2 hours.
- **Other Banking, Telco and payments clients**: Kimball/Inmon-driven DWH architectures; multidimensional modelling on datasets above 2B rows; ETL/ELT integrating 15+ heterogeneous sources; PostgreSQL DWH as cost-effective alternative to Oracle with partitioning strategies and query optimisation.

### Freelance consultant — Oracle DBA · Performance Tuning · DWH Architect · 2013 – 2022
- **FAI Service** (2021 – 2023): Snowflake schema on Oracle Analytics Cloud with ETL on Oracle 19c in OCI; dashboards and reports for billing statistics, customer segmentation, portfolio analysis, cost/revenue tracking. *(contract transitioned to IDEA DB CONSULTING from 2022 with contract novation)*
- **LISCOR → Finwave, Gruppo Lutech** (2020 – 2023): Oracle DBA and DWH development in the financial sector; advanced PL/SQL and query optimisation for applications with millions of daily transactions. *(contract transitioned to IDEA DB CONSULTING from 2022 with contract novation)*
- **NIMIS → Huawei → for TIM** (2020 – 2022): Oracle DBA · DWH Architect · Performance & Tuning Expert; 30+ critical Oracle databases (67+ instances) on 3- and 5-node Exadata clusters supporting 20M+ prepaid mobile users; fact tables ingesting up to 800M records per day with advanced partitioning and compression, SLAs under 500 ms; ASM and TDE. *(contract transitioned to IDEA DB CONSULTING from 2022 with contract novation)*
- **DatabTech, Milan** (2018 – 2021): Oracle DBA and DWH Architect for Allianz and Mediobanca; migration of Oracle Data Integrator (ODI) projects from version 10g to 12c.
- **Other Banking, Insurance and Telco clients** (2013 – 2018): DWH design and development on Oracle and PostgreSQL following Kimball/Inmon methodologies; ETL/ELT pipelines handling **500M rows per load cycle**; SQL performance tuning, PL/SQL and ETL design; Oracle Data Guard HA/DR; team leadership (3–7 people) in multicultural distributed settings with Agile methodology; budgets €100K–€500K.

### Earlier career · 1997 – 2013
- **Auselda AED Group** (2009 – 2013): DWH design and modelling (Kimball/Inmon) for the Italian public sector; ETL/ELT and complex SQL optimisation; Oracle Warehouse Builder (OWB) product specialist.
- **Oracle Italia** (1999 – 2009): DWH design and development for TIM, Vodafone (Italy and Spain), TRE, Bank of Italy, Generali, RAS, Menarini; Kimball/Inmon data models and ETL/ELT with OWB; SQL Performance & Tuning, PL/SQL, BI Reports (Oracle Discoverer, HTMLDB), Oracle OLAP; Oracle trainer 2000 – 2001.
- **S.EL.DAT.** (1997 – 1999): software developer for Telecom and Rover Italia; junior Oracle DBA.

## Education & languages

- Computer Engineering studies (Software Engineering), Roma Tre University, 1994 – 2000 · Scientific high school diploma, 1993 · Advanced English C1/C2, The British Council, 2003 – 2004
- Italian (native) · English C1/C2 · Spanish C1 · Romanian C1 · French A2

<p class="gdpr">I authorise the processing of my personal data pursuant to Art. 13 of EU Regulation 2016/679 (GDPR). Rome, September 2026.</p>
