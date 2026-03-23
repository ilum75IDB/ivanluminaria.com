---
title: "AWR"
description: "Automatic Workload Repository — instrument de diagnostic integrat in Oracle Database pentru colectarea si analiza statisticilor de performanta."
translationKey: "glossary_awr"
aka: "Automatic Workload Repository"
articles:
  - "/posts/oracle/oracle-awr-ash"
  - "/posts/oracle/oracle-cloud-migration"
---

**AWR** (Automatic Workload Repository) este o componenta integrata in Oracle Database care colecteaza automat statistici de performanta ale sistemului la intervale regulate (implicit la fiecare 60 de minute) si le pastreaza pentru o perioada configurabila.

## Cum functioneaza

AWR captureaza snapshot-uri periodice care includ:

- Statistici ale sesiunilor si wait events
- Metrici SQL (top SQL dupa timp de executie, I/O, CPU)
- Statistici ale structurilor de memorie (SGA, PGA)
- Statistici I/O per datafile si tablespace

## La ce serveste

Raportul AWR este instrumentul principal pentru diagnosticarea problemelor de performanta in Oracle. Comparand doua snapshot-uri se pot identifica:

- Query-uri care consuma prea multe resurse
- Modificari in planurile de executie
- Blocaje pe I/O, CPU sau memorie
- Regresii de performanta dupa deploy-uri aplicative

## Cand se foloseste

AWR este primul instrument de consultat cand se primeste o raportare de incetinire. Impreuna cu **ASH** (Active Session History), permite reconstructia a ceea ce s-a intamplat in baza de date intr-un interval de timp specific, chiar si dupa ce problema s-a rezolvat.
