---
categories:
- mysql
date: '2026-08-18'
description: 'Workflow real de patching MySQL 8.0.34→8.0.45 en RHEL 8: vistas inválidas,
  GTID, verificación de réplica y upgrade RPM. Lo que el ticket de cuatro líneas no
  contaba.'
draft: false
image: mysql-8-0-348-0-45-workflow-di-patching-reale-con-errori-inclusi.cover.jpg
seoTitle: 'Upgrade MySQL 8.0 en RHEL 8: guía práctica con GTID y vistas rotas'
tags:
- mysql
- upgrade
- gtid
- replication
- mysqldump
title: El ticket decía 'actualiza MySQL y apaga el servicio'
translationKey: mysql_8_0_348_0_45_workflow_di_patching_reale_con_errori_inclusi
webo_generated_at: 2026-08-08
webo_status: scheduled
---

## El ticket decía "actualiza MySQL y apaga el servicio"

El ticket llegó por la mañana: actualizar MySQL Community de 8.0.34 a 8.0.45 en un servidor RHEL 8.3, y luego apagar el servicio aplicativo para una ventana de mantenimiento. Cuatro líneas, sin ningún detalle.

"Parece sencillo" es la frase más peligrosa que un DBA puede pensar antes de tocar un sistema en producción. Cada vez que nos hemos fiado de esa sensación hemos encontrado algo inesperado. Esta vez no fue diferente: vistas rotas que bloqueaban el dump, GTID habilitados, una réplica configurada pero detenida que nadie sabía explicar. Nada dramático, todo gestionable si se aborda en el orden correcto.

Lo que sigue es el workflow real, con las queries utilizadas y los errores encontrados. No es la documentación oficial de MySQL — esa está en `dev.mysql.com` y la conoce todo el mundo. Aquí está el campo.

---

## ¿Cuánto espacio ocupa realmente esta base de datos?

Antes de hacer cualquier cosa, entender con qué se está trabajando. La base de datos en cuestión era pequeña — unos 135 MB, 58 tablas, un único esquema aplicativo — y "pequeña" no significa "sin sorpresas".

Las queries sobre `information_schema` que uso siempre como primer paso:

```sql
-- Tamaño total del esquema
SELECT
    table_schema                                    AS schema_name,
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS size_mb,
    COUNT(*)                                        AS table_count
FROM information_schema.tables
WHERE table_schema NOT IN ('mysql','information_schema','performance_schema','sys')
GROUP BY table_schema
ORDER BY size_mb DESC;
```

```sql
-- Las tablas más grandes, con estimación de filas y espacio recuperable
SELECT
    table_name,
    ROUND((data_length + index_length) / 1024 / 1024, 2) AS size_mb,
    table_rows                                            AS estimated_rows,
    data_free / 1024 / 1024                               AS free_mb
FROM information_schema.tables
WHERE table_schema = 'app_monitoring'
ORDER BY (data_length + index_length) DESC
LIMIT 10;
```

En este caso las tres tablas más grandes eran todas de monitorización: `event_log` (~43 MB, ~500K filas), `metric_snapshot` (~41 MB, ~320K filas), `alert_history` (~28 MB, ~290K filas). Sin BLOBs, sin TEXTs de gran tamaño — el dump iba a ser rápido.

Verifico también si hay columnas de tipo BLOB o MEDIUMBLOB que pudieran inflar los tiempos:

```sql
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'app_monitoring'
  AND data_type IN ('blob','mediumblob','longblob','text','mediumtext','longtext')
ORDER BY table_name;
```

Cero resultados. Bien. Se procede con el backup.

---

## mysqldump se bloquea: error 1356 y las vistas rotas

Lanzo el dump. Treinta segundos de silencio, y luego:

```text
mysqldump: Got error: 1356: View 'app_monitoring.v_active_alerts' references
invalid table(s) or column(s) or function(s) or definer/invoker of view
lack rights to use them when using LOCK TABLES
```

El dump se ha detenido en una vista. No es raro: alguien modifica una tabla subyacente — renombra una columna, la elimina, cambia su tipo — y la vista que la referencia queda inválida sin que nadie se dé cuenta hasta que se intenta hacer un dump o una consulta directa sobre esa vista.

Lo primero es mapear todas las vistas inválidas del esquema. No solo las que devuelven el error 1356 explícito — también las que tienen `last_altered` o `created` NULL en `information_schema`, que a menudo indican objetos corruptos o que no se pueden compilar [1]:

```sql
-- Metadatos de las vistas: definer, security_type, actualizabilidad
SELECT
    table_name     AS view_name,
    definer,
    security_type,
    is_updatable,
    check_option
FROM information_schema.views
WHERE table_schema = 'app_monitoring'
ORDER BY table_name;
```

```sql
-- Verificación directa: listado de vistas para iterar con SELECT * LIMIT 1 sobre cada una
-- (útil en un script para esquemas grandes)
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'app_monitoring'
  AND table_type = 'VIEW';
```

En este caso encontré 6 vistas problemáticas: 2 con error 1356 explícito, 4 con `created` NULL en `information_schema` — señal de que MySQL no podía compilarlas en el momento de la consulta.

La estrategia es excluirlas del dump principal y guardar solo su DDL aparte con `--force`, para no perder el rastro de su definición:

```bash
# Dump principal sin las vistas rotas
mysqldump \
  --single-transaction \
  --routines \
  --triggers \
  --events \
  --ignore-table=app_monitoring.v_active_alerts \
  --ignore-table=app_monitoring.v_alert_summary \
  --ignore-table=app_monitoring.v_metric_daily \
  --ignore-table=app_monitoring.v_metric_hourly \
  --ignore-table=app_monitoring.v_event_open \
  --ignore-table=app_monitoring.v_event_closed \
  app_monitoring > /backup/app_monitoring_$(date +%Y%m%d_%H%M).sql

# DDL de las vistas rotas (solo estructura, con --force para no bloquearse)
mysqldump \
  --no-data \
  --force \
  app_monitoring \
  v_active_alerts v_alert_summary v_metric_daily \
  v_metric_hourly v_event_open v_event_closed \
  > /backup/app_monitoring_broken_views_$(date +%Y%m%d_%H%M).sql
```

El segundo dump con `--force` produce la DDL de las vistas aunque sean inválidas — útil para recrearlas a posteriori, una vez corregidas las tablas subyacentes. No resuelve el problema de las vistas rotas, pero al menos queda constancia de lo que había.

---

## El warning de GTID y cuándo usar `--set-gtid-purged=OFF`

Durante el dump principal aparece este aviso:

```text
Warning: A partial dump from a server that has GTIDs will by default include
the GTIDs of all transactions, even those that changed suppressed parts of
the database. If you don't want to restore the GTIDs, pass
--set-gtid-purged=OFF. To make a complete dump, pass --all-databases
--triggers --routines --events.
```

Los GTID — *Global Transaction Identifiers* — son identificadores únicos que MySQL asigna a cada transacción cuando `gtid_mode=ON` [2]. Sirven principalmente para la réplica: cada servidor lleva un registro de qué GTIDs ya ha ejecutado, y la réplica usa esa información para saber desde dónde retomar.

El warning dice: estás haciendo un dump parcial (solo un esquema, no `--all-databases`), y el dump incluirá igualmente el conjunto de GTIDs de todo el servidor. Si luego importas ese dump en otro servidor, ese servidor creerá que ya ha ejecutado todas esas transacciones — condición que puede romper una réplica recién configurada.

En este caso el dump sirve únicamente como backup pre-upgrade, no para replicar en otro servidor. Añado `--set-gtid-purged=OFF`:

```bash
mysqldump \
  --single-transaction \
  --routines \
  --triggers \
  --events \
  --set-gtid-purged=OFF \
  --ignore-table=app_monitoring.v_active_alerts \
  [... otros --ignore-table ...] \
  app_monitoring > /backup/app_monitoring_$(date +%Y%m%d_%H%M).sql
```

Regla práctica: si el dump es para backup/restore en el mismo servidor o en un servidor standalone, `--set-gtid-purged=OFF` es casi siempre la elección correcta. Si estás construyendo una réplica o haciendo point-in-time recovery en un servidor con GTID, la situación es más compleja — tema para otro artículo.

---

## Antes de apagar: ¿este servidor es master, réplica o standalone?

El backup está hecho. Ahora viene el paso que muchos se saltan: entender el rol del servidor en el clúster antes de apagarlo.

Apagar un master sin promover una réplica provoca downtime. Apagar un nodo Galera sin verificar el quórum puede corromper el clúster. Incluso en este caso, donde el servidor parecía standalone, la verificación es obligatoria.

Las queries a ejecutar en orden:

```sql
-- 1. Estado de la réplica (si este servidor es réplica de alguno)
SHOW REPLICA STATUS\G
```

```sql
-- 2. Estado como fuente (si este servidor tiene réplicas)
SHOW BINARY LOG STATUS\G
SHOW REPLICAS\G
```

```sql
-- 3. Group Replication o clúster InnoDB
SELECT * FROM performance_schema.replication_group_members;
```

```sql
-- 4. Parámetros clave
SHOW VARIABLES LIKE 'server_id';
SHOW VARIABLES LIKE 'read_only';
SHOW VARIABLES LIKE 'gtid_mode';
SHOW VARIABLES LIKE 'group_replication%';
```

Resultado en este caso: `SHOW REPLICA STATUS` devuelve una fila con `Replica_IO_Running: No` y `Replica_SQL_Running: No` — la réplica estaba configurada pero detenida desde hacía tiempo. `SHOW REPLICAS` devuelve cero filas. `replication_group_members` está vacía. `server_id=1`, `read_only=OFF`.

En la práctica, un servidor standalone con los restos de una configuración de réplica nunca completada o abandonada. Sin riesgo de downtime en cascada. Se procede.

---

## El upgrade RPM: todos los paquetes, en el orden correcto

Parada del servicio:

```bash
systemctl stop mysqld
systemctl status mysqld   # verificar que esté realmente detenido
```

El error más habitual en esta fase es actualizar solo `mysql-community-server` olvidando los paquetes dependientes. En RHEL 8 con los repos MySQL Community, los paquetes a actualizar juntos son [3]:

```bash
# Verificar versión actual
rpm -qa | grep mysql | sort

# Upgrade de todos los paquetes MySQL de una vez
dnf upgrade \
  mysql-community-server \
  mysql-community-client \
  mysql-community-libs \
  mysql-community-common \
  mysql-community-client-plugins \
  mysql-community-icu-data-files
```

Actualizar solo `mysql-community-server` dejando `mysql-community-libs` en la versión anterior produce errores de linking al reiniciar que no son inmediatos de diagnosticar. Mejor actualizar todo junto.

Reinicio y verificación:

```bash
systemctl start mysqld
systemctl status mysqld

# Verificar versión
mysql -u root -p -e "SELECT VERSION();"
```

```text
+-----------+
| VERSION() |
+-----------+
| 8.0.45    |
+-----------+
```

En MySQL 8.0 el upgrade del esquema interno — el que en versiones anteriores requería ejecutar `mysql_upgrade` manualmente — es automático en el primer arranque [4]. El servidor ejecuta las migraciones necesarias y escribe en el log:

```text
[System] [MY-013381] [Server] Server upgrade from '80034' to '80045' started.
[System] [MY-013381] [Server] Server upgrade from '80034' to '80045' completed.
```

Si esas dos líneas no aparecen, algo no ha ido como se esperaba. Verificar siempre:

```bash
grep -i "upgrade" /var/log/mysqld.log | tail -5
```

---

## Verificación post-upgrade: que arranque no es suficiente

El servidor ha arrancado y muestra la versión correcta. Aún no hemos terminado.

```sql
-- Verificación de tablas de sistema
CHECK TABLE mysql.user;
CHECK TABLE mysql.db;

-- Verificar que las tablas aplicativas sean accesibles
SELECT COUNT(*) FROM app_monitoring.event_log;
SELECT COUNT(*) FROM app_monitoring.metric_snapshot;

-- Verificar variables críticas post-upgrade
SHOW VARIABLES LIKE 'gtid_mode';
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
SHOW VARIABLES LIKE 'max_connections';
```

Las vistas rotas existían ya antes del upgrade y siguen rotas después — el upgrade no las arregla, evidentemente. Hay que corregirlas por separado, una vez aclarado con el equipo aplicativo qué tablas subyacentes han cambiado y cómo.

Un último check en el log para errores silenciosos:

```bash
grep -i "error\|warning\|corrupt" /var/log/mysqld.log | grep -v "^#" | tail -20
```

En este caso todo limpio. El patching está completado.

---

## Un ticket de cuatro líneas no refleja la complejidad de la tarea

El patching de MySQL no es complicado. Los comandos son pocos y la documentación oficial es buena. La parte difícil no es ejecutar los pasos — es saber qué preguntas hacer antes de empezar.

¿Cuánto ocupa la base de datos? ¿Hay objetos inválidos? ¿Este servidor tiene un rol en el clúster? ¿Los GTID están habilitados y qué implica eso para el dump? Cada pregunta que se omite es un riesgo que se materializa en el peor momento: durante la ventana de mantenimiento, con alguien esperando.

La diferencia entre un enfoque junior y uno senior no está en los comandos — está en el tiempo invertido antes de lanzarlos. Las queries sobre `information_schema`, el check de la réplica, la verificación del log post-upgrade: son todos pasos que parecen redundantes hasta que dejan de serlo.

Las vistas rotas en este caso ya estaban rotas antes del patching. El upgrade no las creó, simplemente las hizo visibles porque alguien intentó hacer un dump por primera vez en meses. Es el tipo de hallazgo que justifica el tiempo de un análisis pre-backup cuidadoso: no para bloquear el patching, sino para no llevarse sorpresas a mitad de camino.

---

## Fontes oficiales

1. MySQL 8.0 Reference Manual — [INFORMATION_SCHEMA VIEWS Table](https://dev.mysql.com/doc/refman/8.0/en/information-schema-views-table.html)
2. MySQL 8.0 Reference Manual — [Replication with Global Transaction Identifiers](https://dev.mysql.com/doc/refman/8.0/en/replication-gtids.html)
3. MySQL 8.0 Reference Manual — [Installing MySQL on Linux Using the MySQL Yum Repository](https://dev.mysql.com/doc/refman/8.0/en/linux-installation-yum-repo.html)
4. MySQL 8.0 Reference Manual — [Upgrading MySQL](https://dev.mysql.com/doc/refman/8.0/en/upgrading.html)

---

## Glosario candidato

- **GTID** (MySQL) — *Global Transaction Identifier*: identificador único asignado a cada transacción cuando `gtid_mode=ON`. Compuesto por `server_uuid:número_secuencia`, permite a la réplica rastrear exactamente qué transacciones ya ha aplicado, independientemente de la posición en el binlog.

- **mysqldump** — utilidad de backup lógico incluida en MySQL. Produce un archivo SQL con las instrucciones `CREATE` e `INSERT` para recrear la base de datos. Adecuada para bases de datos de tamaño pequeño y mediano; para volúmenes elevados se prefieren herramientas como mydumper o backups físicos con xtrabackup.

- **Vista inválida** (MySQL) — vista cuyo cuerpo SQL hace referencia a objetos que ya no existen o no son accesibles (tablas renombradas, columnas eliminadas, permisos revocados). MySQL no invalida automáticamente las vistas al modificar la tabla subyacente: el error emerge solo en la primera ejecución o durante un dump.

- **`--single-transaction`** (mysqldump) — flag que inicia una transacción `REPEATABLE READ` antes del dump, garantizando consistencia sin adquirir locks sobre las tablas InnoDB. No aplicable a tablas MyISAM, que requieren `--lock-tables`.

- **`replication_group_members`** (MySQL Performance Schema) — tabla de sistema que lista los nodos activos en un clúster Group Replication, con estado (`ONLINE`, `RECOVERING`, `UNREACHABLE`) y rol (`PRIMARY`, `SECONDARY`). Vacía en servidores standalone o con réplica tradicional.
