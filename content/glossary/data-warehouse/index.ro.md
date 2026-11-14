---
title: "Data Warehouse (DWH)"
description: "Sistem de baze de date optimizat pentru analiza datelor istorice, care agregă informații din surse operaționale eterogene, prioritizând citirile masive și agregările."
translationKey: "glossary_data_warehouse"
aka: "DWH, Enterprise Data Warehouse (EDW)"
articles:
  - "/posts/data-warehouse/la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto"
---

Un Data Warehouse este un sistem de stocare conceput pentru a consolida date provenite din surse operaționale multiple — CRM, ERP, sisteme de facturare, loguri aplicative — într-un singur depozit optimizat pentru analiză. Nu înlocuiește bazele de date tranzacționale: le completează, citind din ele prin pipeline-uri ETL sau ELT.

## Cum funcționează

Modelul de acces este opus celui OLTP: puține scrieri masive (batch sau micro-batch) și un volum foarte mare de citiri care parcurg milioane de rânduri. Schema este tipic denormalizată — star schema sau snowflake schema — pentru a minimiza operațiunile JOIN și a maximiza performanța interogărilor analitice.

```sql
-- Interogare analitică tipică pe un DWH telco
SELECT
    d.luna,
    r.regiune,
    SUM(f.venituri_eur)  AS venituri_totale,
    COUNT(f.client_id)   AS clienti_activi
FROM fact_venituri f
JOIN dim_data    d ON f.data_id    = d.data_id
JOIN dim_regiune r ON f.regiune_id = r.regiune_id
WHERE d.an = 2024
GROUP BY d.luna, r.regiune
ORDER BY d.luna, venituri_totale DESC;
```

Materialized view-urile sunt un instrument frecvent utilizat pentru pre-calcularea agregărilor costisitoare și servirea lor cu latență minimă.

## Când se utilizează

Un DWH este alegerea potrivită atunci când sarcina analitică începe să degradeze performanța sistemelor operaționale, când este necesară istoricizarea datelor pe care sistemele sursă nu le păstrează, sau când mai multe surse eterogene trebuie interogate în mod unificat. Nu este potrivit pentru scenarii care necesită date în timp real cu latență sub o secundă: în acele cazuri se evaluează arhitecturi lambda sau kappa cu un strat de streaming.

## Note

Distincția dintre un DWH și un Data Lake privește în principal structura: DWH-ul impune o schemă rigidă la momentul scrierii (schema-on-write), în timp ce Data Lake-ul acceptă date brute și aplică schema la citire (schema-on-read). Multe arhitecturi moderne combină ambele abordări în pattern-ul cunoscut sub numele de Data Lakehouse.
