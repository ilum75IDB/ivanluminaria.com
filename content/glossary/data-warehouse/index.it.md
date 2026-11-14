---
title: "Data Warehouse (DWH)"
description: "Sistema di database ottimizzato per l'analisi dei dati storici, che aggrega informazioni da sorgenti operative eterogenee privilegiando letture massive e aggregazioni."
translationKey: "glossary_data_warehouse"
aka: "DWH, Enterprise Data Warehouse (EDW)"
articles:
  - "/posts/data-warehouse/la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto"
---

Un Data Warehouse è un sistema di archiviazione progettato per consolidare dati provenienti da sorgenti operative diverse — CRM, ERP, sistemi di billing, log applicativi — in un unico repository ottimizzato per l'analisi. Non sostituisce i database transazionali: li affianca, leggendo da essi tramite pipeline ETL o ELT.

## Come funziona

Il modello di accesso è opposto a quello OLTP: poche scritture massive (batch o micro-batch), moltissime letture che attraversano milioni di righe. Lo schema è tipicamente denormalizzato — star schema o snowflake schema — per ridurre i JOIN e massimizzare le performance delle query analitiche.

```sql
-- Esempio di query analitica tipica su un DWH telco
SELECT
    d.mese,
    r.regione,
    SUM(f.ricavi_euro)   AS ricavi_totali,
    COUNT(f.cliente_id)  AS clienti_attivi
FROM fact_ricavi f
JOIN dim_data     d ON f.data_id    = d.data_id
JOIN dim_regione  r ON f.regione_id = r.regione_id
WHERE d.anno = 2024
GROUP BY d.mese, r.regione
ORDER BY d.mese, ricavi_totali DESC;
```

Le materialized view sono uno strumento comune per pre-calcolare aggregazioni costose e renderle disponibili con latenza minima.

## Quando si usa

Un DWH è la scelta corretta quando il carico analitico inizia a degradare le performance dei sistemi operativi, quando serve storicizzare dati che i sistemi sorgente non conservano, o quando più sorgenti eterogenee devono essere interrogate in modo unificato. Non è adatto a scenari che richiedono dati in real-time con latenza inferiore al secondo: in quel caso si valutano architetture lambda o kappa con layer di streaming.

## Note

La distinzione tra DWH e Data Lake riguarda principalmente la struttura: il DWH impone uno schema rigido (schema-on-write), il Data Lake accetta dati grezzi e applica lo schema alla lettura (schema-on-read). Molte architetture moderne combinano entrambi nel pattern detto Data Lakehouse.
