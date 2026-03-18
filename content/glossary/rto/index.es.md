---
title: "RTO"
description: "Recovery Time Objective — el tiempo maximo aceptable para restaurar un servicio despues de un fallo o desastre."
translationKey: "glossary_rto"
aka: "Recovery Time Objective"
articles:
  - "/posts/oracle/oracle-data-guard"
---

**RTO** (Recovery Time Objective) es el tiempo maximo aceptable para restaurar el servicio despues de un fallo o desastre. Se mide desde el momento del fallo hasta el momento en que el sistema vuelve a estar operativo.

## Como se determina

El RTO depende de la estrategia de recuperacion y la infraestructura disponible:

| Estrategia | RTO tipico |
|-----------|-----------|
| Restore desde backup en cinta | 4-12 horas |
| Restore desde backup en disco | 1-4 horas |
| Data Guard con switchover manual | 1-5 minutos |
| Data Guard con Fast-Start Failover | 10-30 segundos |

## RTO vs RPO

- **RTO**: cuanto tiempo se necesita para reiniciar (mira hacia adelante)
- **RPO**: cuantos datos puedes perder (mira hacia atras)

Son metricas independientes. Un restore desde backup puede tener RTO=2 horas y RPO=24 horas. Un Data Guard sincrono puede tener RTO=30 segundos y RPO=0.

## El impacto en el negocio

El RTO tiene un impacto directo y medible: cada minuto de parada se traduce en operaciones bloqueadas, clientes no atendidos, ingresos perdidos. La diferencia entre RTO=6 horas y RTO=42 segundos — como en el caso del paso de single instance a Data Guard — puede valer mas que el coste de toda la infraestructura.
