---
title: "ZDM"
description: "Zero Downtime Migration — instrument Oracle pentru automatizarea migrarilor catre OCI, combinand Data Guard si Data Pump sub un strat de orchestrare."
translationKey: "glossary_zdm"
aka: "Zero Downtime Migration"
articles:
  - "/posts/oracle/oracle-cloud-migration"
---

**ZDM** (Zero Downtime Migration) este instrumentul pe care Oracle il pune la dispozitie pentru automatizarea migrarilor bazelor de date Oracle catre OCI (Oracle Cloud Infrastructure) sau catre baze de date on-premises de versiune superioara. Numele este putin optimist — downtime-ul nu este zero, dar este redus la minim.

## Cum functioneaza

ZDM este in esenta un orchestrator care combina tehnologii Oracle existente intr-un flux automatizat unic. Suporta doua moduri:

- **Migrare fizica** (bazata pe Data Guard): creeaza un standby al bazei de date sursa pe destinatie, il sincronizeaza prin redo transport, apoi executa un switchover. Downtime de ordinul minutelor.
- **Migrare logica** (bazata pe Data Pump): executa export si import logic cu sincronizare incrementala prin GoldenGate sau Data Pump. Mai flexibil dar mai lent.

## Cand sa il folosesti

ZDM este indicat pentru migrari standard unde infrastructura sursa si destinatie sunt configurate conventional. Avantajul este automatizarea: reduce posibilitatea erorii umane in pasii repetitivi.

## Cand sa nu il folosesti

Pentru configuratii complexe — RAC cu DB link-uri cross-engine, dependente externe non-standard, proceduri PL/SQL cu apeluri HTTP — stratul de automatizare al ZDM poate deveni un obstacol. In aceste cazuri, configurarea manuala a Data Guard ofera mai mult control asupra detaliilor si secventei operatiilor.

## Cerinte

ZDM necesita un host dedicat ("ZDM service host") cu acces SSH atat la baza de date sursa cat si la destinatie. Sursa trebuie sa fie Oracle 11.2.0.4 sau superior, iar destinatia poate fi pe OCI sau on-premises.
