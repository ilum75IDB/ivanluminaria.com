---
title: "Hash Join"
description: "Hash Join — estrategia de join optimizada para grandes volumenes de datos, basada en una hash table construida en memoria."
translationKey: "glossary_hash_join"
aka: "Hash Join"
articles:
  - "/posts/postgresql/explain-analyze-postgresql"
---

**Hash join** es una estrategia de join disenada para grandes volumenes de datos. Funciona en dos fases: primero construye una estructura de datos en memoria, luego la usa para encontrar las correspondencias de forma eficiente.

## Como funciona

La base de datos lee la tabla mas pequena (build side) y construye una hash table en memoria, indexando las filas por la columna de join. Luego escanea la tabla mas grande (probe side) y para cada fila busca la correspondencia en la hash table con un lookup O(1).

La complejidad es lineal — proporcional a la suma de las filas de ambas tablas, no al producto como en el nested loop. No se necesitan indices: la hash table sustituye temporalmente al indice.

## Cuando es la eleccion correcta

El optimizer elige hash join cuando ambas tablas son grandes y no hay indices utiles, o cuando las estadisticas indican que el numero de filas a combinar es demasiado alto para un nested loop eficiente. Es una de las estrategias mas comunes en data warehouses y reportes que agregan millones de filas.

## Que puede salir mal

El punto debil es la memoria. La hash table debe caber en `work_mem`: si la tabla mas pequena no cabe, la base de datos escribe lotes en disco (batched hash join), con una degradacion significativa del rendimiento.

- **work_mem demasiado bajo**: la hash table se divide en lotes en disco, multiplicando el I/O
- **Estimaciones erroneas**: el optimizer elige como build side la tabla equivocada porque las estadisticas indican menos filas de las reales
- **Skew en los datos**: si un valor en la columna de join domina la mayoria de las filas, un bucket de la hash table se vuelve enorme mientras los demas quedan vacios
