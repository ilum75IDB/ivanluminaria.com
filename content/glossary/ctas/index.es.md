---
title: "CTAS"
description: "Create Table As Select — técnica Oracle para crear una nueva tabla poblándola con resultados de una query, usada para migraciones y reestructuraciones de tablas de gran tamaño."
translationKey: "glossary_ctas"
aka: "Create Table As Select"
articles:
  - "/posts/oracle/oracle-partitioning"
---

**CTAS** (Create Table As Select) es un comando SQL Oracle que crea una nueva tabla y la puebla en una única operación con los resultados de un SELECT. Es la técnica estándar para migrar datos de una estructura a otra en tablas de gran tamaño.

## Cómo funciona

El comando combina DDL y DML: crea la tabla con la estructura derivada del SELECT e inserta los datos en un solo paso. Con el hint `PARALLEL` y el modo `NOLOGGING`, la copia de cientos de GB puede completarse en pocas horas. Después de la copia, se renombra la tabla original, se renombra la nueva, y el downtime se limita a los pocos segundos del rename.

## Para qué sirve

CTAS es fundamental cuando se necesita reestructurar una tabla sin poder usar `ALTER TABLE` directamente — por ejemplo, añadir partitioning a una tabla existente con miles de millones de filas. Permite trabajar en la nueva estructura mientras el sistema está activo en la antigua.

## Cuándo se usa

Se usa para migraciones a tablas particionadas, reorganización de datos fragmentados, y creación de copias de tablas con estructuras diferentes. En producción, debe combinarse siempre con `NOLOGGING` (para reducir los redo logs) y seguirse de un backup RMAN inmediato.
