---
title: "Página dirty"
description: "Página del buffer pool modificada en memoria pero aún no escrita en disco. Un recuento alto y creciente indica que el flush de InnoDB no sigue el ritmo de las escrituras."
translationKey: "glossary_pagina_dirty"
aka: "Dirty page, página sucia"
articles:
  - "/posts/mysql/innodb-buffer-pool-dimensionamento-hit-ratio-e-warm-up-dopo-restart"
---

En el buffer pool de InnoDB, una **página dirty** es una página de 16 KB que ha sido modificada en memoria — por un INSERT, UPDATE o DELETE — pero cuyo contenido actualizado todavía no ha sido escrito en el archivo de datos en disco. La versión en disco está, por tanto, desactualizada respecto a la que reside en RAM.

## Cómo funciona

Cada vez que una transacción modifica una fila, InnoDB actualiza la página correspondiente en el buffer pool y la marca como dirty. Un hilo de flush en segundo plano (`page_cleaner`) escribe periódicamente las páginas dirty en los archivos `.ibd` siguiendo dos estrategias principales:

- **Fuzzy checkpoint**: flush continuo e incremental para mantener el porcentaje de páginas dirty por debajo de `innodb_max_dirty_pages_pct` (valor por defecto: 90%).
- **Flush adaptativo**: acelera el flush cuando la tasa de escritura en el redo log se acerca a su capacidad máxima, evitando que InnoDB tenga que bloquear las escrituras de usuario para liberar espacio.

```sql
-- Monitorizar las páginas dirty en tiempo real
SELECT VARIABLE_NAME, VARIABLE_VALUE
FROM performance_schema.global_status
WHERE VARIABLE_NAME IN (
    'Innodb_buffer_pool_pages_dirty',
    'Innodb_buffer_pool_pages_total'
);
```

## Contexto operativo

Un número de páginas dirty estable y reducido es normal. La señal de alerta es un **crecimiento sostenido y monótono**: indica que el hilo de flush no consigue vaciar las escrituras entrantes con suficiente rapidez. Las causas más frecuentes son un buffer pool sobredimensionado respecto al rendimiento del disco, un valor de `innodb_io_capacity` demasiado bajo, o un pico repentino de carga de escritura.

En caso de crash, InnoDB utiliza el redo log para recuperar las páginas dirty que no llegaron a ser escritas en disco. Cuantas más páginas dirty haya en el momento del crash, mayor será el tiempo de crash recovery al reiniciar.
