---
title: "Materialized View (MV)"
description: "Vista pre-calculada y almacenada físicamente en disco: las consultas leen datos ya agregados sin recalcular. Compatible con Oracle, PostgreSQL, SQL Server."
translationKey: "glossary_materialized_view"
aka: "Vista materializada"
articles:
  - "/posts/data-warehouse/la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto"
---

Una Materialized View (MV) es una vista cuyo resultado se calcula una vez y se almacena físicamente en disco, a diferencia de una vista ordinaria que re-ejecuta su consulta en cada acceso. Las lecturas posteriores encuentran los datos ya disponibles: sin JOINs ni agregaciones que recalcular en tiempo de ejecución.

## Cómo funciona

La MV se crea con una consulta de definición; el motor ejecuta esa consulta y persiste su resultado como si fuera una tabla. La actualización se realiza mediante un **refresh**: completo (`COMPLETE`) o incremental (`FAST`/`INCREMENTAL`), según el RDBMS y la estructura de la consulta.

```sql
-- PostgreSQL
CREATE MATERIALIZED VIEW mv_revenue_daily AS
SELECT
    date_trunc('day', event_ts) AS day,
    customer_id,
    SUM(amount)                 AS total_revenue
FROM fact_events
GROUP BY 1, 2;

-- Refresh manual
REFRESH MATERIALIZED VIEW mv_revenue_daily;
```

En Oracle, el refresh puede programarse y admite el modo `FAST` mediante materialized view logs. En SQL Server, la construcción equivalente es una **Indexed View**.

## Cuándo se usa

Las MV son la herramienta adecuada cuando:

- la consulta subyacente es costosa (agregaciones sobre miles de millones de filas, JOINs multi-tabla) y los datos cambian con poca frecuencia o de forma predecible;
- se quiere separar la carga OLTP de la carga analítica sin duplicar todo el pipeline;
- un Data Warehouse o Data Mart necesita capas pre-agregadas para dashboards e informes.

El principal trade-off es la **latencia de los datos**: entre un refresh y el siguiente, la MV puede quedar desactualizada. En contextos donde la frescura es crítica (near-real-time), conviene evaluar si los refreshes frecuentes no anulan la ventaja de rendimiento.
