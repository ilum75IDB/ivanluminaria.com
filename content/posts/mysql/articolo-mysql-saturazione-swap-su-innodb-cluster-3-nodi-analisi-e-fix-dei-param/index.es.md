---
categories:
- mysql
date: 2099-12-31
description: 'Diagnóstico en producción de un cluster MySQL InnoDB con swap saturado:
  cómo join_buffer_size a 2 GB por thread colapsa un nodo con 157 GB de RAM.'
draft: true
image: articolo-mysql-saturazione-swap-su-innodb-cluster-3-nodi-analisi-e-fix-dei-param.cover.jpg
seoTitle: 'Swap 100% en InnoDB Cluster: join_buffer_size y memoria MySQL'
tags:
- mysql
- innodb-cluster
- memory-tuning
- performance
- incident-response
title: 'La llamada del martes por la mañana: swap al 100% en InnoDB Cluster y cómo
  join_buffer_size multiplica el problema'
translationKey: articolo_mysql_saturazione_swap_su_innodb_cluster_3_nodi_analisi_e_fix_dei_param
webo_generated_at: 2026-07-01
webo_status: da_tradurre
---

## La llamada del martes por la mañana

Martes por la mañana, poco después de las nueve. El café todavía caliente en el escritorio, la jornada parecía una de esas tranquilas en las que por fin se consigue cerrar los asuntos que quedaron pendientes desde el viernes. Entonces llegó la llamada.

Al otro lado, el equipo de infraestructura de una cadena de distribución alimentaria italiana: el backend de monitoring se había vuelto extremadamente lento, los dashboards internos ya no cargaban, algunas alertas no llegaban. Un nodo del cluster MySQL estaba prácticamente parado. "No hemos tocado nada, ha pasado así."

Bajo el capó había una query de agregación, aparentemente inocua. Algo del tipo:

```sql
SELECT itemid, MIN(clock), MAX(clock), COUNT(*)
FROM history_log
GROUP BY itemid;
```

Sobre una tabla de 1.300 millones de filas, sin particionamiento, sin filtro temporal, sin `LIMIT`. El nodo secondary del cluster empezó a hacer swap de forma agresiva y luego se detuvo.

El contexto: la cadena en cuestión usa un cluster MySQL InnoDB Cluster de 3 nodos como backend para su plataforma de monitoring interna, la que mantiene bajo control los sistemas de caja, los almacenes y la logística de los puntos de venta. Los nodos — `mysql-node-01`, `mysql-node-02`, `mysql-node-03` — gestionan la recopilación y consulta de métricas históricas. La tabla `history_log` es el núcleo del sistema: cada evento de monitoring acaba ahí, acumulado con el tiempo sin una política de retención activa y sin particionamiento por fecha.

Cuando la query arrancó en producción — alguien estaba evidentemente intentando responder a una pregunta de negocio sobre toda la historia de los items — el nodo secondary no tenía suficiente RAM libre para aguantar el full scan. La situación, sin embargo, no se agotaba en esa query. Era la configuración de memoria subyacente la que hacía el cluster estructuralmente frágil ante cualquier carga agregada no trivial.

## `free -h` y la primera sorpresa

La primera señal había llegado del dashboard de monitoring del cliente, compartido en la llamada pocos minutos después: el gráfico del swap en `mysql-node-01` y `mysql-node-02` mostraba una línea plana al máximo desde hacía horas. En `mysql-node-03`, en cambio, todo parecía normal.

```bash
# mysql-node-01
              total        used        free      shared  buff/cache   available
Mem:           157Gi       155Gi       512Mi       1.2Gi       1.5Gi       400Mi
Swap:            6Gi         6Gi         0Bi

# mysql-node-02
              total        used        free      shared  buff/cache   available
Mem:           157Gi       150Gi       2.1Gi       1.1Gi       4.8Gi       1.2Gi
Swap:            6Gi         6Gi         0Bi

# mysql-node-03
              total        used        free      shared  buff/cache   available
Mem:           157Gi        21Gi       130Gi       0.3Gi       5.9Gi       134Gi
Swap:            6Gi       512Mi       5.5Gi
```

La diferencia entre los nodos era clara. `mysql-node-03` era el nodo que había recibido menos carga de queries en ese período — era el secondary "frío", por así decirlo. Los dos primeros soportaban el tráfico principal de lectura y escritura, y la memoria estaba agotada.

`vmstat 1 5` lo confirmaba: swap en uso activo, no solo ocupado estáticamente.

```bash
# vmstat 1 5 en mysql-node-01
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 3  2 6291456  52428  18432 1572864  142  198  2840  3120 4821 9234 28  8 58  6  0
 2  1 6291456  48120  18432 1572864  156  212  3012  3340 5102 9876 31  9 54  6  0
```

`si` y `so` (swap-in y swap-out) activos: el kernel estaba moviendo páginas entre RAM y disco de forma continua. Con una base de datos relacional bajo carga, esta es la forma más rápida de degradar el rendimiento de manera irreversible.

## La matemática que no cuadraba

Mirando la configuración activa en el cluster, el parámetro que saltaba a la vista de inmediato era este:

```sql
SHOW VARIABLES LIKE 'join_buffer_size';
-- join_buffer_size = 2147483648  (2 GB)

SHOW VARIABLES LIKE 'max_connections';
-- max_connections = 151

SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
-- innodb_buffer_pool_size = 133143986176  (124 GB)
```

El `join_buffer_size` a 2 GB es un parámetro **por thread**, no global. Cada conexión MySQL que ejecuta un join sin índice puede asignar hasta 2 GB de memoria adicional. Con `max_connections = 151`, el potencial teórico de asignación es:

```
2 GB × 151 conexiones = 302 GB
```

En máquinas con 157 GB de RAM total, de los cuales 124 GB ya están comprometidos en el `innodb_buffer_pool_size`.

Evidentemente, 302 GB no se asignan todos a la vez en condiciones normales — los buffers por thread se asignan solo cuando se necesitan, y no todas las conexiones ejecutan joins simultáneamente. En un momento de carga agregada, sin embargo, con queries de full scan sobre `history_log` ejecutándose en múltiples conexiones, incluso una fracción de ese potencial es suficiente para saturar la RAM disponible.

También `tmp_table_size` y `max_heap_table_size` estaban sobredimensionados, contribuyendo a la presión sobre las tablas temporales en memoria.

## Lo que decía el `performance_schema`

Para entender qué queries estaban consumiendo recursos realmente, la consulta de `events_statements_summary_by_digest` dio el panorama completo:

```sql
SELECT
    DIGEST_TEXT,
    COUNT_STAR,
    SUM_ROWS_EXAMINED,
    SUM_CREATED_TMP_DISK_TABLES,
    SUM_NO_INDEX_USED,
    ROUND(SUM_TIMER_WAIT / 1e12, 2) AS total_wait_sec
FROM performance_schema.events_statements_summary_by_digest
WHERE SUM_NO_INDEX_USED > 0
   OR SUM_CREATED_TMP_DISK_TABLES > 0
ORDER BY SUM_ROWS_EXAMINED DESC
LIMIT 10;
```

Los números que aparecían eran significativos [1]:

- `Select_full_join` acumulado: hasta **22.631.693** — joins ejecutados sin índice
- `Created_tmp_disk_tables`: más de **200.000** — tablas temporales volcadas a disco porque la memoria no era suficiente

No eran números de un único evento. Eran el resultado de semanas de queries mal optimizadas que se acumulaban en silencio, hasta que un full scan sobre `history_log` hizo desbordar el sistema.

## La estructura de `history_log` y el nodo sin salida

```sql
SHOW CREATE TABLE history_log\G
-- Engine: InnoDB
-- Rows (approx): 1.312.847.203
-- Partitions: none
-- Indexes: PRIMARY KEY (id), KEY idx_itemid_clock (itemid, clock)

SELECT COUNT(*) FROM history_log;
-- 1312847203
```

La tabla tenía un índice sobre `(itemid, clock)`, pero la query de agregación que había causado el crash no usaba el filtro sobre `clock`. MySQL no podía usar el índice de forma eficiente para un `GROUP BY itemid` sobre toda la tabla — el plan de ejecución elegía un full scan, asignaba estructuras temporales en memoria, y cuando la memoria se agotaba, lo volcaba todo a disco. En `mysql-node-02`, con el swap ya al 100%, no había disco virtual disponible: el nodo se detuvo [2].

Sin particionamiento por fecha en `history_log`, cualquier query agregada sobre toda la historia es estructuralmente peligrosa. Es una decisión arquitectónica que había que abordar, y al mismo tiempo no de forma inmediata — el fix urgente era sobre los parámetros de memoria.

## Los nuevos valores y el razonamiento detrás

El plan de intervención era directo. Los parámetros por thread había que redimensionarlos a valores razonables para el workload real:

```ini
# my.cnf — cambios aplicados
[mysqld]

# Buffer por thread: de 2G a 64M
join_buffer_size        = 64M
tmp_table_size          = 64M
max_heap_table_size     = 64M

# InnoDB redo log: capacidad aumentada para reducir la frecuencia de checkpoints
innodb_redo_log_capacity = 8G

# Parámetros InnoDB mantenidos sin cambios
innodb_buffer_pool_size  = 124G   # ya dimensionado correctamente para el dataset
innodb_buffer_pool_instances = 8  # sin cambios
```

La decisión de mantener `innodb_buffer_pool_size` en 124 GB fue deliberada: el buffer pool es memoria global, no por thread, y su dimensionamiento era correcto respecto al tamaño del dataset activo. Reducirlo habría empeorado el rendimiento de I/O sin resolver la causa real.

El `join_buffer_size` a 64 MB es un valor estándar para workloads OLTP mixtos. Con 151 conexiones máximas, el potencial de asignación baja a:

```
64 MB × 151 = 9,6 GB
```

Sumado a los 124 GB del buffer pool y al overhead del sistema operativo, se queda holgadamente dentro de los 157 GB disponibles con margen suficiente para los picos [3].

El `innodb_redo_log_capacity` a 8 GB (desde un valor anterior más bajo) sirve para reducir la frecuencia de los checkpoints de InnoDB, que en presencia de escritura intensiva generan I/O adicional — una contribución secundaria a la presión sobre el sistema.

## El rolling restart y por qué funciona en InnoDB Cluster

InnoDB Cluster con Group Replication permite reiniciar los nodos en secuencia sin interrumpir el servicio, siempre que se mantenga el quorum [4]. Con 3 nodos, se puede dejar offline un nodo a la vez: los otros dos mantienen el quorum y continúan sirviendo las peticiones.

La secuencia aplicada, acordada por teléfono con el equipo del cliente:

```bash
# Paso 1: reinicio de mysql-node-03 (el nodo con swap mínimo, menos riesgo)
# Verificar estado del cluster antes de proceder
mysqlsh -- cluster status

# En mysql-node-03: stop, modificar my.cnf, start
systemctl stop mysqld
# -- modificar /etc/my.cnf con los nuevos parámetros --
systemctl start mysqld

# Esperar rejoin automático al cluster
# Verificar: SECONDARY vuelto a ONLINE

# Paso 2: reinicio de mysql-node-02
# Paso 3: reinicio de mysql-node-01 (PRIMARY al final)
# Antes del reinicio del PRIMARY: switchover manual si es necesario
mysqlsh -- cluster setPrimaryInstance mysql-node-02:3306
```

Reiniciar el nodo PRIMARY al final es una precaución: si el PRIMARY se reinicia mientras los otros dos no están completamente sincronizados, Group Replication elige automáticamente un nuevo PRIMARY, y al mismo tiempo es más limpio gestionar el switchover de forma manual.

Tiempo total de la operación: unos 40 minutos desde la primera llamada, cero interrupciones de servicio para las aplicaciones cliente. Las cajas de los puntos de venta no se enteraron.

## De 100% a 11%: los números después del fix

El gráfico del swap en las horas siguientes al rolling restart mostraba la curva esperada: descenso rápido en `mysql-node-01` y `mysql-node-02`, estabilización en torno al 10-11%.

```bash
# mysql-node-01 — 6 horas después del rolling restart
              total        used        free      shared  buff/cache   available
Mem:           157Gi       132Gi        18Gi       0.8Gi       6.2Gi        23Gi
Swap:            6Gi       672Mi       5.4Gi

# mysql-node-02
              total        used        free      shared  buff/cache   available
Mem:           157Gi       129Gi        21Gi       0.7Gi       6.8Gi        25Gi
Swap:            6Gi       614Mi       5.4Gi
```

La carga de CPU se había estabilizado: los picos ligados al swap I/O habían desaparecido. Las métricas del `performance_schema` mostraban una reducción neta de los `Created_tmp_disk_tables` — no a cero, porque algunas queries seguían haciendo full scan, y al mismo tiempo el sistema ya no estaba bajo presión estructural.

`Select_full_join` seguía acumulándose: esa métrica requiere intervenciones sobre las queries y los índices, no solo sobre los parámetros de memoria. El cluster, sin embargo, aguantaba la carga sin saturar el swap.

## Lo que queda pendiente en `history_log`

El fix sobre los parámetros de memoria era necesario y suficiente para estabilizar el cluster de forma inmediata. La causa estructural, sin embargo — una tabla de 1.300 millones de filas sin particionamiento y sin política de retención — sigue abierta.

Las acciones recomendadas al cliente para el medio plazo:

**Particionamiento por fecha en `history_log`**

```sql
-- Schema objetivo (a aplicar con migración planificada)
ALTER TABLE history_log
    PARTITION BY RANGE (clock) (
        PARTITION p_2023 VALUES LESS THAN (UNIX_TIMESTAMP('2024-01-01')),
        PARTITION p_2024 VALUES LESS THAN (UNIX_TIMESTAMP('2025-01-01')),
        PARTITION p_2025 VALUES LESS THAN (UNIX_TIMESTAMP('2026-01-01')),
        PARTITION p_future VALUES LESS THAN MAXVALUE
    );
```

Con el particionamiento, las queries con filtro sobre `clock` pueden usar el partition pruning y evitar el full scan sobre toda la tabla. La query de agregación que causó el crash, con un filtro temporal razonable, se volvería manejable [2].

**Política de retención activa**

Definir una ventana de retención (por ejemplo, 12 meses) e implementar un procedimiento de purga periódica. Con 1.300 millones de filas, incluso una retención de 6 meses reduce significativamente el dataset activo.

**Query tuning**

Las queries de agregación sin filtro temporal sobre `history_log` hay que tratarlas como operaciones de mantenimiento, no como queries operativas. Deberían ejecutarse sobre réplicas dedicadas, en ventanas de mantenimiento, con `MAX_EXECUTION_TIME` configurado.

```sql
-- Versión segura de la query problemática
SELECT /*+ MAX_EXECUTION_TIME(30000) */ itemid, MIN(clock), MAX(clock), COUNT(*)
FROM history_log
WHERE clock >= UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 30 DAY))
GROUP BY itemid;
```

## La regla básica que se olvida

El fix fue lo que fue: diagnóstico correcto, valores razonables, rolling restart. Sin magia, sin heroísmos — una llamada de unas horas con un equipo que sabía lo que tenía entre manos, y un par de ojos externos que miraron la matemática de los buffers.

Lo que llama la atención, mirando atrás, es con qué frecuencia la configuración de los buffers por thread se descuida frente al dimensionamiento del buffer pool. El `innodb_buffer_pool_size` es el parámetro que todo el mundo mira primero — y con razón, es el más impactante. Los buffers por thread como `join_buffer_size`, `sort_buffer_size`, `read_buffer_size` tienen sin embargo una característica insidiosa: se asignan por conexión, y su impacto real en memoria depende del número de conexiones concurrentes activas.

La fórmula es sencilla:

```
memoria_por_thread × max_connections = presión potencial máxima
```

Hay que calcularla explícitamente al dimensionar un servidor MySQL, y compararla con la RAM disponible una vez descontados el buffer pool y el overhead del SO. Si el resultado supera la RAM física, el sistema es estructuralmente frágil — no "podría tener situaciones críticas", sino que **las tendrá**, cuando la carga sea la adecuada.

En este caso la carga adecuada fue una query agregada sobre una tabla de 1.300 millones de filas, un martes por la mañana cualquiera. Podría haber sido cualquier otra cosa, en cualquier otro momento.

## Fontes oficiales

1. MySQL 8.0 Reference Manual — [Performance Schema Statement Digests](https://dev.mysql.com/doc/refman/8.0/en/performance-schema-statement-digests.html)
2. MySQL 8.0 Reference Manual — [RANGE Partitioning](https://dev.mysql.com/doc/refman/8.0/en/partitioning-range.html)
3. MySQL 8.0 Reference Manual — [Memory Use in MySQL](https://dev.mysql.com/doc/refman/8.0/en/memory-use.html)
4. MySQL 8.0 Reference Manual — [InnoDB Cluster — Rolling Restart](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-innodb-cluster-working-with-cluster.html)

## Glosario
- **[join_buffer_size](/es/glossary/join-buffer-size/)** (MySQL) — Buffer asignado por thread para cada join ejecutado sin índice. A diferencia del buffer pool, se asigna por cada conexión activa: su impacto en la memoria total depende del número de conexiones concurrentes.

- **[innodb_buffer_pool_size](/es/glossary/group-replication/)** (MySQL/InnoDB) — Parámetro global que define el tamaño de la caché principal de InnoDB para datos e índices. Es el parámetro de memoria más impactante en MySQL: habitualmente se dimensiona al 70-80% de la RAM disponible en servidores dedicados.

- **Group Replication** (MySQL) — Mecanismo de replicación síncrona multi-master integrado en MySQL, base de InnoDB Cluster. Garantiza consistencia entre los nodos mediante un protocolo de consenso distribuido; permite rolling restart sin pérdida de quorum con 3 o más nodos.

- **performance_schema** (MySQL) — Schema de sistema que recopila métricas de ejecución en tiempo real: estadísticas por query digest, wait events, memoria asignada por thread. Base para el diagnóstico de rendimiento sin herramientas externas.

- **rolling restart** — Procedimiento de reinicio secuencial de los nodos de un cluster que mantiene el servicio activo durante la operación. En InnoDB Cluster con 3 nodos, permite aplicar cambios de configuración sin downtime, reiniciando un nodo a la vez mientras los demás mantienen el quorum.
