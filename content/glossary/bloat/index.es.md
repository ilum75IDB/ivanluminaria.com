---
title: "Bloat"
description: "Espacio muerto acumulado en una tabla o índice PostgreSQL debido a dead tuples no eliminados, que hincha el tamaño en disco y degrada el rendimiento de las queries."
translationKey: "glossary_bloat"
aka: "Table Bloat / Index Bloat"
articles:
  - "/posts/postgresql/vacuum-autovacuum-postgresql"
---

El **Bloat** es la acumulación de espacio muerto dentro de una tabla o índice PostgreSQL, causada por dead tuples aún no eliminados por VACUUM. Una tabla con un 50% de bloat ocupa el doble del espacio necesario y obliga a los escaneos secuenciales a leer el doble de páginas.

## Cómo funciona

El bloat se mide comparando el tamaño efectivo de la tabla con el tamaño esperado basado en las filas vivas. La extensión `pgstattuple` proporciona el campo `dead_tuple_percent`. Un bloat por encima del 20-30% es una señal de alarma; por encima del 50% es una emergencia.

## Para qué sirve

Monitorizar el bloat es esencial para entender si el autovacuum está manteniendo el ritmo. La consulta a `pg_stat_user_tables` con `n_dead_tup` y `last_autovacuum` es la primera herramienta diagnóstica. Si el bloat está fuera de control, `pg_repack` reconstruye la tabla online sin locks exclusivos prolongados — al contrario que `VACUUM FULL`.

## Qué puede salir mal

VACUUM normal recupera el espacio de los dead tuples pero no compacta la tabla — el espacio fragmentado persiste. Si el bloat alcanza el 50-70%, VACUUM solo no es suficiente. Las opciones son `VACUUM FULL` (lock exclusivo, bloquea todo) o `pg_repack` (online, pero requiere instalación). La verdadera solución es no llegar ahí, con un autovacuum bien configurado.
