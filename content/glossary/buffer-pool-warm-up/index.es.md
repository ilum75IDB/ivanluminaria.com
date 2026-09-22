---
title: "Buffer pool warm-up"
description: "Proceso de recarga de páginas calientes en el buffer pool de InnoDB tras un reinicio, para reducir el cold start de horas a minutos."
translationKey: "glossary_buffer_pool_warm_up"
aka: "Buffer pool preloading"
articles:
  - "/posts/mysql/innodb-buffer-pool-dimensionamento-hit-ratio-e-warm-up-dopo-restart"
---

Cuando MySQL se reinicia, el buffer pool queda vacío: cada consulta debe leer desde disco hasta que las páginas más utilizadas vuelvan a estar en memoria. El buffer pool warm-up es el proceso que acelera esta recuperación, restaurando las páginas calientes antes de que el tráfico de producción las requiera.

## Cómo funciona

InnoDB puede guardar los identificadores de las páginas residentes en memoria en el momento del shutdown y recargarlos en el siguiente arranque. Dos variables de sistema controlan el comportamiento:

```sql
-- Habilitar dump automático al apagar
SET GLOBAL innodb_buffer_pool_dump_at_shutdown = ON;

-- Habilitar carga automática al arrancar (configurar en my.cnf)
-- innodb_buffer_pool_load_at_startup = ON
```

El archivo generado (`ib_buffer_pool`) contiene pares `(tablespace_id, page_id)`, no los datos reales: es ligero y la restauración se ejecuta en segundo plano sin bloquear las conexiones entrantes. La variable `innodb_buffer_pool_dump_pct` (valor por defecto 25) limita el porcentaje de páginas serializadas, equilibrando completitud y tiempo de dump.

## Cuándo se usa

El warm-up es relevante en tres escenarios principales:

- **Reinicios planificados** (parcheo del SO, actualizaciones de MySQL): sin warm-up, el hit ratio puede mantenerse por debajo del 50% durante horas en instancias con buffer pools de decenas de GB.
- **Failover en réplicas**: una réplica promovida a primary arranca con el buffer pool frío; habilitar dump/load también en las réplicas reduce la degradación post-failover.
- **Entornos cloud con instancias spot/preemptible**: los ciclos frecuentes de parada y arranque hacen que el warm-up automático sea prácticamente obligatorio.

El progreso de la carga se puede monitorizar en tiempo real:

```sql
SHOW STATUS LIKE 'Innodb_buffer_pool_load_status';
```
