---
title: "Lift-and-Shift"
description: "Estrategia de migración cloud que traslada sistemas sin modificar su arquitectura ni su código, aplazando cualquier optimización a la fase post-migración."
translationKey: "glossary_lift_and_shift"
aka: "Migración rehost"
articles:
  - "/posts/oracle/latenza-wan-e-change-control-gxp-il-costo-reale-del-lift-and-shift"
---

El lift-and-shift es un enfoque de migración cloud que replica el entorno origen — servidores, bases de datos, aplicaciones — en la plataforma destino sin alterar la arquitectura, la configuración ni el código. El objetivo principal es reducir el perímetro de validación y comprimir los plazos de puesta en producción, aceptando deliberadamente que el sistema migrado no estará optimizado para su nuevo contexto.

## Cómo funciona

El sistema origen se reproduce 1:1 en la plataforma destino: las VMs se convierten o recrean con las mismas especificaciones, las bases de datos se migran mediante backup/restore o herramientas de replicación sin refactorización del esquema, y las dependencias de red se reconstruyen fielmente. En entornos regulados (GxP, SOX, PCI-DSS), este enfoque acota el delta de validación porque el comportamiento de la aplicación permanece nominalmente inalterado.

## Cuándo se utiliza

El lift-and-shift es la opción predominante cuando:

- los plazos de migración están condicionados por vencimientos contractuales o de licencias
- el sistema es legacy y no se dispone de experiencia interna para un refactoring seguro
- el alcance de la validación IQ/OQ/PQ debe mantenerse reducido por razones de presupuesto o calendario

La limitación principal es estructural: los costes operativos cloud (compute, almacenamiento, red) se mantienen elevados porque el sistema no aprovecha la elasticidad, los managed services ni las arquitecturas cloud-native. La latencia WAN y las restricciones de change control en entornos GxP pueden amplificar estos costes de forma significativa, tal como se analiza en el artículo vinculado.
