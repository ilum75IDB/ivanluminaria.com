---
title: "Query Rewriting"
description: "Funcionalidad de Oracle que redirige automáticamente consultas sobre tablas base hacia una Materialized View equivalente, sin modificar el código de la aplicación."
translationKey: "glossary_query_rewriting"
aka: "Automatic Query Rewriting"
articles:
  - "/posts/data-warehouse/la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto"
---

El Query Rewriting es una capacidad del optimizador de consultas de Oracle que intercepta sentencias SQL dirigidas a tablas base y las redirige de forma transparente hacia una Materialized View (MV) que ya contiene el resultado pre-calculado. La aplicación no percibe ningún cambio: envía la misma consulta de siempre y recibe los datos con mayor rapidez.

## Cómo funciona

Cuando se crea o modifica una MV con `ENABLE QUERY REWRITE`, se autoriza al optimizador a utilizarla como fuente alternativa. Oracle verifica que la MV sea semánticamente equivalente a la consulta entrante — mismas agregaciones, mismas columnas, misma lógica de filtrado — y, si la correspondencia es válida, sustituye el plan de ejecución.

```sql
CREATE MATERIALIZED VIEW mv_trafico_diario
BUILD IMMEDIATE
REFRESH COMPLETE ON DEMAND
ENABLE QUERY REWRITE
AS
SELECT fecha_llamada, id_celda, SUM(duracion_seg) AS total_duracion
FROM hecho_llamadas
GROUP BY fecha_llamada, id_celda;
```

Tras esta definición, una consulta como `SELECT fecha_llamada, SUM(duracion_seg) FROM hecho_llamadas GROUP BY fecha_llamada` puede resolverse leyendo la MV en lugar de la tabla base, siempre que el optimizador lo considere conveniente.

## Cuándo se usa

El Query Rewriting resulta más útil en Data Warehouses con consultas analíticas pesadas y repetitivas sobre las mismas agregaciones. El requisito fundamental es que la MV esté **actualizada**: si los datos están desactualizados respecto a la tabla base, Oracle puede optar por no utilizarla — comportamiento controlable mediante el parámetro `QUERY_REWRITE_INTEGRITY`. También debe estar habilitado el parámetro de sesión o sistema `QUERY_REWRITE_ENABLED`. En entornos con refrescos frecuentes o near-real-time, el beneficio se reduce y es necesario equilibrar el coste del refresco con la ganancia en tiempo de lectura.
