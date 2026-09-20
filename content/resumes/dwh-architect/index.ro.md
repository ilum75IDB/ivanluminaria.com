---
title: "Data Warehouse Architect"
seoTitle: "Data Warehouse Architect Oracle/PostgreSQL"
description: "Ivan Luminaria, Data Warehouse Architect Oracle/PostgreSQL: 30 de ani de proiectare DWH, modelare dimensionala Kimball, pipeline-uri ETL și arhitecturi analitice."
date: "2026-09-14"
lastmod: "2026-09-20"
draft: false
layout: "simple"
---

**[Descarcă PDF]({{% staticurl "downloads/CV_DWH_Architect_Ivan_Luminaria_202609_EN.pdf" %}})** | **[Profil LinkedIn](https://www.linkedin.com/in/ivanluminaria)**

> **Un rol, patru piloni.** Acest profil este unul dintre cei patru piloni ai rolului [Technical Leader pentru baze de date și Data Warehouse mission-critical](/ro/resumes/technical-leader/).

---

## Profil Profesional

În majoritatea cazurilor în care am fost chemat să "proiectez un DWH nou", DWH-ul existent era în regulă. Trebuia doar înțeles. Treizeci de ani de Oracle, ultimii cincisprezece ca DWH Architect — am învățat că gâtul de sticlă aproape niciodată nu este platforma.

Ce văd imediat când sosește o ofertă pentru o platformă nouă: strategia de partiționare nerevizuită după cinci ani de creștere. ETL-ul în PL/SQL care rulează în serial când putea rula în paralel. Materialized view-ul pe care nimeni nu l-a mai reîmprospătat după schimbarea de schemă din 2019. Sunt detaliile care se acumulează, nu tehnologiile care îmbătrânesc.

Batch-uri analitice de la 4 ore la sub 30 de minute pe Oracle OCI și Autonomous Database — fără schimbare de hardware, doar lucrând pe design și pe planuri de execuție. Programe DWH multi-țară consolidând 4 țări europene cu peste 60.000 de linii de PL/SQL și încărcare zilnică completă sub 2 ore. DWH asigurări 500 GB–8 TB. Clustere Exadata multi-nod, fact table-uri cu ingest de peste 800M înregistrări pe zi cu SLA sub 500 ms. Migrări ODI 10g→12c gestionate în continuitate, niciodată de la zero. Kimball, Inmon, star/snowflake, SCD, bus matrix. Predare Oracle Italia despre SQL, PL/SQL, tuning. Ce aduc: o a doua opinie independentă înainte să semnezi o ofertă de sute de mii de euro, o metodă care pornește de la datele pe care sistemul le înregistrează deja (AWR, ASH, wait events, planuri de execuție), și disciplina de a spune "sistemul tău actual încă poate rezista — iată cum".

---

## Arii de intervenție

- **Data Warehouse design** — modelare dimensionala, scheme star și snowflake, Slowly Changing Dimensions, bus matrix, source-to-target mapping.
- **Proiectare și optimizare ETL/ELT** — pipeline-uri în PL/SQL, Oracle Data Integrator, migrarea proiectelor Oracle Warehouse Builder legacy, integrare cross-source.
- **DWH performance tuning** — strategii de partitioning, compression, materialised views, query rewriting, analiza execution plans.
- **Modernizare și migrare** — evaluarea DWH-urilor Oracle către alternative PostgreSQL, platforme DWH cloud (OCI, AWS, Azure).

---

## Rezultate în evidență

- **Câteva sute de baze de date Oracle** în 30 de ani, cu focus pe DWH design, ETL/ELT și administrare.
- **DWH Surety** (Atradius) consolidat pe **4 țări europene** (Italia, Spania, Franța, Nordul Europei): **peste 60.000 de linii de PL/SQL**, încărcare zilnică completă în **mai puțin de 2 ore**, monitorizare în timp real a fazelor de load.
- Proiectare DWH pe seturi de date de peste **2 miliarde de rânduri** cu integrare de **peste 15 surse eterogene**.
- Model de date Snowflake pe Oracle Analytics Cloud cu ETL pe Oracle 19c în OCI pentru facturare, segmentare clienți, portofoliu și tracking costuri/venituri.
- Batch-uri analitice critice reduse **de la 4 ore la mai puțin de 30 de minute** pe Oracle în OCI și Autonomous Database.
- Data Warehouse pe PostgreSQL proiectat ca **alternativa cost-effective** la Oracle pentru workload-uri Banking și Telepass.

---

## Competențe Cheie

### Metodologii DWH

- Modelare multidimensională Kimball și Inmon
- Star Schema, Snowflake Schema, Slowly Changing Dimensions (SCD Type 1/2/3), Bus Matrix design

### Stack Oracle

- Oracle Database până la 23ai, Exadata, RAC, Data Guard, Autonomous Database (ADB)
- Performance Tuning (AWR, ADDM, SQL Tuning Advisor), Storage Management (ASM), Backup & Recovery (RMAN), Oracle TDE

### PostgreSQL

- PostgreSQL 14+, Query Optimization, Table Partitioning
- `pg_stat_statements`, PgBouncer, replicare logică, tuning VACUUM/Autovacuum

### Cloud

- Oracle Cloud Infrastructure (OCI): Compute, Storage, Networking, Database Services, Autonomous Database
- AWS Aurora PostgreSQL, medii Microsoft Azure Database

### ETL/ELT și Business Intelligence

- Pipeline-uri ETL în PL/SQL, Unix Shell scripting
- Oracle Data Integrator (ODI), Oracle Warehouse Builder (OWB, proiecte legacy)
- Oracle Analytics Cloud (OAC): Semantic Model Designer, dashboard-uri și rapoarte

### Limbaje, sisteme și transversal

- SQL avansat, PL/SQL avansat, Unix Shell scripting
- Linux (RHEL, CentOS, Oracle Linux), Unix, Windows Server
- Project Management (Agile/Scrum), team leadership până la 7 persoane, formare tehnică

---

## Experiență Profesională

### IDEA DB CONSULTING S.R.L. — Roma, Italia (Full Remote Europa)
**Administrator Unic · Data Warehouse Architect · Oracle & PostgreSQL Expert** | 2022 – Prezent

- **SILICONDEV → POSTE ITALIANE** — Senior Database Consultant | Iul 2025 – Prezent:
  - Administrarea a aproximativ 1.500 de instanțe MySQL și PostgreSQL între producție, certificare și dezvoltare.
  - Monitorizarea performanței, query tuning, gestionarea replicării și capacity planning la scara enterprise.
- **GENERALI Asigurări** — PM DWH Lead | Feb 2024 – Mai 2025:
  - Coordonare tehnică pe Data Warehouse asigurări pe baze de date Oracle de la 500 GB la 8 TB.
  - Interfață directă cu clientul pe cerințe, definirea scope-ului și prezentarea soluțiilor.
- **ATRADIUS, divizia Surety** — DWH Architect | 2022 – 2026:
  - Data Warehouse Oracle unificat pentru consolidarea datelor din 4 țări europene (Italia, Spania, Franța, Nordul Europei) din surse eterogene (Oracle, SQL Server, fișiere externe).
  - Modelarea domeniilor de business core (portofoliu clienți, polițe, contracte, facturare, daune, tranzacții daune).
  - Peste 60.000 de linii de PL/SQL, framework de încărcare cu checkpoint-uri și logging în timp real; încărcare zilnică completă în mai puțin de 2 ore.
- **Alți clienți Banking, Telco și plăți** — Proiectare și arhitectură DWH:
  - Arhitecturi DWH Kimball/Inmon pe seturi de date de peste 2 miliarde de rânduri, integrarea a peste 15 surse eterogene.
  - Batch-uri analitice critice reduse de la 4 ore la mai puțin de 30 de minute pe Oracle în OCI și Autonomous Database.
  - DWH pe PostgreSQL ca alternativă cost-effective la Oracle cu strategii de partitioning și query optimization.

---

### FREELANCE / CONSULTANT INDEPENDENT — Roma, Italia (Full Remote Europa)
**Oracle DBA · Performance Tuning · DWH Architect** | 2013 – 2022

- **FAI SERVICE** — DWH Architect & Oracle DBA | 2021 – 2023:
  - Model de date Snowflake pe Oracle Analytics Cloud, ETL pe Oracle 19c în OCI, dashboard-uri pentru facturare, segmentare și portofoliu.
  - *(contract preluat de IDEA DB CONSULTING din 2022 cu novație contractuală)*
- **LISCOR → Finwave, Gruppo Lutech** — Oracle DBA și dezvoltare DWH în sectorul financiar | 2020 – 2023:
  - Dezvoltare PL/SQL avansată și optimizare de interogări pentru aplicații financiare cu milioane de tranzacții zilnice.
  - *(contract preluat de IDEA DB CONSULTING din 2022 cu novație contractuală)*
- **NIMIS → Huawei → pentru TIM** — Oracle DBA și DWH Architect | 2020 – 2022:
  - Arhitectură DWH telco pe peste 30 de baze de date Oracle critice (67+ instanțe pe cluster-e Exadata) în sprijinul a peste 20 de milioane de utilizatori prepay mobile.
  - Fact tables cu ingestie de până la 800 de milioane de înregistrări de trafic pe zi, strategii avansate de partitioning și compression, SLA sub 500 ms; ASM și Oracle TDE.
  - *(contract preluat de IDEA DB CONSULTING din 2022 cu novație contractuală)*
- **DatabTech, Milano** — Oracle DBA și DWH Architect pentru Allianz și Mediobanca | 2018 – 2021:
  - Migrarea proiectelor Oracle Data Integrator (ODI) de la versiunea 10g la 12c.
- **Alți clienți Banking, Insurance și Telco** | 2013 – 2018:
  - Data Warehouse pe platforme Oracle și PostgreSQL, cu modelare Kimball/Inmon.
  - Pipeline-uri ETL/ELT care gestionează până la 500 de milioane de rânduri pe ciclu de încărcare.
  - Configurări Oracle Data Guard pentru înaltă disponibilitate și disaster recovery.
  - Echipe de la 3 la 7 persoane în contexte multiculturale distribuite, abordare Agile iterativă, bugete în intervalul €100K – €500K.

---

### AUSELDA AED GROUP S.P.A. — Roma, Italia
**Data Warehouse Architect · Performance & Tuning Expert · Oracle Project DBA** (pentru Administratia Publica) | 2009 – 2013

- Proiectare și modelare (Kimball/Inmon) de DWH pentru entitati din Administratia Publica.
- Dezvoltare de procese ETL/ELT, optimizare de interogări SQL complexe, product specialist Oracle Warehouse Builder.

---

### ORACLE ITALIA S.R.L. — Diverse sedii, Italia & Madrid, Spania
**Data Warehouse Architect · Oracle DBA · SQL & PL/SQL Developer · Training Specialist** | 1999 – 2009

- Data Warehouse pentru clienți Telco (TIM, Vodafone, TRE), Finance (Banca Italiei, Generali, RAS) și Farmaceutic (Menarini), cu modelare Kimball/Inmon și ETL pe Oracle Warehouse Builder.
- Angajament international pe Vodafone Spania (Madrid).
- Training Specialist (2000-2001) pe SQL, PL/SQL, Oracle DBA și Performance & Tuning.

---

### ETNOTEAM S.P.A. · 1999 — S.EL.DAT. S.P.A. · 1997 – 1999
**Web și Software Developer · Junior Oracle DBA** (pentru Telecom, Rover Italia)

---

## Formare

- **Facultatea de Inginerie Informatică (Ingineria Software)** | Universitatea Roma Tre, Roma | 1994 – 2000
- **Diploma de Bacalaureat Stiintific** | Liceo Scientifico Isacco Newton / Manieri Copernico, Roma | 1988 – 1993
- **Engleză Avansată (C1/C2)** | The British Council, Roma | 2003 – 2004
- Formare continua: Scrum Agile și Project Management (Randstad / Forma.temp, 2024) · Data Wrangling with SQL (Coursera, UC Davis, 2021) · Advanced SQL for Query Tuning și Oracle 12c (LinkedIn Learning, 2020)

---

## Limbi

- **Italiană**: Maternă
- **Engleză**: C1/C2 (Fluentă, profesională)
- **Spaniolă**: C1 (Fluentă)
- **Română**: C1 (Fluentă)
- **Franceză**: A1/A2 (De bază)

---

## Competențe Transversale

- Citire transversală a situațiilor complexe, până la cauza reală
- Traducere între nivelul tehnic și nivelul business, pentru echipe și management
- Coordonare a echipelor distribuite, în prezență și full remote
- Mentoring și transfer de competențe
- Gestionarea priorităților sub presiune operativă
- Comunicare tehnică clară, bazată pe evidențe

---

*Autorizez prelucrarea datelor mele personale conform Art. 13 din Regulamentul UE 2016/679 (GDPR).*

Roma, Septembrie 2026

---

**[Descarcă PDF]({{% staticurl "downloads/CV_DWH_Architect_Ivan_Luminaria_202609_EN.pdf" %}})** | **[Profil LinkedIn](https://www.linkedin.com/in/ivanluminaria)** | **[Înapoi la pagina anterioară](/ro/resumes/)**
