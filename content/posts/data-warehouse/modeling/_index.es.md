---
title: "Dimensional Modeling"
date: "2026-03-10T10:00:00+01:00"
description: "Modelado dimensional en la práctica: jerarquías, dimensiones, tablas de hechos y las decisiones de diseño que marcan la diferencia entre un DWH que responde y uno que no puede."
layout: "list"
---
El modelado dimensional parece simple.<br>
Hechos y dimensiones. Star schema. Snowflake. Conceptos que se aprenden en una tarde.<br>

Luego llegas a producción y descubres que el diablo está en los detalles. Una jerarquía desbalanceada que rompe todas las agregaciones. Una slowly changing dimension mal gestionada que reescribe la historia. Una granularidad equivocada en la tabla de hechos que hace imposible un reporte que el negocio considera trivial.<br>

En esta sección comparto los problemas reales del modelado dimensional — los que los libros tratan en media página y que en producción te cuestan semanas.
