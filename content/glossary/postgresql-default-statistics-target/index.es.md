---
title: "default_statistics_target"
description: "El parametro PostgreSQL que controla la granularidad de las estadisticas recogidas por ANALYZE (tamano de MCV e histograma)."
translationKey: "glossary_postgresql_default_statistics_target"
aka: "default_statistics_target (PostgreSQL)"
articles:
  - "/posts/postgresql/explain-analyze-postgresql"
---

**default_statistics_target** es el parametro PostgreSQL que controla la **granularidad de las estadisticas** que `ANALYZE` construye para cada columna. El valor por defecto es 100.

## Como funciona

ANALYZE construye para cada columna dos estructuras estadisticas usadas por el optimizer:

- **Most common values (MCV)**: la lista de los valores mas frecuentes, con sus respectivas frecuencias
- **Histograma**: la distribucion de los valores restantes, dividida en buckets de igual poblacion

`default_statistics_target` determina cuantos elementos pueden tener estas estructuras. Con valor `100`: hasta 100 valores en la lista MCV y hasta 100 buckets en el histograma.

**El numero de filas muestreadas es algo separado y depende del target**: vale aproximadamente `300 × default_statistics_target`. Con el default de 100, ANALYZE lee ~30.000 filas por columna; con un target de 500, ~150.000. Asi que subir el target aumenta tanto la granularidad de las estadisticas **como** el costo de ANALYZE.

## Cuando aumentarlo

Para tablas pequenas o con distribucion uniforme, 100 muestras son suficientes. Para tablas grandes con distribucion asimetrica (skewed) — donde pocos valores dominan la mayoria de las filas — 100 muestras pueden dar una representacion distorsionada, llevando al optimizer a estimaciones de cardinalidad erroneas.

Se puede aumentar el target a nivel de columna individual:

    ALTER TABLE orders ALTER COLUMN status SET STATISTICS 500;
    ANALYZE orders;

Valores entre 500 y 1000 mejoran sensiblemente la calidad de las estimaciones en columnas con distribucion no uniforme.

## Limites practicos

Por encima de 1000 el beneficio es marginal y el `ANALYZE` mismo se vuelve mas lento, porque necesita muestrear mas filas y construir estructuras mas grandes. Es un ajuste fino: hay que aplicarlo solo a las columnas que efectivamente causan estimaciones erroneas, no a todas las columnas de todas las tablas.
