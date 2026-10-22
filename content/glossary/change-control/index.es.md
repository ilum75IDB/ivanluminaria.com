---
title: "Change Control"
description: "Proceso formal GxP para gestionar cambios en hardware, software y procedimientos: evaluación de riesgos, protocolo de pruebas, documentación y firmas autorizadas."
translationKey: "glossary_change_control"
aka: "Proceso de Gestión de Cambios"
articles:
  - "/posts/oracle/latenza-wan-e-change-control-gxp-il-costo-reale-del-lift-and-shift"
---

El change control es el proceso formal obligatorio en sistemas validados GxP (Good Practice) que regula cualquier modificación a infraestructura, software o procedimientos operativos. En entornos regulados del sector farmacéutico, médico o biotecnológico, implementar un cambio sin un registro de change control aprobado constituye una desviación documentable con consecuencias regulatorias directas.

## Cómo funciona

El ciclo típico comprende cuatro fases secuenciales:

1. **Solicitud de cambio** — descripción técnica de la modificación propuesta, justificación y sistemas afectados.
2. **Evaluación de riesgos** — análisis del impacto sobre el estado de validación existente (IQ/OQ/PQ), integridad de datos y continuidad operativa.
3. **Protocolo de pruebas** — definición de las pruebas a ejecutar antes del go-live, con criterios de aceptación explícitos.
4. **Aprobación e implementación** — firmas autorizadas de los roles designados (QA, IT, business owner) y documentación post-implementación.

Cada fase genera artefactos trazables que deben conservarse en el sistema de gestión documental para auditorías internas e inspecciones regulatorias.

## Contexto operativo

El change control se convierte en un cuello de botella crítico en proyectos de migración cloud (lift-and-shift), ya que cada componente migrado — base de datos, middleware, sistema operativo — puede requerir una solicitud de cambio independiente. En entornos Oracle sobre sistemas GxP, incluso una actualización de parche menor puede desencadenar un ciclo completo de re-validación si afecta funcionalidades ya cualificadas. El tiempo medio de aprobación en organizaciones medianas oscila entre 2 y 8 semanas para cambios de riesgo medio, un factor que los planes de migración suelen subestimar de forma sistemática.
