---
title: "RTO"
description: "Recovery Time Objective — il tempo massimo accettabile per ripristinare un servizio dopo un guasto o un disastro."
translationKey: "glossary_rto"
aka: "Recovery Time Objective"
articles:
  - "/posts/oracle/oracle-data-guard"
---

**RTO** (Recovery Time Objective) è il tempo massimo accettabile per ripristinare il servizio dopo un guasto o un disastro. Si misura dal momento del guasto al momento in cui il sistema torna operativo.

## Come si determina

L'RTO dipende dalla strategia di recovery e dall'infrastruttura disponibile:

| Strategia | RTO tipico |
|-----------|-----------|
| Restore da backup su nastro | 4-12 ore |
| Restore da backup su disco | 1-4 ore |
| Data Guard con switchover manuale | 1-5 minuti |
| Data Guard con Fast-Start Failover | 10-30 secondi |

## RTO vs RPO

- **RTO**: quanto tempo ci vuole per ripartire (guarda avanti)
- **RPO**: quanti dati puoi perdere (guarda indietro)

Sono metriche indipendenti. Un restore da backup può avere RTO=2 ore e RPO=24 ore. Un Data Guard sincrono può avere RTO=30 secondi e RPO=0.

## L'impatto sul business

L'RTO ha un impatto diretto e misurabile: ogni minuto di fermo si traduce in operazioni bloccate, clienti non serviti, ricavi persi. La differenza tra RTO=6 ore e RTO=42 secondi — come nel caso del passaggio da single instance a Data Guard — può valere più del costo dell'intera infrastruttura.
