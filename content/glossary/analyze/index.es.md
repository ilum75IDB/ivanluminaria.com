---
title: "ANALYZE"
description: "El comando PostgreSQL que actualiza las estadísticas de las tablas utilizadas por el optimizer para elegir el plan de ejecución."
translationKey: "glossary_analyze"
tags: ["glosario"]
---

`ANALYZE` es el comando PostgreSQL que recopila estadísticas sobre la distribución de los datos en las tablas y las almacena en el catálogo `pg_statistic` (legible a través de la vista `pg_stats`). El optimizer usa estas estadísticas para estimar la cardinalidad — cuántas filas devolverá cada operación — y elegir el plan de ejecución más eficiente.

Las estadísticas recopiladas incluyen: valores más frecuentes (most common values), histogramas de distribución, número de valores distintos y porcentaje de NULL por cada columna. Sin estadísticas actualizadas, el optimizer se ve obligado a adivinar, y las estimaciones erróneas llevan a planes de ejecución desastrosos — como elegir un nested loop sobre millones de filas pensando que son cientos.

PostgreSQL ejecuta ANALYZE automáticamente a través del autovacuum, pero el umbral por defecto (50 filas + 10% de las filas vivas) puede ser demasiado alto para tablas que crecen rápidamente. Después de importaciones masivas o cambios significativos en la distribución de los datos, un ANALYZE manual es la primera acción diagnóstica a realizar.

## Artículos relacionados

- [EXPLAIN ANALYZE no basta: cómo leer realmente un plan de ejecución en PostgreSQL](/es/posts/postgresql/explain-analyze-postgresql/)
