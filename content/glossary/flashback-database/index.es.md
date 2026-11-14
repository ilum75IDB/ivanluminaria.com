---
title: "Flashback Database"
description: "Función de Oracle que revierte toda la base de datos a un punto anterior en el tiempo mediante flashback logs, más rápida que un restore RMAN completo ante errores lógicos masivos."
translationKey: "glossary_flashback_database"
aka: "Oracle Flashback Database Recovery"
articles:
  - "/posts/oracle/oracle-flashback-recupero-dati-logici-senza-downtime-da-query-a-database"
---

Flashback Database es una funcionalidad de Oracle que permite revertir toda la base de datos a un estado anterior sin necesidad de restaurar los datafiles desde un backup. A diferencia de un restore RMAN completo, opera sobre logs dedicados escritos de forma continua en segundo plano, lo que hace la recuperación considerablemente más rápida cuando un error lógico ya se ha propagado por múltiples objetos.

## Cómo funciona

Oracle escribe de forma continua imágenes previas de los bloques modificados en los **flashback logs**, almacenados en la Fast Recovery Area (FRA). Al iniciar un Flashback Database, el motor lee esos logs hacia atrás hasta el punto en el tiempo (o SCN) deseado, aplicando las imágenes guardadas sobre los bloques actuales.

La operación requiere que la base de datos esté en modo `MOUNT`:

```sql
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
FLASHBACK DATABASE TO TIMESTAMP (SYSTIMESTAMP - INTERVAL '2' HOUR);
ALTER DATABASE OPEN RESETLOGS;
```

El `OPEN RESETLOGS` es obligatorio: reinicia la secuencia de redo logs y hace que el punto de flashback ya no sea alcanzable hacia adelante.

## Cuándo utilizarlo

Flashback Database es la herramienta adecuada cuando un error lógico — un `DELETE` masivo sin `WHERE`, una migración fallida, un proceso batch que corrompió datos en decenas de tablas — ha superado ya la ventana en la que Flashback Table o Flashback Query serían suficientes.

Restricciones a tener en cuenta:

- `DB_FLASHBACK_RETENTION_TARGET` debe estar configurado y la FRA debe disponer de espacio suficiente para los flashback logs del período requerido.
- Los datafiles añadidos después del punto de flashback no se recuperan automáticamente y deben gestionarse por separado.
- Tras el `RESETLOGS`, las bases de datos standby en una configuración Data Guard deben resincronizarse.
