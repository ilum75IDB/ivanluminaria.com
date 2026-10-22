---
title: "TIA (This Is Acceptable)"
description: "TIA significa 'This Is Acceptable': el umbral de tolerancia implícito con el que un equipo decide convivir con un problema conocido en lugar de resolverlo."
translationKey: "glossary_tia"
aka: "This Is Acceptable"
articles:
  - "/posts/project-management/il-restart-ha-risolto-il-problema-e-ancora-li"
---

TIA — *This Is Acceptable* — es la decisión, frecuentemente no formalizada, de aceptar un defecto, un workaround o un comportamiento anómalo como parte del funcionamiento normal de un sistema. No es una solución: es un umbral de tolerancia que el equipo, de forma consciente o no, ha dejado de cuestionar.

## Cómo funciona en la práctica

Un TIA surge cuando un problema se reporta, se analiza parcialmente y luego se archiva con una nota del tipo "por ahora está bien así". El reinicio semanal que resuelve el problema cada lunes por la mañana, la query lenta que "solo corre de noche", el log de errores que "no afecta a los usuarios": todos son TIAs no declarados. El riesgo es que con el tiempo se vuelvan invisibles — parte de la infraestructura de facto, no de la diseñada.

## Cuándo se convierte en un problema

Un TIA no documentado es deuda técnica disfrazada. Cuando el contexto cambia — nuevo volumen de datos, rotación de personal, actualización de versión — el comportamiento aceptado deja de ser aceptable, pero nadie recuerda por qué se toleró. La falta de trazabilidad convierte una decisión razonable en un punto ciego operativo. Documentar explícitamente un TIA (con fecha, contexto y condiciones de revisión) es la diferencia entre una elección consciente y una bomba de tiempo.

## Notas operativas

Si un TIA debe existir, debe quedar escrito: ticket abierto, decisión registrada, responsable asignado, fecha de revisión. Un TIA sin responsable no es una decisión: es un problema olvidado.
