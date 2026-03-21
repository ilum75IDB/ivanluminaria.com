---
title: "shared_buffers"
description: "Área de memoria compartida de PostgreSQL que sirve como caché para bloques de datos, el parámetro más importante para el tuning de memoria."
translationKey: "glossary_shared-buffers"
aka: "Shared Buffer Cache"
articles:
  - "/posts/postgresql/pg-stat-statements"
---

**shared_buffers** es el parámetro que controla el tamaño del área de memoria compartida que PostgreSQL usa como caché para los bloques de datos leídos del disco. Cada vez que PostgreSQL lee una página de datos (8 KB), la conserva en shared_buffers para las lecturas posteriores.

## Cómo funciona

PostgreSQL asigna la memoria para shared_buffers al arranque del servicio. Todos los procesos backend comparten esta área de memoria. Cuando un proceso necesita un bloque de datos, busca primero en shared_buffers. Si lo encuentra (cache hit), la lectura es inmediata. Si no lo encuentra (cache miss), debe leer del disco — una operación órdenes de magnitud más lenta.

## Cuánto asignar

El valor por defecto es 128 MB — inadecuado para cualquier base de datos de producción. La regla empírica es configurar shared_buffers al 25% de la RAM disponible. En un servidor con 64 GB de RAM, 16 GB es un buen punto de partida. Valores por encima del 40% de la RAM raramente aportan beneficios porque PostgreSQL también se apoya en la caché del sistema operativo.

## Cómo monitorizarlo

La vista `pg_stat_bgwriter` muestra la relación entre `buffers_alloc` (nuevos bloques asignados) y el total de bloques servidos. Un cache hit ratio por debajo del 95% sugiere que shared_buffers podría estar subdimensionado.
