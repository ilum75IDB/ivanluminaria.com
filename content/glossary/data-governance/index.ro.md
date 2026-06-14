---
title: "Data Governance"
description: "Cadru operațional continuu de procese, politici și standarde care asigură calitatea, integritatea, securitatea și conformitatea normativă a datelor organizației."
translationKey: "glossary_data_governance"
aka: "Guvernanța datelor"
articles:
  - "/posts/data-warehouse/data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati"
---

Data Governance reprezintă ansamblul structurat de procese, politici, standarde și metrici care reglementează modul în care o organizație își gestionează activele de date. Nu este un proiect cu o dată de finalizare — este un framework operațional continuu care acoperă oameni, tehnologie și procese.

## Cum funcționează

Un program de Data Governance stabilește proprietatea datelor (cine răspunde de fiecare set de date), scheme de clasificare, reguli de calitate și controale de acces. Instrumentele operaționale includ de obicei un data catalog, trasabilitatea datelor (data lineage), politici de retenție și verificări automate de calitate integrate în pipeline-urile ETL/ELT.

În contextul unui Data Warehouse, governance se aplică la fiecare nivel: de la staging zone până la mart-urile expuse utilizatorilor finali. Un control tipic de calitate poate respinge înregistrările cu valori nule pe coloane critice sau poate genera alerte când distribuțiile statistice ale KPI-urilor depășesc pragurile definite.

## Context operațional

Data Governance devine obligatorie când intră în vigoare reglementări precum GDPR, HIPAA sau PCI-DSS: trasabilitatea completă a cine a creat, modificat sau consumat un datum trebuie demonstrată în cadrul unui audit. Gestionarea datoriei de calitate a datelor este la fel de importantă: fără governance, problemele de calitate se acumulează silențios până când compromit decizii critice de business.

Principalul trade-off este între rigoare și viteză: procesele de governance prea greoaie încetinesc echipele de inginerie. Abordarea practică constă în calibrarea controalelor în funcție de profilul real de risc al fiecărui dataset, nu în aplicarea aceluiași nivel de scrutin pentru fiecare tabel.
