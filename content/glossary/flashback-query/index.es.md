---
title: "Flashback Query"
description: "Funcionalidad de Oracle que permite consultar un estado pasado de la base de datos mediante timestamp o SCN, leyendo directamente los segmentos de undo."
translationKey: "glossary_flashback_query"
aka: "Oracle Flashback Query"
articles:
  - "/posts/oracle/oracle-flashback-recupero-dati-logici-senza-downtime-da-query-a-database"
---

Flashback Query es una funcionalidad de Oracle Database que permite ejecutar una `SELECT` sobre un estado pasado de los datos, especificando un punto en el tiempo mediante timestamp o System Change Number (SCN). No requiere restauración desde backup ni tiempo de inactividad: los datos históricos se leen directamente desde los segmentos de undo.

## Cómo funciona

Oracle conserva versiones anteriores de los bloques de datos en los tablespaces de undo durante un período configurable (`UNDO_RETENTION`). Flashback Query aprovecha este mecanismo para reconstruir la vista de los datos tal como existían en un momento determinado.

```sql
-- Consulta mediante timestamp
SELECT *
FROM pedidos AS OF TIMESTAMP (SYSTIMESTAMP - INTERVAL '2' HOUR)
WHERE estado = 'CANCELADO';

-- Consulta mediante SCN
SELECT *
FROM pedidos AS OF SCN 4521890;
```

La cláusula `AS OF` está disponible en cualquier `SELECT`, incluidas consultas con JOIN y subconsultas.

## Cuándo se utiliza

Los escenarios habituales son la recuperación de filas eliminadas o modificadas por error, el análisis de datos antes de una transacción problemática y la verificación del contenido de una tabla antes de un proceso batch nocturno. La principal limitación es la disponibilidad de los datos de undo: si `UNDO_RETENTION` es demasiado bajo o el tablespace de undo está bajo presión, Oracle puede sobrescribir los bloques históricos antes de que expire la ventana configurada. Para rangos de tiempo más amplios o para consultar el historial completo de cambios fila a fila, se recurre a Flashback Versions Query o Flashback Data Archive.
