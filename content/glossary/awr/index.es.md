---
title: "AWR"
description: "Automatic Workload Repository — herramienta de diagnostico integrada en Oracle Database para la recopilacion y analisis de estadisticas de rendimiento."
translationKey: "glossary_awr"
aka: "Automatic Workload Repository"
articles:
  - "/posts/oracle/oracle-awr-ash"
---

**AWR** (Automatic Workload Repository) es un componente integrado en Oracle Database que recopila automaticamente estadisticas de rendimiento del sistema a intervalos regulares (por defecto cada 60 minutos) y las conserva durante un periodo configurable.

## Como funciona

AWR captura snapshots periodicos que incluyen:

- Estadisticas de sesiones y wait events
- Metricas SQL (top SQL por tiempo de ejecucion, I/O, CPU)
- Estadisticas de estructuras de memoria (SGA, PGA)
- Estadisticas I/O por datafile y tablespace

## Para que sirve

El informe AWR es la herramienta principal para diagnosticar problemas de rendimiento en Oracle. Comparando dos snapshots se pueden identificar:

- Queries que consumen demasiados recursos
- Cambios en los planes de ejecucion
- Cuellos de botella en I/O, CPU o memoria
- Regresiones de rendimiento tras despliegues aplicativos

## Cuando se usa

AWR es la primera herramienta a consultar cuando se recibe una notificacion de lentitud. Junto con **ASH** (Active Session History), permite reconstruir lo que paso en la base de datos durante un intervalo de tiempo especifico, incluso despues de que el problema se haya resuelto.
