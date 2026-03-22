---
title: "pg_stat_statements"
description: "Extensión PostgreSQL que recopila estadísticas de ejecución de todas las queries SQL, herramienta fundamental para la diagnóstica de rendimiento."
translationKey: "glossary_pg-stat-statements"
aka: "pgss"
articles:
  - "/posts/postgresql/pg-stat-statements"
---

**pg_stat_statements** es una extensión de PostgreSQL — incluida en la distribución oficial pero no activa por defecto — que lleva el registro de las estadísticas de ejecución de todas las queries SQL que pasan por el servidor. Las queries se normalizan (los valores literales se reemplazan con parámetros) para agrupar las ejecuciones del mismo patrón.

## Cómo funciona

La extensión requiere ser cargada como shared library al arranque del servidor mediante el parámetro `shared_preload_libraries`. Una vez activa, registra para cada query: número de ejecuciones, tiempo total y medio, filas devueltas, bloques leídos de disco y de caché. El parámetro `pg_stat_statements.max` controla cuántas queries distintas se rastrean (por defecto 5000).

## Para qué sirve

Es la herramienta principal para identificar las queries más costosas en un servidor PostgreSQL. Ordenando por `total_exec_time` se obtiene inmediatamente el ranking de queries que consumen más recursos. Combinado con EXPLAIN ANALYZE, permite un workflow diagnóstico completo: pg_stat_statements identifica el problema, EXPLAIN explica la causa.

## Cuándo se usa

Debería estar activo en cualquier instalación PostgreSQL de producción. El overhead es despreciable (1-2% de CPU). Sin pg_stat_statements, cualquier actividad de performance tuning se basa en suposiciones en lugar de datos.
