---
title: "Oracle PL/SQL Developer"
seoTitle: "Oracle PL/SQL Developer & SQL Tuning"
description: "Ivan Luminaria, Oracle PL/SQL Developer & SQL Tuning Expert: 30 anni in sviluppo, refactoring e ottimizzazione PL/SQL per applicazioni data-intensive enterprise."
date: "2026-09-14"
lastmod: "2026-09-20"
draft: false
layout: "simple"
---

**[Scarica PDF]({{% staticurl "downloads/CV_Oracle_PLSQL_Ivan_Luminaria_202609_EN.pdf" %}})** | **[Profilo LinkedIn](https://www.linkedin.com/in/ivanluminaria)**

> **Un ruolo, quattro pilastri.** Questo profilo è uno dei quattro pilastri del ruolo [Technical Leader per database e Data Warehouse mission-critical](/it/resumes/technical-leader/).

---

## Profilo Professionale

Il PL/SQL ha una caratteristica particolare tra i linguaggi di programmazione: sta in produzione per decenni, spesso attraversando quattro o cinque generazioni di sviluppatori che se lo passano tra di loro. Il valore di chi lo scrive si misura in quello che quei successori possono ancora leggere, capire e modificare.

Quando insegno PL/SQL, mi piace definirlo come **linguaggio orientato alle eccezioni**: la capacità di gestire eccezioni di sistema e di definirne di custom, in modo dichiarativo dentro ogni blocco, è quello che permette al codice di sopravvivere a scenari che al tempo della scrittura non erano prevedibili.

Cursori riga-per-riga che potrebbero essere BULK COLLECT. DML che ignora il partizionamento sottostante. Dinamica SQL costruita con concatenazione di stringhe quando il bind variable esisteva. Sono i dettagli di scrittura che moltiplicano i tempi di esecuzione — la differenza tra un batch di 4 ore e uno di 30 minuti sta quasi sempre in poche pagine di codice. E quando 60.000 righe di codice governano l'insurance business di quattro paesi europei, quello che sembrava legacy diventa la spina dorsale operativa: non codice da riscrivere, ma regolamento eseguibile di come funziona davvero il business.

Package ETL da oltre 60.000 righe per DWH multi-paese, ingestion daily portata da oltre 4 ore a meno di 2 ore con BULK COLLECT/FORALL, partition-aware DML e query rewriting. Batch analitici da 4 ore a meno di 30 minuti su dataset oltre 2 miliardi di righe. Package per gestione transazionale finanziaria a milioni di operazioni giornaliere. PL/SQL Hierarchical Profiler, SQL Trace, TKPROF. Docenza Oracle Italia su SQL e PL/SQL. Venticinque anni di mentoring continuativo di developer junior verso senior in banking, assicurazioni, telco, pubblica amministrazione e postale.

Oltre a PL/SQL e SQL riesco a leggere, comprendere e modificare anche altri linguaggi — Unix Shell Script, Python, Java, C++, JavaScript, HTML, CSS, Pascal e Caml. Alcuni li ho studiati all'università, altri imparati quando è servito toccare il codice attorno al database. Non sono il guru di nessuno di loro; ma quando un pezzo di logica critica vive fuori dal database — in uno script shell, in un servizio Python, in un frontend che chiama procedure PL/SQL — leggere l'altro lato aiuta a capire dove sta davvero il problema.

Cosa porto: PL/SQL che i tuoi developer junior possono leggere e mantenere, refactor mirati che riducono debito tecnico senza rewrite frettolosi, e la disciplina di distinguere quello che è debito tecnico da quello che è patrimonio di business.

---

## Aree di intervento

- **Sviluppo PL/SQL & code review** — package per logica ETL, procedure di elaborazione dati, PL/SQL API, business logic; audit e refactor di codebase legacy.
- **PL/SQL & SQL performance tuning** — analisi Hierarchical Profiler, pattern BULK COLLECT/FORALL, partition-aware DML, riscritture guidate dall'execution plan.
- **Design ETL/ELT in PL/SQL** — template di caricamento standardizzati con checkpoint, logging in tempo reale, error recovery, dashboard di monitoraggio.
- **Mentoring & trasferimento di competenze** — coaching di sviluppatori junior su best practice PL/SQL, code standard, pattern testabili.

---

## Risultati in evidenza

- **Diverse centinaia di database Oracle** in 30 anni, tra sviluppo PL/SQL, tuning, DWH e amministrazione.
- **Oltre 60.000 righe di PL/SQL** progettate e mantenute per il **DWH Surety** (Atradius) multi-paese su **4 Paesi europei** (Italia, Spagna, Francia, Nord Europa); template riutilizzabili e monitoraggio in tempo reale.
- Ingestion giornaliera completa **da oltre 4 ore a meno di 2 ore** con query rewriting, BULK COLLECT/FORALL e partition-aware DML.
- Package PL/SQL per il processing di transazioni finanziarie con **milioni di operazioni giornaliere** su clienti banking e insurance.
- Batch analitici critici ridotti **da 4 ore a meno di 30 minuti** su dataset da oltre 2 miliardi di righe.
- Pipeline ETL/ELT che integrano **oltre 15 sorgenti eterogenee** verso Oracle e dashboard Oracle Analytics Cloud.

---

## Competenze Chiave

### Linguaggi

- PL/SQL avanzato · SQL avanzato (Dynamic SQL, analytic functions, CTE)
- Unix Shell scripting

### Sviluppo PL/SQL

- Package, procedure, function, trigger
- Record, collection, object types · error/exception handling
- Bulk processing (FORALL, BULK COLLECT) · dynamic SQL (DBMS_SQL, EXECUTE IMMEDIATE)
- PL/SQL Hierarchical Profiler
- Interazione con tabelle, view, sequence, synonym

### SQL Optimization & Performance

- Analisi Execution Plan (Explain Plan), SQL Trace, TKPROF
- Tecniche di SQL Tuning (Hints, query rewriting, indexes)
- Impatto del database design sulle performance PL/SQL

### Oracle Database

- Oracle Database fino alla 23ai, Autonomous Database

### Concetti correlati

- Data Warehousing (logica ETL/ELT), data integration
- Modellazione relazionale e multidimensionale

### Strumenti di sviluppo

- SQL Developer, Toad, SQL*Plus
- Git e GitHub per il version control

### Cloud

- Oracle Cloud Infrastructure (OCI) — conoscenza dei database services

---

## Esperienza Professionale

### IDEA DB CONSULTING S.R.L. — Roma, Italia (Full Remote Europa)
**Amministratore Unico · Senior Oracle PL/SQL Developer · DWH Architect** | 2022 – Presente

- **SILICONDEV → POSTE ITALIANE** — Senior Database Consultant | Lug 2025 – Presente:
  - Amministrazione di circa 1.500 istanze MySQL e PostgreSQL tra produzione, certificazione e sviluppo.
  - Query tuning, monitoraggio delle performance, gestione della replica e capacity planning su scala enterprise.
- **GENERALI Assicurazioni** — SQL & PL/SQL Optimization | Feb 2024 – Mag 2025:
  - Ottimizzazione di query complesse e sviluppo PL/SQL su database Oracle da 500 GB a 8 TB per applicazioni del settore assicurativo.
  - Analisi Hierarchical Profiler e SQL tuning per identificare colli di bottiglia.
- **ATRADIUS, divisione Surety** — PL/SQL Developer | 2022 – 2026:
  - Oltre 60.000 righe di codice PL/SQL (package, procedure, function) per il DWH multi-paese (Italia, Spagna, Francia, Nord Europa) che consolida sinistri assicurativi e dati di credito.
  - Template PL/SQL riutilizzabili per procedure di caricamento con checkpoint e logging in tempo reale.
  - Ottimizzazione delle performance batch (query rewriting, BULK COLLECT/FORALL, partition-aware DML): ciclo giornaliero ridotto da oltre 4 ore a meno di 2 ore.
- **Altri clienti Banking, Telco e pagamenti** — Sviluppo PL/SQL:
  - Package di business logic PL/SQL per applicazioni DWH del settore banking su dataset da oltre 2 miliardi di righe.
  - Ottimizzazione del codice PL/SQL e delle query SQL con analisi Hierarchical Profiler per identificare i colli di bottiglia.

---

### FREELANCE / CONSULENTE INDIPENDENTE — Roma, Italia (Full Remote Europa)
**Senior Oracle PL/SQL Developer & DBA · DWH Architect** | 2013 – 2022

- **FAI SERVICE** — PL/SQL Developer | 2021 – 2023:
  - Procedure ETL in PL/SQL su Oracle 19c in OCI per fatturazione, segmentazione clienti e tracking costi/ricavi.
  - Moduli PL/SQL a supporto delle dashboard Oracle Analytics Cloud con KPI finanziari aggregati.
  - *(contract confluito in IDEA DB CONSULTING dal 2022 con sostituzione del contratto)*
- **LISCOR → Finwave, Gruppo Lutech** — PL/SQL Developer nel settore finanziario | 2020 – 2023:
  - Package PL/SQL per il processing di transazioni finanziarie con milioni di operazioni giornaliere su clienti banking e insurance.
  - *(contract confluito in IDEA DB CONSULTING dal 2022 con sostituzione del contratto)*
- **NIMIS → Huawei → per TIM** — Senior Oracle DBA & Performance Expert (focus Development) | 2020 – 2022:
  - Supporto specialistico ai team di sviluppo nell'ottimizzazione di codice PL/SQL e query SQL per applicazioni critiche su Exadata (67+ istanze).
  - Analisi e tuning di processi batch PL/SQL ad alto volume; script PL/SQL per monitoraggio e amministrazione.
  - *(contract confluito in IDEA DB CONSULTING dal 2022 con sostituzione del contratto)*
- **DatabTech, Milano** — Oracle DBA e DWH Architect per Allianz e Mediobanca | 2018 – 2021:
  - Migrazione di progetti Oracle Data Integrator (ODI) dalla versione 10g alla 12c, con sviluppo PL/SQL a supporto delle mapping migrate.
- **Altri clienti Banking, Insurance e Telco** | 2013 – 2018:
  - Soluzioni PL/SQL custom per diversi clienti: package per logica ETL, procedure di elaborazione dati, PL/SQL API.
  - Intensa ottimizzazione di codice PL/SQL e SQL per migliorare le performance di sistemi esistenti.
  - Formazione e mentoring di sviluppatori junior sulle best practice di sviluppo PL/SQL.

---

### AUSELDA AED GROUP S.P.A. — Roma, Italia
**Oracle PL/SQL Developer · DWH Specialist** (per la Pubblica Amministrazione) | 2009 – 2013

- Sviluppo di componenti PL/SQL per sistemi di Data Warehousing e applicazioni gestionali della Pubblica Amministrazione.
- Manutenzione evolutiva e correttiva del codice PL/SQL; ottimizzazione di processi ETL basati su PL/SQL e OWB.

---

### ORACLE ITALIA S.R.L. — Varie sedi, Italia & Madrid, Spagna
**SQL & PL/SQL Developer · DWH Architect · DBA · Training Specialist** | 1999 – 2009

- Sviluppo intensivo di codice PL/SQL per progetti DWH, BI e applicazioni custom per TIM, Vodafone (Italia e Spagna), Banca d'Italia, Generali, Menarini.
- Creazione di package PL/SQL per business logic complessa e procedure di caricamento dati (ETL) con Oracle Warehouse Builder.
- BI Reports e interfacce HTMLDB (Apex) con logica PL/SQL.
- Training Specialist (2000-2001) su corsi Oracle SQL e PL/SQL (base e avanzato).

---

### ETNOTEAM S.P.A. · 1999 — S.EL.DAT. S.P.A. · 1997 – 1999
**Web Developer · Oracle SQL & PL/SQL Developer · Junior DBA** (per Telecom, Rover Italia)

- Sviluppo di portali web e applicazioni client-server con forte interazione Oracle; SQL e PL/SQL per la logica di backend.

---

## Formazione

- **Facoltà di Ingegneria Informatica (Ingegneria del Software)** | Università degli Studi Roma Tre, Roma | 1994 – 2000
- **Diploma di Maturità Scientifica** | Liceo Scientifico Isacco Newton / Manieri Copernico, Roma | 1988 – 1993
- **Inglese Avanzato (C1/C2)** | The British Council, Roma | 2003 – 2004
- Formazione continua: Scrum Agile e Project Management (Randstad / Forma.temp, 2024) · Data Wrangling with SQL (Coursera, UC Davis, 2021) · Advanced SQL for Query Tuning e Oracle 12c (LinkedIn Learning, 2020)

---

## Lingue

- **Italiano**: Madrelingua
- **Inglese**: C1/C2 (Fluente, professionale)
- **Spagnolo**: C1 (Fluente)
- **Rumeno**: C1 (Fluente)
- **Francese**: A1/A2 (Base)

---

## Competenze Trasversali

- Approccio analitico e orientamento alla risoluzione di problemi complessi
- Scrittura di codice pulito, efficiente e manutenibile
- Debugging e troubleshooting avanzati
- Comprensione di requisiti funzionali e tecnici
- Collaborazione efficace in team di sviluppo
- Attenzione al dettaglio e alla qualità del software

---

*Autorizzo il trattamento dei miei dati personali ai sensi dell'Art. 13 del Regolamento UE 2016/679 (GDPR).*

Roma, Settembre 2026

---

**[Scarica PDF]({{% staticurl "downloads/CV_Oracle_PLSQL_Ivan_Luminaria_202609_EN.pdf" %}})** | **[Profilo LinkedIn](https://www.linkedin.com/in/ivanluminaria)** | **[Torna alla pagina precedente](/it/resumes/)**
