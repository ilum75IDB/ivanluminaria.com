---
title: "Transient Ischemic Attack"
description: "Un TIA (Transient Ischemic Attack) es un fallo breve y aparentemente autoresuelto que señala un problema estructural subyacente en el sistema."
translationKey: "glossary_transient_ischemic_attack"
aka: "TIA, mini-ictus (metáfora de sistemas)"
articles:
  - "/posts/project-management/il-restart-ha-risolto-il-problema-e-ancora-li"
---

En medicina, un Transient Ischemic Attack (TIA) es un episodio neurológico transitorio que se resuelve espontáneamente en menos de 24 horas sin dejar daño permanente detectable. En gestión de proyectos IT y operaciones de sistemas, el término se usa como metáfora para describir fallos breves y aparentemente autoresueltos que en realidad revelan un problema estructural no resuelto.

## El mecanismo de la metáfora

Al igual que un TIA clínico suele preceder a un ictus completo, un "TIA de sistema" — un crash resuelto con un reinicio, un timeout que desapareció solo, un pico de latencia que se calmó sin intervención — es una señal de alerta, no una resolución. El sistema se recuperó, pero la causa raíz sigue presente. Cerrar el episodio porque "se resolvió solo" es exactamente el razonamiento que convierte una advertencia en una emergencia mayor.

## Contexto operativo

En proyectos IT, los TIA se manifiestan como:

- reinicios nocturnos de aplicaciones que "arreglan todo" sin que nadie sepa por qué
- consultas lentas que vuelven a la normalidad tras reiniciar el connection pool
- errores intermitentes en colas de mensajes que desaparecen antes de que alguien abra un ticket

La respuesta correcta no es celebrar la recuperación, sino abrir un análisis post-mortem incluso cuando el sistema ha vuelto a operar con normalidad. Un TIA no diagnosticado es deuda técnica con fecha de vencimiento desconocida.

## Notas

El término es deliberadamente provocador: usarlo en una retrospectiva o en un informe de incidente ayuda al equipo a desplazar el foco del "ya está arriba" al "por qué cayó".
