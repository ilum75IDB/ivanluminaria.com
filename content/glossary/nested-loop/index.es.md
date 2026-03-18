---
title: "Nested Loop"
description: "Nested Loop Join — la estrategia de join que escanea la tabla interna por cada fila de la tabla externa, ideal para datasets pequenos con indice."
translationKey: "glossary_nested_loop"
aka: "Nested Loop Join"
articles:
  - "/posts/postgresql/explain-analyze-postgresql"
---

**Nested loop** es la estrategia de join mas simple: por cada fila de la tabla externa, la base de datos busca las filas correspondientes en la tabla interna. Funciona como un doble ciclo `for` anidado — de ahi el nombre.

## Como funciona

El optimizer elige una tabla como "externa" (outer) y una como "interna" (inner). Por cada fila de la tabla externa, ejecuta una busqueda en la tabla interna sobre la columna de join. Si la tabla interna tiene un indice en la columna de join, cada busqueda es un acceso directo via B-tree. Sin indice, cada busqueda se convierte en un sequential scan completo.

## Cuando es la eleccion correcta

El nested loop es imbatible cuando la tabla externa tiene pocas filas y la tabla interna tiene un indice en la columna de join. Un join sobre 100 filas externas con un indice B-tree en la tabla interna es practicamente instantaneo: pocas iteraciones, acceso directo, memoria minima.

Es tambien la estrategia preferida para las lookups de dimensiones en data warehouses, donde se une una fact table filtrada (pocas filas) con una dimension table indexada.

## Que puede salir mal

Se convierte en un desastre cuando el optimizer lo elige en datasets grandes por error — tipicamente porque las estadisticas subestiman el numero de filas. Un nested loop sobre 2 millones de filas externas significa 2 millones de busquedas en la tabla interna. Sin indice, cada busqueda es un scan completo.

En estos casos un hash join o un merge join serian ordenes de magnitud mas rapidos. La causa raiz es casi siempre una estimacion de cardinalidad erronea: estadisticas obsoletas o un `default_statistics_target` demasiado bajo.
