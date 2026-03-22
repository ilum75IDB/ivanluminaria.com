---
title: "Execution Plan"
description: "Plan de ejecucion — la secuencia de operaciones elegida por el optimizer de la base de datos para resolver una consulta SQL."
translationKey: "glossary_execution_plan"
aka: "Plan de Ejecucion"
articles:
  - "/posts/postgresql/explain-analyze-postgresql"
  - "/posts/postgresql/pg-stat-statements"
---

Un **execution plan** (plan de ejecucion) es la secuencia de operaciones que la base de datos elige para resolver una consulta SQL. Cuando escribes un SELECT con JOINs, filtros WHERE y ordenamientos, el optimizer evalua decenas de estrategias posibles y elige una basandose en las estadisticas disponibles.

## Como funciona

El plan se representa como un arbol de nodos: cada nodo es una operacion (scan, join, sort, aggregate) que recibe datos de sus nodos hijos y los pasa al nodo padre. En PostgreSQL se visualiza con `EXPLAIN` (plan estimado) o `EXPLAIN ANALYZE` (plan real con tiempos efectivos y conteos de filas).

El optimizer decide para cada nodo que estrategia usar: sequential scan o index scan para el acceso a tablas, nested loop, hash join o merge join para las uniones, sort o hash para los agrupamientos.

## Por que es importante

La lectura correcta de un plan de ejecucion es la competencia mas importante para el tuning de consultas. No basta mirar el tiempo total: hay que comparar las filas estimadas con las reales nodo por nodo, verificar los buffers de I/O e identificar donde el optimizer tomo decisiones incorrectas.

Una estimacion erronea en un solo nodo puede propagarse en cascada por todo el plan, transformando una consulta de milisegundos en una de minutos.

## Que puede salir mal

Los problemas mas frecuentes en los planes de ejecucion:

- **Estimaciones de cardinalidad erroneas**: el optimizer piensa que una tabla devuelve 100 filas y llegan 2 millones
- **Join equivocado**: un nested loop elegido donde hacia falta un hash join, por estadisticas obsoletas
- **Indice ignorado**: un sequential scan sobre una tabla grande porque las estadisticas no reflejan la distribucion real de los datos
- **Spill a disco**: operaciones de sort o hash que no caben en `work_mem` y terminan escribiendo en disco
