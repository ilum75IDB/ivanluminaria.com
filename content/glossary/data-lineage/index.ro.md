---
title: "Data Lineage"
description: "Data Lineage: urmărirea traseului complet al unei date de la sursă prin transformări până la destinație, esențial pentru audit, troubleshooting și impact analysis."
translationKey: "glossary_data_lineage"
aka: "Data Provenance, Trasabilitatea Datelor"
articles:
  - "/posts/data-warehouse/data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati"
---

Data Lineage reprezintă capacitatea de a reconstitui traseul complet al unei date: de unde provine, prin ce sisteme trece, ce transformări suferă și unde ajunge. Într-un data warehouse modern, unde datele parcurg pipeline-uri ETL/ELT, staging layer-e și marts dimensionale, această trasabilitate este o cerință operațională, nu un element opțional.

## Cum funcționează

Lineage-ul se capturează la două niveluri de granularitate:

- **Column-level lineage**: urmărește fiecare coloană individuală prin transformările SQL. Instrumente precum dbt expun acest nivel nativ prin graful de dependențe.
- **Table-level lineage**: mapează dependențele dintre tabele sau dataset-uri, suficient pentru impact analysis și documentație.

Cu dbt, fiecare model `.sql` generează automat metadate de lineage accesibile prin `dbt docs generate`. La nivel de platformă, Apache Atlas și OpenLineage (standard deschis) permit agregarea lineage-ului din surse eterogene.

```sql
-- dbt model: marts/finance/revenue.sql
-- Lineage-ul urmărește automat dependența față de staging.orders și staging.payments
SELECT
  o.order_id,
  p.amount AS revenue
FROM {{ ref('stg_orders') }} o
JOIN {{ ref('stg_payments') }} p ON o.order_id = p.order_id
```

## Când se folosește

Trei scenarii justifică investiția în Data Lineage:

1. **Audit de reglementare** (GDPR, SOX, DORA): demonstrarea originii și a transformărilor datelor sensibile sau financiare necesită un lineage documentat și verificabil.
2. **Troubleshooting**: un KPI incorect într-un raport poate fi urmărit în amonte — ce transformare a introdus eroarea, ce tabel sursă era corupt.
3. **Impact analysis**: înainte de a modifica un tabel sursă, cunoașterea numărului de modele downstream care depind de acesta previne regresiile silențioase.

Costul de implementare crește odată cu granularitatea: lineage-ul la nivel de coloană necesită instrumente dedicate sau platforme care îl suportă nativ.
