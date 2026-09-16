---
title: "?SYNTAX ERROR"
description: "Mensaje de error del Commodore 64 que indica una violación de las reglas sintácticas del BASIC, señalando la línea detectada por el intérprete."
translationKey: "glossary_syntax_error"
aka: "Syntax Error (Commodore BASIC)"
articles:
  - "/posts/project-management/il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire"
---

`?SYNTAX ERROR` es el mensaje que emite el intérprete BASIC del Commodore 64 cuando una línea de código viola las reglas gramaticales del lenguaje. El signo de interrogación inicial forma parte del formato estándar de errores del sistema Commodore (KERNAL + BASIC V2), no es un añadido editorial.

## Cómo funciona

El intérprete BASIC del C64 analiza el código línea por línea, tanto en tiempo de ejecución como al introducir instrucciones en modo directo. Cuando encuentra un token irreconocible — una palabra clave mal escrita, un paréntesis sin cerrar, un operador fuera de lugar — se detiene e imprime el mensaje seguido del número de línea:

```
?SYNTAX ERROR IN 100
READY.
```

El número de línea indicado es donde el intérprete *detectó* el problema, no necesariamente donde se *originó*. Una expresión incompleta en la línea 90 puede manifestarse como error en la línea 100, donde el intérprete intenta consumir tokens que ya no están disponibles.

## Contexto operativo

Al depurar programas BASIC en el C64, `?SYNTAX ERROR` suele ser un punto de partida engañoso: la línea reportada debe leerse junto con las líneas anteriores, especialmente con construcciones multi-token como `IF...THEN`, `FOR...NEXT` o cadenas de comandos separados por `:`. La ausencia de un depurador simbólico hace que el proceso sea completamente manual. Este comportamiento — el error reportado en un lugar distinto a su causa raíz — es un patrón que reaparece en muchos sistemas de análisis secuencial, desde compiladores hasta motores SQL, y enseña a no confiar ciegamente en el número de línea reportado.
