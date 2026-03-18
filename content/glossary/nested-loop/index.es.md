---
title: "Nested Loop (Join)"
description: "Cómo funciona el nested loop join y cuándo el optimizer lo elige — o lo elige por error."
translationKey: "glossary_nested_loop"
tags: ["glosario"]
---

El nested loop es la estrategia de join más simple: por cada fila de la tabla externa, la base de datos busca las filas correspondientes en la tabla interna. Funciona como un doble ciclo for anidado — de ahí el nombre.

Es la elección ideal cuando la tabla externa tiene pocas filas y la tabla interna tiene un índice en la columna de join. En este escenario, el nested loop es imbatible: pocas iteraciones, acceso directo por índice, memoria mínima. Un join sobre 100 filas externas con un índice B-tree en la tabla interna es prácticamente instantáneo.

Se convierte en un desastre cuando el optimizer lo elige en datasets grandes por error — típicamente porque las estadísticas subestiman el número de filas. Un nested loop sobre 2 millones de filas externas significa 2 millones de búsquedas en la tabla interna, y sin índice cada búsqueda es un scan completo. En estos casos, un hash join o un merge join serían órdenes de magnitud más rápidos.

## Artículos relacionados

- [EXPLAIN ANALYZE no basta: cómo leer realmente un plan de ejecución en PostgreSQL](/es/posts/postgresql/explain-analyze-postgresql/)
