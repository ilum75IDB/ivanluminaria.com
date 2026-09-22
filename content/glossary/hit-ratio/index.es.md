---
title: "Hit ratio"
description: "Porcentaje de lecturas InnoDB servidas desde el Buffer Pool frente al total. Valores por debajo de 990/1000 indican presión excesiva en disco."
translationKey: "glossary_hit_ratio"
aka: "Buffer Pool hit ratio"
articles:
  - "/posts/mysql/innodb-buffer-pool-dimensionamento-hit-ratio-e-warm-up-dopo-restart"
---

El hit ratio mide cuántas lecturas de páginas InnoDB se resuelven directamente desde el Buffer Pool, sin acceder al disco. Es el indicador principal de la eficacia de la memoria asignada a InnoDB: un valor alto significa que el working set activo cabe en RAM; un valor bajo implica I/O físico frecuente y latencias más elevadas.

## Cómo interpretarlo

MySQL expone el hit ratio en la salida de `SHOW ENGINE INNODB STATUS`, dentro de la sección `BUFFER POOL AND MEMORY`:

```
Buffer pool hit rate X / 1000
```

Un valor de `997 / 1000` indica que 997 de cada 1000 lecturas se sirvieron desde memoria. El umbral operativo generalmente aceptado es **990/1000**: caer por debajo señala que el Buffer Pool está subdimensionado respecto al working set activo.

## Contexto operativo

El hit ratio es especialmente inestable tras un reinicio de MySQL: el Buffer Pool está frío y las primeras consultas generan page faults en cascada, haciendo caer el valor incluso por debajo de 900/1000. InnoDB ofrece volcado y recarga automática del Buffer Pool (`innodb_buffer_pool_dump_at_shutdown` / `innodb_buffer_pool_load_at_startup`) precisamente para acelerar el warm-up.

Un hit ratio crónicamente bajo no siempre se resuelve aumentando `innodb_buffer_pool_size`. Las consultas ineficientes que realizan full scan sobre tablas grandes contaminan el Buffer Pool con páginas de un solo uso, desplazando los datos calientes independientemente de la memoria disponible.
