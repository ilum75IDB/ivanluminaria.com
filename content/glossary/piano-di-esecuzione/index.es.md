---
title: "Plan de ejecución"
description: "Secuencia de operaciones elegida por el optimizador SQL para ejecutar una consulta: escaneos, joins, ordenaciones. Las estadísticas obsoletas lo degradan en silencio."
translationKey: "glossary_piano_di_esecuzione"
aka: "Query execution plan, Query plan"
articles:
  - "/posts/project-management/il-preventivo-dell-upgrade-e-la-domanda-che-non-e-istintiva"
---

El plan de ejecución es la receta que sigue el motor de base de datos para responder a una consulta SQL. El optimizador evalúa varias estrategias posibles — qué índices usar, en qué orden unir las tablas, si ordenar antes o después del join — y elige la de menor coste estimado. El resultado es un árbol de operadores que el motor ejecuta en secuencia.

## Cómo funciona

El optimizador se apoya en **estadísticas** (distribución de valores, cardinalidad de tablas, selectividad de índices) para estimar el coste de cada plan candidato. En PostgreSQL el punto de partida es `EXPLAIN` o `EXPLAIN ANALYZE`:

```sql
EXPLAIN ANALYZE
SELECT o.id, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'pending';
```

La salida muestra cada nodo (Seq Scan, Index Scan, Hash Join, Sort…), el coste estimado y — con `ANALYZE` — el tiempo real y las filas efectivamente procesadas. La diferencia entre filas estimadas y filas reales es la primera señal de estadísticas obsoletas.

## Cuándo se convierte en un problema

Un plan degradado aparece típicamente tras:

- **cargas masivas** que alteran la distribución de datos sin un `ANALYZE` posterior;
- **actualizaciones de versión** del motor, donde el optimizador cambia sus heurísticas;
- **crecimiento orgánico** de las tablas más allá de los umbrales para los que el plan fue calibrado.

El síntoma clásico es una consulta que funcionaba en milisegundos y de repente tarda decenas de segundos, sin ningún cambio en el código de aplicación. Añadir hardware no resuelve el problema: un Full Table Scan sobre 500 millones de filas es costoso independientemente de la RAM disponible. El remedio es actualizar las estadísticas (`ANALYZE`, `UPDATE STATISTICS`, `DBMS_STATS`) y verificar que el optimizador elija el plan esperado.
