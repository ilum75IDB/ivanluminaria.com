---
title: "pg_stat_user_indexes"
description: "Vista de sistema PostgreSQL que registra cuántas veces ha sido usado cada índice por el planner — la herramienta principal para identificar índices inútiles en producción."
translationKey: "glossary_pg_stat_user_indexes"
aka: ""
articles:
  - "/posts/postgresql/postgresql-indici-quando-fanno-male"
---

`pg_stat_user_indexes` es una vista de sistema PostgreSQL que expone las estadísticas de uso de todos los índices sobre tablas de usuario (excluyendo las del sistema). Para cada índice mantiene un contador de cuántas veces el planner lo ha elegido realmente.

## Cómo funciona

La columna clave es `idx_scan`: arranca a cero al iniciar la base de datos (o al último `pg_stat_reset()`) y se incrementa en uno cada vez que el planner elige ese índice para ejecutar una consulta. Otras columnas útiles incluyen:

- `idx_tup_read` — cuántos punteros a fila se han leído del índice
- `idx_tup_fetch` — cuántas filas se han leído efectivamente de la tabla a través del índice
- `relname` — nombre de la tabla a la que pertenece el índice
- `indexrelname` — nombre del índice

## Para qué sirve

Es la herramienta principal para identificar **índices inútiles en producción**. Si un índice tiene `idx_scan = 0` después de semanas o meses de actividad, el planner nunca lo ha considerado útil para ninguna consulta. Es candidato a eliminación (tras verificar que no sea un índice usado solo para restricciones de unicidad o foreign key).

## Cuándo se usa

Se consulta como primer diagnóstico cuando se quiere entender cuánto valen realmente los índices de una tabla, sobre todo cuando hay muchos. Ejemplo típico:

```sql
SELECT relname, indexrelname, idx_scan,
       pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
WHERE relname = 'tabla'
ORDER BY idx_scan ASC;
```

Combinar con `pg_stat_reset()` si hace falta poner a cero las estadísticas tras un cambio significativo de workload.
