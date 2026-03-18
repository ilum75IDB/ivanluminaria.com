---
title: "MVCC"
description: "Multi-Version Concurrency Control — modelo de concurrencia de PostgreSQL que mantiene múltiples versiones de las filas para garantizar aislamiento transaccional sin locks exclusivos en las lecturas."
translationKey: "glossary_mvcc"
aka: "Multi-Version Concurrency Control"
articles:
  - "/posts/postgresql/vacuum-autovacuum-postgresql"
---

**MVCC** (Multi-Version Concurrency Control) es el modelo de concurrencia usado por PostgreSQL para gestionar el acceso simultáneo a los datos. Cada UPDATE crea una nueva versión de la fila y marca la antigua como "muerta"; cada DELETE marca la fila como ya no visible. Las lecturas no bloquean las escrituras y viceversa.

## Cómo funciona

Cada transacción ve un snapshot consistente de la base de datos en el momento de su inicio. Las filas modificadas por otras transacciones aún no confirmadas son invisibles. Esto elimina la necesidad de locks exclusivos en las lecturas, permitiendo alta concurrencia — pero genera "basura" en forma de dead tuples que deben ser limpiados por el VACUUM.

## Para qué sirve

MVCC es el compromiso arquitectónico de PostgreSQL: alta concurrencia sin locks, al precio de tener que gestionar la limpieza de las versiones obsoletas. Es un precio razonable — siempre que el autovacuum esté correctamente configurado para mantener el ritmo de modificación de las tablas.

## Por qué es crítico

Si el VACUUM no puede mantener el ritmo de generación de dead tuples, las tablas se hinchan (bloat), los escaneos secuenciales se ralentizan y los índices se vuelven ineficientes. El patrón clásico: el lunes la base de datos va bien, el viernes es un desastre.
