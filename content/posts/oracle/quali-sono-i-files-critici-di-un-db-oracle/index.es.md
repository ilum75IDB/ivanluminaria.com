---
date: '2026-07-14'
draft: false
section: oracle
title: 'ORA-00205 alle tre di notte: capire i file critici Oracle prima di averne
  bisogno'
webo_generated_at: 2026-06-09
webo_status: scheduled
---

## La llamada

[3:08] El teléfono vibra en la mesita de noche. Es Paolo, DBA del cliente farmacéutico — Oracle 19c, trazabilidad de lotes, compliance regulatorio. La ventana de mantenimiento de storage había cerrado a las 2:30. Él había intentado el startup. La instancia no había arrancado.

Me lee el mensaje desde el móvil, voz plana pero con esa tensión sutil de quien sabe que el sistema está parado y aún no sabe por qué:

```text
ORA-00205: error in identifying control file
  '/u01/app/oracle/oradata/PHARMDB/control01.ctl'
```

Es la primera emergencia real que gestiona como guardia. No está mal preparado: conoce Oracle, sabe usar los comandos, ha leído la documentación del cliente. El punto es que esa documentación está escrita como referencia, no como método. Y en ese momento necesita un método.

---

## La fase MOUNT

[3:09] Lo primero que le pregunto no es "¿has comprobado los permisos?" ni "¿el listener está arriba?". Le pregunto: "¿en qué fase de startup se ha detenido Oracle?".

No es una pregunta retórica. Es el punto de partida de cualquier diagnóstico sobre una instancia que no arranca.

Oracle inicia una base de datos en tres fases distintas [1]:

**`NOMOUNT`** — Oracle asigna la SGA y arranca los procesos en background leyendo el **parameter file** (SPFILE o PFILE). En esta fase aún no conoce la base de datos física: solo sabe cómo configurar la instancia en memoria.

**`MOUNT`** — Oracle lee el **control file**. Aquí la instancia "descubre" la estructura física de la base de datos: qué datafiles existen, dónde están, cuál es la SCN actual, cuál es el estado de los redo logs. Solo después del MOUNT Oracle sabe qué está gestionando.

**`OPEN`** — Oracle verifica la consistencia de los **online redo log files** y los datafiles, aplica recovery si es necesario, y abre la base de datos a los usuarios.

La consecuencia práctica es directa: si el parameter file está corrupto o falta, Oracle no llega ni al NOMOUNT. Si el control file es inaccesible, la instancia se detiene en MOUNT. Si los redo logs están corruptos, el bloqueo ocurre en OPEN.

Conocer esta secuencia significa saber, leyendo un código ORA, en qué fase se detuvo todo — y por tanto qué archivo buscar primero, sin hipótesis a ciegas.

Paolo lo piensa un segundo. "ORA-00205 está en MOUNT. Entonces es el control file."

Exacto.

---

## El control file y el remount

[3:11] Le dicto las tres verificaciones a hacer en secuencia, en este orden:

**(a)** dame el path exacto del mensaje ORA-00205
**(b)** `ls -la` sobre ese path y dime propietario y permisos
**(c)** compara con el runbook pre-mantenimiento que habíamos escrito juntos el año anterior

Mientras Paolo abre el terminal, le explico por qué el control file es el punto crítico de esa fase.

El control file es un archivo binario que Oracle actualiza continuamente durante el funcionamiento. Contiene información que ningún otro archivo puede proporcionar [3]:

- el nombre de la base de datos (`db_name`)
- la lista de todos los datafiles con sus respectivos paths y status
- la lista de los online redo log files
- la SCN (System Change Number) actual — el "timestamp lógico" de la base de datos
- la información de checkpoint
- el catálogo de backups RMAN, cuando se usa RMAN con el control file como repositorio

Oracle no puede montar la base de datos sin control file: le faltaría la forma de saber qué datafiles pertenecen a la instancia, cuál es su estado y si la base de datos es consistente. Es una dependencia estructural.

Para verificar los control files en una instancia activa [4]:

```sql
SELECT name FROM v$controlfile;
```

En `oracle-node-01` con el SID `PHARMDB`, la salida con una configuración multiplexada es:

```text
NAME
--------------------------------------------------
/u01/app/oracle/oradata/PHARMDB/control01.ctl
/u02/app/oracle/fast_recovery_area/PHARMDB/control02.ctl
```

Dos copias, en paths físicamente separados. El multiplexing no es una opción: si el control file vive en un solo disco y ese disco tiene un problema, la base de datos no abre y el recovery se vuelve significativamente más complejo. Se configura en el parameter file:

```text
control_files = '/u01/app/oracle/oradata/PHARMDB/control01.ctl',
                '/u02/app/oracle/fast_recovery_area/PHARMDB/control02.ctl'
```

Oracle escribe de forma síncrona en todas las copias. Si una se vuelve inaccesible, registra el error y continúa funcionando con las copias restantes — mientras al menos una esté disponible.

**Nota sobre ASM**: en entornos que usan Automatic Storage Management los paths físicos se reemplazan por paths lógicos del tipo `+DATA/PHARMDB/CONTROLFILE/current.260.1234567890`. El concepto es idéntico — siguen siendo los mismos tres tipos de archivos críticos — solo cambia la gestión física, delegada a ASM. Los comandos SQL de verificación son los mismos; solo cambia la salida.

[3:14] Paolo hace el `ls -la`. Los permisos han cambiado: antes del mantenimiento el propietario era `oracle:oinstall`, ahora es `root:root`. Oracle no puede leer el archivo.

El control file estaba físicamente intacto. El equipo de storage había remontado el filesystem `/u01` con permisos distintos tras el mantenimiento, y Oracle no podía abrirlo.

Le digo de inmediato: "ok, llamamos a storage. No toques nada tú, nada de `chmod` a mano." No porque no sepa hacerlo — sabría — sino porque en un sistema de compliance regulatorio cualquier modificación manual fuera de procedimiento se convierte en un problema documental además de técnico. El fix tiene que pasar por el equipo de storage, con ticket abierto y trazado.

Mientras esperamos que storage se conecte, le hago notar algo: si el `ls -la` hubiera mostrado el archivo intacto y accesible, el siguiente paso habría sido subir una fase, al parameter file. Error distinto, fase distinta: típicamente `ORA-01078` (failure in processing system parameters) o `LRM-00109` (could not open parameter file), y en ese caso Oracle no habría llegado ni al NOMOUNT.

El parameter file es el punto de partida absoluto: Oracle lo lee antes que cualquier otra cosa para saber cómo configurar la instancia en memoria, y sobre todo para saber dónde se encuentran los control files. El parámetro `control_files` que indica los paths está contenido precisamente ahí.

Existen dos variantes [2]:

**PFILE** (`init<SID>.ora`) — archivo de texto, editable con cualquier editor. Requiere un reinicio para aplicar los cambios. Útil en entornos de desarrollo o como backup legible de los parámetros.

**SPFILE** (`spfile<SID>.ora`) — archivo binario, gestionado por Oracle. Permite cambios en caliente con `ALTER SYSTEM SET` sin reiniciar la instancia. En producción se usa casi siempre el SPFILE.

El orden de búsqueda de Oracle es preciso: busca primero el SPFILE en el path por defecto, luego el PFILE. En Linux/Unix:

```bash
# SPFILE (por defecto)
$ORACLE_HOME/dbs/spfilePHARMDB.ora

# PFILE (fallback)
$ORACLE_HOME/dbs/initPHARMDB.ora
```

Para verificar qué parameter file está en uso en una instancia activa:

```sql
-- Si VALUE está vacío, Oracle está usando un PFILE
SHOW PARAMETER spfile;
```

Paolo toma nota. En nuestro caso el parameter file estaba bien — el problema estaba en una fase más adelante — y el modelo mental ahora está completo.

---

## El startup completo

[3:23] Storage aplica `chmod 640` y restaura `oracle:oinstall` como propietario en los archivos de `/u01`. Paolo reinicia la instancia.

[3:38] La instancia supera el MOUNT. Luego se detiene en OPEN con un warning sobre los redo logs.

Le explico qué está mirando.

Los online redo log files son el último elemento de la tríada crítica. Cada modificación que ocurre en la base de datos — un `INSERT`, un `UPDATE`, un `DELETE` — se escribe primero en los redo logs, y solo después (de forma asíncrona) en los datafiles. Este mecanismo se llama **write-ahead logging**: si el sistema cae antes de que los datos se escriban en los datafiles, Oracle puede reconstruir los cambios leyendo los redo logs. Sin redo logs, Oracle no puede garantizar la consistencia de la base de datos en caso de crash — y por eso, si están corruptos o faltan, la base de datos no abre [5].

Los redo logs están organizados en **grupos**. Oracle escribe de forma circular: llena el grupo 1, pasa al 2, luego al 3, luego vuelve al grupo 1. Cada grupo puede contener uno o más **miembros** — copias idénticas del log en paths distintos, para redundancia.

```sql
-- Estado de los grupos redo log
SELECT group#, members, status, bytes/1024/1024 AS mb
FROM v$log;

-- Paths físicos de los miembros
SELECT group#, member
FROM v$logfile
ORDER BY group#;
```

La salida para `PHARMDB` con tres grupos de 200MB:

```text
GROUP#  MEMBERS  STATUS    MB
------  -------  --------  ---
     1        1  INACTIVE  200
     2        1  CURRENT   200
     3        1  INACTIVE  200
```

`CURRENT` es el grupo en el que Oracle está escribiendo en ese momento. `INACTIVE` indica grupos ya ciclados, que ya no son necesarios para el recovery de la instancia actual. `ACTIVE` señalaría un grupo todavía necesario para el recovery pero que ya no es el corriente — un estado que requiere atención antes de cualquier operación sobre los logs.

Los paths físicos en `oracle-node-01`:

```bash
/u01/app/oracle/oradata/PHARMDB/redo01.log   # GROUP 1, 200MB
/u01/app/oracle/oradata/PHARMDB/redo02.log   # GROUP 2, 200MB
/u01/app/oracle/oradata/PHARMDB/redo03.log   # GROUP 3, 200MB
```

Los errores típicos cuando los redo logs son inaccesibles o están corruptos:

```text
ORA-00313: open failed for members of log group 1 of thread 1
ORA-00312: online log 1 thread 1: '/u01/app/oracle/oradata/PHARMDB/redo01.log'
```

En este caso no era una criticidad real. El remount de `/u01` había tocado también el directorio de los redo logs, y Oracle había registrado un warning durante el primer intento de apertura. Paolo verifica el status de los grupos con `v$log`, comprueba los permisos de los archivos físicos: todo en orden tras el `chmod` aplicado por storage. El warning ya había desaparecido.

[3:42] Base de datos OPEN. La trazabilidad de lotes vuelve a estar online.

---

## Ficha de referencia

Paolo me llama justo después. "Ivan, gracias de verdad, solo no habría llegado a tiempo. He leído la documentación del cliente pero está escrita como referencia, no como método. Ahora he entendido la secuencia, y he entendido por qué hace falta el runbook."

Le digo que se apunte dos tablas en el cuaderno — las que tendríamos que haber puesto en el runbook desde el principio.

**Paths estándar y convenciones OFA**

Oracle recomienda una convención de layout llamada **OFA** (Optimal Flexible Architecture) que organiza los archivos de la instancia de forma predecible. Seguirla no es obligatorio, y en producción hace que el mantenimiento ordinario y el recovery sean significativamente más manejables.

| Archivo | Path típico Linux (OFA) | Comando de verificación |
|---|---|---|
| SPFILE | `/u01/app/oracle/product/19.0.0/dbhome_1/dbs/spfilePHARMDB.ora` | `SHOW PARAMETER spfile` |
| Control file 1 | `/u01/app/oracle/oradata/PHARMDB/control01.ctl` | `SELECT name FROM v$controlfile` |
| Control file 2 | `/u02/app/oracle/fast_recovery_area/PHARMDB/control02.ctl` | `SELECT name FROM v$controlfile` |
| Redo log grupo 1 | `/u01/app/oracle/oradata/PHARMDB/redo01.log` | `SELECT group#, member FROM v$logfile` |
| Redo log grupo 2 | `/u01/app/oracle/oradata/PHARMDB/redo02.log` | `SELECT group#, member FROM v$logfile` |
| Redo log grupo 3 | `/u01/app/oracle/oradata/PHARMDB/redo03.log` | `SELECT group#, member FROM v$logfile` |

**Mapa diagnóstico: qué bloquea qué**

Cuando una instancia Oracle no arranca, la primera pregunta es: ¿en qué fase se ha detenido? La respuesta casi siempre está en el alert log, y el código ORA indica directamente qué archivo crítico está involucrado.

| Archivo faltante/corrupto | Fase bloqueada | Error ORA típico | Primera acción |
|---|---|---|---|
| SPFILE/PFILE | Pre-NOMOUNT | `ORA-01078`, `LRM-00109` | Verificar existencia y permisos en `$ORACLE_HOME/dbs/` |
| Control file | MOUNT | `ORA-00205` | Verificar path en `control_files`, permisos filesystem, disponibilidad de copias multiplexadas |
| Online redo log | OPEN | `ORA-00313`, `ORA-00312` | Verificar `v$logfile`, status de grupos en `v$log`, integridad física de los archivos |

Esto no es una guía de recovery — ese es un tema aparte, que requiere distinguir entre control file corrupto y control file faltante, entre redo log CURRENT y redo log INACTIVE, entre recovery con RMAN y recovery manual. Es un mapa diagnóstico: sirve para no ir en las direcciones equivocadas en las primeras fases de una emergencia.

---

## La reflexión

Paolo no estaba mal preparado por incompetente. Conocía la sintaxis — sabía qué hace `SHOW PARAMETER spfile`, sabía consultar `v$controlfile`. Lo que aún no había interiorizado era la secuencia de startup como método diagnóstico: qué archivo lee Oracle en cada fase, y por tanto qué archivo buscar primero cuando algo falla.

La diferencia entre veinte minutos gastados en red, listener y OS y tres verificaciones directas al punto no es experiencia acumulada durante años. Es tener un modelo mental de la secuencia — NOMOUNT, MOUNT, OPEN — y saber qué mapea con qué.

El valor de esa llamada no fue resolver el problema en su lugar. Fue transferir ese modelo en treinta minutos, con un caso real delante. Ahora Paolo sabe qué preguntarle al equipo de storage la próxima vez ("¿los permisos en `/u01` se modificaron durante el mantenimiento?"), sabe qué líneas del alert log importan, sabe en qué orden descartar las hipótesis.

El DBA senior al que ya no llaman en plena noche ha invertido en dos cosas: en el runbook bien escrito junto al equipo del cliente, y en la capacidad de guiar a distancia a quien está de guardia dándole las tres verificaciones correctas en lugar de hacerle hacer treinta a ciegas.

---

## Fuentes oficiales

1. Oracle Database Concepts 19c — Startup and Shutdown: secuencia NOMOUNT/MOUNT/OPEN y rol de los archivos críticos — `<TODO: scout URL exacto para Oracle 19c Concepts, capítulo "Starting Up a Database">`

2. Oracle Database Administrator's Guide 19c — Managing Initialization Parameters: SPFILE, PFILE, orden de búsqueda, `ALTER SYSTEM SET` — `<TODO: scout URL exacto para capítulo "Managing Initialization Parameters Using a Server Parameter File">`

3. Oracle Database Administrator's Guide 19c — [Managing the Online Redo Log](https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-the-online-redo-log.html) — grupos, miembros, status, `v$log`, `v$logfile`, errores ORA-00313/ORA-00312

4. Oracle Database Reference 19c — [V$CONTROLFILE](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/V-CONTROLFILE.html) — estructura y consultas de verificación de los control files

5. Oracle Database Reference 19c — [V$LOG](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/V-LOG.html) — columnas `GROUP#`, `MEMBERS`, `STATUS`, `BYTES`; interpretación de los status CURRENT/ACTIVE/INACTIVE

6. oracle-base.com (Tim Hall) — `<TODO: scout URL específico para "Oracle Database Startup and Shutdown" en oracle-base.com>` — secuencia de startup, errores comunes, ejemplos prácticos

---

## Glosario candidato

- **SPFILE** (Oracle) — Server Parameter File: archivo binario leído por Oracle al arranque que contiene los parámetros de configuración de la instancia (`db_name`, `control_files`, `memory_target`, etc.). Modificable en caliente con `ALTER SYSTEM SET` sin reiniciar la base de datos.

- **Control File** (Oracle) — Archivo binario actualizado continuamente por Oracle que registra la estructura física de la base de datos: paths de datafiles y redo logs, SCN actual, información de checkpoint. Indispensable para la fase de MOUNT; debe multiplexarse en paths físicamente separados.

- **Online Redo Log** (Oracle) — Archivo circular que registra en secuencia todas las modificaciones aplicadas a la base de datos (redo entries) antes de que se escriban en los datafiles. Organizado en grupos con posibles miembros múltiples para redundancia; base del mecanismo de recovery en caso de crash.

- **SCN** (System Change Number) — Número secuencial monotónicamente creciente que Oracle usa para identificar un punto preciso en la vida de la base de datos. Presente en el control file y en los datafiles; usado para determinar la consistencia y el punto de recovery.

- **OFA** (Optimal Flexible Architecture) — Convención de naming y layout de paths recomendada por Oracle para organizar los archivos de una instancia (datafiles, control files, redo logs, backups) de forma predecible, mantenible y portable entre entornos distintos.
