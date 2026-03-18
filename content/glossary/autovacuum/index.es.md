---
title: "Autovacuum"
description: "Daemon de PostgreSQL que ejecuta automáticamente VACUUM y ANALYZE en las tablas cuando el número de dead tuples supera un umbral configurable."
translationKey: "glossary_autovacuum"
aka: "Autovacuum Daemon"
articles:
  - "/posts/postgresql/vacuum-autovacuum-postgresql"
---

El **Autovacuum** es un daemon de PostgreSQL que ejecuta automáticamente VACUUM y ANALYZE en las tablas cuando el número de dead tuples supera un umbral calculado como: `threshold + scale_factor × n_live_tup`. Con los valores por defecto (threshold=50, scale_factor=0.2), en una tabla con 10 millones de filas se activa tras 2 millones de dead tuples.

## Cómo funciona

El daemon comprueba periódicamente `pg_stat_user_tables` y lanza un worker por cada tabla que supera el umbral. El número máximo de workers simultáneos se controla con `autovacuum_max_workers` (por defecto 3). El parámetro `autovacuum_vacuum_cost_delay` controla cuánto se autofrena el vacuum para no sobrecargar el I/O.

## Para qué sirve

Es el custodio silencioso que impide que las tablas se hinchen por acumulación de dead tuples. Nunca debe deshabilitarse — es lo peor que se puede hacer a un PostgreSQL en producción. Debe configurarse por tabla: las tablas de alto tráfico necesitan scale_factors bajos (0.01-0.05) y cost_delay reducidos.

## Qué puede salir mal

Con los valores por defecto, el autovacuum es demasiado conservador para tablas de alto tráfico. 3 workers para decenas de tablas activas no bastan. Un scale_factor del 20% en tablas grandes genera millones de dead tuples antes de la intervención. El tuning por tabla con `ALTER TABLE ... SET (autovacuum_vacuum_scale_factor = 0.01)` es esencial.
