---
title: "Hash Join"
description: "Cómo funciona el hash join y por qué es la mejor opción para joins sobre grandes volúmenes de datos."
translationKey: "glossary_hash_join"
tags: ["glosario"]
---

El hash join es una estrategia de join diseñada para grandes volúmenes de datos. Funciona en dos fases: primero la base de datos lee la tabla más pequeña y construye una hash table en memoria, indexando las filas por la columna de join. Luego escanea la tabla más grande y para cada fila busca la correspondencia en la hash table con un lookup O(1).

La ventaja es que no se necesitan índices y la complejidad es lineal — proporcional a la suma de las filas de ambas tablas, no al producto como en el nested loop. La desventaja es que requiere memoria para la hash table: si la tabla más pequeña no cabe en `work_mem`, la base de datos debe escribir lotes en disco (batched hash join), ralentizando la operación.

El optimizer elige hash join cuando ambas tablas son grandes y no hay índices útiles, o cuando las estadísticas indican que el número de filas a combinar es demasiado alto para un nested loop eficiente. Es una de las estrategias más comunes en data warehouses y reportes que agregan millones de filas.

## Artículos relacionados

- [EXPLAIN ANALYZE no basta: cómo leer realmente un plan de ejecución en PostgreSQL](/es/posts/postgresql/explain-analyze-postgresql/)
