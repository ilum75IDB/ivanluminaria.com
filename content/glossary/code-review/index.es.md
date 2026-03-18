---
title: "Code Review"
description: "Práctica de revisión del código por parte de un colega antes del merge, para capturar bugs, mejorar la calidad y compartir conocimiento en el equipo."
translationKey: "glossary_code-review"
articles:
  - "/posts/project-management/ai-github-project-management"
---

La **Code Review** es la práctica por la cual un colega examina el código escrito por otro desarrollador antes de que se incorpore al branch principal. En GitHub ocurre dentro de las Pull Requests.

## Cómo funciona

El desarrollador abre una Pull Request con sus cambios. Un reviewer asignado examina el diff del código, deja comentarios, sugiere mejoras y finalmente aprueba o solicita cambios. El proceso es asíncrono: no hacen falta reuniones, la revisión ocurre en la herramienta. Solo después de la aprobación el código se fusiona en el branch principal.

## Para qué sirve

La code review captura bugs que los tests automáticos no encuentran, mejora la calidad del código, y — aspecto frecuentemente subestimado — difunde el conocimiento del codebase en el equipo. Si solo una persona conoce un módulo y se va, el proyecto tiene un problema. Con las code reviews, al menos dos personas conocen cada pieza de código.

## Cuándo se usa

En cada Pull Request, sin excepciones. No es una formalidad: es una inversión en calidad. El tiempo gastado en review es siempre menor que el tiempo que se gastaría corrigiendo bugs en producción descubiertos demasiado tarde.
