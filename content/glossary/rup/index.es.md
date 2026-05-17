---
title: "RUP"
description: "Rational Unified Process. Método de desarrollo software iterativo liberado por Rational en 1998, organizado en cuatro fases (Inception, Elaboration, Construction, Transition)."
translationKey: "glossary_rup"
aka: "Rational Unified Process"
articles:
  - "/posts/project-management/da-rivali-a-co-autori-uml-rup"
---

**RUP — Rational Unified Process** es un método de desarrollo software iterativo, liberado como producto comercial por Rational Software en 1998. Basado en las contribuciones previas de los **Three Amigos** (en particular de Booch y Jacobson), es el **proceso enterprise heavyweight** que acompañó la adopción de UML en los años '90 y 2000.

## Cómo funciona

RUP organiza un proyecto en **cuatro fases secuenciales**, cada una compuesta por una o más iteraciones internas:

- **Inception** — visión, business case, scope general
- **Elaboration** — arquitectura, requisitos detallados, mitigación de los riesgos técnicos
- **Construction** — implementación iterativa del software
- **Transition** — deploy en producción, beta, rollout, formación

A diferencia del *waterfall* clásico, RUP es iterativo (se vuelve atrás entre las fases varias veces). A diferencia de Scrum, es *document-intensive* — una Elaboration típica enterprise dura meses, con artefactos rastreados y milestone documentadas.

## Cuándo tiene sentido hoy

El espacio de RUP en los nuevos proyectos ha sido erosionado por el Agile a partir de 2001. Pero sobrevive vivo y coleando en los **sectores donde el rigor documental es obligatorio por ley o por auditoría**: aviación (DO-178C), médico (IEC 62304), banca crítica, R&D farmacéutico. En estos contextos un método ágil puro no pasa la auditoría, y RUP — o un descendiente suyo — es todavía el estándar.

## Qué cambia respecto a Agile

Agile pone en el centro a las personas y las iteraciones breves; RUP pone en el centro los procesos y los artefactos trazables. No son superiores el uno al otro — son adecuados a contextos diferentes. Muchas ideas de Agile (user story, sprint, "Three Amigos meeting" en BDD) tienen origen conceptual en el mundo UML/RUP — solo despojadas del peso del proceso.
