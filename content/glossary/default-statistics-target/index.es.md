---
title: "default_statistics_target"
description: "El parámetro PostgreSQL que controla cuántas muestras recopila el optimizer para estimar la distribución de datos en una columna."
translationKey: "glossary_default_statistics_target"
tags: ["glosario"]
---

`default_statistics_target` es el parámetro PostgreSQL que define el número de muestras recopiladas por el comando ANALYZE para construir las estadísticas de cada columna. El valor por defecto es 100, lo que significa que PostgreSQL muestrea 100 valores para construir histogramas y listas de valores frecuentes.

Para tablas pequeñas o con distribución uniforme, 100 muestras son suficientes. Para tablas grandes con distribución asimétrica (skewed) — donde pocos valores dominan la mayoría de las filas — 100 muestras pueden dar una representación distorsionada, llevando al optimizer a estimaciones de cardinalidad erróneas.

Se puede aumentar el target a nivel de columna individual con `ALTER TABLE ... ALTER COLUMN ... SET STATISTICS N`. Valores entre 500 y 1000 mejoran sensiblemente la calidad de las estimaciones en columnas con distribución no uniforme. Por encima de 1000 el beneficio es marginal y el ANALYZE mismo se vuelve más lento. Es un ajuste fino que marca la diferencia en consultas con joins complejos sobre tablas con millones de filas.

## Artículos relacionados

- [EXPLAIN ANALYZE no basta: cómo leer realmente un plan de ejecución en PostgreSQL](/es/posts/postgresql/explain-analyze-postgresql/)
