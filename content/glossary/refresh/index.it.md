---
title: "Refresh (MV)"
description: "Aggiornamento dei dati di una Materialized View: completo (COMPLETE) o incrementale (FAST) tramite MV log. Impatto diretto su performance e freschezza dei dati."
translationKey: "glossary_refresh"
aka: "Materialized View Refresh"
articles:
  - "/posts/data-warehouse/la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto"
---

Il Refresh è l'operazione che sincronizza i dati di una Materialized View con le tabelle base da cui è derivata. Senza refresh, la MV è uno snapshot statico: utile per le query, ma progressivamente disallineato rispetto alla realtà del dato sorgente.

## Modalità di refresh

Esistono due modalità principali:

- **COMPLETE**: ricalcola l'intera MV da zero. Semplice da gestire, costoso su volumi grandi.
- **FAST**: applica solo le variazioni tracciate in un MV log (struttura di change tracking creata sulla tabella base). Richiede la presenza del log e vincoli sulla query della MV.

```sql
-- Refresh completo (Oracle)
EXEC DBMS_MVIEW.REFRESH('MV_REVENUE_DAILY', method => 'C');

-- Refresh incrementale (richiede MV log sulla tabella base)
EXEC DBMS_MVIEW.REFRESH('MV_REVENUE_DAILY', method => 'F');
```

Su PostgreSQL il refresh è sempre COMPLETE (`REFRESH MATERIALIZED VIEW`), con l'opzione `CONCURRENTLY` per non bloccare le letture durante l'operazione.

## Quando scegliere l'una o l'altra

Il FAST refresh riduce il tempo di aggiornamento ma introduce complessità: il MV log consuma spazio, va mantenuto, e non tutte le query sono compatibili (aggregazioni complesse, `DISTINCT`, subquery correlate spesso escludono il FAST). Il COMPLETE è sempre applicabile ma scala male su tabelle da milioni di righe.

La frequenza è altrettanto critica: un refresh on-demand su richiesta utente, uno schedulato ogni ora, o un refresh automatico al COMMIT (`ON COMMIT`) hanno impatti radicalmente diversi su throughput e latenza delle transazioni base.
