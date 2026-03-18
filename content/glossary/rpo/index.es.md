---
title: "RPO"
description: "Recovery Point Objective — la cantidad maxima de datos que una organizacion puede permitirse perder en caso de desastre, medida en tiempo."
translationKey: "glossary_rpo"
aka: "Recovery Point Objective"
articles:
  - "/posts/oracle/oracle-data-guard"
---

**RPO** (Recovery Point Objective) es la cantidad maxima de datos que una organizacion puede permitirse perder en caso de fallo o desastre. Se mide en tiempo: un RPO de 1 hora significa aceptar la perdida de como maximo la ultima hora de transacciones.

## Como se determina

El RPO depende de la estrategia de backup y replica:

| Estrategia | RPO tipico |
|-----------|-----------|
| Backup nocturno en cinta | 12-24 horas |
| Backup + archived logs en almacenamiento remoto | 1-4 horas |
| Data Guard asincrono (MaxPerformance) | Pocos segundos |
| Data Guard sincrono (MaxAvailability) | Cero |

## RPO vs RTO

RPO y RTO son complementarios pero distintos:

- **RPO**: cuantos datos puedes perder (mira hacia atras en el tiempo)
- **RTO**: cuanto tiempo se necesita para restaurar el servicio (mira hacia adelante en el tiempo)

Una organizacion puede tener RPO=0 (cero perdida de datos) pero RTO=4 horas (se necesitan 4 horas para reiniciar), o viceversa.

## Por que importa

El RPO determina la inversion necesaria en infraestructura de replica. Pasar de RPO=24 horas a RPO=0 puede costar ordenes de magnitud mas, pero el coste debe compararse con el valor de los datos perdidos — como en el caso de seis horas de polizas de seguros no emitidas.
