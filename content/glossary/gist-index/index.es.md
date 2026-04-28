---
title: "GiST Index"
description: "Generalized Search Tree — familia de índices PostgreSQL para datos con estructura geométrica, de rangos o de similitud, indispensable para consultas espaciales y de intervalos."
translationKey: "glossary_gist_index"
aka: "Generalized Search Tree"
articles:
  - "/posts/postgresql/postgresql-indici-quando-fanno-male"
---

**GiST** (*Generalized Search Tree*) es una familia de índices PostgreSQL pensada para datos que no se pueden ordenar linealmente: geometrías, rangos, vectores de similitud, full-text. Es un árbol equilibrado que organiza los datos por *bounding boxes* jerárquicos en lugar de ordenamiento lexicográfico.

## Cómo funciona

Mientras un B-tree ordena los valores de "mínimo" a "máximo" y hace búsqueda dicotómica, GiST agrupa los datos en regiones (bounding boxes) anidadas. Cada nodo del árbol representa una región que contiene todos los datos de sus hijos. Cuando se busca un valor, GiST descarta regiones enteras con una comparación de solapamiento — sin bajar a los nodos que no pueden contener el resultado.

Esta estructura permite indexar:

- **Geometrías**: puntos, polígonos, líneas (con PostGIS)
- **Rangos**: `int4range`, `tsrange`, `daterange` y otros tipos rango
- **Full-text**: vectores `tsvector` para búsqueda textual
- **Similitud**: con extensiones como `pg_trgm` para búsquedas aproximadas

## Para qué sirve

Resuelve consultas "espaciales" o de intervalos que un B-tree no sabe gestionar:

- Encontrar todos los puntos dentro de un rectángulo o radio
- Encontrar todos los registros con un rango que se solapa con otro rango
- Encontrar textos similares a una consulta, incluso con erratas
- Buscar por containment: `range1 @> range2` o `geom1 && geom2`

## Cuándo se usa

Se usa con `CREATE INDEX ... USING GIST (columna)`. Es el complemento natural de GIN: GIN para containment de arrays/JSONB, GiST para geometría/rangos/similitud. En tablas con mucho churn tiene un coste de escritura similar a GIN — así que debe evaluarse caso por caso.
