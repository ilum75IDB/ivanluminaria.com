---
title: "Switchover"
description: "Operacion planificada de Data Guard que invierte los roles entre primary y standby sin perdida de datos, reversible y controlada."
translationKey: "glossary_switchover"
articles:
  - "/posts/oracle/oracle-cloud-migration"
---

El **switchover** es una operacion planificada de Oracle Data Guard que invierte los roles entre la base de datos primary y la standby. El primary se convierte en standby, el standby se convierte en primary. Ningun dato se pierde, ninguna transaccion falla — es un cambio limpio y controlado.

## Switchover vs Failover

La distincion es fundamental:

| | Switchover | Failover |
|---|---|---|
| **Cuando** | Planificado (mantenimiento, migracion) | Emergencia (fallo del primary) |
| **Perdida de datos** | Cero | Posible (depende del modo) |
| **Reversibilidad** | Si, con otro switchover | No, el standby se convierte en primary permanentemente |
| **Tiempo** | Minutos (tipicamente 1-3) | Segundos a minutos |

## Como se ejecuta

Con Data Guard Broker, el switchover es un unico comando:

    DGMGRL> SWITCHOVER TO standby_db;

El broker gestiona automaticamente la secuencia: detencion del redo transport, aplicacion de los ultimos redo en el standby, inversion de roles, reinicio del redo transport en la direccion opuesta.

## Uso en migraciones

El switchover es la estrategia preferida para las migraciones Oracle cross-site. Se configura el Data Guard entre el entorno origen y destino, se deja sincronizar, y en el momento del cutover se ejecuta el switchover. Si algo sale mal en la nueva infraestructura, un segundo switchover devuelve todo al punto de partida — una red de seguridad que Data Pump no puede ofrecer.
