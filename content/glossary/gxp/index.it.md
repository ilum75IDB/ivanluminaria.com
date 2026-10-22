---
title: "GxP"
description: "Insieme di linee guida regolatorie Good Practice per l'industria farmaceutica: impone change control, test documentati e approvazione formale per ogni modifica a sistemi computerizzati."
translationKey: "glossary_gxp"
aka: "Good Practice (GMP, GLP, GCP, GDP)"
articles:
  - "/posts/oracle/latenza-wan-e-change-control-gxp-il-costo-reale-del-lift-and-shift"
---

GxP è un acronimo collettivo che raggruppa le linee guida regolatorie "Good Practice" applicabili all'industria farmaceutica, biotecnologica e dei dispositivi medici. La "x" è un segnaposto per la disciplina specifica: GMP (Manufacturing), GLP (Laboratory), GCP (Clinical), GDP (Distribution). Ogni sistema computerizzato che ricade sotto GxP è soggetto a requisiti stringenti di validazione, tracciabilità e controllo delle modifiche.

## Perimetro normativo

I riferimenti principali per i sistemi informatici sono due: **EU GMP Annex 11** (Europa) e **21 CFR Part 11** (FDA, USA). Entrambi richiedono che ogni sistema computerizzato GxP sia validato, che i dati siano integri e che le modifiche siano tracciate con audit trail. In ambito database, questo si traduce in controllo delle versioni degli schemi, log immutabili e procedure di backup verificate periodicamente.

## Impatto operativo sul change control

Qualsiasi modifica a un sistema GxP — aggiornamento del DBMS, migrazione di schema, cambio di parametri di configurazione — deve seguire un processo formale di change control:

1. **Impact Assessment**: valutazione del rischio sulla validazione esistente.
2. **Test documentati**: IQ (Installation Qualification), OQ (Operational Qualification), PQ (Performance Qualification).
3. **Approvazione della Qualità**: firma formale prima del rilascio in produzione.

Un lift-and-shift di un database Oracle verso cloud, per esempio, non è mai trasparente in ambiente GxP: cambia l'infrastruttura sottostante, e questo riapre il ciclo di validazione. I tempi di change control — spesso 4-12 settimane — sono il costo nascosto che i piani di migrazione tendono a sottostimare.

## Quando il DBA diventa parte del processo regolatorio

In ambienti GxP il DBA non gestisce solo performance e disponibilità: è un attore del sistema qualità. Le DDL eseguite in produzione devono essere pre-approvate, i backup devono essere testati con frequenza documentata, e ogni anomalia deve generare una deviation report. La latenza WAN o un failover non pianificato non sono solo incidenti tecnici — possono essere eventi regolatori che richiedono indagine formale.
