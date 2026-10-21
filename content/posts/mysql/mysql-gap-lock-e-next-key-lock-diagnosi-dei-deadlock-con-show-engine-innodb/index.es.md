---
categories:
- mysql
date: '2026-11-03'
description: 'Gap lock y next-key lock de InnoDB explicados en un caso real: deadlocks
  en INSERT concurrentes, diagnóstico con SHOW ENGINE INNODB STATUS y cuándo READ
  COMMITTED resuelve todo.'
draft: false
image: mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb.cover.jpg
seoTitle: 'MySQL gap lock y next-key lock: diagnóstico de deadlocks InnoDB'
tags:
- innodb
- locking
- deadlock
- isolation-level
- concurrency
title: 'MySQL gap lock y next-key lock: diagnóstico y solución de deadlocks'
translationKey: mysql_gap_lock_e_next_key_lock_diagnosi_dei_deadlock_con_show_engine_innodb
webo_generated_at: 2026-10-21
webo_status: scheduled
---

## La reunión del martes por la mañana

Era un martes por la mañana y la reunión había empezado mal. A un lado el equipo de desarrollo, al otro el DBA del cliente — un operador postal y logístico nacional con alrededor de mil quinientas instancias MySQL distribuidas en otros tantos nodos. El sistema de seguimiento de paquetes generaba deadlocks esporádicos en las INSERT, unos tres o cuatro al día en condiciones de carga normal, muchos más en los picos de clasificación.

Los desarrolladores habían traído los logs de la aplicación: "el database bloquea nuestras INSERT sin motivo". El DBA había traído las gráficas de utilización: "las queries están mal escritas, hacen range scan sobre tablas enormes". Ambos tenían razón en algo. Ambos se equivocaban en la causa.

El problema estaba en los gap lock de InnoDB — un mecanismo que la mayoría de los equipos conoce de nombre pero no entiende de verdad hasta que se lo encuentra de frente en producción.

## Record lock, gap lock, next-key lock: tres cosas distintas

Antes de entrar en el caso concreto, vale la pena aclarar la terminología porque InnoDB usa tres tipos de lock distintos que a menudo se confunden.

Un **record lock** bloquea una única fila del índice. Si haces `SELECT ... FOR UPDATE WHERE id = 42`, InnoDB pone un record lock sobre la fila con `id = 42`. Intuitivo.

Un **gap lock** bloquea un *intervalo* entre dos valores del índice — el "hueco" entre dos registros existentes — sin bloquear los registros en sí. Si en el índice tienes los valores 10, 20, 30, un gap lock sobre el intervalo (10, 20) impide que cualquier otra transacción inserte un valor en ese intervalo. El punto clave: el gap lock no bloquea los registros existentes, bloquea el espacio entre ellos.

Un **next-key lock** es la combinación de ambos: record lock sobre el registro actual más gap lock sobre el intervalo que lo precede. Es el tipo de lock predeterminado que InnoDB usa para los escaneos de índice en `REPEATABLE READ`. Si haces un range scan que toca los valores 10, 20, 30, InnoDB pone next-key lock sobre (-∞, 10], (10, 20], (20, 30], (30, +∞). Estás bloqueando no solo los registros que has leído, sino todos los "huecos" entre ellos.

¿Por qué hace esto InnoDB? Para prevenir los **phantom read** — la situación en que una transacción lee un rango dos veces y obtiene resultados distintos porque otra transacción ha insertado filas en medio. En `REPEATABLE READ`, el estándar SQL exige que esto no ocurra, e InnoDB lo garantiza bloqueando los gaps.

```sql
-- Ejemplo: esta query en REPEATABLE READ
-- adquiere next-key lock sobre el intervalo escaneado
SELECT * FROM shipment_log
WHERE status = 'PENDING' AND created_at > '2024-01-15 08:00:00'
FOR UPDATE;
```

El problema surge cuando dos transacciones hacen range scan sobre intervalos solapados y luego ambas intentan hacer INSERT en el mismo gap. Deadlock clásico.

## Por qué REPEATABLE READ es el contexto donde todo explota

MySQL usa `REPEATABLE READ` como isolation level predeterminado [1]. Es una decisión histórica ligada a la replicación basada en statements — en `READ COMMITTED`, ciertos patrones de replicación binlog podían producir inconsistencias en el esclavo. Con la replicación row-based (predeterminada desde MySQL 5.7.7) esa preocupación está en gran medida superada, pero el default se mantuvo.

En `REPEATABLE READ`, InnoDB debe garantizar que una transacción vea siempre el mismo snapshot de los datos durante toda su duración. Para las lecturas normales (sin `FOR UPDATE`) usa MVCC — lee una versión histórica de los datos y no adquiere locks. Pero para las lecturas con lock (`SELECT ... FOR UPDATE`, `SELECT ... LOCK IN SHARE MODE`) y para las operaciones de escritura, debe usar los next-key lock para prevenir los phantoms.

El patrón que generaba deadlocks en el caso del seguimiento de paquetes era este:

1. Transacción A: busca los paquetes en estado `PENDING` en un determinado intervalo de tiempo → adquiere next-key lock sobre un rango del índice
2. Transacción B: hace lo mismo sobre un rango solapado → adquiere next-key lock sobre un rango que se solapa parcialmente
3. Transacción A: intenta insertar un nuevo registro de log → el registro cae en el gap bloqueado por B → espera
4. Transacción B: intenta insertar un nuevo registro de log → el registro cae en el gap bloqueado por A → espera
5. InnoDB detecta el ciclo y mata una de las dos transacciones

El código de la aplicación no tenía nada incorrecto en sentido absoluto. El problema era la interacción entre el patrón de acceso (range scan + INSERT en el mismo gap) y el isolation level predeterminado.

## Diagnóstico: SHOW ENGINE INNODB STATUS

Cuando se sospecha un deadlock en MySQL, la primera herramienta es `SHOW ENGINE INNODB STATUS` [2]. La sección que interesa es `LATEST DETECTED DEADLOCK`, que muestra el último deadlock detectado por InnoDB con todos los detalles: las transacciones implicadas, los locks que mantenían, los locks que esperaban y qué transacción fue elegida como víctima.

```sql
SHOW ENGINE INNODB STATUS\G
```

La salida es verbosa y hay que leerla con atención. Un ejemplo simplificado de lo que se encuentra en la sección de deadlock:

```text
------------------------
LATEST DETECTED DEADLOCK
------------------------
2024-01-16 09:23:41 0x7f8b4c001700
*** (1) TRANSACTION:
TRANSACTION 421938, ACTIVE 0 sec inserting
mysql tables in use 1, locked 1
LOCK WAIT 4 lock struct(s), heap size 1136, 2 row lock(s)
MySQL thread id 1842, OS thread handle 140234..., query id 98234 ...
INSERT INTO shipment_log (shipment_id, status, created_at)
VALUES (10045, 'PROCESSING', NOW())

*** (1) HOLDS THE LOCK(S):
RECORD LOCKS space id 312 page no 4 n bits 72 index idx_status_created
of table `tracking`.`shipment_log` trx id 421938 lock_mode X locks gap before rec

*** (1) WAITING FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS space id 312 page no 4 n bits 72 index idx_status_created
of table `tracking`.`shipment_log` trx id 421938 lock_mode X locks gap before rec insert intention waiting

*** (2) TRANSACTION:
TRANSACTION 421939, ACTIVE 0 sec inserting
...
*** (2) HOLDS THE LOCK(S):
RECORD LOCKS ... lock_mode X locks gap before rec

*** (2) WAITING FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS ... lock_mode X locks gap before rec insert intention waiting

*** WE ROLL BACK TRANSACTION (2)
```

Las frases clave que hay que buscar: `lock_mode X locks gap before rec` (gap lock adquirido) e `insert intention waiting` (INSERT esperando entrar en un gap bloqueado). Cuando ves ambas en un deadlock, estás mirando exactamente el patrón gap lock / INSERT intention lock.

Otra herramienta útil, disponible desde MySQL 5.6, es la tabla `performance_schema.data_locks` (o `information_schema.INNODB_LOCKS` en versiones anteriores):

```sql
-- MySQL 8.0+
SELECT
    r.trx_id AS waiting_trx,
    r.trx_mysql_thread_id AS waiting_thread,
    r.trx_query AS waiting_query,
    b.trx_id AS blocking_trx,
    b.trx_mysql_thread_id AS blocking_thread,
    b.trx_query AS blocking_query
FROM information_schema.INNODB_TRX b
JOIN information_schema.INNODB_TRX r
    ON r.trx_id != b.trx_id
JOIN performance_schema.data_locks dl
    ON dl.ENGINE_TRANSACTION_ID = r.trx_id
    AND dl.LOCK_STATUS = 'WAITING'
WHERE b.trx_id = dl.BLOCKING_ENGINE_TRANSACTION_ID;
```

## El caso reconstruido paso a paso

La tabla implicada tenía una estructura similar a esta:

```sql
CREATE TABLE shipment_log (
    id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    shipment_id BIGINT UNSIGNED NOT NULL,
    status      VARCHAR(20) NOT NULL,
    created_at  DATETIME NOT NULL,
    INDEX idx_status_created (status, created_at)
);
```

El código de la aplicación, simplificado, hacía esto en una única transacción:

```sql
-- Paso 1: busca los registros recientes en estado PENDING
SELECT id, shipment_id FROM shipment_log
WHERE status = 'PENDING'
  AND created_at > NOW() - INTERVAL 5 MINUTE
FOR UPDATE;

-- Paso 2: actualiza el estado de los registros encontrados
UPDATE shipment_log SET status = 'PROCESSING'
WHERE id IN (...);

-- Paso 3: inserta un registro de auditoría
INSERT INTO shipment_log (shipment_id, status, created_at)
VALUES (?, 'PROCESSING', NOW());
```

El `FOR UPDATE` en el paso 1 era intencional — el equipo quería evitar que dos workers paralelos procesaran el mismo paquete. Razonable. El problema es que ese `SELECT ... FOR UPDATE` con la condición sobre `created_at > NOW() - INTERVAL 5 MINUTE` adquiría next-key lock sobre todo el rango del índice `idx_status_created` para los valores de `created_at` en los últimos cinco minutos. Y el INSERT del paso 3 insertaba un registro con `created_at = NOW()` — exactamente en el gap bloqueado por la otra transacción concurrente.

Dos workers que arrancaban con pocos milisegundos de diferencia se encallaban sistemáticamente.

## READ COMMITTED: cuándo es la respuesta correcta

La solución más directa, en el caso concreto, era bajar el isolation level a `READ COMMITTED` para esas transacciones [3]:

```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

En `READ COMMITTED`, InnoDB no usa gap lock para las lecturas. Usa solo record lock sobre las filas efectivamente encontradas. El motivo es que en `READ COMMITTED` los phantom read están permitidos — cada statement ve los datos committed en el momento de su ejecución, no en el momento de inicio de la transacción. Sin necesidad de prevenir los phantoms, no hacen falta los gap lock, y el patrón de deadlock desaparece.

La pregunta legítima es: ¿es seguro? Depende del contexto, y vale la pena ser explícito sobre los trade-offs.

`READ COMMITTED` es seguro cuando:
- La lógica de la aplicación no depende de la estabilidad del rango entre dos lecturas dentro de la misma transacción (es decir, no importa si otra transacción inserta filas en medio)
- Se está usando replicación row-based (predeterminada desde MySQL 5.7.7) — con la replicación statement-based, `READ COMMITTED` puede producir inconsistencias en el esclavo en ciertos escenarios de UPDATE/DELETE con subqueries [4]
- Los phantom read no son un problema para la semántica de la aplicación

En el caso del seguimiento de paquetes, la respuesta a las tres preguntas era sí. El worker no necesitaba un rango estable — necesitaba procesar los paquetes disponibles en ese momento, no garantizar que ningún otro paquete hubiera aparecido en medio. La replicación era row-based. Los phantom read eran irrelevantes para la corrección del sistema.

El cambio se hizo a nivel de sesión en el connection pool, no a nivel global — una decisión conservadora que permitía dejar `REPEATABLE READ` como default para el resto del sistema.

## Patrones para reducir los deadlocks sin cambiar el isolation level

`READ COMMITTED` no es siempre la respuesta. Cuando no se puede o no se quiere cambiar el isolation level, hay otros patrones que reducen la probabilidad de deadlock.

**Orden de acceso consistente.** La mayoría de los deadlocks clásicos (no por gap lock) surge de transacciones que acceden a los mismos recursos en orden distinto. Si la transacción A bloquea primero la tabla X y luego la Y, y la transacción B hace lo contrario, el deadlock está casi garantizado. Estandarizar el orden de acceso a los recursos elimina esta clase de situaciones.

**Batch size reducido.** Los range scan sobre intervalos grandes adquieren gap lock sobre intervalos grandes. Reducir la ventana temporal de la query (de 5 minutos a 30 segundos, por ejemplo) reduce la amplitud de los gap lock y la probabilidad de solapamiento.

```sql
-- En lugar de:
WHERE status = 'PENDING' AND created_at > NOW() - INTERVAL 5 MINUTE

-- Considera:
WHERE status = 'PENDING' AND created_at > NOW() - INTERVAL 30 SECOND
  AND created_at <= NOW() - INTERVAL 5 SECOND  -- evita la ventana más reciente
```

**Retry logic en la aplicación.** Los deadlocks en InnoDB son eventos normales, no anomalías. InnoDB siempre elige una víctima y hace rollback de una de las transacciones — la aplicación debe estar preparada para reintentar. Un patrón robusto prevé un retry con backoff exponencial y un número máximo de intentos:

```python
import time
import random
import mysql.connector

def execute_with_retry(conn, fn, max_retries=3):
    for attempt in range(max_retries):
        try:
            return fn(conn)
        except mysql.connector.errors.DatabaseError as e:
            if e.errno == 1213 and attempt < max_retries - 1:
                # ER_LOCK_DEADLOCK — reintenta con backoff
                wait = (2 ** attempt) + random.uniform(0, 0.5)
                time.sleep(wait)
                continue
            raise
```

**Índices selectivos en la columna de lock.** Si el `FOR UPDATE` es necesario, un índice más selectivo reduce el número de filas (y gaps) implicados en el escaneo. En el caso concreto, añadir `shipment_id` al índice y filtrar por worker específico habría reducido drásticamente la amplitud del rango bloqueado.

## Lo que queda después de la reunión

El cambio a `READ COMMITTED` a nivel de sesión eliminó los deadlocks en menos de una hora desde el despliegue. No era magia — era la consecuencia directa de entender qué estaba pasando bajo el capó.

Lo más útil que salió de esa semana de análisis no era la solución en sí, sino el método: leer `SHOW ENGINE INNODB STATUS` con atención, entender la diferencia entre record lock y gap lock, y no dar por sentado que el default de MySQL es siempre el adecuado para el propio caso de uso. `REPEATABLE READ` es una elección conservadora y correcta en muchos contextos. En otros, como el de los workers concurrentes con range scan + INSERT, es la causa directa de los problemas.

El DBA del cliente añadió el monitoreo de deadlocks a su sistema de alertas — una query periódica sobre `information_schema.INNODB_METRICS` que rastrea el contador `lock_deadlocks`. Los desarrolladores añadieron la retry logic. Ambas cosas eran necesarias, y ninguna de las dos por sí sola habría sido suficiente.

## Fontes oficiales

1. MySQL Documentation — [InnoDB Transaction Isolation Levels](https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-isolation-levels.html)
2. MySQL Documentation — [SHOW ENGINE INNODB STATUS](https://dev.mysql.com/doc/refman/8.0/en/innodb-standard-monitor.html)
3. MySQL Documentation — [InnoDB Locking: Gap Locks](https://dev.mysql.com/doc/refman/8.0/en/innodb-locking.html#innodb-gap-locks)
4. MySQL Documentation — [Binary Logging Formats and READ COMMITTED](https://dev.mysql.com/doc/refman/8.0/en/binary-log-formats.html)

## Glosario
- **[Gap lock](/es/glossary/gap-lock/)** (InnoDB) — lock que bloquea un intervalo entre dos valores de un índice, sin bloquear los registros en sí. Impide INSERT en el intervalo bloqueado. Activo en `REPEATABLE READ`, ausente en `READ COMMITTED`.

- **[Next-key lock](/es/glossary/gap-lock/)** (InnoDB) — combinación de record lock sobre el registro actual y gap lock sobre el intervalo que lo precede. Tipo de lock predeterminado para los escaneos de índice en `REPEATABLE READ`; previene los phantom read.

- **[Insert intention lock](/es/glossary/next-key-lock/)** (InnoDB) — lock de intención adquirido por un INSERT antes de insertar un registro en un gap. Compatible con otros insert intention lock sobre el mismo gap, pero bloqueado por los gap lock existentes. Causa directa de los deadlocks por INSERT concurrentes.

- **[REPEATABLE READ](/es/glossary/gap-lock/)** — isolation level predeterminado de MySQL/InnoDB. Garantiza que una transacción vea siempre el mismo snapshot de los datos durante toda su duración; implementado mediante MVCC para las lecturas y next-key lock para las operaciones con lock.

- **[Phantom read](/es/glossary/next-key-lock/)** — anomalía de concurrencia en la que una transacción lee un rango dos veces y obtiene resultados distintos porque otra transacción ha insertado o eliminado filas en medio. Prevenido por `REPEATABLE READ` mediante gap lock; permitido en `READ COMMITTED`.
