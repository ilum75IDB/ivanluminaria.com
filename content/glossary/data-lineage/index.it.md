---
title: "Data Lineage"
description: "Data Lineage: tracciare il percorso di un dato dalla sorgente alla destinazione, attraverso trasformazioni e sistemi intermedi, per audit e troubleshooting."
translationKey: "glossary_data_lineage"
aka: "Data Provenance, Data Traceability"
articles:
  - "/posts/data-warehouse/data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati"
---

Il Data Lineage è la capacità di ricostruire il percorso completo di un dato: da dove nasce, attraverso quali sistemi transita, quali trasformazioni subisce e dove arriva. In un data warehouse moderno, dove i dati attraversano pipeline ETL/ELT, staging layer e mart dimensionali, questa tracciabilità non è opzionale.

## Come funziona

Il lineage può essere catturato a due livelli:

- **Column-level lineage**: traccia ogni singola colonna attraverso le trasformazioni SQL. Strumenti come dbt espongono questo livello nativamente tramite il grafo di dipendenze.
- **Table-level lineage**: mappa le dipendenze tra tabelle/dataset, sufficiente per impact analysis e documentazione.

Un esempio concreto con dbt: ogni model `.sql` genera automaticamente metadati di lineage consultabili via `dbt docs generate`. A livello di piattaforma, Apache Atlas e OpenLineage (standard aperto) permettono di aggregare lineage da sorgenti eterogenee.

```sql
-- dbt model: marts/finance/revenue.sql
-- Il lineage traccia automaticamente la dipendenza da staging.orders e staging.payments
SELECT
  o.order_id,
  p.amount AS revenue
FROM {{ ref('stg_orders') }} o
JOIN {{ ref('stg_payments') }} p ON o.order_id = p.order_id
```

## Quando si usa

Tre scenari principali giustificano l'investimento in Data Lineage:

1. **Audit regolatori** (GDPR, SOX, DORA): dimostrare l'origine e le trasformazioni di dati sensibili o finanziari richiede lineage documentato e verificabile.
2. **Troubleshooting**: un KPI errato in un report si risale a monte — quale trasformazione ha introdotto il problema, quale tabella sorgente era corrotta.
3. **Impact analysis**: prima di modificare una tabella sorgente, sapere quanti downstream model ne dipendono evita regressioni silenziose.

Il costo di implementazione scala con la granularità: il lineage a livello di colonna richiede strumenti dedicati o piattaforme che lo supportano nativamente.
