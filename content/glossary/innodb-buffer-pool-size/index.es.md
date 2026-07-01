---
title: "innodb_buffer_pool_size"
description: "Parámetro global de MySQL que define el tamaño del buffer pool de InnoDB para caché de datos e índices: el ajuste de memoria más crítico del servidor."
translationKey: "glossary_innodb_buffer_pool_size"
aka: "InnoDB Buffer Pool"
articles:
  - "/posts/mysql/articolo-mysql-saturazione-swap-su-innodb-cluster-3-nodi-analisi-e-fix-dei-param"
---

`innodb_buffer_pool_size` es el parámetro global de MySQL que controla cuánta RAM se reserva para el Buffer Pool de InnoDB — la estructura en memoria que almacena en caché páginas de datos e índices para reducir el acceso a disco. Es el parámetro con mayor impacto en el rendimiento de un servidor MySQL dedicado.

## Cómo funciona

InnoDB gestiona el Buffer Pool como un conjunto de páginas de 16 KB (por defecto). Cuando una consulta accede a una fila, InnoDB carga la página correspondiente en el Buffer Pool; las lecturas posteriores sobre esa misma página se sirven desde RAM sin acceder al disco. Las páginas modificadas (dirty pages) se escriben en disco de forma asíncrona mediante hilos de flushing en segundo plano.

El valor se configura en `my.cnf` o `my.ini`:

```ini
[mysqld]
innodb_buffer_pool_size = 12G
```

En servidores con RAM ≥ 1 GB, MySQL permite también la reconfiguración dinámica en tiempo de ejecución:

```sql
SET GLOBAL innodb_buffer_pool_size = 12884901888;
```

## Dimensionamiento y contexto operativo

En servidores dedicados a MySQL, la regla empírica consolidada es **70-80% de la RAM disponible**. Dejar menos del 20% libre somete al sistema operativo a presión de memoria y, en los peores casos, provoca el uso del swap — con una degradación drástica del rendimiento.

En un clúster InnoDB de 3 nodos, cada nodo mantiene su propio Buffer Pool independiente. Un dimensionamiento excesivo en máquinas donde la RAM se comparte con otros procesos (agentes de monitorización, servidores de binlog, etc.) es una causa frecuente de saturación del swap.

Monitorizar el **Buffer Pool hit rate** es el primer indicador que hay que vigilar:

```sql
SELECT
  (1 - (Innodb_buffer_pool_reads / Innodb_buffer_pool_read_requests)) * 100
    AS hit_rate_pct
FROM information_schema.GLOBAL_STATUS
WHERE Variable_name IN ('Innodb_buffer_pool_reads','Innodb_buffer_pool_read_requests');
```

Un hit rate por debajo del 95% en cargas OLTP indica que el Buffer Pool está subdimensionado.
