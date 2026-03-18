---
title: "Pull Request"
description: "Mecanismo de propuesta y revisión de cambios en el código en plataformas como GitHub. Permite code review, discusión y aprobación antes del merge en el branch principal."
translationKey: "glossary_pull-request"
aka: "PR, Merge Request"
articles:
  - "/posts/project-management/ai-github-project-management"
---

Una **Pull Request** (PR) es una solicitud formal de incorporar los cambios de un branch de desarrollo al branch principal del repositorio. Es el mecanismo central de colaboración en GitHub y plataformas similares.

## Cómo funciona

El desarrollador trabaja en un branch dedicado (ej. `fix/issue-234-error-calculo`), completa los cambios, y abre una PR. La PR muestra el diff del código, permite a los colegas comentar línea por línea, solicitar cambios o aprobar. Solo después de la aprobación el código se une (merge) al branch principal. Esto garantiza que el código "bueno" siga siendo bueno.

## Para qué sirve

La PR transforma el desarrollo de una actividad individual a un proceso de equipo. Previene sobreescrituras accidentales, captura bugs antes de que lleguen a producción, y crea un historial completo de quién hizo qué, cuándo y por qué. En proyectos caóticos, es la diferencia entre control y desorden.

## Cuándo se usa

En cada cambio de código, sin excepciones. Incluso las correcciones pequeñas pasan por una PR, porque el valor no está solo en la revisión sino en la trazabilidad. En plataformas GitLab la misma funcionalidad se llama Merge Request.
