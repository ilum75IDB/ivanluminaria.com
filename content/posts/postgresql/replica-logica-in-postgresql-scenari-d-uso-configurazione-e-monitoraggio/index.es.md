---
title: "Replicación lógica en PostgreSQL: las preguntas de un colega que aclaran el tema"
seoTitle: "Replicación lógica PostgreSQL: escenarios y configuración"
description: "Replicación lógica PostgreSQL explicada con las preguntas de un colega: migración cross-version, CDC hacia data warehouse, configuración paso a paso."
date: "2026-07-07T08:03:00+01:00"
draft: false
translationKey: "replica_logica_in_postgresql_scenari_uso"
tags: ["replica-logica", "cdc", "migration", "postgresql-13", "postgresql-15"]
categories: ["postgresql"]
image: "replica-logica-in-postgresql-scenari-d-uso-configurazione-e-monitoraggio.cover.jpg"
webo_generated_at: 2026-06-08
webo_status: scheduled
---

## Un acompañamiento que no era una clase

Claudio estaba ahí para observar, no para aprender en sentido formal. El acompañamiento era trabajo real: un sistema de gestión de siniestros y pólizas en producción, un gran grupo asegurador italiano, y la necesidad concreta de migrar de PostgreSQL 13 a PostgreSQL 15 sin interrumpir las operaciones. En paralelo, el equipo de análisis de fraudes esperaba un flujo de datos hacia el data warehouse para alimentar sus modelos.

No era el contexto ideal para explicar la replicación lógica desde cero. Sin embargo, Claudio hizo exactamente las preguntas que cualquiera haría la primera vez — y responder a esas preguntas en voz alta, de forma que se sostuvieran, hizo más sólida cada decisión que ya había tomado en silencio.

Este artículo sigue esa secuencia: primero las preguntas, luego los conceptos, luego la configuración concreta.

---

## Replicación física y replicación lógica: el dilema inicial

La primera pregunta de Claudio llegó antes de abrir un terminal: «¿Por qué no usamos la replicación física? ¿No es la que se usa normalmente?»

Es la pregunta correcta. La replicación física — streaming replication — es la opción consolidada para alta disponibilidad y disaster recovery. Funciona a nivel de bloque: el servidor primario transmite los WAL (Write-Ahead Log) a la réplica, que los aplica de forma idéntica. El resultado es una copia byte a byte del clúster. Sencilla de configurar, fiable, bien documentada [1].

El límite es exactamente su fortaleza: replica *todo*, en el mismo formato, con la misma versión de PostgreSQL. No se puede replicar solo algunas tablas. No se puede replicar hacia una versión diferente del motor. No se puede usar la réplica como fuente para un sistema externo que habla un protocolo distinto.

La replicación lógica opera a nivel de fila, no de bloque. El publisher decodifica los cambios de los WAL y los transmite como operaciones lógicas — `INSERT`, `UPDATE`, `DELETE` — hacia uno o más subscribers. Esto abre tres posibilidades que la replicación física no ofrece:

- replicar un subconjunto de tablas o filas
- replicar entre versiones diferentes de PostgreSQL (desde la 10 en adelante, con limitaciones)
- alimentar sistemas heterogéneos como data warehouses o message brokers mediante Change Data Capture (CDC)

En nuestro caso, las tres necesidades estaban presentes al mismo tiempo.

---

## Los tres escenarios y las preguntas de Claudio

### Migración cross-versión sin downtime

«¿No puedo hacer un `pg_upgrade`?» preguntó Claudio, mirando la documentación en el monitor de al lado.

Sí, `pg_upgrade` funciona. Pero requiere dejar el sistema offline, ejecutar el upgrade, verificar, y solo entonces reabrir el tráfico. Con 100 millones de filas en `claim_events.claims` y 300 millones en `claim_events.claim_details`, el tiempo de inactividad habría sido del orden de horas — inaceptable para un sistema que gestiona liquidaciones activas.

La replicación lógica permite un enfoque diferente: se prepara el nuevo clúster PostgreSQL 15 (`pg-claims-new-01`), se alimenta mediante subscription, y cuando el lag de replicación se reduce a segundos se ejecuta el switchover. El downtime se reduce al tiempo necesario para redirigir las conexiones — minutos, no horas.

### Integración CDC hacia el data warehouse

«¿Es como un trigger distribuido?» preguntó Claudio, con cierta satisfacción por la analogía.

No — y la diferencia es sustancial. Un trigger se ejecuta en transacción, añade latencia y escala mal con volúmenes elevados. La replicación lógica lee los WAL *después* de que la transacción ya ha sido confirmada: ningún impacto en el camino crítico de las escrituras, ningún lock adicional, ninguna sobrecarga en el publisher más allá de la decodificación WAL.

Para el equipo antifraude, la necesidad era recibir en tiempo casi real las nuevas solicitudes de indemnización (`fraud_detection_audit.new_claims_for_analysis`) en `pg-dw-subscriber-01`. La publication dedicada `fraud_audit_pub` resolvió exactamente este requisito, sin tocar la lógica aplicativa.

### Replicación selectiva

«¿Y si solo quiero los datos de los clientes activos?» preguntó Claudio, pensando ya en un caso de uso futuro.

Aquí la respuesta es más matizada. La replicación lógica permite seleccionar las tablas a incluir en una publication. A partir de PostgreSQL 15, es posible añadir también una cláusula `WHERE` para filtrar las filas [2]. La limitación principal afecta a las DDL: los cambios de esquema no se replican automáticamente — punto al que vuelvo en la sección de monitorización.

---

## Conceptos clave: publication, subscription y slot de replicación

Antes de pasar a la configuración, tres conceptos que conviene tener claros.

**Publication** — define *qué* se replica en el publisher. Puede incluir tablas específicas, todas las tablas de una base de datos (`FOR ALL TABLES`), o — desde la versión 15 — secuencias. Cada publication tiene un nombre y puede ser referenciada por múltiples subscribers.

**Subscription** — define *quién* recibe los datos y *desde dónde*. La subscription se crea en el subscriber y especifica la cadena de conexión al publisher y el nombre de la publication a la que se suscribe. En el momento de la creación, PostgreSQL ejecuta una copia inicial de los datos (initial snapshot) y luego aplica los cambios posteriores en streaming.

**Slot de replicación lógica** — es el mecanismo que garantiza la persistencia. El publisher mantiene los segmentos WAL necesarios hasta que el subscriber los ha consumido. Esto es fundamental para la consistencia, pero introduce un riesgo: si un subscriber se desconecta durante mucho tiempo, los WAL se acumulan y el espacio en disco del publisher puede agotarse. La monitorización de los slots es obligatoria en producción.

---

## Configuración práctica

### Publisher: `pg-claims-primary-01` (PostgreSQL 13.10)

El parámetro más importante es `wal_level`, que debe estar configurado en `logical`. Los demás parámetros dimensionan los recursos para los slots y los workers.

```sql
-- En pg-claims-primary-01
ALTER SYSTEM SET wal_level = 'logical';
ALTER SYSTEM SET max_replication_slots = '10';
ALTER SYSTEM SET max_worker_processes = '10';
SELECT pg_reload_conf();
```

`wal_level = 'logical'` requiere un reinicio del servidor para activarse. Los demás parámetros se pueden aplicar con `pg_reload_conf()`, pero es buena práctica verificar los valores efectivos después del reload:

```sql
SHOW wal_level;
SHOW max_replication_slots;
```

Tras el reinicio, se crean las publications. Para la migración, las tablas principales:

```sql
CREATE PUBLICATION claims_pub
  FOR TABLE insurance_policies.policies,
             claim_events.claims;
```

Para la integración con el data warehouse, una publication separada y dedicada:

```sql
CREATE PUBLICATION fraud_audit_pub
  FOR TABLE fraud_detection_audit.new_claims_for_analysis;
```

Separar las publications por caso de uso es una decisión deliberada: permite gestionar permisos, monitorización y ciclo de vida de forma independiente.

**Usuario de replicación** — el subscriber se conecta con un usuario dedicado que debe tener el rol `REPLICATION` y permisos `SELECT` sobre las tablas publicadas:

```sql
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD '...';
GRANT SELECT ON insurance_policies.policies TO replicator;
GRANT SELECT ON claim_events.claims TO replicator;
GRANT SELECT ON fraud_detection_audit.new_claims_for_analysis TO replicator;
```

Verificar también que `pg_hba.conf` permita la conexión desde la IP del subscriber con el método de autenticación apropiado (preferiblemente `scram-sha-256`).

### Subscriber para migración: `pg-claims-new-01` (PostgreSQL 15.3)

```sql
-- En pg-claims-new-01
ALTER SYSTEM SET max_worker_processes = '10';
SELECT pg_reload_conf();

CREATE SUBSCRIPTION claims_sub
  CONNECTION 'host=pg-claims-primary-01 port=5432 user=replicator password=...'
  PUBLICATION claims_pub;
```

En el momento del `CREATE SUBSCRIPTION`, PostgreSQL inicia el snapshot inicial: copia todas las filas existentes en las tablas publicadas y luego pasa a replicar los cambios en streaming. Con 150 millones de filas entre `policies` y `claims`, este snapshot requirió varias horas — planificado en un momento de baja actividad.

### Subscriber para el data warehouse: `pg-dw-subscriber-01` (PostgreSQL 15.3)

```sql
-- En pg-dw-subscriber-01
ALTER SYSTEM SET max_worker_processes = '5';
SELECT pg_reload_conf();

CREATE SUBSCRIPTION fraud_audit_sub
  CONNECTION 'host=pg-claims-primary-01 port=5432 user=replicator password=...'
  PUBLICATION fraud_audit_pub;
```

---

## Monitorización y troubleshooting

«¿Cómo sé si está funcionando?» — la pregunta de Claudio más útil de todas.

### Lag de replicación

La vista `pg_replication_slots` en el publisher muestra el estado de los slots activos y el volumen de WAL retenido:

```sql
SELECT
  slot_name,
  active,
  pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS replication_lag_bytes
FROM pg_replication_slots
WHERE slot_type = 'logical';
```

Un `replication_lag_bytes` en crecimiento constante indica un subscriber con problemas. Si `active` es `false` y el lag sigue aumentando, el slot está acumulando WAL sin consumirlos: situación que hay que resolver rápidamente.

En el subscriber, `pg_stat_subscription` y `pg_stat_subscription_stats` muestran el estado de la aplicación:

```sql
SELECT
  subname,
  subenabled,
  subconninfo,
  subslotname,
  substate,
  subbinary
FROM pg_subscription;

SELECT
  subid,
  relid,
  last_applied_lsn,
  last_received_lsn,
  pg_wal_lsn_diff(last_received_lsn, last_applied_lsn) AS apply_lag_bytes
FROM pg_stat_subscription_stats;
```

`apply_lag_bytes` mide el retraso entre lo que el subscriber ha recibido y lo que ha aplicado efectivamente. Un valor estable y bajo indica un sistema en buen estado.

### Conflictos y primary key

El conflicto más habitual en replicación lógica es la violación de primary key: el subscriber recibe un `INSERT` para una fila que ya existe localmente. Esto ocurre típicamente cuando el subscriber tiene datos preexistentes no alineados con el publisher.

PostgreSQL registra los conflictos en el log del subscriber con mensajes del tipo:

```
ERROR: duplicate key value violates unique constraint "claims_pkey"
```

La replicación se detiene hasta que se resuelve el conflicto. Las opciones son: eliminar la fila conflictiva en el subscriber, o usar `ALTER SUBSCRIPTION ... SKIP` para saltar la transacción problemática (siendo consciente de las implicaciones sobre la consistencia).

### Gestión de las DDL

«Si añado una columna en el publisher, ¿el subscriber la ve?» preguntó Claudio, y la respuesta requirió una pausa.

No — no automáticamente. La replicación lógica transporta los datos, no los cambios de esquema. Si se añade una columna `NOT NULL` sin valor por defecto en el publisher, la replicación se interrumpe porque el subscriber no sabe dónde colocar el valor.

El procedimiento correcto es:

1. Añadir la columna en el subscriber antes que en el publisher (con un valor por defecto o como `NULL`)
2. Añadir la columna en el publisher
3. Verificar que la replicación se reanuda correctamente

Para cambios de esquema frecuentes o complejos, herramientas como `pg_logical` o soluciones CDC dedicadas (Debezium, pgoutput con consumers externos) ofrecen una gestión más sofisticada. En este proyecto, las DDL eran poco frecuentes y planificadas: el procedimiento manual era suficiente.

---

## Buenas prácticas y consideraciones operativas

**Espacio WAL** — dimensionar `max_slot_wal_keep_size` (disponible desde la versión 13) para limitar la acumulación de WAL en caso de subscribers inactivos. Sin este parámetro, un subscriber desconectado puede agotar el espacio en disco del publisher.

**Seguridad** — usar siempre `scram-sha-256` en `pg_hba.conf` para las conexiones de replicación. Valorar SSL obligatorio añadiendo `sslmode=require` en la cadena de conexión de la subscription. No usar el usuario `postgres` para la replicación.

**Slots huérfanos** — un slot de replicación que ya no se usa pero no se ha eliminado sigue reteniendo WAL. Monitorizar periódicamente `pg_replication_slots` y eliminar los slots obsoletos con `SELECT pg_drop_replication_slot('nombre_slot')`.

**Tablas sin primary key** — la replicación lógica en modo `UPDATE` y `DELETE` requiere una primary key o una replica identity configurada (`REPLICA IDENTITY FULL` como alternativa, con impacto en el rendimiento). Verificar todas las tablas antes de crear la publication.

**Switchover final** — en el caso de la migración, el momento crítico es el corte: se deshabilita la escritura en el publisher (o se redirige el tráfico), se espera a que el lag baje a cero, se verifica la consistencia, se promueve el nuevo clúster. Con el lag monitorizado durante los días anteriores y estable por debajo de los 500ms, el switchover requirió menos de tres minutos.

---

## Las preguntas de Claudio

El sistema entró en producción sin contratiempos. No hubo un problema de última hora, no hubo un momento de tensión que contar. El nuevo clúster PostgreSQL 15 asumió el tráfico, el data warehouse siguió recibiendo los datos antifraude, y el grupo asegurador tuvo su upgrade sin ventanas de mantenimiento visibles para los usuarios.

Claudio tiene una comprensión más concreta de lo que observó. Yo tengo una comprensión más articulada de lo que sé — porque tuve que encontrar las palabras correctas, no solo los comandos correctos. Explicar la diferencia entre replicación física y lógica a alguien que no la conoce significa tener que entenderla lo suficientemente bien como para elegir el ejemplo adecuado, no solo el técnicamente preciso.

Las preguntas de Claudio no cambiaron las decisiones técnicas. Las hicieron más sólidas.

---

## Fuentes oficiales

[1] PostgreSQL Documentation — [Logical Replication](https://www.postgresql.org/docs/current/logical-replication.html) — conceptos generales, arquitectura, diferencias con la replicación física.

[2] PostgreSQL Documentation — [CREATE PUBLICATION](https://www.postgresql.org/docs/current/sql-create-publication.html) — sintaxis completa, opciones de filtrado por fila (PostgreSQL 15+), gestión de secuencias.

[3] PostgreSQL Documentation — [CREATE SUBSCRIPTION](https://www.postgresql.org/docs/current/sql-create-subscription.html) — sintaxis, opciones de conexión, gestión del snapshot inicial.

[4] PostgreSQL Documentation — [Monitoring — pg_stat_replication_slots](https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-REPLICATION-SLOTS-VIEW) — vistas de sistema para la monitorización de slots.

[5] PostgreSQL Documentation — [Replication Slots](https://www.postgresql.org/docs/current/warm-standby.html#STREAMING-REPLICATION-SLOTS) — mecanismo de slots, riesgos de acumulación WAL, `max_slot_wal_keep_size`.

---

## Glosario candidato

**Publication** — objeto PostgreSQL que define el conjunto de tablas (y opcionalmente filas, desde la versión 15) cuyos cambios se ponen a disposición para la replicación lógica. Se crea en el publisher con `CREATE PUBLICATION` y puede ser referenciada por múltiples subscribers independientes.

**Subscription** — objeto PostgreSQL creado en el subscriber que establece la conexión al publisher, especifica la publication a la que suscribirse y gestiona el ciclo de vida de la replicación: snapshot inicial, streaming de los cambios, reconexión automática.

**Slot de replicación lógica** — estructura persistente en el publisher que rastrea la posición de consumo de los WAL para cada subscriber. Garantiza que ningún cambio se pierda ante una desconexión temporal, a costa de retener los segmentos WAL hasta su consumo.

**WAL (Write-Ahead Log)** — registro secuencial de todos los cambios aplicados a la base de datos PostgreSQL, escrito antes de que los cambios se apliquen a los archivos de datos. Es la fuente de la que la replicación lógica extrae las operaciones a transmitir a los subscribers mediante el proceso de decodificación lógica.

**CDC (Change Data Capture)** — técnica que intercepta y transmite en tiempo casi real los cambios en los datos de una fuente hacia sistemas destinatarios (data warehouse, message broker, aplicaciones). La replicación lógica de PostgreSQL implementa CDC de forma nativa mediante el protocolo `pgoutput`.
