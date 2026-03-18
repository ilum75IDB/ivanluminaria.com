---
title: "Local Index"
description: "Índice Oracle particionado con la misma clave que la tabla, donde cada partición de la tabla tiene su partición de índice correspondiente. Más mantenible que un índice global."
translationKey: "glossary_local-index"
articles:
  - "/posts/oracle/oracle-partitioning"
---

Un **Local Index** es un índice Oracle creado sobre una tabla particionada, que se particiona automáticamente con la misma clave y los mismos límites que la tabla. Cada partición de la tabla tiene una partición de índice correspondiente.

## Cómo funciona

Cuando se crea un índice con la cláusula `LOCAL`, Oracle crea una partición de índice por cada partición de la tabla. Si la tabla tiene 100 particiones mensuales, el índice tendrá 100 particiones correspondientes. Las operaciones DDL sobre una partición (DROP, TRUNCATE, SPLIT) invalidan solo la partición de índice correspondiente, no el índice entero.

## Para qué sirve

El Local Index es la opción preferida para índices en tablas particionadas porque mantiene la independencia de las particiones. Un `DROP PARTITION` tarda menos de un segundo y no invalida ningún otro índice. Con un índice global, la misma operación invalidaría el índice entero, requiriendo horas de rebuild.

## Cuándo se usa

Se usa cuando el índice incluye la clave de partición o cuando las queries siempre filtran por la columna de partición. Para lookups puntuales en columnas que no son la partición (ej. clave primaria), se necesita un índice global. La regla: local donde sea posible, global solo donde sea necesario.
