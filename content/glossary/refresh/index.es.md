---
title: "Refresh (MV)"
description: "Actualización de una Materialized View: COMPLETE (recálculo total) o FAST (incremental mediante MV log). Decisión arquitectónica con impacto directo en rendimiento y frescura del dato."
translationKey: "glossary_refresh"
aka: "Materialized View Refresh"
articles:
  - "/posts/data-warehouse/la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto"
---

El Refresh es la operación que sincroniza los datos de una Materialized View con las tablas base de las que deriva. Sin él, la MV es un snapshot estático: eficiente para las consultas, pero progresivamente desalineado respecto al dato real.

## Modos de refresh

Existen dos modalidades principales:

- **COMPLETE**: recalcula toda la MV desde cero. Sencillo de gestionar, costoso en volúmenes grandes.
- **FAST**: aplica únicamente los cambios registrados en un MV log (estructura de seguimiento de cambios creada sobre la tabla base). Requiere la existencia del log y restringe las queries admisibles en la definición de la MV.

```sql
-- Refresh completo (Oracle)
EXEC DBMS_MVIEW.REFRESH('MV_REVENUE_DAILY', method => 'C');

-- Refresh incremental — requiere MV log en la tabla base
EXEC DBMS_MVIEW.REFRESH('MV_REVENUE_DAILY', method => 'F');
```

En PostgreSQL el refresh es siempre COMPLETE (`REFRESH MATERIALIZED VIEW`), con la opción `CONCURRENTLY` para no bloquear lecturas durante la operación.

## Cuándo usar cada modalidad

El FAST refresh reduce el tiempo de actualización pero introduce complejidad operativa: el MV log consume espacio, requiere mantenimiento y no es compatible con todas las queries — agregaciones complejas, `DISTINCT` o subconsultas correlacionadas suelen descartarlo. El COMPLETE es siempre aplicable, pero escala mal en tablas de millones de filas.

La frecuencia es igual de determinante: un refresh bajo demanda, uno programado cada hora o uno automático ON COMMIT tienen implicaciones radicalmente distintas sobre el throughput de las transacciones base y la latencia del dato.
