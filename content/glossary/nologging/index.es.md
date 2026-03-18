---
title: "NOLOGGING"
description: "Modo Oracle que suprime la generación de redo log durante operaciones masivas (CTAS, INSERT APPEND, ALTER TABLE MOVE), acelerando las operaciones pero requiriendo un backup inmediato."
translationKey: "glossary_nologging"
articles:
  - "/posts/oracle/oracle-partitioning"
---

**NOLOGGING** es un modo Oracle que deshabilita la generación de redo log durante operaciones de carga masiva. Las operaciones se completan mucho más rápido, pero los datos no son recuperables mediante redo en caso de crash antes de un backup.

## Cómo funciona

Cuando un segmento (tabla, índice, partición) está en modo NOLOGGING, las operaciones masivas como CTAS, `INSERT /*+ APPEND */` y `ALTER TABLE MOVE` no escriben redo log para los bloques de datos. En una copia de 380 GB, esto elimina la generación de la misma cantidad de redo, evitando saturar el área de archivelog y reduciendo los tiempos de días a horas.

## Para qué sirve

NOLOGGING es esencial para operaciones de migración en tablas de gran tamaño. Sin NOLOGGING, un CTAS de 380 GB generaría 380 GB de redo log, poniendo el sistema en modo archivelog durante días. Con NOLOGGING, la misma operación se completa en pocas horas con impacto mínimo en el sistema.

## Cuándo se usa

Se activa antes de la operación masiva y se desactiva inmediatamente después (`ALTER TABLE ... LOGGING`). Es obligatorio ejecutar un backup RMAN inmediatamente después, porque los segmentos NOLOGGING no son recuperables con un restore desde redo. Nunca dejar NOLOGGING activo permanentemente en tablas de producción.
