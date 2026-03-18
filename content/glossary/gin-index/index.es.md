---
title: "GIN Index"
description: "Generalized Inverted Index — tipo de índice PostgreSQL optimizado para búsqueda full-text, pattern matching con trigramas y queries sobre arrays y JSONB."
translationKey: "glossary_gin-index"
aka: "Generalized Inverted Index"
articles:
  - "/posts/postgresql/like-optimization-postgresql"
---

Un **GIN Index** (Generalized Inverted Index) es un tipo de índice PostgreSQL diseñado para indexar valores compuestos: arrays, documentos JSONB, texto con trigramas y búsquedas full-text. A diferencia del B-Tree, un GIN crea un mapping inverso: de cada elemento (palabra, trigrama, clave JSON) a los registros que lo contienen.

## Cómo funciona

Para cada valor distinto en el dato indexado, GIN mantiene una lista de punteros a las filas que contienen ese valor. En el caso de `pg_trgm`, el texto se descompone en trigramas (secuencias de 3 caracteres) y cada trigrama se indexa. Una búsqueda `LIKE '%ABC%'` se traduce en una intersección de trigramas, evitando el escaneo secuencial.

## Para qué sirve

GIN resuelve el problema de las búsquedas "contiene" (`LIKE '%valor%'`) en columnas de texto, que con un B-Tree requerirían un escaneo secuencial de toda la tabla. En tablas de millones de filas, la diferencia es entre segundos y milisegundos.

## Cuándo se usa

GIN es ideal en tablas append-only o con bajo churn (pocos UPDATE/DELETE), ya que el coste de mantenimiento del índice es más alto que el de un B-Tree. La creación en producción debe hacerse con `CREATE INDEX CONCURRENTLY` para evitar locks en las escrituras.
