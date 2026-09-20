---
title: "Oracle DBA & Performance Tuning Expert"
seoTitle: "Oracle DBA & Performance Tuning Expert"
description: "Ivan Luminaria, Oracle DBA & Performance Tuning Expert: 30 años administrando bases de datos mission-critical, RAC, Data Guard, Exadata, AWR/ASH y Oracle Cloud."
date: "2026-09-14"
lastmod: "2026-09-20"
draft: false
layout: "simple"
---

**[Descargar PDF]({{% staticurl "downloads/CV_Oracle_DBA_Ivan_Luminaria_202609_EN.pdf" %}})** | **[Perfil LinkedIn](https://www.linkedin.com/in/ivanluminaria)**

> **Un rol, cuatro pilares.** Este perfil es uno de los cuatro pilares del rol [Technical Leader para bases de datos y Data Warehouse mission-critical](/es/resumes/technical-leader/).

---

## Perfil Profesional

Cientos de bases de datos Oracle administradas en treinta años entre banca, seguros, telco, administración pública y postal — clusters Exadata multi-nodo, fact tables con ingesta de 800M+ registros al día con SLA por debajo de 500 ms, entornos al servicio de 20M+ usuarios finales. Administración MySQL y PostgreSQL a escala enterprise. Batches analíticos de 4 horas a menos de 30 minutos en Oracle OCI y Autonomous Database — sin cambio de plataforma. OCP de los tiempos en que eran raros. Docencia Oracle Italia sobre SQL, PL/SQL, administración, performance tuning; veinticinco años de mentoring continuo de DBA junior hacia nivel senior.

Lo que veo cuando llega una solicitud de intervención post-incident: las métricas de monitoring en verde hasta cuarenta minutos antes. El ticket del vendor cerrado con «unable to reproduce». El DBA junior que heredó el sistema de un senior que se fue a fin de año y aún no tiene el mapa mental para conectar los puntos. La cadena causal casi siempre está en el cruce entre capas — aplicación, base de datos, storage, red — no dentro de una sola capa. Las herramientas muestran síntomas, no causas.

Post-Incident Root Cause Analysis en casos donde los logs del momento habían sido rotados o comprimidos mal: histórico AWR y ASH, logs de sistema operativo y storage, registro de los cambios. He reconstruido cadenas causales que el equipo pensaba perdidas, y producido documentos que pasaron ante el board sin que el DBA senior fuera puesto en medio por defecto. Lo que aporto: un método cross-layer construido sobre sistemas reales. No buscamos culpables — reconstruimos lo que realmente pasó.

---

## Áreas de intervención

- **Health Check de las bases de datos** — evaluación estructurada de performance, fiabilidad, capacidad y riesgos latentes, con informe de evidencias y roadmap de prioridades.
- **Post-Incident Root Cause Analysis** — reconstrucción del incidente sobre datos reales (AWR, ASH, wait events, logs aplicativos e infraestructurales), separando causas, consecuencias y simples correlaciones.
- **DBA leadership continuo** — tuning avanzado, planes de upgrade y patching, estrategias HA/DR, coordinación con desarrollo e infraestructura.
- **Modernización advisory** — evaluación de migraciones Oracle → PostgreSQL, servicios cloud database y paso a Autonomous Database, con análisis de costes y riesgos independiente de vendors.

---

## Resultados destacados

- **Varios cientos de bases de datos Oracle** en 30 años, entre administración, tuning, DWH, PL/SQL y project management.
- Aproximadamente **1.500 instancias** MySQL y PostgreSQL administradas hoy para **POSTE ITALIANE**.
- **30+ bases de datos Oracle sobre Exadata** (3+5 nodos, **67+ instancias**) en encargo telco para **TIM (vía Huawei)**, al servicio de **más de 20 millones de usuarios prepago mobile**: hasta **800 millones de registros al día**; consultas críticas por debajo de los **500 ms** en guardia 24/7.
- Batches analíticos críticos reducidos **de 4 horas a menos de 30 minutos** sobre Oracle en OCI y Autonomous Database.
- **DWH Surety** (Atradius) sobre **4 países europeos** (Italia, España, Francia, Norte de Europa) soportado a nivel DBA: **más de 60.000 líneas de PL/SQL** y carga diaria completa en **menos de 2 horas**.
- Pipelines ETL/ELT que integran **más de 15 fuentes heterogéneas** sobre datasets superiores a los **2 mil millones de filas**.

---

## Competencias Clave

### Oracle Database Administration

- Oracle Database hasta la 23ai, Autonomous Database
- Exadata, RAC, Data Guard, GoldenGate (básico)

### Performance tuning avanzado

- Análisis y diagnóstico: AWR, ADDM, ASH, Statspack, SQL Trace, TKPROF, Explain Plan
- SQL tuning: consultas complejas, hints, SQL Profiles, SQL Plan Management (SPM)
- Instance tuning: memoria (SGA/PGA), parámetros de inicialización, análisis de wait events
- Diseño para performance: indexación (B-tree, Bitmap, Function-based), partitioning (Range, List, Hash, Composite), compression

### HA/DR y seguridad

- RMAN (backup, recovery, cloning), Data Guard, Flashback Technologies
- Oracle TDE, gestión de usuarios y privilegios, auditing
- ASM (Automatic Storage Management), gestión de tablespaces

### Instalación, patching, migraciones

- Instalación de nuevas instancias, PSU/CPU/RU, upgrades de versión, migraciones cross-platform

### Cloud

- Oracle Cloud Infrastructure (OCI): Compute, Storage, Networking, Database Services (VM DB, Bare Metal, Exadata CS, Autonomous Database)
- AWS Aurora PostgreSQL, entornos Microsoft Azure Database

### Otras bases de datos y herramientas

- PostgreSQL (administración, tuning, partitioning, replicación)
- MySQL (administración, replicación, optimización InnoDB)
- Oracle Enterprise Manager (OEM) Cloud Control, SQL Developer, SQL*Plus, Toad
- PL/SQL, SQL, Unix Shell scripting

---

## Experiencia Profesional

### IDEA DB CONSULTING S.R.L. — Roma, Italia (Full Remote Europa)
**Administrador Único · Senior Oracle DBA & Performance Tuning Expert** | 2022 – Presente

- **SILICONDEV → POSTE ITALIANE** — Senior Database Consultant — MySQL & PostgreSQL DBA | Jul 2025 – Presente:
  - Administración de aproximadamente 1.500 instancias MySQL y PostgreSQL entre producción, certificación y desarrollo.
  - Monitorización de las performance, query tuning, gestión de la replicación y capacity planning a escala enterprise.
- **GENERALI Seguros** — Oracle DBA & Tuning Expert | Feb 2024 – May 2025:
  - Administración y tuning avanzado de bases de datos Oracle de 500 GB a 8 TB para aplicaciones del sector asegurador.
  - Análisis AWR/ADDM, optimización SQL, resolución proactiva de cuellos de botella.
- **ATRADIUS, división Surety** — Oracle DBA | 2022 – 2026:
  - Capa DBA en soporte del DWH multi-país (Italia, España, Francia, Norte de Europa) — más de 60.000 líneas de PL/SQL ETL, carga diaria completa en menos de 2 horas en OCI.
- **Otros clientes Banking, Telco y pagos**:
  - Batches analíticos críticos reducidos de 4 horas a menos de 30 minutos sobre Oracle en OCI y Autonomous Database.
  - ETL/ELT desde más de 15 fuentes heterogéneas sobre datasets superiores a los 2 mil millones de filas; RMAN, OEM, patching; DWH sobre PostgreSQL como alternativa cost-effective a Oracle.

---

### FREELANCE / CONSULTOR INDEPENDIENTE — Roma, Italia (Full Remote Europa)
**Senior Oracle DBA & Performance Tuning Expert · DWH Architect** | 2013 – 2022

- **FAI SERVICE** — Oracle DBA | 2021 – 2023:
  - Administración y tuning de Oracle 19c en OCI en soporte de ETL y dashboards Oracle Analytics Cloud.
  - *(contrato absorbido por IDEA DB CONSULTING desde 2022 con novación del contrato)*
- **LISCOR → Finwave, Gruppo Lutech** — Oracle DBA en el sector financiero | 2020 – 2023:
  - Desarrollo PL/SQL avanzado y optimización de consultas para aplicaciones financieras con millones de transacciones diarias.
  - *(contrato absorbido por IDEA DB CONSULTING desde 2022 con novación del contrato)*
- **NIMIS → Huawei → para TIM** — Senior Oracle DBA & Performance Tuning Expert | 2020 – 2022:
  - Más de 30 bases de datos Oracle críticas (67+ instancias) sobre clusters Exadata de 3 y 5 nodos.
  - Responsabilidad directa en performance tuning avanzado: análisis AWR/ADDM, optimización SQL, indexación, partitioning y compression; ingesta de hasta 800 millones de registros al día, SLA por debajo de los 500 ms.
  - Storage management (ASM) y Oracle TDE para la seguridad de los datos; guardia 24/7 para la resolución de las criticidades.
  - *(contrato absorbido por IDEA DB CONSULTING desde 2022 con novación del contrato)*
- **DatabTech, Milán** — Oracle DBA y DWH Architect para Allianz y Mediobanca | 2018 – 2021:
  - Migración de proyectos Oracle Data Integrator (ODI) de la versión 10g a la 12c.
- **Otros clientes Banking, Insurance y Telco** | 2013 – 2018:
  - Consultoría Oracle DBA y performance tuning para clientes Banking, Insurance y Telco.
  - Optimización de consultas SQL complejas y tuning de instancias Oracle; RMAN y Oracle Data Guard HA/DR con procedimientos de switchover/failover.
  - Coordinación de pequeños equipos técnicos en proyectos de migración y upgrade.

---

### AUSELDA AED GROUP S.P.A. — Roma, Italia
**Project Oracle DBA · Performance & Tuning Expert** (para la Administración Pública) | 2009 – 2013

- Administración y optimización de bases de datos Oracle en soporte de aplicaciones de la Administración Pública.
- Tuning de consultas SQL y procesos ETL para sistemas DWH; instalación, patching y gestión de la seguridad.

---

### ORACLE ITALIA S.R.L. — Varias sedes, Italia & Madrid, España
**Oracle DBA · DWH Architect · SQL & PL/SQL Developer · Training Specialist** | 1999 – 2009

- Administración de bases de datos Oracle para clientes Telco (TIM, Vodafone, TRE), Finance (Banco de Italia, Generali, RAS) y Farmacéutico (Menarini) con responsabilidades crecientes.
- Ingaje internacional en Vodafone España (Madrid).
- Training Specialist (2000-2001) sobre Oracle Database Administration y Performance & Tuning.

---

### ETNOTEAM S.P.A. · 1999 — S.EL.DAT. S.P.A. · 1997 – 1999
**Software Developer · Junior Oracle DBA** (para Telecom, Rover Italia)

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

- Análisis metódico de los problemas de performance, hasta la causa real
- Gestión de prioridades y cumplimiento de deadlines bajo presión operativa
- Comunicación técnica clara, basada en evidencias
- Atención al detalle y precisión operativa
- Aprendizaje continuo y adaptabilidad tecnológica

---

*Autorizo el tratamiento de mis datos personales conforme al Art. 13 del Reglamento UE 2016/679 (GDPR).*

Roma, Septiembre 2026

---

**[Descargar PDF]({{% staticurl "downloads/CV_Oracle_DBA_Ivan_Luminaria_202609_EN.pdf" %}})** | **[Perfil LinkedIn](https://www.linkedin.com/in/ivanluminaria)** | **[Volver a la página anterior](/es/resumes/)**
