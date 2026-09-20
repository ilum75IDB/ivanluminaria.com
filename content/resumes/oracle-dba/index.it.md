---
title: "Oracle DBA & Performance Tuning Expert"
seoTitle: "Oracle DBA & Performance Tuning Expert"
description: "Ivan Luminaria, Oracle DBA & Performance Tuning Expert: 30 anni in amministrazione database mission-critical, RAC, Data Guard, Exadata, AWR/ASH e Oracle Cloud."
date: "2026-09-14"
lastmod: "2026-09-20"
draft: false
layout: "simple"
---

**[Scarica PDF]({{% staticurl "downloads/CV_Oracle_DBA_Ivan_Luminaria_202609_EN.pdf" %}})** | **[Profilo LinkedIn](https://www.linkedin.com/in/ivanluminaria)**

> **Un ruolo, quattro pilastri.** Questo profilo è uno dei quattro pilastri del ruolo [Technical Leader per database e Data Warehouse mission-critical](/it/resumes/technical-leader/).

---

## Profilo Professionale

Centinaia di database Oracle amministrati in trent'anni tra banking, assicurazioni, telco, pubblica amministrazione e postale — cluster Exadata multi-nodo, fact table oltre 800M record al giorno con SLA sotto i 500 ms, ambienti a supporto di 20M+ utenti finali. Amministrazione MySQL e PostgreSQL a scala enterprise. Batch analitici da 4 ore a meno di 30 minuti su Oracle OCI e Autonomous Database — senza cambio di piattaforma. OCP dai tempi in cui erano rari. Docenza Oracle Italia su SQL, PL/SQL, amministrazione, performance tuning; venticinque anni di mentoring continuativo di DBA junior verso senior.

Quello che vedo quando arriva una richiesta di intervento post-incident: le metriche dei monitoring nel verde fino a quaranta minuti prima. Il ticket vendor chiuso con «unable to reproduce». Il DBA junior che ha ereditato il sistema da un senior uscito a fine anno e non ha ancora la mappa mentale per collegare i puntini. La catena causale sta quasi sempre nell'intreccio tra layer — applicazione, database, storage, rete — non dentro un layer solo. Gli strumenti mostrano sintomi, non cause.

Post-Incident Root Cause Analysis su casi in cui i log del momento erano stati rotati o compressi male: storico AWR e ASH, log di sistema operativo e storage, registro dei change. Ho ricostruito catene causali che il team pensava perse, e prodotto documenti che sono passati davanti al board senza che il DBA senior fosse messo in mezzo per default. Cosa porto: un metodo cross-layer costruito su sistemi reali. Non cerchiamo colpevoli, ricostruiamo cosa è successo davvero.

---

## Aree di intervento

- **Health Check dei database** — valutazione strutturata di performance, affidabilità, capacità e rischi latenti, con report di evidenze e roadmap di priorità.
- **Post-Incident Root Cause Analysis** — ricostruzione dell'incidente sui dati reali (AWR, ASH, wait event, log applicativi e infrastrutturali), separando cause, conseguenze e semplici correlazioni.
- **DBA leadership continuativa** — tuning avanzato, piani di upgrade e patching, strategie HA/DR, coordinamento con sviluppo e infrastruttura.
- **Modernizzazione advisory** — valutazione di migrazioni Oracle → PostgreSQL, servizi database cloud e passaggio ad Autonomous Database, con analisi di costi e rischi indipendente dai vendor.

---

## Risultati in evidenza

- **Diverse centinaia di database Oracle** in 30 anni, tra amministrazione, tuning, DWH, PL/SQL e project management.
- Circa **1.500 istanze** MySQL e PostgreSQL amministrate oggi per **POSTE ITALIANE**.
- **30+ database Oracle su Exadata** (3+5 nodi, **67+ istanze**) su commessa telco per **TIM (via Huawei)**, al servizio di **oltre 20 milioni di utenti prepagati mobile**: fino a **800 milioni di record al giorno**; query critiche sotto i **500 ms** in reperibilità 24/7.
- Batch analitici critici ridotti **da 4 ore a meno di 30 minuti** su Oracle in OCI e Autonomous Database.
- **DWH Surety** (Atradius) su **4 Paesi europei** (Italia, Spagna, Francia, Nord Europa) supportato lato DBA: **oltre 60.000 righe di PL/SQL** e caricamento giornaliero in **meno di 2 ore**.
- Pipeline ETL/ELT che integrano **oltre 15 sorgenti eterogenee** su dataset superiori ai **2 miliardi di righe**.

---

## Competenze Chiave

### Oracle Database Administration

- Oracle Database fino alla 23ai, Autonomous Database
- Exadata, RAC, Data Guard, GoldenGate (base)

### Performance tuning avanzato

- Analisi e diagnostica: AWR, ADDM, ASH, Statspack, SQL Trace, TKPROF, Explain Plan
- SQL tuning: query complesse, hints, SQL Profiles, SQL Plan Management (SPM)
- Instance tuning: memoria (SGA/PGA), parametri di inizializzazione, analisi dei wait event
- Design per la performance: indicizzazione (B-tree, Bitmap, Function-based), partitioning (Range, List, Hash, Composite), compression

### HA/DR e sicurezza

- RMAN (backup, recovery, cloning), Data Guard, Flashback Technologies
- Oracle TDE, gestione utenti e privilegi, auditing
- ASM (Automatic Storage Management), gestione tablespace

### Installazione, patching, migrazioni

- Installazione nuove istanze, PSU/CPU/RU, upgrade di versione, migrazioni cross-platform

### Cloud

- Oracle Cloud Infrastructure (OCI): Compute, Storage, Networking, Database Services (VM DB, Bare Metal, Exadata CS, Autonomous Database)
- AWS Aurora PostgreSQL, ambienti Microsoft Azure Database

### Altri database e strumenti

- PostgreSQL (amministrazione, tuning, partitioning, replica)
- MySQL (amministrazione, replica, ottimizzazione InnoDB)
- Oracle Enterprise Manager (OEM) Cloud Control, SQL Developer, SQL*Plus, Toad
- PL/SQL, SQL, Unix Shell scripting

---

## Esperienza Professionale

### IDEA DB CONSULTING S.R.L. — Roma, Italia (Full Remote Europa)
**Amministratore Unico · Senior Oracle DBA & Performance Tuning Expert** | 2022 – Presente

- **SILICONDEV → POSTE ITALIANE** — Senior Database Consultant — MySQL & PostgreSQL DBA | Lug 2025 – Presente:
  - Amministrazione di circa 1.500 istanze MySQL e PostgreSQL tra produzione, certificazione e sviluppo.
  - Monitoraggio delle performance, query tuning, gestione della replica e capacity planning su scala enterprise.
- **GENERALI Assicurazioni** — Oracle DBA & Tuning Expert | Feb 2024 – Mag 2025:
  - Amministrazione e tuning avanzato di database Oracle da 500 GB a 8 TB per applicazioni del settore assicurativo.
  - Analisi AWR/ADDM, ottimizzazione SQL, risoluzione proattiva dei colli di bottiglia.
- **ATRADIUS, divisione Surety** — Oracle DBA | 2022 – 2026:
  - Amministrazione e tuning a supporto del DWH multi-paese (Italia, Spagna, Francia, Nord Europa) — oltre 60.000 righe di PL/SQL ETL, caricamento giornaliero sotto le 2 ore in OCI.
- **Altri clienti Banking, Telco e pagamenti**:
  - Batch analitici critici ridotti da 4 ore a meno di 30 minuti su Oracle in OCI e Autonomous Database.
  - ETL/ELT da oltre 15 sorgenti eterogenee su dataset superiori ai 2 miliardi di righe; RMAN, OEM, patching; DWH su PostgreSQL come alternativa cost-effective a Oracle.

---

### FREELANCE / CONSULENTE INDIPENDENTE — Roma, Italia (Full Remote Europa)
**Senior Oracle DBA & Performance Tuning Expert · DWH Architect** | 2013 – 2022

- **FAI SERVICE** — Oracle DBA | 2021 – 2023:
  - Amministrazione e tuning di Oracle 19c in OCI a supporto di ETL e dashboard Oracle Analytics Cloud.
  - *(contract confluito in IDEA DB CONSULTING dal 2022 con sostituzione del contratto)*
- **LISCOR → Finwave, Gruppo Lutech** — Oracle DBA nel settore finanziario | 2020 – 2023:
  - Sviluppo PL/SQL avanzato e query optimization per applicazioni finanziarie con milioni di transazioni giornaliere.
  - *(contract confluito in IDEA DB CONSULTING dal 2022 con sostituzione del contratto)*
- **NIMIS → Huawei → per TIM** — Senior Oracle DBA & Performance Tuning Expert | 2020 – 2022:
  - Oltre 30 database Oracle critici (67+ istanze) su cluster Exadata a 3 e 5 nodi.
  - Responsabilità diretta su performance tuning avanzato: analisi AWR/ADDM, ottimizzazione SQL, indicizzazione, partitioning e compression; ingestion fino a 800 milioni di record al giorno, SLA sotto i 500 ms.
  - Storage management (ASM) e Oracle TDE per la sicurezza dei dati; reperibilità 24/7 per la risoluzione delle criticità.
  - *(contract confluito in IDEA DB CONSULTING dal 2022 con sostituzione del contratto)*
- **DatabTech, Milano** — Oracle DBA e DWH Architect per Allianz e Mediobanca | 2018 – 2021:
  - Migrazione di progetti Oracle Data Integrator (ODI) dalla versione 10g alla 12c.
- **Altri clienti Banking, Insurance e Telco** | 2013 – 2018:
  - Consulenza Oracle DBA e performance tuning per clienti Banking, Insurance e Telco.
  - Ottimizzazione di query SQL complesse e tuning di istanze Oracle; RMAN e Oracle Data Guard HA/DR con procedure di switchover/failover.
  - Coordinamento di piccoli team tecnici in progetti di migrazione e upgrade.

---

### AUSELDA AED GROUP S.P.A. — Roma, Italia
**Project Oracle DBA · Performance & Tuning Expert** (per la Pubblica Amministrazione) | 2009 – 2013

- Amministrazione e ottimizzazione di database Oracle a supporto di applicazioni della Pubblica Amministrazione.
- Tuning di query SQL e processi ETL per sistemi DWH; installazione, patching e gestione della sicurezza.

---

### ORACLE ITALIA S.R.L. — Varie sedi, Italia & Madrid, Spagna
**Oracle DBA · DWH Architect · SQL & PL/SQL Developer · Training Specialist** | 1999 – 2009

- Amministrazione di database Oracle per clienti Telco (TIM, Vodafone, TRE), Finance (Banca d'Italia, Generali, RAS) e Farmaceutico (Menarini) con responsabilità crescenti.
- Ingaggio internazionale su Vodafone Spagna (Madrid).
- Training Specialist (2000-2001) su Oracle Database Administration e Performance & Tuning.

---

### ETNOTEAM S.P.A. · 1999 — S.EL.DAT. S.P.A. · 1997 – 1999
**Software Developer · Junior Oracle DBA** (per Telecom, Rover Italia)

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

- Analisi metodica dei problemi di performance, fino alla causa reale
- Gestione delle priorità e rispetto delle deadline sotto pressione operativa
- Comunicazione tecnica chiara, basata sulle evidenze
- Attenzione al dettaglio e alla precisione operativa
- Apprendimento continuo e adattabilità tecnologica

---

*Autorizzo il trattamento dei miei dati personali ai sensi dell'Art. 13 del Regolamento UE 2016/679 (GDPR).*

Roma, Settembre 2026

---

**[Scarica PDF]({{% staticurl "downloads/CV_Oracle_DBA_Ivan_Luminaria_202609_EN.pdf" %}})** | **[Profilo LinkedIn](https://www.linkedin.com/in/ivanluminaria)** | **[Torna alla pagina precedente](/it/resumes/)**
