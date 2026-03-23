---
title: "Data Guard"
description: "Tecnologia Oracle para la replica en tiempo real de una base de datos en un servidor standby, garantizando alta disponibilidad y disaster recovery."
translationKey: "glossary_data_guard"
aka: "Oracle Active Data Guard"
articles:
  - "/posts/oracle/oracle-data-guard"
  - "/posts/oracle/oracle-cloud-migration"
---

**Data Guard** es la tecnologia Oracle que mantiene una o mas copias sincronizadas (standby) de una base de datos de produccion (primario). El standby recibe y aplica continuamente los redo logs generados por el primario, manteniendose alineado en tiempo real o casi.

## Como funciona

El primario genera redo logs con cada transaccion. Estos logs se transmiten al standby por red, donde se aplican de dos formas posibles:

- **Physical standby**: aplica los redo a nivel de bloque (replica exacta, byte a byte)
- **Logical standby**: reconstruye las instrucciones SQL desde los redo y las rejecuta

En caso de fallo del primario, el standby puede convertirse en el nuevo primario mediante **switchover** (planificado) o **failover** (de emergencia).

## Active Data Guard

La variante Active Data Guard permite abrir el standby en modo solo lectura mientras sigue aplicando los redo. Esto permite usarlo para informes, backups y consultas analiticas, aligerando la carga del primario.

## Modos de proteccion

| Modo | Comportamiento | Perdida de datos |
|------|---------------|-----------------|
| MaxPerformance | Replica asincrona, sin impacto en el rendimiento del primario | Posible (pocos segundos) |
| MaxAvailability | Replica sincrona, degrada a MaxPerformance si el standby no es alcanzable | Cero en condiciones normales |
| MaxProtection | Replica sincrona, el primario se detiene si el standby no confirma | Cero garantizado |
