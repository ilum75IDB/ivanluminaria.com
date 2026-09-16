---
title: "BASIC"
description: "BASIC es un lenguaje de programación interpretado de los años 80, diseñado para ordenadores domésticos con líneas numeradas y sintaxis legible para usuarios no especializados."
translationKey: "glossary_basic"
aka: "Beginner's All-purpose Symbolic Instruction Code"
articles:
  - "/posts/project-management/il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire"
---

BASIC (Beginner's All-purpose Symbolic Instruction Code) es un lenguaje de programación creado en 1964 en el Dartmouth College que se convirtió en el lenguaje dominante de los ordenadores domésticos durante los años 80. En máquinas como el Commodore 64, el ZX Spectrum o el Apple II, BASIC era con frecuencia el único entorno de desarrollo disponible al arrancar el sistema.

## Cómo funciona

Los programas BASIC son secuencias de líneas numeradas, ejecutadas en orden ascendente por el intérprete. El número de línea sirve también como destino para los saltos condicionales (`GOTO`) y las llamadas a subrutinas (`GOSUB`).

```basic
10 PRINT "Introduce un número: "
20 INPUT N
30 IF N > 10 THEN GOTO 60
40 PRINT "Número pequeño"
50 GOTO 70
60 PRINT "Número grande"
70 END
```

El intérprete lee y ejecuta cada línea en tiempo de ejecución, sin una fase de compilación separada. Esto hace que el ciclo editar-ejecutar sea inmediato, pero el rendimiento es inferior al de los lenguajes compilados.

## Contexto operativo

BASIC estaba pensado para usuarios no especializados: estudiantes, aficionados y profesionales que querían automatizar cálculos sin formación formal en programación. La simplicidad de la sintaxis tenía un coste concreto — ausencia de estructuras de datos complejas, gestión manual de memoria mediante `PEEK` y `POKE`, y una dependencia del `GOTO` que dificultaba el mantenimiento de programas de más de unos pocos cientos de líneas.

En los entornos empresariales de los años 80, BASIC se utilizaba para software de gestión elemental, hojas de cálculo rudimentarias y automatización de informes en miniordenadores. Hoy sobrevive en entornos embebidos y en dialectos modernos como FreeBASIC o QB64, pero su papel histórico más relevante fue acercar a toda una generación al concepto de programación como herramienta de trabajo cotidiana.
