---
title: "RTO"
description: "Recovery Time Objective — timpul maxim acceptabil pentru restaurarea unui serviciu dupa o defectiune sau un dezastru."
translationKey: "glossary_rto"
aka: "Recovery Time Objective"
articles:
  - "/posts/oracle/oracle-data-guard"
---

**RTO** (Recovery Time Objective) este timpul maxim acceptabil pentru restaurarea serviciului dupa o defectiune sau un dezastru. Se masoara din momentul defectiunii pana in momentul in care sistemul redevine operational.

## Cum se determina

RTO-ul depinde de strategia de recuperare si de infrastructura disponibila:

| Strategie | RTO tipic |
|-----------|----------|
| Restore din backup pe banda | 4-12 ore |
| Restore din backup pe disc | 1-4 ore |
| Data Guard cu switchover manual | 1-5 minute |
| Data Guard cu Fast-Start Failover | 10-30 secunde |

## RTO vs RPO

- **RTO**: cat timp dureaza repornirea (priveste inainte)
- **RPO**: cate date poti pierde (priveste inapoi)

Sunt metrici independente. Un restore din backup poate avea RTO=2 ore si RPO=24 ore. Un Data Guard sincron poate avea RTO=30 secunde si RPO=0.

## Impactul asupra business-ului

RTO-ul are un impact direct si masurabil: fiecare minut de oprire se traduce in operatiuni blocate, clienti nedeserviti, venituri pierdute. Diferenta intre RTO=6 ore si RTO=42 secunde — ca in cazul trecerii de la single instance la Data Guard — poate valora mai mult decat costul intregii infrastructuri.
