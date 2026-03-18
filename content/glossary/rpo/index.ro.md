---
title: "RPO"
description: "Recovery Point Objective — cantitatea maxima de date pe care o organizatie si-o poate permite sa piarda in caz de dezastru, masurata in timp."
translationKey: "glossary_rpo"
aka: "Recovery Point Objective"
articles:
  - "/posts/oracle/oracle-data-guard"
---

**RPO** (Recovery Point Objective) este cantitatea maxima de date pe care o organizatie si-o poate permite sa piarda in caz de defectiune sau dezastru. Se masoara in timp: un RPO de 1 ora inseamna acceptarea pierderii a cel mult ultimei ore de tranzactii.

## Cum se determina

RPO-ul depinde de strategia de backup si replicare:

| Strategie | RPO tipic |
|-----------|----------|
| Backup nocturn pe banda | 12-24 ore |
| Backup + archived log-uri pe storage remote | 1-4 ore |
| Data Guard asincron (MaxPerformance) | Cateva secunde |
| Data Guard sincron (MaxAvailability) | Zero |

## RPO vs RTO

RPO si RTO sunt complementare dar distincte:

- **RPO**: cate date poti pierde (priveste inapoi in timp)
- **RTO**: cat timp dureaza restaurarea serviciului (priveste inainte in timp)

O organizatie poate avea RPO=0 (zero pierderi de date) dar RTO=4 ore (dureaza 4 ore sa reporneasca), sau invers.

## De ce conteaza

RPO-ul determina investitia necesara in infrastructura de replicare. Trecerea de la RPO=24 ore la RPO=0 poate costa cu ordine de marime mai mult, dar costul trebuie comparat cu valoarea datelor pierdute — ca in cazul a sase ore de polite de asigurare neemise.
