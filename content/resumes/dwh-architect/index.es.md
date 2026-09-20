---
title: "Data Warehouse Architect"
seoTitle: "Data Warehouse Architect Oracle/PostgreSQL"
description: "Ivan Luminaria, Data Warehouse Architect Oracle/PostgreSQL: 30 años de diseño DWH, modelado dimensional Kimball, pipelines ETL y arquitecturas analíticas."
date: "2026-09-14"
lastmod: "2026-09-20"
draft: false
layout: "simple"
---

**[Descargar PDF]({{% staticurl "downloads/CV_DWH_Architect_Ivan_Luminaria_202609_EN.pdf" %}})** | **[Perfil LinkedIn](https://www.linkedin.com/in/ivanluminaria)**

> **Un rol, cuatro pilares.** Este perfil es uno de los cuatro pilares del rol [Technical Leader para bases de datos y Data Warehouse mission-critical](/es/resumes/technical-leader/).

---

## Perfil Profesional

En la mayoría de los casos en que me han llamado para "diseñar un DWH nuevo", el DWH existente estaba bien. Solo faltaba entenderlo. Treinta años de Oracle, los últimos quince como DWH Architect — he aprendido que el cuello de botella casi nunca es la plataforma.

Lo que veo de inmediato cuando llega un presupuesto para una nueva plataforma: la partición nunca revisada después de cinco años de crecimiento. El ETL en PL/SQL que corre en serie cuando podría correr en paralelo. La materialized view que nadie ha actualizado desde el cambio de esquema de 2019. Son los detalles que se acumulan, no las tecnologías que envejecen.

Batch analíticos de 4 horas a menos de 30 minutos en Oracle OCI y Autonomous Database — sin cambio de hardware, solo trabajando en diseño y planes de ejecución. Programas de DWH multi-país consolidando 4 países europeos con más de 60.000 líneas de PL/SQL y carga diaria completa por debajo de 2 horas. DWH aseguradores 500 GB–8 TB. Clusters Exadata multi-nodo, fact tables con ingesta de 800M+ registros al día con SLA por debajo de 500 ms. Migraciones ODI 10g→12c gestionadas en continuidad, nunca desde cero. Kimball, Inmon, star/snowflake, SCD, bus matrix. Docencia Oracle Italia sobre SQL, PL/SQL, tuning. Lo que aporto: una segunda opinión independiente antes de que firmes un presupuesto de cientos de miles de euros, un método que parte de los datos que el sistema ya registra (AWR, ASH, wait events, planes de ejecución), y la disciplina de decir "tu sistema actual todavía puede aguantar — te explico cómo".

---

## Áreas de intervención

- **Data Warehouse design** — modelado dimensional, esquemas star y snowflake, Slowly Changing Dimensions, bus matrix, source-to-target mapping.
- **Diseño y optimización ETL/ELT** — pipelines en PL/SQL, Oracle Data Integrator, migración de proyectos Oracle Warehouse Builder legacy, integración cross-source.
- **DWH performance tuning** — estrategias de partitioning, compression, materialised views, query rewriting, análisis de execution plans.
- **Modernización y migración** — evaluación de DWH Oracle hacia alternativas PostgreSQL, plataformas DWH cloud (OCI, AWS, Azure).

---

## Resultados destacados

- **Varios cientos de bases de datos Oracle** en 30 años, con foco en DWH design, ETL/ELT y administración.
- **DWH Surety** (Atradius) consolidado sobre **4 países europeos** (Italia, España, Francia, Norte de Europa): **más de 60.000 líneas de PL/SQL**, carga diaria completa en **menos de 2 horas**, monitorización en tiempo real de las fases de load.
- Diseño DWH sobre datasets superiores a los **2 mil millones de filas** con integración de **más de 15 fuentes heterogéneas**.
- Modelo de datos Snowflake sobre Oracle Analytics Cloud con ETL sobre Oracle 19c en OCI para facturación, segmentación de clientes, portfolio y tracking de costes/ingresos.
- Batches analíticos críticos reducidos **de 4 horas a menos de 30 minutos** sobre Oracle en OCI y Autonomous Database.
- Data Warehouse sobre PostgreSQL diseñado como **alternativa cost-effective** a Oracle para workloads Banking y Telepass.

---

## Competencias Clave

### Metodologías DWH

- Modelado multidimensional Kimball e Inmon
- Star Schema, Snowflake Schema, Slowly Changing Dimensions (SCD Type 1/2/3), Bus Matrix design

### Stack Oracle

- Oracle Database hasta la 23ai, Exadata, RAC, Data Guard, Autonomous Database (ADB)
- Performance Tuning (AWR, ADDM, SQL Tuning Advisor), Storage Management (ASM), Backup & Recovery (RMAN), Oracle TDE

### PostgreSQL

- PostgreSQL 14+, Query Optimization, Table Partitioning
- `pg_stat_statements`, PgBouncer, replicación lógica, tuning de VACUUM/Autovacuum

### Cloud

- Oracle Cloud Infrastructure (OCI): Compute, Storage, Networking, Database Services, Autonomous Database
- AWS Aurora PostgreSQL, entornos Microsoft Azure Database

### ETL/ELT y Business Intelligence

- Pipelines ETL en PL/SQL, Unix Shell scripting
- Oracle Data Integrator (ODI), Oracle Warehouse Builder (OWB, proyectos legacy)
- Oracle Analytics Cloud (OAC): Semantic Model Designer, dashboards e informes

### Lenguajes, sistemas y transversal

- SQL avanzado, PL/SQL avanzado, Unix Shell scripting
- Linux (RHEL, CentOS, Oracle Linux), Unix, Windows Server
- Project Management (Agile/Scrum), team leadership hasta 7 personas, formación técnica

---

## Experiencia Profesional

### IDEA DB CONSULTING S.R.L. — Roma, Italia (Full Remote Europa)
**Administrador Único · Data Warehouse Architect · Oracle & PostgreSQL Expert** | 2022 – Presente

- **SILICONDEV → POSTE ITALIANE** — Senior Database Consultant | Jul 2025 – Presente:
  - Administración de aproximadamente 1.500 instancias MySQL y PostgreSQL entre producción, certificación y desarrollo.
  - Monitorización de las performance, query tuning, gestión de la replicación y capacity planning a escala enterprise.
- **GENERALI Seguros** — PM DWH Lead | Feb 2024 – May 2025:
  - Coordinación técnica sobre Data Warehouse asegurador sobre bases de datos Oracle de 500 GB a 8 TB.
  - Interfaz directa con el cliente sobre requisitos, definición del scope y presentación de las soluciones.
- **ATRADIUS, división Surety** — DWH Architect | 2022 – 2026:
  - Data Warehouse Oracle unificado para consolidar los datos de 4 países europeos (Italia, España, Francia, Norte de Europa) desde fuentes heterogéneas (Oracle, SQL Server, archivos externos).
  - Modelado de los dominios core (cartera de clientes, pólizas, contratos, facturación, siniestros, movimientos de siniestros).
  - Más de 60.000 líneas de PL/SQL, framework de carga con checkpoints y logging en tiempo real; carga diaria completa en menos de 2 horas.
- **Otros clientes Banking, Telco y pagos** — Diseño y arquitectura DWH:
  - Arquitecturas DWH Kimball/Inmon sobre datasets superiores a los 2 mil millones de filas, integración de más de 15 fuentes heterogéneas.
  - Batches analíticos críticos reducidos de 4 horas a menos de 30 minutos sobre Oracle en OCI y Autonomous Database.
  - DWH sobre PostgreSQL como alternativa cost-effective a Oracle con estrategias de partitioning y query optimization.

---

### FREELANCE / CONSULTOR INDEPENDIENTE — Roma, Italia (Full Remote Europa)
**Oracle DBA · Performance Tuning · DWH Architect** | 2013 – 2022

- **FAI SERVICE** — DWH Architect & Oracle DBA | 2021 – 2023:
  - Modelo de datos Snowflake sobre Oracle Analytics Cloud, ETL sobre Oracle 19c en OCI, dashboards para facturación, segmentación y portfolio.
  - *(contrato absorbido por IDEA DB CONSULTING desde 2022 con novación del contrato)*
- **LISCOR → Finwave, Gruppo Lutech** — Oracle DBA y desarrollo DWH en el sector financiero | 2020 – 2023:
  - Desarrollo PL/SQL avanzado y optimización de consultas para aplicaciones financieras con millones de transacciones diarias.
  - *(contrato absorbido por IDEA DB CONSULTING desde 2022 con novación del contrato)*
- **NIMIS → Huawei → para TIM** — Oracle DBA y DWH Architect | 2020 – 2022:
  - Arquitectura DWH telco sobre más de 30 bases de datos Oracle críticas (67+ instancias sobre clusters Exadata) al servicio de más de 20 millones de usuarios prepago mobile.
  - Fact tables con ingesta de hasta 800 millones de registros de tráfico al día, estrategias avanzadas de partitioning y compression, SLA por debajo de los 500 ms; ASM y Oracle TDE.
  - *(contrato absorbido por IDEA DB CONSULTING desde 2022 con novación del contrato)*
- **DatabTech, Milán** — Oracle DBA y DWH Architect para Allianz y Mediobanca | 2018 – 2021:
  - Migración de proyectos Oracle Data Integrator (ODI) de la versión 10g a la 12c.
- **Otros clientes Banking, Insurance y Telco** | 2013 – 2018:
  - Data Warehouses sobre plataformas Oracle y PostgreSQL, con modelado Kimball/Inmon.
  - Pipelines ETL/ELT que gestionan hasta 500 millones de filas por ciclo de carga.
  - Configuraciones Oracle Data Guard para alta disponibilidad y disaster recovery.
  - Equipos de 3 a 7 personas en contextos multiculturales distribuidos, enfoque Agile iterativo, presupuestos en la franja €100K – €500K.

---

### AUSELDA AED GROUP S.P.A. — Roma, Italia
**Data Warehouse Architect · Performance & Tuning Expert · Oracle Project DBA** (para la Administración Pública) | 2009 – 2013

- Diseño y modelado (Kimball/Inmon) de DWH para entes de la Administración Pública.
- Desarrollo de procesos ETL/ELT, optimización de consultas SQL complejas, product specialist Oracle Warehouse Builder.

---

### ORACLE ITALIA S.R.L. — Varias sedes, Italia & Madrid, España
**Data Warehouse Architect · Oracle DBA · SQL & PL/SQL Developer · Training Specialist** | 1999 – 2009

- Data Warehouses para clientes Telco (TIM, Vodafone, TRE), Finance (Banco de Italia, Generali, RAS) y Farmacéutico (Menarini), con modelado Kimball/Inmon y ETL sobre Oracle Warehouse Builder.
- Ingaje internacional en Vodafone España (Madrid).
- Training Specialist (2000-2001) sobre SQL, PL/SQL, Oracle DBA y Performance & Tuning.

---

### ETNOTEAM S.P.A. · 1999 — S.EL.DAT. S.P.A. · 1997 – 1999
**Web y Software Developer · Junior Oracle DBA** (para Telecom, Rover Italia)

---

## Formación

- **Facultad de Ingeniería Informática (Ingeniería del Software)** | Universidad de Roma Tre, Roma | 1994 – 2000
- **Diploma de Bachillerato Científico** | Liceo Scientifico Isacco Newton / Manieri Copernico, Roma | 1988 – 1993
- **Inglés Avanzado (C1/C2)** | The British Council, Roma | 2003 – 2004
- Formación continua: Scrum Agile y Project Management (Randstad / Forma.temp, 2024) · Data Wrangling with SQL (Coursera, UC Davis, 2021) · Advanced SQL for Query Tuning y Oracle 12c (LinkedIn Learning, 2020)

---

## Idiomas

- **Italiano**: Nativo
- **Inglés**: C1/C2 (Fluido, profesional)
- **Español**: C1 (Fluido)
- **Rumano**: C1 (Fluido)
- **Francés**: A1/A2 (Básico)

---

## Competencias Transversales

- Lectura transversal de las situaciones complejas, hasta la causa real
- Traducción entre nivel técnico y nivel business, para equipos y management
- Coordinación de equipos distribuidos, en presencia y full remote
- Mentoring y transferencia de competencias
- Gestión de las prioridades bajo presión operativa
- Comunicación técnica clara, basada en evidencias

---

*Autorizo el tratamiento de mis datos personales conforme al Art. 13 del Reglamento UE 2016/679 (GDPR).*

Roma, Septiembre 2026

---

**[Descargar PDF]({{% staticurl "downloads/CV_DWH_Architect_Ivan_Luminaria_202609_EN.pdf" %}})** | **[Perfil LinkedIn](https://www.linkedin.com/in/ivanluminaria)** | **[Volver a la página anterior](/es/resumes/)**
