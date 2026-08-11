---
title: "Relay log"
description: "El relay log es la copia local del binlog del master en el slave MySQL: el IO thread lo escribe y el SQL thread lo lee para aplicar las transacciones."
translationKey: "glossary_relay_log"
aka: null
articles:
  - "/posts/mysql/mysql-slave-lag-diagnosi-e-fix-con-parallel-replication"
---

El relay log es el archivo binario que el slave de MySQL mantiene localmente como copia de los eventos recibidos desde el master. Actúa como buffer entre la recepción de los eventos de replicación y su aplicación efectiva en la base de datos: dos threads independientes se encargan de cada fase, y el relay log es el punto de transferencia entre ambos.

## Cómo funciona

La replicación MySQL en el slave se apoya en dos threads separados:

- **IO thread**: se conecta al master, lee el binlog y escribe los eventos en el relay log local.
- **SQL thread**: lee el relay log y aplica los eventos (INSERT, UPDATE, DELETE, DDL) en la base de datos slave.

Este desacoplamiento permite al slave seguir recibiendo eventos aunque el SQL thread esté retrasado. Los archivos del relay log siguen una convención de nombres del tipo `hostname-relay-bin.000001` y se rotan automáticamente.

```sql
-- Verificar el estado del relay log en el slave
SHOW SLAVE STATUS\G
-- Campos relevantes:
-- Relay_Log_File: archivo actual leído por el SQL thread
-- Relay_Log_Pos: posición actual
-- Relay_Master_Log_File: archivo del binlog del master correspondiente
-- Exec_Master_Log_Pos: posición aplicada en el master
```

## Contexto operativo

El relay log es clave para diagnosticar el lag de replicación. Cuando `Seconds_Behind_Master` crece, el relay log acumula eventos pendientes de aplicar: el IO thread va por delante del SQL thread. Monitorizar el tamaño de los archivos del relay log y la diferencia entre `Read_Master_Log_Pos` y `Exec_Master_Log_Pos` permite identificar dónde está el cuello de botella.

Tras un crash del slave, MySQL utiliza el archivo `relay-log.info` para reanudar desde la última posición aplicada. Con `relay_log_recovery = ON`, el relay log se regenera desde el master al reiniciar, reduciendo el riesgo de corrupción.
