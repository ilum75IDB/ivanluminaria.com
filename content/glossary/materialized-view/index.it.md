---
title: "Materialized View (MV)"
description: "Vista pre-calcolata e memorizzata fisicamente su disco: le query leggono dati già aggregati senza ricalcolare. Supportata da Oracle, PostgreSQL, SQL Server."
translationKey: "glossary_materialized_view"
aka: "Vista materializzata"
articles:
  - "/posts/data-warehouse/la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto"
---

Una Materialized View (MV) è una vista il cui risultato viene calcolato una volta e salvato fisicamente su disco, a differenza di una view ordinaria che riesegue la query ad ogni accesso. Le letture successive trovano dati già pronti: nessun JOIN, nessuna aggregazione da ricalcolare a runtime.

## Come funziona

La MV viene creata con una query di definizione; il motore esegue quella query e ne persiste il risultato come se fosse una tabella. L'aggiornamento avviene tramite **refresh**: completo (`COMPLETE`) o incrementale (`FAST`/`INCREMENTAL`) a seconda del RDBMS e della struttura della query.

```sql
-- PostgreSQL
CREATE MATERIALIZED VIEW mv_revenue_daily AS
SELECT
    date_trunc('day', event_ts) AS day,
    customer_id,
    SUM(amount)                 AS total_revenue
FROM fact_events
GROUP BY 1, 2;

-- Refresh manuale
REFRESH MATERIALIZED VIEW mv_revenue_daily;
```

In Oracle il refresh può essere schedulato e supporta la modalità `FAST` tramite materialized view log. In SQL Server la struttura equivalente è l'**Indexed View**.

## Quando si usa

Le MV sono lo strumento giusto quando:

- la query sottostante è costosa (aggregazioni su miliardi di righe, JOIN multi-tabella) e i dati cambiano con frequenza bassa o prevedibile;
- si vuole separare il carico OLTP dal carico analitico senza replicare l'intera pipeline;
- un Data Warehouse o Data Mart richiede layer pre-aggregati per dashboard e report.

Il trade-off principale è la **latenza dei dati**: tra un refresh e il successivo la MV può essere stale. Nei contesti dove la freschezza è critica (near-real-time), valutare se il refresh frequente non annulli il vantaggio di performance.
