---
title: "InnoDB Buffer Pool"
description: "Área de memoria principal de InnoDB que almacena en caché páginas de datos e índices para reducir las lecturas en disco. Se configura con innodb_buffer_pool_size."
translationKey: "glossary_innodb_buffer_pool"
aka: "InnoDB Buffer Pool (MySQL)"
articles:
  - "/posts/mysql/innodb-buffer-pool-dimensionamento-hit-ratio-e-warm-up-dopo-restart"
---

El InnoDB Buffer Pool es el componente de memoria central del motor de almacenamiento InnoDB en MySQL. Actúa como una caché compartida para páginas de datos y páginas de índice: cada vez que una consulta lee o modifica una fila, InnoDB carga la página correspondiente en el buffer pool y la mantiene en memoria el mayor tiempo posible. Cuanto mayor sea el buffer pool en relación con el dataset activo, menos I/O llega al disco.

## Cómo funciona

InnoDB gestiona el buffer pool con un algoritmo LRU (Least Recently Used) modificado, dividido en una "young list" (páginas accedidas recientemente) y una "old list" (candidatas a eviction). Cuando una página no está en memoria, se produce un **buffer pool miss** e InnoDB la lee desde el disco. La relación entre aciertos y fallos se denomina **buffer pool hit ratio**.

El parámetro principal es `innodb_buffer_pool_size`. En servidores dedicados a MySQL se suele establecer en el 80% de la RAM disponible:

```sql
-- Verificar el tamaño actual
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';

-- Modificar en tiempo de ejecución (MySQL 5.7.5+)
SET GLOBAL innodb_buffer_pool_size = 12884901888; -- 12 GB
```

## Contexto operativo

El buffer pool se vacía en cada reinicio del servidor. MySQL soporta el **warm-up automático** mediante `innodb_buffer_pool_dump_at_shutdown` e `innodb_buffer_pool_load_at_startup`, que serializan y restauran la lista de páginas más utilizadas. Sin warm-up, las primeras horas tras un reinicio muestran un hit ratio bajo y latencias elevadas.

En sistemas donde el dataset supera la RAM disponible, monitorizar el hit ratio mediante `SHOW ENGINE INNODB STATUS` o la tabla `information_schema.INNODB_BUFFER_POOL_STATS` es indispensable para determinar si un aumento de memoria está justificado.
