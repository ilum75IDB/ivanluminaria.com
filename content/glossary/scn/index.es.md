---
title: "SCN"
description: "System Change Number: el número secuencial monotónicamente creciente que Oracle usa para marcar cada COMMIT y garantizar consistencia y recovery point-in-time."
translationKey: "glossary_scn"
aka: "System Change Number"
articles:
  - "/posts/oracle/quali-sono-i-files-critici-di-un-db-oracle"
---

El SCN (System Change Number) es el contador interno con el que Oracle ordena cada cambio producido en la base de datos. Crece de forma estrictamente monotónica: cada COMMIT recibe un SCN mayor que el anterior, lo que permite reconstruir con precisión el estado de la base de datos en cualquier momento pasado.

## Cómo funciona

Cada vez que una transacción ejecuta un COMMIT, Oracle asigna un SCN único y lo registra en el redo log, en el control file y en los headers de los datafiles. Este valor es el punto de referencia para todas las operaciones de consistencia y recovery.

```sql
-- Lectura del SCN actual de la base de datos
SELECT CURRENT_SCN FROM V$DATABASE;

-- SCN registrado en el header de un datafile
SELECT NAME, CHECKPOINT_CHANGE# FROM V$DATAFILE;
```

Durante un instance recovery, Oracle compara el SCN almacenado en el control file con el de los headers de cada datafile para determinar qué bloques necesitan redo y cuáles ya son consistentes.

## Contexto operativo

El SCN es central en tres escenarios principales:

- **Point-in-time recovery (PITR)**: se especifica un SCN objetivo y Oracle reaaplica el redo hasta ese punto exacto.
- **Flashback**: Flashback Query y Flashback Database utilizan el SCN para navegar por el historial de los datos.
- **Data Guard y replicación**: el standby aplica el archived redo hasta el SCN transmitido por el primary, garantizando la sincronización.

El SCN tiene un máximo teórico (vinculado a la arquitectura de 48 bits en versiones recientes), pero en condiciones normales no representa una limitación operativa. Las situaciones anómalas de SCN headroom reducido se pueden monitorizar mediante `V$DATABASE_INCARNATION` y las notas MOS relacionadas.
