---
title: "GxP"
description: "Termen colectiv pentru ghidurile de reglementare Good Practice din industria farmaceutică: impune change control, teste documentate și aprobare formală din partea Calității pentru orice modificare a sistemelor informatice."
translationKey: "glossary_gxp"
aka: "Good Practice (GMP, GLP, GCP, GDP)"
articles:
  - "/posts/oracle/latenza-wan-e-change-control-gxp-il-costo-reale-del-lift-and-shift"
---

GxP este un acronim colectiv care reunește ghidurile de reglementare „Good Practice" aplicabile industriilor farmaceutică, biotehnologică și a dispozitivelor medicale. „x" este un substituent pentru disciplina specifică: GMP (Manufacturing), GLP (Laboratory), GCP (Clinical), GDP (Distribution). Orice sistem informatizat care intră în sfera GxP este supus unor cerințe stricte de validare, integritate a datelor și control al modificărilor.

## Cadrul normativ

Cele două referințe principale pentru sistemele informatizate sunt **EU GMP Annex 11** (Europa) și **21 CFR Part 11** (FDA, SUA). Ambele impun ca fiecare sistem informatizat GxP să fie validat, că integritatea datelor este menținută și că modificările sunt urmărite printr-un audit trail. La nivelul bazei de date, aceasta înseamnă controlul versiunilor de schemă, loguri imutabile și proceduri de backup verificate la intervale documentate.

## Impactul operațional asupra change control

Orice modificare a unui sistem GxP — actualizare DBMS, migrare de schemă, schimbare de parametri de configurare — trebuie să urmeze un proces formal de change control:

1. **Impact Assessment**: evaluarea riscului față de starea validată existentă.
2. **Teste documentate**: IQ (Installation Qualification), OQ (Operational Qualification), PQ (Performance Qualification).
3. **Aprobarea Calității**: semnătură formală înainte de lansarea în producție.

Un lift-and-shift al unei baze de date Oracle către cloud, de exemplu, nu este niciodată transparent într-un mediu GxP: infrastructura subiacentă se schimbă, iar aceasta redeschide ciclul de validare. Termenele de change control — adesea între 4 și 12 săptămâni — reprezintă costul ascuns pe care planurile de migrare tind să îl subestimeze sistematic.

## Când DBA devine parte a procesului de reglementare

În mediile GxP, DBA nu gestionează doar performanța și disponibilitatea: este un actor în cadrul sistemului de calitate. Instrucțiunile DDL executate în producție trebuie pre-aprobate, backup-urile trebuie testate cu frecvență documentată și orice anomalie trebuie să genereze un deviation report. Latența WAN sau un failover neplanificat nu sunt doar incidente tehnice — pot fi evenimente de reglementare care necesită o investigație formală.
