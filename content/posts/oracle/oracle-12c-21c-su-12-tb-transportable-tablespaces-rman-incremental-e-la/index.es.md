---
title: "Oracle 12c → 21c en 12 TB: transportable tablespaces, RMAN incremental y la ventana del sábado noche"
date: 2099-12-31
draft: true
translationKey: "oracle_12c_21c_su_12_tb_transportable_tablespaces_rman_incremental_e_la"
tags: []
categories: ["oracle"]
image: "oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la.cover.jpg"
webo_status: da_tradurre
webo_generated_at: 2026-09-04
---

```
---
title: "El sábado por la noche que nadie quiere"
seoTitle: "Migración Oracle 12c a 21c: TTS + RMAN incremental en 4 horas"
description: "12 TB, una ventana de 4 horas, Oracle 12c a 21c. La estrategia híbrida con Transportable Tablespaces y RMAN incremental que funcionó con 8 minutos de margen."
tags: ["oracle", "migration", "rman", "transportable-tablespaces", "upgrade"]
---
```

## El sábado por la noche que nadie quiere

La petición había llegado unas semanas antes, en una de esas reuniones donde los números se presentan como si fueran detalles: "hay que migrar la base de datos Oracle de 12c a 21c, tenemos una ventana de mantenimiento el sábado por la noche, cuatro horas". Doce terabytes. Un servidor con ocho años de vida, fuera de soporte hardware. El nuevo servidor ya en el rack, Oracle 21c instalado, listo.

Cuatro horas para doce terabytes.

Quien lleva un tiempo trabajando con Oracle ya sabe dónde está el problema: no en la base de datos, no en la versión, no en el hardware nuevo. Está en la matemática. Un Data Pump sobre doce terabytes, incluso con paralelismo agresivo y almacenamiento rápido, no termina en cuatro horas. No termina en ocho. Probablemente no termina en el fin de semana.

Lo que sigue es el razonamiento que llevó a una estrategia híbrida — transportable tablespaces cross-version más RMAN incremental — y los detalles de lo que ocurrió de verdad en las cuatro horas críticas. Los números son los reales, los comandos son los que se usaron, los problemas son los que solo aparecen cuando ya estás dentro.

---

## Por qué Data Pump no es la respuesta a esta escala

Data Pump es la herramienta adecuada para migraciones de hasta unos pocos cientos de gigabytes, o para export/import selectivos de esquemas concretos. Por encima de ese umbral, las limitaciones se vuelven estructurales.

Con doce terabytes, el problema principal es el throughput de I/O. Data Pump exporta los datos serializando filas en formato propietario Oracle, y luego las reimporta reconstruyendo segmentos, índices y estadísticas. Incluso con `PARALLEL=16` y almacenamiento NVMe en ambos lados, el throughput efectivo raramente supera los 3-4 GB/minuto en escenarios reales (no benchmarks). Doce terabytes a 4 GB/minuto: cincuenta horas. En el mejor de los casos.

Está también el problema del espacio: hace falta un área de staging que contenga el export completo, más el espacio en el destino durante el import. Con doce terabytes de datos, estamos hablando de veinte o veinticinco terabytes de espacio temporal necesario entre las dos máquinas.

El último problema es la ventana: Data Pump no es incremental. Si el export arranca el viernes por la noche y la base de datos sigue recibiendo escrituras, al terminar el export los datos ya están parcialmente obsoletos. No existe un mecanismo nativo para sincronizar los cambios ocurridos durante el export.

---

## Las opciones reales para migraciones multi-terabyte

Cuando Data Pump queda descartado, las alternativas reales son cuatro [1]:

**RMAN Duplicate** — duplica la base de datos completa vía RMAN, incluyendo todos los ficheros físicos. Requiere espacio doble en el destino (o casi), pero es fiable y está bien documentado. El problema: con doce terabytes, incluso la fase de copia inicial requiere muchas horas, y no resuelve el problema de la ventana corta.

**Transportable Tablespaces (TTS)** — copia los datafiles directamente, sin serialización ni deserialización. Es el método más rápido para mover grandes volúmenes porque el throughput solo está limitado por la velocidad del canal de transferencia (red, almacenamiento compartido, cinta). La restricción histórica era el endianness: plataformas distintas (p. ej. Solaris SPARC → Linux x86) requerían conversión. Entre dos Linux x86_64, el problema no existe [2].

**Data Guard como puente** — se configura una standby database en la nueva máquina, se deja que la sincronización ocurra vía redo log (horas o días, sin impacto en el primario), y luego se ejecuta un failover controlado en la ventana de mantenimiento. Elegante, pero requiere que las versiones sean compatibles para el redo shipping — y entre 12c y 21c hay restricciones precisas.

**GoldenGate** — replicación lógica, máxima flexibilidad cross-version y cross-platform. Requiere licencia separada, un setup no trivial, y un período de warm-up para la sincronización inicial. Para una migración one-shot con ventana definida, suele ser sobredimensionado.

---

## La estrategia elegida: TTS + RMAN incremental

La solución adoptada combina dos técnicas: transportable tablespaces para mover la masa de datos antes de la ventana, y RMAN incremental backup para sincronizar los cambios acumulados en el ínterin.

La idea de fondo es sencilla: si no puedo mover doce terabytes en cuatro horas, muevo once y medio en los días anteriores, y en las cuatro horas críticas muevo solo el delta.

El plan se articula en tres fases:

1. **Fase preparatoria** (días antes de la ventana): copia de los datafiles en modo read-only vía TTS, transferencia al nuevo servidor
2. **Fase de sincronización** (horas antes de la ventana): RMAN incremental backup en el origen, restore en el destino, para reducir el gap
3. **Ventana de downtime** (cuatro horas): último incremental, conversión final, apertura de la base de datos 21c

---

## Pre-check: lo que se descubre antes de tocar nada

Antes de mover un solo byte, hace falta un análisis de compatibilidad. Entre Oracle 12.2 y Oracle 21c hay casi diez años de versiones intermedias, y algunas cosas han cambiado de forma no retrocompatible.

**Character set**: verificar que origen y destino usen el mismo character set, o que el destino sea un superconjunto. Una migración TTS entre AL32UTF8 y WE8ISO8859P1 requiere conversión explícita y no es trivial.

```sql
-- En la base de datos origen (12c)
SELECT value FROM nls_database_parameters WHERE parameter = 'NLS_CHARACTERSET';
SELECT value FROM nls_database_parameters WHERE parameter = 'NLS_NCHAR_CHARACTERSET';
```

**Endianness**: en Linux x86_64 → Linux x86_64 no hay problema. En migraciones cross-platform (p. ej. AIX → Linux), hace falta `RMAN CONVERT TABLESPACE`.

```sql
-- Verificación de plataforma
SELECT platform_name, endian_format FROM v$transportable_platform
WHERE endian_format = (SELECT endian_format FROM v$database);
```

**Componentes deprecados**: Oracle 21c ha eliminado o deprecado algunas funcionalidades de 12c. El script `utlupgrd.sql` (o su sucesor `dbupgrade`) genera un informe de pre-upgrade [3]:

```bash
# En el origen, con el Oracle 21c home ya disponible
$ORACLE_HOME_21C/rdbms/admin/preupgrd.sql
```

El informe señala objetos inválidos, parámetros obsoletos y componentes que hay que eliminar antes del upgrade. Entre los más habituales en el paso 12c → 21c: `AUDIT_TRAIL` (sustituido por Unified Auditing), `SQLNET.ALLOWED_LOGON_VERSION` (deprecado), y algunas vistas de compatibilidad.

**Tablespace SYSTEM y SYSAUX**: no son transportables. Permanecen en el origen y se recrean en el destino mediante el proceso de upgrade estándar.

---

## El plan paso a paso

### Fase 1 — Preparación TTS (días antes)

Se ponen en read-only las tablespaces a transportar (excluidas SYSTEM, SYSAUX, TEMP, UNDO):

```sql
-- En el origen
ALTER TABLESPACE data_01 READ ONLY;
ALTER TABLESPACE data_02 READ ONLY;
ALTER TABLESPACE idx_01 READ ONLY;
-- repetir para todas las tablespaces aplicativas
```

Se verifica la self-containment — ningún objeto en las tablespaces a transportar debe tener dependencias sobre objetos fuera de ellas:

```sql
EXECUTE DBMS_TTS.TRANSPORT_SET_CHECK('DATA_01,DATA_02,IDX_01', TRUE);
SELECT * FROM transport_set_violations;
```

Si `transport_set_violations` está vacía, se procede con el export del metadata:

```bash
expdp system/*** TRANSPORT_TABLESPACES=DATA_01,DATA_02,IDX_01 \
  TRANSPORT_FULL_CHECK=Y \
  DUMPFILE=tts_export.dmp \
  LOGFILE=tts_export.log
```

Los datafiles físicos se copian al nuevo servidor vía `rsync` o replicación de almacenamiento. Con doce terabytes sobre red 10GbE, la transferencia requiere unas tres o cuatro horas. Mientras tanto la base de datos origen sigue funcionando: las tablespaces en read-only solo reciben lecturas, las escrituras van a las tablespaces que siguen en read-write (SYSTEM, SYSAUX, y las tablespaces aplicativas excluidas del TTS).

### Fase 2 — Sincronización incremental

En las horas siguientes a la transferencia inicial, las tablespaces del origen se vuelven a poner en read-write (la base de datos tiene que volver a estar operativa). A partir de ese momento, los cambios se acumulan como delta a sincronizar.

Se configura RMAN para backup incremental level 0 en el origen:

```bash
rman target /
BACKUP INCREMENTAL LEVEL 0 TABLESPACE DATA_01,DATA_02,IDX_01
FORMAT '/backup/rman/incr0_%U'
TAG 'PRE_MIGRATION_L0';
```

Este backup level 0 se transfiere al destino y se aplica sobre los datafiles ya copiados:

```bash
# En el destino (21c)
rman target /
CATALOG START WITH '/backup/rman/';
RECOVER TABLESPACE DATA_01,DATA_02,IDX_01
FROM TAG 'PRE_MIGRATION_L0';
```

En las horas siguientes se ejecutan backups incrementales level 1 periódicos para reducir progresivamente el gap. Cada level 1 es solo el delta desde el último backup — unos pocos gigabytes en lugar de terabytes.

### Fase 3 — La ventana de cuatro horas

Las 23:00 del sábado. La base de datos origen se pone en modo restricted:

```sql
ALTER SYSTEM ENABLE RESTRICTED SESSION;
```

Se ejecuta el último backup incremental level 1:

```bash
rman target /
BACKUP INCREMENTAL LEVEL 1 TABLESPACE DATA_01,DATA_02,IDX_01
FORMAT '/backup/rman/incr1_final_%U'
TAG 'FINAL_SYNC';
```

Este backup contiene solo los cambios de las últimas horas — típicamente unos pocos gigabytes. Transferencia al destino y apply:

```bash
# En el destino
RECOVER TABLESPACE DATA_01,DATA_02,IDX_01
FROM TAG 'FINAL_SYNC';
```

Las tablespaces se ponen en read-only en el origen (definitivamente esta vez), y se importa el metadata TTS en el destino:

```bash
impdp system/*** TRANSPORT_DATAFILES='/u01/oradata/data_01.dbf','/u01/oradata/data_02.dbf' \
  DUMPFILE=tts_export.dmp \
  LOGFILE=tts_import.log
```

En este punto las tablespaces están en el destino en Oracle 21c. Se ejecuta el proceso de upgrade del diccionario de datos:

```bash
$ORACLE_HOME/bin/dbupgrade -d $ORACLE_BASE/diag/rdbms -l /tmp/upgrade_log
```

---

## Lo que los manuales no cuentan

Cuatro problemas que solo aparecen cuando ya estás dentro de la ventana.

**Password file format**: Oracle 21c usa un formato de password file distinto al de 12c. Si se copia el password file del origen, la instancia 21c puede no reconocerlo. La solución es regenerarlo en el destino antes de abrir la base de datos:

```bash
orapwd file=$ORACLE_HOME/dbs/orapwORCL password=<sys_password> format=12.2
```

**Unified Auditing**: en Oracle 21c, Unified Auditing está habilitado por defecto y no se puede deshabilitar como en 12c. Si la base de datos origen usaba el antiguo `AUDIT_TRAIL=DB`, las políticas de auditoría hay que recrearlas en el nuevo framework. Esto no bloquea la migración, pero puede sorprender al equipo de aplicación el lunes por la mañana cuando los logs de auditoría tienen un formato diferente.

**Auto-Indexing**: Oracle 21c tiene Auto-Indexing habilitado (introducido en 19c). Si no se quiere que Oracle empiece a crear índices automáticamente en la nueva base de datos, hay que deshabilitarlo explícitamente:

```sql
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE','OFF');
```

**Conversión a PDB**: Oracle 21c todavía soporta bases de datos non-CDB, pero es la última versión en hacerlo. Si el plan futuro contempla la conversión a CDB/PDB (obligatoria a partir de Oracle 23c), es el momento de valorarlo. La conversión non-CDB → PDB se hace con `DBMS_PDB.DESCRIBE` y requiere una ventana separada — no hay que meterla en la misma noche.

---

## Los números de la noche

| Fase | Duración real |
|---|---|
| Export TTS metadata | 12 minutos |
| Transferencia datafiles (11,8 TB vía rsync sobre 10GbE) | 3h 40min |
| Backup RMAN level 0 | 1h 15min |
| Apply level 0 en el destino | 48 minutos |
| Backup RMAN level 1 (delta ~180 GB) | 22 minutos |
| Apply level 1 final | 14 minutos |
| Import TTS metadata en el destino | 8 minutos |
| dbupgrade (diccionario de datos) | 41 minutos |
| Validación post-migración | 35 minutos |
| **Total ventana de downtime** | **3h 52min** |

Ocho minutos de margen. No es mucho, pero fue suficiente.

---

## Validación: los controles que no se saltan

Tras abrir la base de datos 21c, la validación no es opcional. Cuatro controles en el orden correcto.

**Objetos inválidos**: el proceso de upgrade puede dejar objetos de sistema inválidos. `utl_recomp` los recompila:

```sql
EXECUTE UTL_RECOMP.RECOMP_SERIAL();
-- o en paralelo
EXECUTE UTL_RECOMP.RECOMP_PARALLEL(4);
```

**Scripts de diagnóstico post-upgrade**: Oracle proporciona `dbupgdiag.sql` para verificar el estado del diccionario de datos tras el upgrade [4]:

```bash
sqlplus / as sysdba @$ORACLE_HOME/rdbms/admin/dbupgdiag.sql
```

**Estadísticas del optimizer**: las estadísticas del diccionario de datos hay que regenerarlas en la nueva base de datos. Las estadísticas de los objetos aplicativos se pueden importar desde el origen o regenerar:

```sql
EXECUTE DBMS_STATS.GATHER_DICTIONARY_STATS;
EXECUTE DBMS_STATS.GATHER_FIXED_OBJECTS_STATS;
```

**Verificación de componentes**: todos los componentes Oracle deben estar en estado `VALID`:

```sql
SELECT comp_name, version, status FROM dba_registry ORDER BY comp_name;
```

Cualquier componente en estado `INVALID` o `UPGRADED` (en lugar de `VALID`) requiere atención antes de declarar la migración completada.

---

## Lo que queda del runbook

La migración salió adelante. La base de datos 21c lleva en producción desde el lunes por la mañana, y las aplicaciones no notaron nada — o casi: un par de consultas con hints obsoletos necesitaron revisión en los días siguientes, porque el optimizer de 21c tiene estadísticas más precisas y elige planes distintos.

Lo que vale la pena llevarse de aquí no es la técnica concreta — TTS más RMAN incremental es una estrategia documentada, no un invento. Es el razonamiento que precede a la elección: entender por qué Data Pump no funciona a esa escala, entender cuáles son las restricciones reales (ventana, espacio, versiones), y elegir la combinación de herramientas que respeta esas restricciones.

La parte más larga no fue la noche del sábado. Fue la semana anterior: los pre-checks, las pruebas en el destino con un subconjunto de datos, la simulación del proceso de upgrade sobre un clon, la verificación de que cada paso del runbook producía el output esperado. Cuando se llega a la ventana de cuatro horas con un runbook ya probado, las sorpresas son manejables. Cuando se llega sin haberlo probado, esos ocho minutos de margen se convierten en cero muy deprisa.

---

## Fuentes oficiales

1. Oracle Database Backup and Recovery User's Guide 21c — [Transportable Tablespaces](https://docs.oracle.com/en/database/oracle/oracle-database/21/bradv/rman-transporting-data-across-platforms.html)
2. Oracle Database Administrator's Guide 21c — [Transporting Tablespaces Between Databases](https://docs.oracle.com/en/database/oracle/oracle-database/21/admin/transporting-data.html)
3. Oracle Database Upgrade Guide 21c — [Pre-Upgrade Information Tool](https://docs.oracle.com/en/database/oracle/oracle-database/21/upgrd/using-preupgrade-information-tool-for-oracle-database.html)
4. Oracle Database Upgrade Guide 21c — [Post-Upgrade Status Tool](https://docs.oracle.com/en/database/oracle/oracle-database/21/upgrd/post-upgrade-status-tool-postupgrade-fixups-script.html)

---

## Glosario candidato

- **Transportable Tablespaces (TTS)** — técnica Oracle que permite mover tablespaces entre bases de datos copiando los datafiles físicos e importando solo el metadata vía Data Pump. Mucho más rápido que un export/import completo sobre grandes volúmenes.

- **RMAN Incremental Backup** — backup RMAN que registra solo los bloques modificados desde el último backup de nivel igual o superior. Level 0 es la base completa, level 1 es el delta. Se usa en migración para sincronizar el gap entre la copia inicial y la ventana de downtime.

- **dbupgrade** — utilidad Oracle (sucesora de `catupgrd.sql`) que actualiza el diccionario de datos del sistema durante un upgrade de versión. Recompila los componentes internos y lleva la base de datos al nivel de la nueva versión Oracle instalada.

- **Unified Auditing** — framework de auditoría Oracle introducido en 12c y obligatorio en 21c, que consolida todos los logs de auditoría (base de datos, fine-grained, SYSDBA) en una única estructura `AUDSYS`. Sustituye al antiguo parámetro `AUDIT_TRAIL`.

- **Auto-Indexing** — funcionalidad Oracle (disponible desde 19c, configurable en 21c) que analiza el workload y crea automáticamente índices invisibles, los valida, y los hace visibles si mejoran el rendimiento. Hay que deshabilitarlo explícitamente si no se desea en producción.
