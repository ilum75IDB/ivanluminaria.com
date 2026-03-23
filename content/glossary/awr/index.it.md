---
title: "AWR"
description: "Automatic Workload Repository — strumento diagnostico integrato in Oracle Database per la raccolta e l'analisi delle statistiche di performance."
translationKey: "glossary_awr"
aka: "Automatic Workload Repository"
articles:
  - "/posts/oracle/oracle-awr-ash"
  - "/posts/oracle/oracle-cloud-migration"
---

**AWR** (Automatic Workload Repository) è un componente integrato nel database Oracle che raccoglie automaticamente statistiche sulle performance del sistema a intervalli regolari (di default ogni 60 minuti) e le conserva per un periodo configurabile.

## Come funziona

AWR cattura snapshot periodici che includono:

- Statistiche delle sessioni e dei wait event
- Metriche SQL (top SQL per tempo di esecuzione, I/O, CPU)
- Statistiche sulle strutture di memoria (SGA, PGA)
- Statistiche I/O per datafile e tablespace

## A cosa serve

Il report AWR è lo strumento principale per diagnosticare problemi di performance in Oracle. Confrontando due snapshot è possibile identificare:

- Query che consumano troppe risorse
- Cambiamenti nei piani di esecuzione
- Colli di bottiglia su I/O, CPU o memoria
- Regressioni di performance dopo deploy applicativi

## Quando si usa

AWR è il primo strumento da consultare quando si riceve una segnalazione di lentezza. Insieme ad **ASH** (Active Session History), permette di ricostruire cosa è successo nel database in un intervallo di tempo specifico, anche dopo che il problema si è risolto.
