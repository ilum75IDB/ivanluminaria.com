---
title: "Slot de replicación lógica"
description: "Estructura PostgreSQL persistente en el publisher que rastrea la posición de consumo de los WAL por subscriber. Protege de la pérdida de datos en caso de desconexión."
translationKey: "glossary_slot_di_replica_logica"
aka: "Logical Replication Slot"
articles:
  - "/posts/postgresql/replica-logica-in-postgresql-scenari-d-uso-configurazione-e-monitoraggio"
---

El **slot de replicación lógica** es una estructura persistente en el publisher PostgreSQL que memoriza la posición de consumo de los WAL para cada subscriber. Garantiza que no se pierda ningún cambio incluso si el subscriber se desconecta temporalmente: los segmentos WAL se retienen hasta que han sido consumidos y confirmados.

## Por qué existe

Sin un slot, PostgreSQL recicla los segmentos WAL apenas se vuelven superfluos para el crash recovery — típicamente en pocos minutos en sistemas activos. Un subscriber desconectado por una hora se encontraría con un hueco irrecuperable y la única salida sería reinicializar la subscription desde snapshot. El slot resuelve esto manteniendo los WAL disponibles.

## El riesgo del slot huérfano

Un slot que deja de consumir (subscriber crasheado, dropped sin antes eliminar el slot, migración interrumpida) **sigue reteniendo WAL indefinidamente**, llenando el disco del publisher. Es la causa número uno de outage de replicación lógica en producción.

## Monitorización esencial

La vista `pg_replication_slots` expone `active` (¿está en uso?), `restart_lsn` (desde dónde reanudaría), y calculando el delta entre `pg_current_wal_lsn()` y `restart_lsn` se obtiene el volumen de WAL retenido. En sistemas críticos es obligatorio una alarma cuando el delta supera un umbral (por ejemplo 10 GB) o cuando un slot permanece `active = false` demasiado tiempo. Desde PostgreSQL 13 también existe `max_slot_wal_keep_size` como tope de seguridad.
