---
title: "Parallel Replication"
description: "Modo de replicación de MySQL que aplica eventos del binlog con múltiples worker threads, reduciendo el lag de la réplica mediante LOGICAL_CLOCK."
translationKey: "glossary_parallel_replication"
aka: "Multi-threaded Replication (MTR)"
articles:
  - "/posts/mysql/mysql-slave-lag-parallel-replication"
---

La Parallel Replication es el modo en que MySQL aplica los eventos del binlog en la réplica usando múltiples worker threads de forma simultánea, en lugar del tradicional SQL thread único. El objetivo es reducir el replication lag cuando el primario genera transacciones a mayor velocidad de la que la réplica puede aplicarlas en secuencia.

## Cómo funciona

MySQL expone dos políticas configurables mediante `slave_parallel_type`:

- **`DATABASE`**: paraleliza transacciones que afectan a bases de datos distintas. Solo es efectivo si la carga está distribuida entre varios esquemas.
- **`LOGICAL_CLOCK`**: usa los commit timestamps registrados en el binlog para identificar transacciones que se ejecutaban de forma concurrente en el primario y que, por tanto, pueden aplicarse en paralelo en la réplica sin comprometer la consistencia.

`LOGICAL_CLOCK` es el modo recomendado en la mayoría de los casos. El número de workers se controla con `slave_parallel_workers`.

```sql
-- Configuración típica en la réplica
SET GLOBAL slave_parallel_type = 'LOGICAL_CLOCK';
SET GLOBAL slave_parallel_workers = 8;
```

## Cuándo se utiliza

La Parallel Replication resulta relevante cuando la réplica acumula lag a pesar de que el hardware no está saturado: el cuello de botella es la serialización de eventos, no los recursos. Es especialmente eficaz en cargas OLTP con muchas transacciones cortas y concurrentes en el primario.

Tiene sus límites: si el primario ejecuta transacciones mayormente seriales o concentradas en una sola tabla, la mejora es marginal. Además, incrementar `slave_parallel_workers` más allá de cierto umbral introduce overhead de coordinación que puede empeorar el rendimiento en lugar de mejorarlo. El valor óptimo debe determinarse empíricamente según el perfil de carga real.
