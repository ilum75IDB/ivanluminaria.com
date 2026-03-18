---
title: "Dead Tuple"
description: "Fila obsoleta en una tabla PostgreSQL, marcada como ya no visible después de un UPDATE o DELETE pero aún no eliminada físicamente del disco."
translationKey: "glossary_dead-tuple"
aka: "Tupla muerta"
articles:
  - "/posts/postgresql/vacuum-autovacuum-postgresql"
---

Un **Dead Tuple** es una fila en una tabla PostgreSQL que ha sido actualizada (UPDATE) o eliminada (DELETE) pero aún no ha sido removida físicamente. Permanece en las páginas de datos, ocupando espacio en disco y ralentizando los escaneos.

## Cómo funciona

Cuando PostgreSQL ejecuta un UPDATE, no sobrescribe la fila original: crea una nueva versión y marca la antigua como "muerta." La fila antigua permanece físicamente en la página de datos hasta que VACUUM la limpia. Los dead tuples son el precio del modelo MVCC — necesarios para garantizar el aislamiento transaccional.

## Para qué sirve

Los dead tuples son un indicador clave de la salud de una tabla. La vista `pg_stat_user_tables` muestra `n_dead_tup` y `last_autovacuum` — si los dead tuples crecen más rápido de lo que el autovacuum puede limpiar, la tabla tiene un problema. Un dead_tuple_percent por encima del 20-30% es una señal de alarma.

## Qué puede salir mal

En una tabla con 500.000 updates al día y los valores por defecto del autovacuum (scale_factor 0.2), VACUUM se activa cada 4 días. Mientras tanto los dead tuples se acumulan, las tablas se hinchan y las queries se ralentizan progresivamente — el patrón "lunes bien, viernes desastre".
