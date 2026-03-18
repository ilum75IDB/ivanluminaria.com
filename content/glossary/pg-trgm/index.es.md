---
title: "pg_trgm"
description: "Extensión PostgreSQL que proporciona funciones y operadores para búsqueda de similitud basada en trigramas, habilitando índices GIN para LIKE con wildcards."
translationKey: "glossary_pg-trgm"
articles:
  - "/posts/postgresql/like-optimization-postgresql"
---

**pg_trgm** es una extensión de PostgreSQL que implementa la búsqueda basada en trigramas — secuencias de tres caracteres consecutivos extraídos del texto. Habilita el uso de índices GIN y GiST para acelerar búsquedas `LIKE '%valor%'` e `ILIKE`, que de otro modo requerirían escaneos secuenciales.

## Cómo funciona

La extensión descompone cada cadena en trigramas: por ejemplo, "hello" se convierte en {"  h", " he", "hel", "ell", "llo", "lo "}. Un índice GIN con operator class `gin_trgm_ops` indexa estos trigramas. Al ejecutar un `LIKE '%ell%'`, PostgreSQL busca los trigramas correspondientes en el índice en lugar de escanear toda la tabla.

## Para qué sirve

pg_trgm resuelve uno de los problemas más comunes en PostgreSQL: la búsqueda "contiene" en columnas de texto grandes. Sin pg_trgm, un `LIKE '%valor%'` en una tabla de millones de filas requiere un escaneo completo. Con pg_trgm y un índice GIN, la misma búsqueda usa el índice y responde en milisegundos.

## Cuándo se usa

Se activa con `CREATE EXTENSION IF NOT EXISTS pg_trgm` y se crea el índice con `USING gin (columna gin_trgm_ops)`. Es ideal en tablas con bajo churn (pocos UPDATE/DELETE). La creación del índice debe hacerse con `CONCURRENTLY` en producción para evitar locks.
