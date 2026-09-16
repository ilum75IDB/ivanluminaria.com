---
title: "REM"
description: "Instrucción de BASIC que introduce un comentario en el código fuente: el intérprete ignora la línea, que sirve únicamente para documentar el programa."
translationKey: "glossary_rem"
aka: "REMark"
articles:
  - "/posts/project-management/il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire"
---

`REM` es una instrucción del lenguaje BASIC — abreviatura de **REMark** — que marca una línea como comentario dentro del código fuente. El intérprete omite completamente esa línea: no genera salida, no ejecuta cálculos ni modifica variables. Su única función es comunicar intenciones a quien lee el listado.

## Cómo funciona

Cuando el intérprete de BASIC encuentra `REM`, salta a la siguiente línea numerada y continúa la ejecución desde allí. En la mayoría de dialectos (Commodore BASIC, GW-BASIC, QBasic), el número de línea precede a la instrucción:

```basic
10 REM Programa de cálculo de IVA
20 LET TASA = 0.21
30 REM Introducir el precio neto
40 INPUT PRECIO
50 LET IVA = PRECIO * TASA
60 PRINT "IVA: "; IVA
```

Algunos dialectos admiten también el apóstrofo (`'`) como sinónimo de `REM`, con un comportamiento idéntico en tiempo de ejecución.

## Cuándo resulta relevante

`REM` era frecuentemente el único mecanismo disponible para dejar una explicación legible dentro de un programa, en una época sin IDEs, herramientas de diff ni sistemas de control de versiones. Un listado sin instrucciones `REM` podía volverse opaco incluso para su propio autor pocas semanas después de haberlo escrito.

Hoy `REM` es sobre todo una referencia histórica y cultural: representa el punto de partida de la documentación inline del código, práctica que en los lenguajes modernos ha evolucionado hacia docstrings, anotaciones y formatos de comentario estructurados.
