---
categories:
- oracle
date: '2026-09-15'
description: Doce terabytes, cuatro horas de ventana. Cómo combinar Transportable
  Tablespaces y RMAN incremental para migrar Oracle 12.2 a 21c con downtime mínimo.
draft: false
image: oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la.cover.jpg
seoTitle: 'Migración Oracle 12.2 a 21c: TTS + RMAN incremental en 4 horas'
tags:
- oracle
- migration
- rman
- transportable-tablespaces
- multitenant
title: 'El sábado noche que nadie quiere: migración Oracle 12.2 a 21c en cuatro horas'
translationKey: oracle_12c_21c_su_12_tb_transportable_tablespaces_rman_incremental_e_la
webo_generated_at: 2026-09-04
webo_status: scheduled
---

## El sábado noche que nadie quiere

La petición había llegado unas semanas antes, en una de esas reuniones donde los números se presentan como si fueran detalles: "hay que migrar la base de datos Oracle de 12.2 a 21c, tenemos una ventana de mantenimiento el sábado noche, cuatro horas". Doce terabytes. Un servidor con ocho años de vida, fuera de soporte hardware. El nuevo servidor ya en el rack, Oracle 21c instalado — un CDB, porque en 21c no hay otra opción, y sobre esto volvemos en un momento.

Cuatro horas para doce terabytes.

Quien lleva un tiempo trabajando con Oracle ya sabe dónde está el problema: no en la base de datos, no en la versión, no en el hardware nuevo. Está en la matemática. Un Data Pump sobre doce terabytes, incluso con paralelismo agresivo y almacenamiento rápido, no termina en cuatro horas. No termina en ocho. Probablemente no termina en el fin de semana.

Lo que sigue es el razonamiento que llevó a una estrategia híbrida — transportable tablespaces cross-version más RMAN incremental — y los detalles de lo que pasó de verdad en las cuatro horas críticas. Los números son los reales, los comandos son los que se usaron, los problemas son los que solo aparecen cuando ya estás dentro.

---

## Por qué Data Pump no es la respuesta a esta escala

Data Pump es la herramienta adecuada para migraciones de hasta unos pocos cientos de gigabytes, o para export/import selectivos de esquemas concretos. Por encima de ese umbral, los límites se vuelven estructurales.

Con doce terabytes, el problema principal es el throughput de I/O. Data Pump exporta los datos serializando filas en formato propietario Oracle, y luego las reimporta reconstruyendo segmentos, índices y estadísticas. Incluso con `PARALLEL=16` y almacenamiento NVMe en ambos lados, el throughput efectivo rara vez supera los 3-4 GB/minuto en escenarios reales (no benchmarks). Doce terabytes a 4 GB/minuto: cincuenta horas. En el mejor de los casos.

Luego está el problema del espacio: hace falta un área de staging que contenga el export completo, más el espacio en el destino durante el import. Con doce terabytes de datos, hablamos de veinte o veinticinco terabytes de espacio temporal necesario entre las dos máquinas.

El último problema es la ventana: Data Pump no es incremental. Si el export arranca el viernes por la noche y la base de datos sigue recibiendo escrituras, al terminar el export los datos ya están parcialmente obsoletos. No existe un mecanismo nativo para sincronizar los cambios producidos durante el export.

---

## Las opciones reales para migraciones multi-terabyte

Cuando Data Pump queda descartado, las alternativas reales son cuatro [1]:

**RMAN Duplicate** — duplica la base de datos completa vía RMAN, incluyendo todos los ficheros físicos. Requiere espacio doble en el destino (o casi), pero es fiable y está bien documentado. El problema: con doce terabytes, incluso la fase de copia inicial requiere muchas horas, y no resuelve el problema de la ventana corta.

**Transportable Tablespaces (TTS)** — copia los datafiles directamente, sin serialización ni deserialización. Es el método más rápido para mover grandes volúmenes porque el throughput está limitado solo por la velocidad del canal de transferencia (red, almacenamiento compartido, cinta). La restricción histórica era el endianness: plataformas distintas (p. ej. Solaris SPARC → Linux x86) requerían conversión. Entre dos Linux x86_64, el problema no existe [2].

**Data Guard como puente** — se configura una standby database en la nueva máquina, se deja que la sincronización ocurra vía redo log (horas o días, sin impacto en el primario), y luego se ejecuta un failover controlado en la ventana de mantenimiento. Elegante, pero requiere que las versiones sean compatibles para el redo shipping — y entre 12c y 21c hay restricciones precisas.

**GoldenGate** — replicación lógica, máxima flexibilidad cross-version y cross-platform. Requiere licencia separada, configuración no trivial, y un período de calentamiento para la sincronización inicial. Para una migración one-shot con ventana definida, suele ser sobredimensionado.

---

## La estrategia elegida: TTS + RMAN incremental

La solución adoptada combina dos técnicas: transportable tablespaces para mover la masa de datos antes de la ventana, y RMAN incremental backup para sincronizar los cambios acumulados mientras tanto.

La idea de fondo es sencilla: si no puedo mover doce terabytes en cuatro horas, muevo once y medio en los días anteriores, y en las cuatro horas críticas muevo solo el delta.

El plan se articula en tres fases:

1. **Fase preparatoria** (días antes de la ventana): backup RMAN level 0 transportable **con la base de datos abierta y en escritura**, transferencia al nuevo servidor, restore como foreign datafile copy
2. **Fase de sincronización** (días y horas antes de la ventana): level 1 incrementales, siempre con la base de datos operativa, para reducir progresivamente el gap
3. **Ventana de downtime** (cuatro horas): tablespace en read-only, último incremental, plug-in de los metadatos en la PDB, apertura

La diferencia entre este plan y el que vendría de forma instintiva — poner las tablespace en read-only, copiarlas con calma y luego alinearlas — está toda en el primer punto, y es la razón por la que existe la cláusula `ALLOW INCONSISTENT`.

---

## Pre-check: lo que se descubre antes de tocar nada

Antes de mover un byte, hace falta un análisis de compatibilidad. Entre Oracle 12.2 y Oracle 21c hay casi diez años de versiones intermedias, y algunas cosas han cambiado de forma no retrocompatible.

**Character set**: verificar que origen y destino usen el mismo character set, o que el destino sea un superconjunto. Una migración TTS entre AL32UTF8 y WE8ISO8859P1 requiere conversión explícita y no es trivial.

```sql
-- En la base de datos origen (12c)
SELECT value FROM nls_database_parameters WHERE parameter = 'NLS_CHARACTERSET';
SELECT value FROM nls_database_parameters WHERE parameter = 'NLS_NCHAR_CHARACTERSET';
```

**Endianness**: en Linux x86_64 → Linux x86_64 no hay problemas. En migraciones cross-platform (p. ej. AIX → Linux), hace falta `RMAN CONVERT TABLESPACE`.

```sql
-- Verificación de plataforma
SELECT platform_name, endian_format FROM v$transportable_platform
WHERE endian_format = (SELECT endian_format FROM v$database);
```

**Arquitectura de destino**: es la restricción que determina la forma de toda la migración, y conviene descubrirla antes de pedir el servidor, no la semana antes de la ventana. **En Oracle 21c la arquitectura non-CDB ya no tiene soporte**: multitenant es la única arquitectura soportada [3]. Un 12.2 non-CDB no se convierte en un 21c non-CDB, porque ese destino ya no existe — se convierte en una **PDB dentro de un CDB 21c**. No es un detalle de empaquetado: cambia dónde aterrizan las tablespace, cómo se abre la base de datos, y qué comandos se usan en la ventana.

**Componentes deprecados**: el informe de pre-upgrade ya no se genera con un script SQL. A partir de Oracle 21c el Pre-Upgrade Information Tool (`preupgrade.jar`) ya no se distribuye, y sus funciones se han integrado en **AutoUpgrade** [4]:

```bash
# Con el home 21c disponible — solo análisis, no modifica nada
java -jar $ORACLE_HOME_21C/rdbms/admin/autoupgrade.jar \
  -preupgrade "target_version=21,dir=/tmp/preupg" -mode analyze
```

El informe señala objetos inválidos, parámetros obsoletos y componentes que hay que eliminar antes del upgrade. Entre los más habituales en el paso 12.2 → 21c: `SQLNET.ALLOWED_LOGON_VERSION` (deprecado), algunas vistas de compatibilidad, y las políticas de auditoría — sobre la auditoría volvemos más adelante, porque es el punto donde circula más desinformación.

`-mode analyze` es de solo lectura: se puede lanzar en producción, en horario laboral, semanas antes. Es lo que conviene hacer primero, y es lo que casi siempre se hace demasiado tarde.

**Tablespace SYSTEM y SYSAUX**: no son transportables. Permanecen en el origen; en el destino el diccionario es el de la PDB, creado ya a nivel 21c por el CDB que la aloja.

---

## El plan paso a paso

El punto del que depende todo: **las tablespace permanecen en lectura y escritura hasta el último paso**. Es exactamente la razón por la que existe el backup incremental `FOR TRANSPORT`: el read-only solo hace falta para el backup final, el que cierra la ventana. Quien pone las tablespace en read-only al principio, para copiarlas con calma en los días anteriores, acaba de desplazar el downtime — no de reducirlo: una aplicación que no puede escribir está parada, tanto si la base de datos está abierta como si no.

### Fase 1 — Copia inicial en caliente (días antes)

Primero la self-containment: ningún objeto en las tablespace a transportar puede depender de objetos fuera de ellas.

```sql
-- En el origen
EXECUTE DBMS_TTS.TRANSPORT_SET_CHECK('DATA_01,DATA_02,IDX_01', TRUE);
SELECT * FROM transport_set_violations;
```

Si `transport_set_violations` está vacía, se continúa. El backup level 0 se toma **con la base de datos abierta y en escritura**, con `FOR TRANSPORT ALLOW INCONSISTENT` [1]: es la cláusula que autoriza a RMAN a producir un backset transportable desde tablespace no consistentes entre sí, que se realinearán con los incrementales posteriores.

```bash
rman target /
BACKUP INCREMENTAL LEVEL 0
  FOR TRANSPORT ALLOW INCONSISTENT
  TABLESPACE DATA_01, DATA_02, IDX_01
  FORMAT '/backup/rman/xtts_l0_%U';
```

El backset se transfiere al nuevo servidor vía `rsync` o replicación de almacenamiento. Con doce terabytes sobre red 10GbE la transferencia requiere unas tres o cuatro horas. **Mientras tanto la base de datos origen trabaja con normalidad**: ninguna tablespace está en read-only, las aplicaciones escriben, y los cambios que se acumulan son exactamente el delta que recuperarán los incrementales.

En el destino, los datafiles se materializan como *foreign datafile copy*:

```bash
# En el destino (CDB 21c, conectado a la PDB de destino)
rman target /
RESTORE FOREIGN TABLESPACE DATA_01, DATA_02, IDX_01 TO NEW
  FROM BACKUPSET '/backup/rman/xtts_l0_1_1';
```

### Fase 2 — Sincronización incremental

En los días que separan la copia inicial de la ventana se ejecutan uno o más level 1, siempre con la base de datos en escritura. Cada pasada reduce el gap: el primer incremental puede valer varios cientos de gigabytes; el último antes de la ventana, típicamente unas pocas decenas.

```bash
# En el origen — base de datos siempre operativa
BACKUP INCREMENTAL LEVEL 1
  FOR TRANSPORT ALLOW INCONSISTENT
  TABLESPACE DATA_01, DATA_02, IDX_01
  FORMAT '/backup/rman/xtts_l1_%U';
```

En el destino, cada backset se aplica a los foreign datafile copy ya presentes, **uno a uno y en el orden en que se produjo**:

```bash
# En el destino — un solo backupset por RECOVER
RECOVER FOREIGN DATAFILECOPY '/u02/oradata/pdb1/data_01.dbf',
                             '/u02/oradata/pdb1/data_02.dbf',
                             '/u02/oradata/pdb1/idx_01.dbf'
  FROM BACKUPSET '/backup/rman/xtts_l1_2_1';
```

Atención a una limitación que no se descubre leyendo, sino chocando contra ella: **no se pueden aplicar varios backupsets en un solo `RECOVER`**. Cada incremental es un comando independiente, en secuencia. Un script que los encadena en un único comando falla, y lo hace en el peor momento.

### Fase 3 — La ventana de cuatro horas

Las 23:00 del sábado. El origen se cierra a las aplicaciones:

```sql
ALTER SYSTEM ENABLE RESTRICTED SESSION;
```

**Solo ahora** las tablespace pasan a read-only — es el paso que congela los datos y abre la ventana:

```sql
ALTER TABLESPACE data_01 READ ONLY;
ALTER TABLESPACE data_02 READ ONLY;
ALTER TABLESPACE idx_01 READ ONLY;
-- repetir para todas las tablespace aplicativas
```

El último incremental se toma ahora, **sin** `ALLOW INCONSISTENT` (las tablespace ya son consistentes) y con `DATAPUMP FORMAT`, que hace que RMAN produzca también el dump de metadatos junto al backset:

```bash
rman target /
BACKUP INCREMENTAL LEVEL 1
  FOR TRANSPORT
  DATAPUMP FORMAT '/backup/rman/xtts_meta.bck'
  TABLESPACE DATA_01, DATA_02, IDX_01
  FORMAT '/backup/rman/xtts_l1_final_%U';
```

Contiene solo los cambios de las últimas horas — típicamente pocos gigabytes. Transferencia al destino y apply final:

```bash
# En el destino
RECOVER FOREIGN DATAFILECOPY '/u02/oradata/pdb1/data_01.dbf',
                             '/u02/oradata/pdb1/data_02.dbf',
                             '/u02/oradata/pdb1/idx_01.dbf'
  FROM BACKUPSET '/backup/rman/xtts_l1_final_3_1';
```

Queda el plug-in de los metadatos en la PDB de destino. Data Pump necesita un *directory object* — no un path del filesystem — y la lista completa de datafiles:

```sql
-- En el destino, dentro de la PDB
CREATE DIRECTORY dump_dir AS '/backup/rman';
```

```bash
impdp system/***@pdb1 \
  DIRECTORY=dump_dir \
  DUMPFILE=tts_export.dmp \
  LOGFILE=tts_import.log \
  TRANSPORT_TABLESPACES=DATA_01,DATA_02,IDX_01 \
  TRANSPORT_DATAFILES='/u02/oradata/pdb1/data_01.dbf','/u02/oradata/pdb1/data_02.dbf','/u02/oradata/pdb1/idx_01.dbf'
```

El `DUMPFILE` es el producido en el origen con el export de metadatos TTS, que se lanza después de poner las tablespace en read-only:

```bash
# En el origen, con las tablespace ya en read-only
expdp system/*** \
  DIRECTORY=dump_dir \
  DUMPFILE=tts_export.dmp \
  LOGFILE=tts_export.log \
  TRANSPORT_TABLESPACES=DATA_01,DATA_02,IDX_01 \
  TRANSPORT_FULL_CHECK=Y
```

En este punto las tablespace están en la PDB, que se abre y vuelve a escritura:

```sql
ALTER PLUGGABLE DATABASE pdb1 OPEN;
ALTER TABLESPACE data_01 READ WRITE;
ALTER TABLESPACE data_02 READ WRITE;
ALTER TABLESPACE idx_01 READ WRITE;
```

No hay `dbupgrade` en este recorrido: el diccionario de datos no se migra, porque es el de la PDB — creado ya a nivel 21c por el CDB que la aloja. Es una diferencia que vale la pena tener presente cuando se comparan los tiempos con los de un upgrade in place, donde la fase que domina es precisamente el upgrade del diccionario.

---

## Lo que los manuales no dicen

Cuatro problemas que solo aparecen cuando ya estás dentro de la ventana.

**Password file**: el formato en sí no cambia — `12.2` es el valor por defecto tanto en 12.2 como en 21c. Lo que cambia es la tolerancia: en 21c el parámetro `IGNORECASE` ya no tiene soporte y los password files son siempre case-sensitive [6]. Un password file heredado de un entorno que convivía con contraseñas case-insensitive deja de dejar entrar a los usuarios administrativos, y ocurre en el primer `sqlplus sys as sysdba` remoto — es decir, en el peor momento. Se regenera en el destino antes de la apertura:

```bash
orapwd file=$ORACLE_HOME/dbs/orapwCDB1 password=<sys_password> format=12.2
```

**Auditoría, y lo que se lee por ahí**: la versión que circula es "en 21c la auditoría tradicional ya no existe". No es así, y la diferencia importa cuando se planifica. En 21c el modo por defecto sigue siendo el **mixed mode** — unified auditing activo junto a la auditoría tradicional — exactamente igual que desde 12c en adelante; la auditoría tradicional está **deprecada** en 21c y **sin soporte** solo a partir de 23c [5]. El *pure* unified auditing no es un parámetro: se obtiene reenlazando el binario Oracle con `uniaud_on` y reiniciando la instancia. En la práctica: la migración no obliga a rehacer las políticas de auditoría esa noche, pero la factura llega en la siguiente release — y conviene planificar la conversión, no descubrirla cuando ya es obligatoria.

**Auto-Indexing**: Oracle 21c tiene Auto-Indexing habilitado (introducido en 19c). Si no se quiere que Oracle empiece a crear índices automáticamente en la nueva base de datos, hay que deshabilitarlo explícitamente:

```sql
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE','OFF');
```

**El CDB no es una decisión que se puede aplazar**: quien viene de 12.2 tiende a tratar multitenant como una decisión arquitectónica que se puede tomar con calma, quizás en la siguiente release. En 21c esa calma no existe: el non-CDB ya no tiene soporte, así que el destino es una PDB y punto. La consecuencia operativa es que el CDB hay que crearlo y probarlo **antes** de la ventana, con su `db_name`, sus parámetros de memoria, sus servicios — y hay que trasladar a la PDB los objetos que en la base de datos antigua vivían fuera de las tablespace transportadas: perfiles, roles, usuarios, directory objects, DB links, jobs del scheduler. No viajan con el TTS, y son la partida que más a menudo se descubre que falta el lunes por la mañana.

---

## Los números de la noche

La distinción que importa es entre lo que ocurrió **antes**, con la base de datos en producción, y lo que ocurrió **dentro** de la ventana. Solo la segunda tabla es downtime.

**Fuera de la ventana — base de datos abierta, aplicaciones operativas**

| Fase | Duración |
|---|---|
| Backup RMAN level 0 `FOR TRANSPORT ALLOW INCONSISTENT` | 1h 15min |
| Transferencia del backset (11,8 TB vía rsync sobre 10GbE) | 3h 40min |
| `RESTORE FOREIGN TABLESPACE` en el destino | 48 min |
| Level 1 intermedios de los días siguientes + apply | 1h 05min |
| **Total trabajo preparatorio** | **6h 48min** |

**Dentro de la ventana — downtime aplicativo**

| Fase | Duración |
|---|---|
| Restricted session + tablespace en read-only | 9 min |
| Último level 1 `FOR TRANSPORT` + `DATAPUMP` (delta ~180 GB) | 22 min |
| Export de metadatos TTS en el origen | 12 min |
| Transferencia del delta + dump al destino | 25 min |
| `RECOVER FOREIGN DATAFILECOPY` final | 18 min |
| `impdp` plug-in de los metadatos en la PDB | 12 min |
| Apertura de la PDB + tablespace en read-write | 4 min |
| Recreación de objetos no transportados (usuarios, roles, DB links, jobs) | 35 min |
| Estadísticas del diccionario + recompilación de objetos inválidos | 45 min |
| Validación y smoke test aplicativo | 50 min |
| **Total ventana de downtime** | **3h 52min** |

Ocho minutos de margen sobre las cuatro horas. No es mucho, pero fue suficiente.

Vale la pena mirar las dos tablas juntas: el trabajo total fue de casi once horas, de las cuales menos de cuatro fueron visibles para el usuario. No hicimos la migración más rápida — la desplazamos casi entera fuera de la ventana. Es lo único que este método sabe hacer, y era todo lo que se necesitaba.

---

## Validación: los controles que no se saltan

Tras la apertura de la PDB, la validación no es opcional. Cuatro controles en el orden correcto — todos hay que ejecutarlos **dentro de la PDB**, no en el root del CDB, porque si no se está mirando la base de datos equivocada:

```sql
ALTER SESSION SET CONTAINER = pdb1;
```

**Objetos inválidos**: el plug-in de los metadatos puede dejar objetos aplicativos inválidos, típicamente por dependencias hacia objetos aún no recreados. `utl_recomp` los recompila:

```sql
EXECUTE UTL_RECOMP.RECOMP_SERIAL();
-- o en paralelo
EXECUTE UTL_RECOMP.RECOMP_PARALLEL(4);
```

**Violaciones del plug-in**: es el control específico de este recorrido, y no tiene equivalente en un upgrade in place. `PDB_PLUG_IN_VIOLATIONS` lista lo que el CDB encontró incompatible al acoger la PDB — opciones no instaladas, parámetros por debajo del umbral, componentes ausentes:

```sql
SELECT name, cause, type, status, message
FROM pdb_plug_in_violations
WHERE status <> 'RESOLVED'
ORDER BY time;
```

Las filas de tipo `ERROR` hay que resolverlas antes de declarar cerrada la migración; las de tipo `WARNING` hay que leerlas una a una, no archivarlas en bloque.

**Estadísticas del optimizer**: las estadísticas del diccionario hay que regenerarlas. Las estadísticas de los objetos aplicativos se pueden importar desde el origen o regenerar:

```sql
EXECUTE DBMS_STATS.GATHER_DICTIONARY_STATS;
EXECUTE DBMS_STATS.GATHER_FIXED_OBJECTS_STATS;
```

**Verificación de componentes**: todos los componentes Oracle deben estar en estado `VALID`:

```sql
SELECT comp_name, version, status FROM dba_registry ORDER BY comp_name;
```

Cualquier componente en estado `INVALID` o `UPGRADED` (en lugar de `VALID`) requiere atención antes de declarar completada la migración. En una PDB recién poblada vía TTS, el registro refleja el CDB que la aloja: si algo está inválido ahí, el problema es del contenedor, no del transporte.

---

## Lo que queda del runbook

La migración salió adelante. La PDB lleva en producción desde el lunes por la mañana, y las aplicaciones no se dieron cuenta de nada — o casi: un par de consultas con hints obsoletos requirieron revisión en los días siguientes, porque el optimizer de 21c tiene estadísticas más precisas y elige planes distintos.

Lo que vale la pena llevarse no es la técnica concreta — TTS más RMAN incremental es una estrategia documentada, no una invención. Es el razonamiento que precede a la elección: entender por qué Data Pump no funciona a esa escala, entender cuáles son las restricciones reales (ventana, espacio, arquitectura de destino), y elegir la combinación de herramientas que las respeta. La restricción que más pesó no fue ni siquiera técnica en sentido estricto: fue descubrir a tiempo que el non-CDB ya no existía como destino. Descubrirlo tarde no alarga la ventana — cambia el proyecto.

La parte más larga no fue la noche del sábado. Fue la semana anterior: los pre-checks con AutoUpgrade, las pruebas en el destino con un subconjunto de datos, el ensayo del plug-in sobre una PDB de prueba, la verificación de que cada paso del runbook producía la salida esperada. Cuando se llega a la ventana de cuatro horas con un runbook ya probado, las sorpresas son manejables. Cuando se llega sin haberlo probado, esos ocho minutos de margen se convierten en cero muy rápido.

---

## Fontes ufficiali

1. Oracle Database Backup and Recovery User's Guide 21c — [Transporting Data Across Platforms](https://docs.oracle.com/en/database/oracle/oracle-database/21/bradv/rman-transporting-data-across-platforms.html) (`BACKUP … FOR TRANSPORT ALLOW INCONSISTENT`, `RESTORE FOREIGN TABLESPACE`, `RECOVER FOREIGN DATAFILECOPY`)
2. Oracle Database Administrator's Guide 21c — [Transporting Tablespaces Between Databases](https://docs.oracle.com/en/database/oracle/oracle-database/21/admin/transporting-data.html)
3. Oracle Database Upgrade Guide 21c — [Manual Non-CDB Release Upgrades to Multitenant Architecture](https://docs.oracle.com/en/database/oracle/oracle-database/21/upgrd/upgrade-scenarios-non-cdb-oracle-databases.html) (fin del soporte para la arquitectura non-CDB)
4. Oracle Database Upgrade Guide 21c — [Using the Pre-Upgrade Information Tool](https://docs.oracle.com/en/database/oracle/oracle-database/21/upgrd/using-preupgrade-information-tool-for-oracle-database.html) (`preupgrade.jar` ya no distribuido, funciones integradas en AutoUpgrade)
5. Oracle Database Security Guide 21c — [Introduction to Auditing](https://docs.oracle.com/en/database/oracle/oracle-database/21/dbseg/introduction-to-auditing.html) (mixed mode por defecto, `uniaud_on` para el pure unified auditing)
6. Oracle Database Administrator's Reference 21c — [Creating and Populating Password Files](https://docs.oracle.com/en/database/oracle/oracle-database/21/ntqrf/creating-and-populating-password-files.html) (`format`, fin del soporte de `IGNORECASE`)

---

## Glosario
- **[Transportable Tablespaces (TTS)](/es/glossary/transportable-tablespaces/)** — técnica Oracle que permite mover tablespace entre bases de datos copiando los datafiles físicos e importando solo los metadatos mediante Data Pump. Mucho más rápido que un export/import completo con grandes volúmenes.

- **[RMAN Incremental Backup](/es/glossary/transportable-tablespaces/)** — backup RMAN que registra solo los bloques modificados desde el último backup de nivel igual o superior. Level 0 es la base completa, level 1 es el delta. Se usa en migración para sincronizar el gap entre la copia inicial y la ventana de downtime.

- **[AutoUpgrade](/es/glossary/transportable-tablespaces/)** — utilidad Java (`autoupgrade.jar`) que desde Oracle 21c es la herramienta única para análisis pre-upgrade, correcciones y el upgrade propiamente dicho. Con `-preupgrade … -mode analyze` produce en modo solo lectura el informe que antes se obtenía con `preupgrade.jar`, ya no distribuido.

- **[Foreign datafile copy](/es/glossary/rman-incremental-backup/)** — datafile que RMAN materializa en la base de datos de destino a partir de un backset transportable, antes de que las tablespace sean conectadas. Es el objeto sobre el que actúan `RESTORE FOREIGN TABLESPACE` y `RECOVER FOREIGN DATAFILECOPY` en el transporte incremental.

- **[Unified Auditing](/es/glossary/transportable-tablespaces/)** — framework de auditoría introducido en 12c que consolida los logs (base de datos, fine-grained, SYSDBA) en la estructura `AUDSYS`. En 21c convive con la auditoría tradicional en *mixed mode*, que sigue siendo el valor por defecto; el *pure* unified auditing requiere reenlazar el binario con `uniaud_on`.

- **[Auto-Indexing](/es/glossary/rman-incremental-backup/)** — funcionalidad Oracle (disponible desde 19c, configurable en 21c) que analiza el workload y crea automáticamente índices invisibles, los valida y los hace visibles si mejoran el rendimiento. Hay que deshabilitarlo explícitamente si no se desea en producción.
