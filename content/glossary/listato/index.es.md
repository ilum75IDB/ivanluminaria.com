---
title: "Listado"
description: "Código fuente completo impreso o mostrado línea a línea. En los ordenadores domésticos de los años 80 se publicaba en revistas para ser copiado manualmente."
translationKey: "glossary_listato"
aka: "listado de programa, source listing"
articles:
  - "/posts/project-management/il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire"
---

Un **listado** es la representación textual completa del código fuente de un programa, presentada línea a línea en el orden en que lo procesa el intérprete o el compilador. El término fue habitual en la informática de los años 70 y 80, cuando imprimir o publicar el código era el único mecanismo de distribución masiva disponible.

## Cómo funciona

En los ordenadores domésticos de 8 bits (Commodore 64, ZX Spectrum, MSX), el listado solía ser un programa BASIC numerado por líneas:

```basic
10 PRINT "HOLA MUNDO"
20 GOTO 10
```

Revistas como *Microhobby* o *Commodore World* publicaban listados de decenas de páginas. El lector los tecleaba manualmente, línea a línea. Un solo carácter incorrecto podía dejar el programa sin funcionar o provocar comportamientos imprevisibles, sin ninguna herramienta de diff ni control de versiones que ayudara a localizar el error.

## Contexto operativo

El listado como mecanismo de distribución de software es históricamente relevante para entender la cultura del debugging de aquella época. Los errores se buscaban comparando visualmente el texto tecleado con el impreso, línea a línea, con atención al detalle sintáctico. Esa disciplina anticipa competencias que siguen siendo fundamentales hoy: revisar scripts de migración SQL, auditar ficheros de configuración o rastrear la lógica en procedimientos almacenados.

En el uso técnico moderno el término sobrevive en funciones de exportación "Listing" de algunos IDEs y de forma informal para describir volcados completos de esquema (por ejemplo, la salida de `pg_dump` como "listado" de un esquema PostgreSQL).
