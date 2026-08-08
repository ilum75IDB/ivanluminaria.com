---
categories:
- mysql
date: 2099-12-31
description: 'Cuatro horas de lag en un sistema logístico: cómo diagnosticamos el
  problema, por qué Seconds_Behind_Master engaña y qué cambios lo resolvieron.'
draft: true
image: replica-mysql-quando-lo-slave-resta-indietro-e-nessuno-se-ne-accorge.cover.jpg
seoTitle: 'Lag réplica MySQL: GTID, parallel replication y pt-heartbeat'
tags:
- mysql
- replication
- performance-tuning
- monitoring
- gtid
title: 'El informe del lunes por la mañana: lag de réplica MySQL y por qué Seconds_Behind_Master
  miente'
translationKey: replica_mysql_quando_lo_slave_resta_indietro_e_nessuno_se_ne_accorge
webo_generated_at: 2026-08-08
webo_status: da_tradurre
---

## El informe del lunes por la mañana

Era un lunes por la mañana. El responsable comercial de un gran operador postal y logístico nacional acababa de abrir el informe semanal de envíos y estaba mirando números que no cuadraban. Las entregas del viernes por la tarde seguían apareciendo como "en tránsito". Los KPI del sábado estaban a cero. Algo fallaba, y la primera hipótesis había sido un bug en la aplicación de reporting.

Cuando llegamos a echar un vistazo, el bug no existía. Había algo más sutil: la réplica MySQL sobre la que corrían todas las consultas de reporting acumulaba cuatro horas de retraso respecto al master. Los datos estaban ahí, correctos, en el master — pero la réplica los estaba aplicando con horas de demora. Y ninguna alerta había saltado.

Cuatro horas de lag en un sistema logístico significan decisiones operativas tomadas con números equivocados. Significa que el responsable de almacén planificó los turnos del fin de semana con datos que no reflejaban la realidad. Significa que el sistema de priorización de envíos urgentes trabajaba sobre una fotografía de media jornada laboral atrás.

Este artículo cuenta cómo funciona la réplica MySQL bajo el capó, por qué su principal herramienta de monitorización es poco fiable, y qué hicimos para resolverlo — sin magia, con profiling y algunas decisiones arquitectónicas.

---

## Binlog, relay log, y los dos threads que no se hablan lo suficiente

Para entender por qué la réplica acumula lag, hay que entender cómo funciona de verdad. La réplica MySQL asíncrona se basa en tres componentes principales: el **binary log** en el master, el **relay log** en el slave, y dos threads que trabajan en secuencia.

El **IO thread** en el slave se conecta al master y lee los eventos del binlog, escribiéndolos localmente en el relay log. Es una lectura secuencial, generalmente rápida, raramente el cuello de botella.

El **SQL thread** lee el relay log y aplica los eventos a la base de datos local del slave. Aquí está el problema: en configuración clásica, este thread es **single-threaded**. Aplica un evento cada vez, en secuencia. Si el master tiene diez sesiones escribiendo en paralelo, el slave las aplica una detrás de otra.

```text
MASTER
  ├── sesión 1 → INSERT INTO spedizioni (...)
  ├── sesión 2 → UPDATE tracking SET stato = 'consegnato' WHERE ...
  ├── sesión 3 → INSERT INTO eventi_logistici (...)
  └── ... (N sesiones paralelas)
         │
         ▼ binlog (serializado)
SLAVE IO thread → relay log → SQL thread (single-threaded)
         ▼
  aplica evento 1, luego evento 2, luego evento 3...
```

El master escribe en paralelo, el slave aplica en serie. En un sistema con carga sostenida, esta asimetría es la causa principal del lag.

---

## Por qué Seconds_Behind_Master miente

Lo primero que miras cuando sospechas lag es `SHOW SLAVE STATUS\G`. El campo `Seconds_Behind_Master` parece exactamente lo que necesitas. No lo es.

```sql
SHOW SLAVE STATUS\G
-- ...
Seconds_Behind_Master: 14523
-- ...
```

Catorce mil segundos. Cuatro horas. El número estaba ahí — pero el problema es que este valor se calcula de una forma que lo hace poco fiable en varios escenarios habituales.

`Seconds_Behind_Master` mide la diferencia entre el timestamp del evento que el SQL thread está **aplicando en ese momento** y la hora actual del sistema. Si el SQL thread está parado (porque está bloqueado por un lock, porque ha tenido un error, porque el relay log se ha agotado y el IO thread aún no ha recibido nuevos eventos), el valor deja de actualizarse o se comporta de forma imprevisible.

Aún más insidioso: si la réplica se interrumpe y luego se reinicia, `Seconds_Behind_Master` puede volver a cero antes de que el lag se haya recuperado realmente, porque el IO thread ha descargado el relay log pero el SQL thread aún no ha terminado de aplicarlo. El campo refleja el estado del SQL thread, no el retraso real respecto al master.

En la práctica, `Seconds_Behind_Master` es útil como indicador grueso, pero no como base para el alerting. [1]

**Qué usar en su lugar**: con la **replicación basada en GTID** activa, se puede calcular el lag real comparando el conjunto de transacciones ejecutadas en el master (`gtid_executed` en el master) con el aplicado en el slave (`gtid_executed` en el slave). La diferencia — el número de transacciones pendientes — es una métrica mucho más fiable.

```sql
-- En el master
SELECT @@global.gtid_executed;

-- En el slave
SELECT @@global.gtid_executed;
-- La diferencia entre los dos conjuntos es el lag real en términos de transacciones
```

Con herramientas como `pt-heartbeat` de Percona Toolkit se puede medir el lag de forma aún más precisa: la herramienta escribe un timestamp en el master a intervalos regulares y mide cuánto tarda en aparecer en el slave. [2]

---

## Las causas más comunes de slave lag

En este caso concreto, identificamos tres causas concurrentes:

**1. Consultas pesadas sin optimizar en el master**

El master ejecutaba cada noche un batch de actualización masiva: `UPDATE spedizioni SET stato_elaborazione = 'archiviato' WHERE data_spedizione < DATE_SUB(NOW(), INTERVAL 90 DAY)`. Sin índice en `data_spedizione`. La consulta hacía un full table scan sobre una tabla de 180 millones de filas, producía un único evento binlog enorme, y el slave tardaba 40 minutos en aplicarlo — durante los cuales no aplicaba nada más.

**2. SQL thread single-threaded bajo carga sostenida**

Durante las horas pico (de 14 a 18 h), el master recibía unas 800 escrituras por segundo distribuidas en decenas de sesiones paralelas. El SQL thread no conseguía mantenerse al día: cada hora de producción intensa añadía unos 20-30 minutos de lag acumulado.

**3. I/O lento en el slave**

El slave estaba en almacenamiento compartido con otros servicios. En las horas pico, la latencia de escritura en disco subía a valores que ralentizaban aún más la aplicación de eventos. El relay log se escribía y leía con latencias que multiplicaban el problema del single-thread.

---

## GTID: por qué vale la pena migrar cuanto antes

El **Global Transaction ID** (GTID) es un identificador único asignado a cada transacción commiteada en el master. [3] Cada transacción tiene un GTID con el formato `source_id:transaction_id`, donde `source_id` es el UUID del servidor master.

```sql
-- Habilitar GTID en el master (requiere restart o SET PERSIST en MySQL 8.0+)
SET PERSIST gtid_mode = ON;
SET PERSIST enforce_gtid_consistency = ON;

-- Verificar el estado
SHOW VARIABLES LIKE 'gtid_mode';
-- gtid_mode | ON
```

Las ventajas respecto a la réplica basada en posición de binlog son concretas:

- **Failover más sencillo**: con GTID, un nuevo slave sabe exactamente desde dónde retomar sin tener que calcular manualmente la posición en el binlog
- **Monitorización del lag real**: como se ha descrito, comparar los conjuntos GTID es mucho más fiable que `Seconds_Behind_Master`
- **Detección de transacciones faltantes**: si una transacción se ha aplicado en el master pero no en el slave, el gap es inmediatamente visible en el conjunto GTID

En el contexto de este proyecto, la migración a GTID ya estaba planificada pero aún no ejecutada. Haberla completado antes de afrontar el problema del lag habría hecho el diagnóstico mucho más rápido.

---

## De single-thread a parallel replication

La solución al cuello de botella del SQL thread es la **parallel replication**, disponible en MySQL 5.7+ y MariaDB 10.0+. [4]

La idea de base: en lugar de aplicar los eventos en secuencia con un único thread, se usan varios worker threads que aplican transacciones en paralelo — respetando las restricciones de consistencia.

MySQL ofrece dos modos de paralelización:

- **`DATABASE`**: las transacciones que modifican bases de datos distintas se aplican en paralelo. Sencillo, pero inútil si todas las escrituras van a la misma base de datos.
- **`LOGICAL_CLOCK`** (el modo correcto para la mayoría de los casos): aprovecha la información de commit timestamp en el binlog para identificar transacciones que estaban en ejecución simultáneamente en el master y que, por tanto, pueden aplicarse en paralelo en el slave.

```sql
-- Configuración en el slave
STOP SLAVE SQL_THREAD;

SET GLOBAL slave_parallel_type = 'LOGICAL_CLOCK';
SET GLOBAL slave_parallel_workers = 8;
SET GLOBAL slave_preserve_commit_order = ON;

START SLAVE SQL_THREAD;
```

El parámetro `slave_preserve_commit_order = ON` garantiza que las transacciones se commiteen en el slave en el mismo orden que en el master — fundamental para la consistencia de las lecturas. [4]

Para aprovechar al máximo `LOGICAL_CLOCK`, el master debe tener `binlog_group_commit_sync_delay` configurado de forma que agrupe varias transacciones en el mismo commit group. Esto aumenta ligeramente la latencia de commit en el master, pero incrementa significativamente el paralelismo disponible en el slave.

```sql
-- En el master: ampliar la ventana de group commit
-- (valor en microsegundos, 1000 = 1ms)
SET GLOBAL binlog_group_commit_sync_delay = 1000;
SET GLOBAL binlog_group_commit_sync_no_delay_count = 10;
```

---

## Lo que funcionó de verdad

Trabajamos en tres frentes en paralelo, y el resultado final fue reducir el lag de cuatro horas a menos de treinta segundos en condiciones normales.

**Frente 1: parallel replication con 8 workers**

Tras habilitar `LOGICAL_CLOCK` con 8 worker threads, el throughput del slave aumentó de forma significativa. El lag acumulado se redujo en pocas horas. El DBA del cliente ya había valorado esta opción anteriormente, pero había encontrado resistencia interna porque "llevaba años funcionando así" — la crisis desbloqueó la conversación.

**Frente 2: optimización de la consulta batch**

La consulta de archivado nocturno se reescribió para operar en lotes más pequeños, añadiendo un índice en `data_spedizione`:

```sql
-- Antes: un único UPDATE enorme
UPDATE spedizioni
SET stato_elaborazione = 'archiviato'
WHERE data_spedizione < DATE_SUB(NOW(), INTERVAL 90 DAY);

-- Después: lotes de 10.000 filas con pausa entre cada lote
-- (ejecutado desde un script Python con loop + sleep)
UPDATE spedizioni
SET stato_elaborazione = 'archiviato'
WHERE data_spedizione < DATE_SUB(NOW(), INTERVAL 90 DAY)
  AND stato_elaborazione != 'archiviato'
LIMIT 10000;
```

```sql
-- Índice añadido
ALTER TABLE spedizioni
ADD INDEX idx_data_elaborazione (data_spedizione, stato_elaborazione);
```

Esto eliminó el pico de lag nocturno: en lugar de un único evento de 40 minutos, el slave aplicaba miles de eventos pequeños distribuidos a lo largo de una hora, sin bloquearse en ningún momento.

**Frente 3: almacenamiento dedicado para el slave**

El slave se trasladó a almacenamiento dedicado con latencias de escritura consistentes. Esto por sí solo no habría resuelto el problema, pero eliminó la variabilidad que hacía el lag impredecible en las horas pico.

---

## Monitorización que no engaña

Tras resolver el lag, construimos un sistema de alerting que no dependiera de `Seconds_Behind_Master`.

La solución adoptada fue `pt-heartbeat` de Percona Toolkit, configurado para escribir un timestamp en el master cada segundo y medir el retraso en el slave:

```bash
# En el master: arrancar el daemon que escribe el heartbeat
pt-heartbeat \
  --user=monitor_user \
  --password=*** \
  --host=mysql-master-01 \
  --database=monitoring \
  --create-table \
  --daemonize \
  --update

# En el slave: medir el lag real
pt-heartbeat \
  --user=monitor_user \
  --password=*** \
  --host=mysql-replica-01 \
  --database=monitoring \
  --monitor \
  --master-server-id=1
```

El valor que devuelve `pt-heartbeat --monitor` es el lag real en segundos, calculado a partir de timestamps efectivos — no de la posición en el binlog ni de `Seconds_Behind_Master`.

Configuramos alertas en dos umbrales:

- **Warning a 60 segundos**: notificación al equipo, sin acción automática
- **Critical a 300 segundos (5 minutos)**: notificación urgente + bloqueo automático de las consultas de reporting (redirección temporal al master con consultas de solo lectura)

El bloqueo automático era la parte más delicada: mejor devolver un error explícito al usuario ("datos temporalmente no disponibles, vuelva a intentarlo en unos minutos") que devolver datos de horas atrás sin ningún aviso.

---

## Cuatro horas se convierten en treinta segundos

El lag de cuatro horas era el síntoma visible de tres problemas superpuestos: arquitectura single-thread, consulta batch sin optimizar, almacenamiento compartido. Ninguno de los tres, por separado, habría causado cuatro horas de retraso — juntos, se amplificaban mutuamente.

La parte más interesante de esta historia no es técnica: es que el problema llevaba meses existiendo, probablemente, y nadie se había dado cuenta porque `Seconds_Behind_Master` no se monitorizaba de forma sistemática, y cuando se comprobaba manualmente daba valores que parecían razonables en las horas de baja actividad.

La monitorización del lag de réplica no es un nice-to-have. Es una métrica operativa que impacta directamente en la calidad de los datos que el negocio usa para tomar decisiones. Si las consultas de reporting corren sobre una réplica, el lag de esa réplica es parte integral de la calidad del dato — y hay que tratarlo como tal, con alertas, umbrales y un plan de respuesta.

`Seconds_Behind_Master` es un punto de partida, no una respuesta. `pt-heartbeat` o la comparación de conjuntos GTID son herramientas mucho más fiables. Y la parallel replication, en MySQL 5.7+ con `LOGICAL_CLOCK`, es hoy la configuración razonable por defecto para cualquier réplica que reciba carga sostenida.

---

## Fontes oficiales

1. MySQL 8.0 Reference Manual — [Replication Slave Status Variables: Seconds_Behind_Master](https://dev.mysql.com/doc/refman/8.0/en/show-replica-status.html)
2. Percona Toolkit Documentation — [pt-heartbeat](https://docs.percona.com/percona-toolkit/pt-heartbeat.html)
3. MySQL 8.0 Reference Manual — [GTID-Based Replication](https://dev.mysql.com/doc/refman/8.0/en/replication-gtids.html)
4. MySQL 8.0 Reference Manual — [Replication with Multithreaded Appliers](https://dev.mysql.com/doc/refman/8.0/en/replication-threads-applier.html)

---

## Glosario
- **[Binlog](/es/glossary/binlog/)** (MySQL binary log) — registro secuencial de todas las modificaciones a los datos en el master MySQL. Base de la réplica: el slave lee el binlog para saber qué aplicar. Formato ROW, STATEMENT o MIXED.

- **[Relay log](/es/glossary/gtid/)** — copia local del binlog del master, escrita por el IO thread en el slave. El SQL thread lee el relay log para aplicar las transacciones. Es el buffer entre la recepción y la aplicación de los eventos.

- **GTID** (Global Transaction Identifier) — identificador único asignado a cada transacción commiteada en un servidor MySQL. Formato `source_uuid:transaction_id`. Permite failover simplificado y monitorización precisa del lag de réplica.

- **Parallel replication** — modo de aplicación de los eventos de réplica que usa varios worker threads en lugar de un único SQL thread. En MySQL, el modo `LOGICAL_CLOCK` identifica transacciones ejecutables en paralelo basándose en los commit timestamps del binlog.

- **pt-heartbeat** — herramienta de Percona Toolkit que mide el lag de réplica MySQL escribiendo timestamps en el master y comparándolos con los valores leídos en el slave. Más fiable que `Seconds_Behind_Master` para el alerting en producción.
