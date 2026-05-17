---
title: "Use Case"
description: "Técnica de análisis de requisitos introducida por Ivar Jacobson que describe el sistema desde el punto de vista del actor que lo usa, no de los objetos que lo componen."
translationKey: "glossary_use_case"
aka: "Use Case (Jacobson)"
articles:
  - "/posts/project-management/da-rivali-a-co-autori-uml-rup"
---

El **use case** es una técnica de análisis de requisitos introducida por **Ivar Jacobson** a finales de los años '80 en su método *Objectory*, y posteriormente incorporada a UML como uno de los nueve diagramas estándar de 1997. Describe el sistema **desde el punto de vista del actor que lo usa** (usuario, sistema externo, scheduler), no de los objetos software que lo componen.

## Cómo funciona

Un use case se compone de:

- un **actor** (quien inicia la interacción)
- un **objetivo** (qué quiere lograr el actor)
- un **escenario principal** (la secuencia de pasos típica)
- eventuales **escenarios alternativos** (qué sucede en caso de error o variante)

Ejemplo clásico: *"Como cliente registrado quiero cancelar un pedido, porque he cambiado de opinión sobre la compra."* El actor es el cliente registrado, el objetivo es cancelar un pedido, los escenarios describen los pasos (login, búsqueda pedido, confirmación) y las excepciones (pedido ya enviado, sesión expirada).

## Por qué cambió el análisis de requisitos

Antes del use case, el análisis tendía a describir el sistema en términos de **funciones** (qué hace) o de **datos** (qué contiene). Jacobson propuso en cambio partir del **comportamiento observable para quien usa el sistema** — un cambio de perspectiva simple pero revolucionario, porque puso en conversación a developer y business en un lenguaje común.

## La herencia en las metodologías Agile

La **user story** del Agile es un use case despojado del formalismo académico. La sintaxis *"como [actor] quiero [hacer X] para [lograr Y]"* (Mike Cohn) es el destilado conversacional del use case de Jacobson. Misma arquitectura narrativa, mismo rol de puente entre business y técnico — solo más breve y menos estructurada.
