---
title: "Branch"
description: "Rama de desarrollo independiente en un sistema de control de versiones. Permite trabajar en cambios aislados sin afectar el código principal hasta el merge."
translationKey: "glossary_branch"
articles:
  - "/posts/project-management/ai-github-project-management"
---

Un **Branch** (rama) es una línea de desarrollo independiente en un repositorio Git. Cada branch contiene una copia del código sobre la que se puede trabajar sin afectar el branch principal (main) o el trabajo de otros desarrolladores.

## Cómo funciona

Cuando un desarrollador crea un branch (ej. `fix/issue-234-error-calculo`), Git crea un puntero a la versión actual del código. Desde ese momento, los cambios hechos en el branch quedan aislados. Al terminar el trabajo, los cambios se proponen al equipo mediante Pull Request y, tras la aprobación, se unen (merge) al branch principal.

## Para qué sirve

Los branches eliminan el problema de las sobreescrituras accidentales y los conflictos no gestionados. Cada desarrollador trabaja en su propia área aislada: no sobrescribe el trabajo de los demás ni rompe el código funcional. El branch principal se mantiene siempre en un estado "bueno" porque solo recibe código aprobado.

## Cuándo se usa

Se crea un branch para cada tarea, corrección de bug o funcionalidad. La convención de naming ayuda a identificar el propósito: `fix/` para bugs, `feature/` para nuevas funcionalidades, `hotfix/` para correcciones urgentes. El branch se elimina después del merge para mantener el repositorio limpio.
