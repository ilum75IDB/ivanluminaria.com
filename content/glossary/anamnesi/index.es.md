---
title: "Anamnesis"
description: "Recopilación sistemática de síntomas, eventos recientes y configuración del sistema como punto de partida para diagnosticar un problema técnico."
translationKey: "glossary_anamnesi"
aka: "Recopilación del historial del sistema"
articles:
  - "/posts/project-management/il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire"
---

En medicina, la anamnesis es la recopilación estructurada del historial clínico del paciente antes de formular cualquier diagnóstico. Aplicado a sistemas informáticos, el término describe el mismo proceso orientado a máquinas, bases de datos y aplicaciones: recopilar de forma sistemática los síntomas observados, los cambios recientes, los detalles de configuración y el contexto operativo, antes de plantear cualquier hipótesis sobre la causa raíz.

## Cómo funciona

Una anamnesis técnica sigue una serie de preguntas precisas y secuenciales:

- **¿Qué cambió recientemente?** Despliegues, actualizaciones de paquetes, modificaciones en parámetros de configuración, ventanas de mantenimiento.
- **¿Cuándo apareció el síntoma por primera vez?** Marcas de tiempo exactas, correlación con eventos programados (backups, procesos batch, picos de carga).
- **¿Quién tuvo acceso y qué hizo?** Logs de acceso, historial de comandos, tickets abiertos en las horas previas al incidente.
- **¿Cuál es la configuración actual?** Versión del software, recursos de hardware, topología de red, dependencias externas.

Solo después de reunir esta información tiene sentido formular hipótesis diagnósticas. Saltarse este paso casi siempre lleva a perseguir causas equivocadas.

## Cuándo se aplica

La anamnesis es el primer paso cada vez que un problema no es inmediatamente reproducible o su causa no es evidente: ralentizaciones repentinas, errores intermitentes, comportamientos anómalos tras una actualización. Es especialmente crítica en entornos de producción, donde el tiempo de diagnóstico tiene un coste directo, y en sistemas legacy donde la documentación es escasa y el conocimiento histórico está repartido entre varias personas.

Una anamnesis bien realizada reduce el riesgo de aplicar correcciones que resuelven el síntoma sin tocar la causa raíz.
