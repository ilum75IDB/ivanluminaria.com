---
title: "BYOL"
description: "Bring Your Own License — program Oracle care permite reutilizarea licentelor on-premises in cloud-ul OCI fara costuri suplimentare de licentiere."
translationKey: "glossary_byol"
aka: "Bring Your Own License"
articles:
  - "/posts/oracle/oracle-cloud-migration"
---

**BYOL** (Bring Your Own License) este un program Oracle care permite organizatiilor sa transfere licentele software achizitionate pentru infrastructura on-premises catre Oracle Cloud Infrastructure (OCI), fara a fi nevoie sa achizitioneze licente cloud noi.

## Cum functioneaza

Cand o organizatie detine deja licente Oracle — de obicei Enterprise Edition cu optiuni precum RAC, Data Guard sau Partitioning — le poate "lua cu sine" in migrarea catre OCI. Contractul de suport (Software Update License & Support) se mentine, iar licentele sunt asociate resurselor cloud in locul serverelor fizice.

Pe OCI, fiecare OCPU corespunde unei processor license, cu un raport 1:1 transparent. Acest lucru face calculul predictibil si conform cu politicile de licentiere Oracle.

## De ce conteaza in migrari

BYOL este adesea factorul decisiv in alegerea OCI fata de alti furnizori cloud. Pe AWS sau Azure, Oracle aplica reguli de licentiere diferite: fiecare vCPU conteaza ca jumatate de procesor, iar optiuni precum RAC nu sunt suportate sau necesita licente suplimentare. Un audit Oracle pe un cloud non-OCI poate transforma o economie aparenta intr-un cost neprevazut foarte semnificativ.

## Ce acopera

- Oracle Database (toate editiile)
- Optiuni ale bazei de date (RAC, Data Guard, Partitioning, Advanced Compression, etc.)
- Oracle Middleware si alte produse Oracle cu licente eligibile

BYOL nu este automat: trebuie solicitat si configurat la momentul provizionarii resurselor OCI, specificand licentele existente in contract.
