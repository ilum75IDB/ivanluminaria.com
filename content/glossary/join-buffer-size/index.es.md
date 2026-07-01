---
title: "join_buffer_size"
description: "Buffer MySQL asignado por thread para cada join sin índice. Multiplicado por las conexiones activas, puede agotar la RAM del servidor."
translationKey: "glossary_join_buffer_size"
aka: "Join Buffer (MySQL)"
articles:
  - "/posts/mysql/articolo-mysql-saturazione-swap-su-innodb-cluster-3-nodi-analisi-e-fix-dei-param"
---

`join_buffer_size` es un parámetro de sesión en MySQL que controla el tamaño del buffer utilizado para ejecutar joins entre tablas cuando no hay un índice adecuado disponible. A diferencia de `innodb_buffer_pool_size`, que es un recurso compartido, este buffer se asigna **por cada thread activo** que ejecuta un join de ese tipo.

## Cómo funciona

Cuando MySQL no puede usar un índice para unir dos tablas, recurre a un **Block Nested-Loop Join** (o, en versiones más recientes, a un Hash Join). En ambos casos, las filas de la tabla "externa" se cargan en el `join_buffer` para compararlas con la tabla "interna".

```sql
-- Verificar el valor actual a nivel de sesión
SHOW VARIABLES LIKE 'join_buffer_size';

-- Modificar para la sesión actual
SET SESSION join_buffer_size = 4 * 1024 * 1024; -- 4 MB
```

Si el buffer no es suficiente para contener todas las filas relevantes, MySQL realiza múltiples pasadas sobre la tabla interna, incrementando el I/O.

## Contexto operativo

El riesgo principal no es el valor absoluto del parámetro, sino su **efecto multiplicativo**: con 500 conexiones concurrentes y un `join_buffer_size` de 8 MB, el consumo potencial de memoria supera los 4 GB, independientemente de cuántos joins estén activos en un momento dado.

Pautas prácticas:

- Mantener el valor global bajo (256 KB – 1 MB) y aumentarlo a nivel de sesión solo para consultas específicas que se beneficien de ello.
- Antes de aumentar el buffer, verificar si la ausencia de índice es intencional o una omisión: un índice adecuado elimina el problema de raíz.
- Monitorizar `Select_full_join` y `Select_range_check` en `SHOW GLOBAL STATUS` para cuantificar la frecuencia de joins sin índice.
