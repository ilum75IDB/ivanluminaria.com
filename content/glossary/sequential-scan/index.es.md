---
title: "Sequential Scan"
description: "Operación de lectura donde PostgreSQL lee todos los bloques de una tabla sin usar índices, eficiente en tablas pequeñas pero problemática en tablas grandes."
translationKey: "glossary_sequential-scan"
aka: "Seq Scan / Full Table Scan"
articles:
  - "/posts/postgresql/pg-stat-statements"
---

El **Sequential Scan** (Seq Scan) es la operación con la que PostgreSQL lee una tabla de principio a fin, bloque por bloque, sin utilizar ningún índice. Es el equivalente en PostgreSQL del Full Table Scan de Oracle.

## Cuándo es normal

En tablas pequeñas (unos pocos miles de filas), el sequential scan suele ser la opción más eficiente. Leer una tabla entera en secuencia es más rápido que hacer lookups en un índice cuando la tabla cabe en pocas páginas. El optimizer elige el sequential scan cuando estima que es más económico que un index scan.

## Cuándo es un problema

En tablas grandes (millones de filas), un sequential scan para devolver pocas filas es una señal de alarma. Significa que falta un índice apropiado o que las estadísticas de la tabla están obsoletas y el optimizer hace estimaciones erróneas. pg_stat_statements ayuda a identificar estas situaciones mostrando las queries con peor ratio bloques leídos / filas devueltas.

## Cómo diagnosticarlo

EXPLAIN muestra "Seq Scan on tabla" en el plan de ejecución. Si el filtro posterior descarta la mayoría de las filas (rows removed by filter >> rows), casi con certeza se necesita un índice en la columna del filtro.
