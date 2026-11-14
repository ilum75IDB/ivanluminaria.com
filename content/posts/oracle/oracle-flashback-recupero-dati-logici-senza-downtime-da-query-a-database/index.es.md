---
categories:
- oracle
date: '2026-11-24'
description: 'Flashback Query, Table, Drop y Database en Oracle: cómo recuperar datos
  perdidos por errores lógicos en minutos, sin restore desde backup y sin downtime.'
draft: false
image: oracle-flashback-recupero-dati-logici-senza-downtime-da-query-a-database.cover.jpg
seoTitle: 'Oracle Flashback: recuperación de datos lógicos sin downtime'
tags:
- oracle
- flashback
- recovery
- undo
- rto
title: 'La reunión del martes por la mañana: recuperación de datos con Oracle Flashback
  sin downtime'
translationKey: oracle_flashback_recupero_dati_logici_senza_downtime_da_query_a_database
webo_generated_at: 2026-11-14
webo_status: scheduled
---

## La reunión del martes por la mañana

La notificación llegó durante una reunión semanal en Teams, no como alerta de monitorización, no como ticket urgente. Uno de los responsables de área compartió la pantalla y dijo, con un tono más desconcertado que alarmado: "Los números de ayer no cuadran. Y los de anteayer tampoco."

El dashboard directivo de un gran grupo asegurador italiano — el que cada mañana alimenta las decisiones operativas sobre primas y siniestros — mostraba datos incongruentes. No un crash, no una página en blanco. Los datos estaban ahí, pero eran incorrectos. O mejor dicho: estaban incompletos, y nadie había recibido una alerta porque técnicamente el sistema funcionaba. El pipeline corría, las tablas eran accesibles, las queries respondían. Sencillamente, algunas filas habían desaparecido hacía aproximadamente cuarenta y ocho horas.

Treinta minutos de reunión para recoger las observaciones de los compañeros, acotar la ventana temporal del problema, entender que no se trataba de una interrupción de servicio sino de un error lógico silencioso. Luego la pregunta inevitable: ¿cómo se recuperan esos datos?

La respuesta, en ese contexto, no era "restauramos desde el backup".

## Por qué el backup completo no era el primer movimiento

Un restore desde backup sobre una tabla de unos 500 GB y 2.000 millones de filas no es una operación que se hace en una hora. Requiere una ventana de mantenimiento, un entorno de staging donde restaurar selectivamente, la gestión de las dependencias con las otras tablas, y casi con toda seguridad una interrupción del servicio para los usuarios. En un contexto asegurador donde el dashboard alimenta decisiones diarias sobre carteras activas, esto tiene un coste real.

Oracle, sin embargo, lleva años ofreciendo un conjunto de funcionalidades que permite hacer algo mucho más quirúrgico: retroceder en el tiempo a nivel de una sola query, de una tabla, o incluso de toda la base de datos, aprovechando datos que el motor ya conserva para otros fines — los undo segments y los flashback logs. Colectivamente, estas tecnologías se denominan **Oracle Flashback** [1].

El principio es sencillo: Oracle mantiene versiones anteriores de los bloques de datos para gestionar la consistencia de las lecturas (MVCC) y el rollback de las transacciones. Las funcionalidades Flashback aprovechan esta infraestructura para permitir operaciones de recovery selectivas, sin tocar los backups.

## Flashback Query: quince minutos para encontrar la aguja

Lo primero era entender exactamente qué faltaba. Flashback Query permite ejecutar una `SELECT` como si la base de datos estuviera en un estado anterior, especificando un timestamp o un SCN (System Change Number) [2].

El SCN es un contador interno de Oracle que avanza de forma monótona en cada commit: identifica un punto preciso en la historia de la base de datos. Cada fila tiene un SCN asociado a la última modificación. Flashback Query usa los undo segments para reconstruir la versión de una fila en un SCN pasado.

La primera query fue un conteo simple, para verificar cuántas filas había dos días atrás respecto al estado actual:

```sql
-- Conteo de filas presentes hace 48 horas
SELECT COUNT(*)
FROM DASHBOARD_DATA.DAILY_SALES_METRICS
AS OF TIMESTAMP (SYSTIMESTAMP - INTERVAL '2' DAY);
```

El resultado confirmó la hipótesis: la tabla contenía unas 340.000 filas más respecto al estado actual. Algo las había eliminado, y el sistema no había generado ninguna alerta porque la eliminación se había producido mediante una transacción aparentemente normal.

La segunda query aisló las filas que faltaban para una fecha específica:

```sql
-- Filas presentes ayer para una fecha de venta específica
SELECT *
FROM DASHBOARD_DATA.DAILY_SALES_METRICS
AS OF TIMESTAMP (SYSTIMESTAMP - INTERVAL '1' DAY)
WHERE sales_date = TO_DATE('2024-11-22', 'YYYY-MM-DD');
```

Quince minutos de análisis. Las filas existían, habían sido eliminadas, y el patrón de la eliminación apuntaba a un job batch mal configurado que había ejecutado un `DELETE` con una condición más amplia de lo previsto. Sin error aplicativo, sin rollback: la transacción había completado correctamente, pero había hecho más de lo necesario.

El recovery fue igual de directo: un `INSERT ... SELECT ... AS OF TIMESTAMP` para reinsertar las filas que faltaban desde la versión histórica de la tabla. Cinco minutos, sin interrupción de servicio, sin ventana de mantenimiento.

```sql
-- Reinserción de las filas eliminadas accidentalmente
INSERT INTO DASHBOARD_DATA.DAILY_SALES_METRICS
SELECT *
FROM DASHBOARD_DATA.DAILY_SALES_METRICS
AS OF TIMESTAMP (SYSTIMESTAMP - INTERVAL '2' DAY)
WHERE sales_date BETWEEN TO_DATE('2024-11-20', 'YYYY-MM-DD')
                     AND TO_DATE('2024-11-22', 'YYYY-MM-DD')
  AND metric_id NOT IN (
      SELECT metric_id FROM DASHBOARD_DATA.DAILY_SALES_METRICS
  );
```

Para que Flashback Query funcione, es necesario que los datos de undo sigan disponibles — es decir, que el parámetro `UNDO_RETENTION` esté configurado para un período suficiente y que los undo segments no hayan sido sobreescritos por presión de espacio. En este caso, el sistema estaba configurado con una retención de 24 horas, suficiente para cubrir la ventana de cuarenta y ocho horas gracias a la combinación con los flashback logs.

## Flashback Table y Flashback Drop: cuando hace falta algo más

Flashback Query es la herramienta adecuada cuando se sabe qué buscar y se quieren recuperar filas específicas. Pero hay escenarios donde se necesita un enfoque diferente.

### Restaurar una tabla entera

`FLASHBACK TABLE` devuelve una tabla entera — datos y estructura — a un punto en el tiempo anterior [3]. Es útil cuando la corrupción es extensa y no vale la pena identificar fila a fila qué recuperar.

```sql
-- Restauración de una tabla a hace una hora
FLASHBACK TABLE DASHBOARD_DATA.DAILY_SALES_METRICS
TO TIMESTAMP (SYSTIMESTAMP - INTERVAL '1' HOUR);
```

Dos requisitos que conviene tener presentes:

**ROW MOVEMENT** debe estar habilitado en la tabla. Oracle, durante el flashback, puede necesitar mover físicamente las filas (el ROWID cambia), y esto requiere que la tabla lo permita explícitamente:

```sql
ALTER TABLE DASHBOARD_DATA.DAILY_SALES_METRICS ENABLE ROW MOVEMENT;
```

**UNDO retention** debe cubrir el punto en el tiempo al que se quiere volver. Si los undo segments han sido sobreescritos, la operación falla con `ORA-01555: snapshot too old`.

A diferencia de un restore desde backup, `FLASHBACK TABLE` no requiere llevar la base de datos a modo mount, no interrumpe las sesiones activas en las otras tablas, y no necesita una ventana de mantenimiento. El servicio permanece disponible.

### Recuperar una tabla eliminada

`FLASHBACK DROP` es el caso más dramático y, paradójicamente, uno de los más sencillos de gestionar [3]. Cuando se ejecuta un `DROP TABLE` sin `PURGE`, Oracle no elimina físicamente la tabla: la mueve a la **Recycle Bin**, un área lógica del espacio tablespace donde los objetos eliminados permanecen hasta que el espacio sea necesario para otros fines.

```sql
-- Recuperación de una tabla eliminada por error
FLASHBACK TABLE DASHBOARD_DATA.STAGING_METRICS TO BEFORE DROP;
```

Para ver qué hay en la Recycle Bin:

```sql
SELECT object_name, original_name, droptime, space
FROM recyclebin
ORDER BY droptime DESC;
```

Los límites son dos: si la tabla se eliminó con `PURGE`, o si la Recycle Bin fue vaciada (`PURGE RECYCLEBIN`), no hay nada que recuperar. Y si el espacio del tablespace está bajo presión, Oracle puede reutilizar automáticamente el espacio de la Recycle Bin sin previo aviso.

## Flashback Database: el caso más serio

Las tres funcionalidades anteriores operan a nivel de objeto o de fila. `FLASHBACK DATABASE` es otra categoría: devuelve toda la base de datos a un punto en el tiempo anterior, como si se pulsara un botón de "deshacer" global [4].

Se usa en escenarios donde el error es generalizado: un parche aplicativo que ha corrompido datos en decenas de tablas, una actualización de esquema que salió mal, un error lógico que se propagó a través de procedimientos y triggers antes de que alguien lo detectara.

Los requisitos son más exigentes que los de las otras funcionalidades:

- **Flashback Logging** debe estar habilitado (`ALTER DATABASE FLASHBACK ON`)
- Una **Fast Recovery Area (FRA)** debe estar configurada con espacio suficiente
- El parámetro `DB_FLASHBACK_RETENTION_TARGET` define cuántos minutos la base de datos conserva los flashback logs (en el sistema del grupo asegurador estaba configurado a 4320 minutos, es decir, 3 días)

El workflow de recovery requiere llevar la base de datos a modo mount:

```sql
-- Workflow Flashback Database
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
FLASHBACK DATABASE TO TIMESTAMP
    TO_TIMESTAMP('2024-11-22 08:00:00', 'YYYY-MM-DD HH24:MI:SS');
ALTER DATABASE OPEN RESETLOGS;
```

`RESETLOGS` es obligatorio: tras un Flashback Database, los redo logs se reinician porque la historia de la base de datos ha sido reescrita. Esto implica que los backups anteriores al `RESETLOGS` ya no son directamente aplicables para un recovery incremental — es necesario hacer inmediatamente un backup completo tras la operación.

La diferencia respecto a un restore tradicional está en el tiempo: un Flashback Database sobre un sistema con la FRA bien dimensionada puede completarse en minutos en lugar de horas, porque trabaja sobre los flashback logs (bloques modificados) en vez de tener que restaurar toda la estructura física de la base de datos.

## Los límites que no se pueden ignorar

Oracle Flashback no es un sustituto del backup. Es un complemento para errores lógicos con una ventana temporal definida. Tres aspectos prácticos a tener en cuenta:

**Dependencia del UNDO retention.** Flashback Query y Flashback Table dependen de la disponibilidad de los datos de undo. Si el tablespace UNDO está bajo presión, Oracle puede sobreescribir los datos de undo antes de que expire la retención configurada. El parámetro `UNDO_RETENTION` es un objetivo, no una garantía absoluta — a menos de habilitar `RETENTION GUARANTEE` en el tablespace UNDO, que impide la sobreescritura aunque eso suponga que fallen las transacciones que necesitan espacio.

**Impacto en el espacio.** Los flashback logs para `FLASHBACK DATABASE` ocupan espacio en la FRA. Con `DB_FLASHBACK_RETENTION_TARGET` a 3 días en una base de datos con carga de trabajo intensa, la FRA puede crecer rápidamente. La monitorización del espacio de la FRA forma parte de la rutina operativa, no es una actividad ocasional [5].

```sql
-- Monitorización del espacio de la FRA
SELECT name, space_limit/1024/1024/1024 AS limit_gb,
       space_used/1024/1024/1024 AS used_gb,
       space_reclaimable/1024/1024/1024 AS reclaimable_gb
FROM v$recovery_file_dest;
```

**Errores físicos y media failure.** Flashback no ayuda en caso de corrupción física de los bloques de datos, pérdida de datafiles, o fallo de hardware. Para estos escenarios hacen falta los backups tradicionales, Data Guard, o ambos. La suite Flashback cubre la categoría de los errores lógicos — los que, estadísticamente, son la causa más frecuente de pérdida de datos en producción, pero no la única.

## Lo que queda después de la reunión

Los datos fueron recuperados. El dashboard volvía a ser fiable antes del mediodía, sin que ningún usuario percibiera una interrupción. El job batch responsable de la eliminación fue corregido y añadido a la lista de verificaciones del change management.

El punto que vale la pena destacar no es la velocidad del recovery — cincuenta minutos desde el inicio de la reunión hasta el dashboard restaurado — sino la naturaleza de la herramienta. Flashback Query no requirió detener nada. No requirió involucrar al equipo de infraestructura para un restore. No requirió ninguna comunicación a los usuarios.

Solo requirió saber que existía y cómo funcionaba.

En muchos entornos Oracle, las funcionalidades Flashback están habilitadas por defecto o con configuración mínima, pero nunca se usan porque no forman parte del playbook operativo cotidiano. Acaban en los manuales, no en los runbooks. Y cuando se necesita un recovery rápido, se tiende a saltar directamente al backup — que es la respuesta correcta para muchos escenarios, pero no para todos.

Invertir unas horas en entender la diferencia entre `FLASHBACK TABLE` y un restore desde RMAN, en probar `FLASHBACK DATABASE` en un entorno de pre-producción, en configurar correctamente `UNDO_RETENTION` y la FRA: es el tipo de trabajo preparatorio que no produce resultados visibles hasta que hace falta. Y cuando hace falta, produce resultados muy visibles.

## Fuentes oficiales

1. Oracle Database — [Using Oracle Flashback Technology](https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/using-oracle-flashback-technology.html) — visión general de las funcionalidades Flashback, SCN, undo segments, arquitectura general.
2. Oracle Database SQL Language Reference 19c — [SELECT (Flashback Queries)](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/SELECT.html) — sintaxis `AS OF TIMESTAMP` y `AS OF SCN`, cláusulas Flashback Version Query y Flashback Transaction Query.
3. Oracle Database SQL Language Reference 19c — [FLASHBACK TABLE](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/FLASHBACK-TABLE.html) — sintaxis `FLASHBACK TABLE ... TO TIMESTAMP`, `TO BEFORE DROP`, requisitos ROW MOVEMENT, Recycle Bin.
4. Oracle Database Backup and Recovery User's Guide 19c — [Performing Flashback Database and Database Point-in-Time Recovery](https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/rman-performing-flashback-dbpitr.html) — workflow `FLASHBACK DATABASE`, requisitos FRA y Flashback Logging, `OPEN RESETLOGS`.
5. Oracle Database Reference 19c — [DB_FLASHBACK_RETENTION_TARGET](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/DB_FLASHBACK_RETENTION_TARGET.html) — parámetro de configuración, unidad (minutos), interacción con la FRA.

## Glosario
- **[Flashback Query](/es/glossary/flashback-query/)** (Oracle) — Funcionalidad que permite ejecutar una `SELECT` sobre un estado pasado de la base de datos, especificando un timestamp o un SCN. Aprovecha los datos de undo sin necesitar restore desde backup. Útil para identificar y recuperar filas eliminadas o modificadas accidentalmente.

- **[Flashback Table](/es/glossary/scn/)** (Oracle) — Comando que restaura una tabla entera a un punto en el tiempo anterior, incluidos los datos. Requiere `ROW MOVEMENT` habilitado en la tabla y que los datos de undo sigan disponibles. No interrumpe las sesiones activas en las otras tablas de la base de datos.

- **[Flashback Database](/es/glossary/rto/)** (Oracle) — Técnica de recovery que devuelve toda la base de datos a un punto en el tiempo anterior, usando los flashback logs en la Fast Recovery Area. Requiere `STARTUP MOUNT` y se cierra con `OPEN RESETLOGS`. Más rápido que un restore RMAN completo para errores lógicos generalizados.

- **[SCN](/es/glossary/flashback-query/)** (System Change Number) — Contador interno de Oracle que avanza de forma monótona en cada commit. Identifica un punto preciso en la historia de la base de datos. Las operaciones Flashback usan el SCN como referencia temporal precisa, alternativa o complementaria al timestamp.

- **[RTO](/es/glossary/flashback-table/)** (Recovery Time Objective) — Tiempo máximo aceptable de indisponibilidad de un sistema tras un error o un desastre. Las funcionalidades Flashback reducen el RTO para errores lógicos de horas (restore desde backup) a minutos, sin necesitar ventanas de mantenimiento.
