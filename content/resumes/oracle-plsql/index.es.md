---
title: "Oracle PL/SQL Developer"
seoTitle: "Oracle PL/SQL Developer & SQL Tuning"
description: "Ivan Luminaria, Oracle PL/SQL Developer & SQL Tuning Expert: 30 años desarrollando, refactorizando y optimizando código PL/SQL para apps data-intensive enterprise."
date: "2026-09-14"
lastmod: "2026-09-20"
draft: false
layout: "simple"
---

**[Descargar PDF]({{% staticurl "downloads/CV_Oracle_PLSQL_Ivan_Luminaria_202609_EN.pdf" %}})** | **[Perfil LinkedIn](https://www.linkedin.com/in/ivanluminaria)**

> **Un rol, cuatro pilares.** Este perfil es uno de los cuatro pilares del rol [Technical Leader para bases de datos y Data Warehouse mission-critical](/es/resumes/technical-leader/).

---

## Perfil Profesional

El PL/SQL tiene una característica particular entre los lenguajes de programación: se queda en producción durante décadas, pasando a menudo por cuatro o cinco generaciones de desarrolladores que se lo van pasando. El valor de quien lo escribe se mide en lo que esos sucesores todavía pueden leer, entender y modificar.

Cuando enseño PL/SQL, me gusta definirlo como **lenguaje orientado a las excepciones**: la capacidad de gestionar excepciones de sistema y de definir excepciones custom, de forma declarativa dentro de cada bloque, es lo que permite al código sobrevivir a escenarios que en el momento de la escritura no eran previsibles.

Cursores fila por fila que podrían ser BULK COLLECT. DML que ignora el particionamiento subyacente. SQL dinámico construido con concatenación de strings cuando el bind variable ya existía. Son los detalles de escritura que multiplican los tiempos de ejecución — la diferencia entre un batch de 4 horas y uno de 30 minutos casi siempre está en pocas páginas de código. Y cuando 60.000 líneas de código gobiernan el insurance business de cuatro países europeos, lo que parecía legacy se convierte en la columna vertebral operativa: no código para reescribir, sino reglamento ejecutable de cómo funciona realmente el negocio.

Packages ETL de más de 60.000 líneas para DWH multi-país, ingesta daily reducida de más de 4 horas a menos de 2 horas con BULK COLLECT/FORALL, partition-aware DML y query rewriting. Batches analíticos de 4 horas a menos de 30 minutos sobre datasets de más de 2 mil millones de filas. Packages para gestión transaccional financiera con millones de operaciones diarias. PL/SQL Hierarchical Profiler, SQL Trace, TKPROF. Docencia Oracle Italia sobre SQL y PL/SQL. Veinticinco años de mentoring continuo de desarrolladores junior hacia nivel senior en banca, seguros, telco, administración pública y postal.

Además de PL/SQL y SQL puedo leer, comprender y modificar también otros lenguajes — Unix Shell Script, Python, Java, C++, JavaScript, HTML, CSS, Pascal y CaML. Algunos los he estudiado en la universidad, otros los he aprendido cuando ha hecho falta tocar el código alrededor de la base de datos. No soy un guru de ninguno de ellos; pero cuando un trozo de lógica crítica vive fuera de la base de datos — en un script shell, en un servicio Python, en un frontend que llama a procedures PL/SQL — leer el otro lado ayuda a entender dónde está realmente el problema.

Lo que aporto: PL/SQL que tus desarrolladores junior pueden leer y mantener, refactors específicos que reducen deuda técnica sin rewrites apresurados, y la disciplina de distinguir lo que es deuda técnica de lo que es patrimonio de negocio.

---

## Áreas de intervención

- **Desarrollo PL/SQL & code review** — packages para lógica ETL, procedures de procesamiento de datos, PL/SQL APIs, business logic; auditoría y refactor de codebases legacy.
- **PL/SQL & SQL performance tuning** — análisis Hierarchical Profiler, patterns BULK COLLECT/FORALL, partition-aware DML, reescrituras guiadas por execution plan.
- **Diseño ETL/ELT en PL/SQL** — templates de carga estandarizados con checkpoints, logging en tiempo real, error recovery, dashboards de monitorización.
- **Mentoring & transferencia de competencias** — coaching de desarrolladores junior sobre best practices PL/SQL, estándares de código, patterns testables.

---

## Resultados destacados

- **Varios cientos de bases de datos Oracle** en 30 años, entre desarrollo PL/SQL, tuning, DWH y administración.
- **Más de 60.000 líneas de PL/SQL** diseñadas y mantenidas para el **DWH Surety** (Atradius) multi-país sobre **4 países europeos** (Italia, España, Francia, Norte de Europa); templates reutilizables y monitorización en tiempo real de las cargas.
- Ingestion diaria completa **de más de 4 horas a menos de 2 horas** mediante query rewriting, BULK COLLECT/FORALL y partition-aware DML.
- Packages PL/SQL para el procesamiento de transacciones financieras con **millones de operaciones diarias** en clientes banking y insurance.
- Batches analíticos críticos reducidos **de 4 horas a menos de 30 minutos** sobre datasets de más de 2 mil millones de filas.
- Pipelines ETL/ELT que integran **más de 15 fuentes heterogéneas** hacia Oracle y dashboards Oracle Analytics Cloud.

---

## Competencias Clave

### Lenguajes

- PL/SQL avanzado · SQL avanzado (Dynamic SQL, analytic functions, CTEs)
- Unix Shell scripting

### Desarrollo PL/SQL

- Packages, procedures, functions, triggers
- Records, collections, object types · error/exception handling
- Bulk processing (FORALL, BULK COLLECT) · dynamic SQL (DBMS_SQL, EXECUTE IMMEDIATE)
- PL/SQL Hierarchical Profiler
- Interacción con tablas, vistas, sequences, synonyms

### SQL Optimisation & Performance

- Análisis de Execution Plan (Explain Plan), SQL Trace, TKPROF
- Técnicas de SQL Tuning (Hints, query rewriting, indexes)
- Impacto del diseño de base de datos sobre las performance PL/SQL

### Oracle Database

- Oracle Database hasta la 23ai, Autonomous Database

### Conceptos relacionados

- Data Warehousing (lógica ETL/ELT), data integration
- Modelado relacional y multidimensional

### Herramientas de desarrollo

- SQL Developer, Toad, SQL*Plus
- Git y GitHub para el version control

### Cloud

- Oracle Cloud Infrastructure (OCI) — conocimiento de los database services

---

## Experiencia Profesional

### IDEA DB CONSULTING S.R.L. — Roma, Italia (Full Remote Europa)
**Administrador Único · Senior Oracle PL/SQL Developer · DWH Architect** | 2022 – Presente

- **SILICONDEV → POSTE ITALIANE** — Senior Database Consultant | Jul 2025 – Presente:
  - Administración de aproximadamente 1.500 instancias MySQL y PostgreSQL entre producción, certificación y desarrollo.
  - Query tuning, monitorización de las performance, gestión de la replicación y capacity planning a escala enterprise.
- **GENERALI Seguros** — SQL & PL/SQL Optimization | Feb 2024 – May 2025:
  - Optimización de consultas complejas y desarrollo PL/SQL sobre bases de datos Oracle de 500 GB a 8 TB para aplicaciones del sector asegurador.
  - Análisis Hierarchical Profiler y SQL tuning para identificar cuellos de botella.
- **ATRADIUS, división Surety** — PL/SQL Developer | 2022 – 2026:
  - Más de 60.000 líneas de código PL/SQL (packages, procedures, functions) para el DWH multi-país (Italia, España, Francia, Norte de Europa) que consolida siniestros de seguros y datos de crédito.
  - Templates PL/SQL reutilizables para procedures de carga con checkpoints y logging en tiempo real.
  - Optimización de las performance batch (query rewriting, BULK COLLECT/FORALL, partition-aware DML): ciclo diario reducido de más de 4 horas a menos de 2 horas.
- **Otros clientes Banking, Telco y pagos** — Desarrollo PL/SQL:
  - Packages de business logic PL/SQL para aplicaciones DWH del sector banking sobre datasets de más de 2 mil millones de filas.
  - Optimización del código PL/SQL y de las consultas SQL con análisis Hierarchical Profiler para identificar cuellos de botella.

---

### FREELANCE / CONSULTOR INDEPENDIENTE — Roma, Italia (Full Remote Europa)
**Senior Oracle PL/SQL Developer & DBA · DWH Architect** | 2013 – 2022

- **FAI SERVICE** — PL/SQL Developer | 2021 – 2023:
  - Procedures ETL en PL/SQL sobre Oracle 19c en OCI para facturación, segmentación de clientes y tracking de costes/ingresos.
  - Módulos PL/SQL de soporte a los dashboards Oracle Analytics Cloud con KPIs financieros agregados.
  - *(contrato absorbido por IDEA DB CONSULTING desde 2022 con novación del contrato)*
- **LISCOR → Finwave, Gruppo Lutech** — PL/SQL Developer en el sector financiero | 2020 – 2023:
  - Packages PL/SQL para el procesamiento de transacciones financieras con millones de operaciones diarias en clientes banking y insurance.
  - *(contrato absorbido por IDEA DB CONSULTING desde 2022 con novación del contrato)*
- **NIMIS → Huawei → para TIM** — Senior Oracle DBA & Performance Expert (enfoque Development) | 2020 – 2022:
  - Soporte especializado a los equipos de desarrollo en la optimización de código PL/SQL y consultas SQL para aplicaciones críticas sobre Exadata (67+ instancias).
  - Análisis y tuning de procesos batch PL/SQL de alto volumen; scripts PL/SQL para monitorización y administración.
  - *(contrato absorbido por IDEA DB CONSULTING desde 2022 con novación del contrato)*
- **DatabTech, Milán** — Oracle DBA y DWH Architect para Allianz y Mediobanca | 2018 – 2021:
  - Migración de proyectos Oracle Data Integrator (ODI) de la versión 10g a la 12c, con desarrollo PL/SQL de soporte a los mappings migrados.
- **Otros clientes Banking, Insurance y Telco** | 2013 – 2018:
  - Soluciones PL/SQL custom para diversos clientes: packages para lógica ETL, procedures de procesamiento de datos, PL/SQL APIs.
  - Intensa optimización de código PL/SQL y SQL para mejorar las performance de sistemas existentes.
  - Formación y mentoring de desarrolladores junior sobre best practices de desarrollo PL/SQL.

---

### AUSELDA AED GROUP S.P.A. — Roma, Italia
**Oracle PL/SQL Developer · DWH Specialist** (para la Administración Pública) | 2009 – 2013

- Desarrollo de componentes PL/SQL para sistemas de Data Warehousing y aplicaciones de gestión para la Administración Pública.
- Mantenimiento evolutivo y correctivo del código PL/SQL; optimización de procesos ETL basados en PL/SQL y OWB.

---

### ORACLE ITALIA S.R.L. — Varias sedes, Italia & Madrid, España
**SQL & PL/SQL Developer · DWH Architect · DBA · Training Specialist** | 1999 – 2009

- Desarrollo intensivo de código PL/SQL para proyectos DWH, BI y aplicaciones custom para TIM, Vodafone (Italia y España), Banco de Italia, Generali, Menarini.
- Creación de packages PL/SQL para business logic compleja y procedures de carga de datos (ETL) con Oracle Warehouse Builder.
- BI Reports e interfaces HTMLDB (Apex) con lógica PL/SQL.
- Training Specialist (2000-2001) sobre cursos Oracle SQL y PL/SQL (básico y avanzado).

---

### ETNOTEAM S.P.A. · 1999 — S.EL.DAT. S.P.A. · 1997 – 1999
**Web Developer · Oracle SQL & PL/SQL Developer · Junior DBA** (para Telecom, Rover Italia)

- Desarrollo de portales web y aplicaciones client-server con fuerte interacción Oracle; SQL y PL/SQL para la lógica de backend.

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

- Enfoque analítico y orientación a la resolución de problemas complejos
- Escritura de código limpio, eficiente y mantenible
- Debugging y troubleshooting avanzados
- Comprensión de requisitos funcionales y técnicos
- Colaboración eficaz en equipos de desarrollo
- Atención al detalle y a la calidad del software

---

*Autorizo el tratamiento de mis datos personales conforme al Art. 13 del Reglamento UE 2016/679 (GDPR).*

Roma, Septiembre 2026

---

**[Descargar PDF]({{% staticurl "downloads/CV_Oracle_PLSQL_Ivan_Luminaria_202609_EN.pdf" %}})** | **[Perfil LinkedIn](https://www.linkedin.com/in/ivanluminaria)** | **[Volver a la página anterior](/es/resumes/)**
