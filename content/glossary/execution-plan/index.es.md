---
title: "Execution Plan (Plan de Ejecución)"
description: "Qué es un plan de ejecución y cómo el optimizer de la base de datos decide la estrategia para ejecutar una consulta."
translationKey: "glossary_execution_plan"
tags: ["glosario"]
---

El plan de ejecución es la secuencia de operaciones que la base de datos elige para resolver una consulta SQL. Cuando escribes un SELECT con JOINs, filtros WHERE y ordenamientos, el optimizer evalúa decenas de estrategias posibles — qué índice usar, qué tipo de join, en qué orden leer las tablas — y elige una basándose en las estadísticas disponibles.

En PostgreSQL se visualiza con `EXPLAIN` (solo el plan estimado) o `EXPLAIN ANALYZE` (plan real con tiempos efectivos). El plan se representa como un árbol de nodos: cada nodo es una operación (scan, join, sort, aggregate) que recibe datos de sus nodos hijos y los pasa al nodo padre.

La lectura correcta de un plan de ejecución es la competencia más importante para el tuning de consultas. No basta mirar el tiempo total: hay que comparar las filas estimadas con las reales nodo por nodo, verificar los buffers de I/O e identificar dónde el optimizer tomó decisiones incorrectas.

## Artículos relacionados

- [EXPLAIN ANALYZE no basta: cómo leer realmente un plan de ejecución en PostgreSQL](/es/posts/postgresql/explain-analyze-postgresql/)
