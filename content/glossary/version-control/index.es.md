---
title: "Version Control"
description: "Sistema que rastrea cada cambio en el código fuente, permitiendo visualizar el historial, revertir cambios y colaborar sin sobreescrituras. Git es el estándar actual."
translationKey: "glossary_version-control"
aka: "Control de versiones, VCS"
articles:
  - "/posts/project-management/ai-github-project-management"
---

El **Version Control** (control de versiones) es un sistema que registra cada cambio en los archivos de un proyecto, manteniendo un historial completo de quién cambió qué, cuándo y por qué. Git es el sistema de control de versiones más usado en el mundo.

## Cómo funciona

Cada cambio se registra como "commit" con un mensaje descriptivo, un autor y un timestamp. El sistema mantiene toda la historia del proyecto: es posible volver a cualquier versión anterior, comparar versiones diferentes y entender la evolución del código en el tiempo. Con Git, cada desarrollador tiene una copia completa de la historia en su propio ordenador.

## Para qué sirve

Sin control de versiones, el código vive en carpetas compartidas donde las sobreescrituras accidentales son la norma y nadie sabe cuál es la versión "buena". Con control de versiones, cada cambio es rastreado y reversible, los conflictos entre desarrolladores se gestionan de forma estructurada, y la historia del proyecto es un recurso, no un misterio.

## Cuándo se usa

Siempre, en cualquier proyecto software con más de un archivo o más de un desarrollador. La ausencia de control de versiones es la primera señal de un proyecto fuera de control. GitHub, GitLab y Bitbucket son plataformas que añaden colaboración (Pull Requests, Issue tracker) sobre Git.
