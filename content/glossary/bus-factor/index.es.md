---
title: "Bus Factor"
description: "Número de personas del equipo que, si faltaran a la vez, bloquearían el proyecto. Mide la concentración de conocimiento crítico en pocas cabezas."
translationKey: "glossary_bus_factor"
aka: "Truck Factor, Lottery Factor"
articles:
  - "/posts/project-management/team-di-progetto-che-reggono"
---

**Bus Factor** (también conocido como Truck Factor o Lottery Factor) es una métrica empírica que responde a la pregunta: *"¿Cuántas personas del equipo tienen que faltar a la vez para que el proyecto se pare?"*. El nombre, un poco macabro, proviene del escenario hipotético del compañero atropellado por un autobús — pero vale igualmente para vacaciones prolongadas, enfermedades, dimisiones, traslados.

## Cómo se calcula

No existe una fórmula matemática exacta, sino una estimación razonada que parte de algunas preguntas:

- ¿Quién es la única persona que sabe configurar el cluster de producción?
- ¿Quién es la única persona que conoce el dominio funcional de cierta área?
- ¿Quién escribió el trozo de código más crítico sin documentarlo?
- ¿Quién mantiene la relación con un stakeholder clave del cliente?

Si la respuesta a cada pregunta es "una sola persona", el bus factor es 1 sobre esa competencia. El bus factor del equipo es el mínimo entre todos los bus factor de las competencias críticas individuales.

## Valores típicos

- **Bus factor = 1**: riesgo crítico. Una sola persona tiene conocimiento que bloquearía el proyecto. Frecuente en equipos pequeños o en actividades "de gurú".
- **Bus factor = 2**: frágil. Cubierto si falta una persona, pero si faltan ambas el proyecto se para.
- **Bus factor ≥ 3**: resistente. El conocimiento está distribuido lo suficiente para absorber ausencias múltiples.

El objetivo pragmático en los proyectos reales es mantener el bus factor ≥ 3 en las competencias realmente críticas, aceptando valores inferiores en áreas más periféricas.

## Cómo se sube el bus factor

Cuatro herramientas, todas de bajo coste pero que requieren tiempo de calendario:

- **Documentación mínima**: no enciclopedias, sino runbooks operativos de 2-5 páginas sobre los procedimientos críticos
- **Pair working**: dos personas en la misma actividad, alternando entre "manos en el teclado" y "observa y pregunta"
- **Rotación**: quien siempre ha hecho X este mes pasa a Y, y viceversa. Aunque sea solo una semana
- **Knowledge transfer recurrente**: 30 minutos en agenda cada semana sobre un tema específico, grabados

## Señales de que el bus factor es bajo

- Cuando una persona se va de vacaciones, el equipo se ralentiza visiblemente
- Algunas actividades se asignan sistemáticamente siempre a la misma persona
- Un procedimiento crítico nunca se ha documentado
- El lead es el único que conoce el "por qué" de ciertas elecciones arquitectónicas
