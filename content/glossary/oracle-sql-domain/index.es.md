---
title: "SQL Domain"
description: "Constructo introducido en Oracle Database 23ai que define un dominio reutilizable (tipo base + CHECK + DEFAULT + annotations) como objeto del diccionario de datos."
translationKey: "glossary_oracle_sql_domain"
aka: "SQL Domain (Oracle 23ai)"
articles:
  - "/posts/oracle/enum-oracle-workaround-fino-a-23ai"
---

El **SQL Domain** es un constructo introducido en Oracle Database 23ai que permite definir un **dominio reutilizable** para una columna: un tipo base (ej. `VARCHAR2(20)`), un vínculo `CHECK`, un valor de `DEFAULT`, y eventuales **annotations** de metadatos, todo encapsulado en un objeto del diccionario de datos que puede ser reutilizado en muchas columnas diferentes.

## Cómo funciona

Se declara con `CREATE DOMAIN nombre AS tipo_base ... CONSTRAINT chk_X CHECK (...) DEFAULT ... ANNOTATIONS (...)`. Una vez creado, el dominio es visible en `DBA_DOMAINS` y puede usarse como tipo de columna en cualquier `CREATE TABLE`. Oracle valida los `CHECK` del dominio en cada INSERT/UPDATE como lo haría con un constraint inline.

## Para qué sirve

Centralizar en un único punto el dominio de una columna, evitando replicar la misma lista de valores (o el mismo vínculo) en docenas de tablas. Cuando el conjunto evoluciona, basta un `ALTER DOMAIN` y Oracle propaga el cambio a todas las columnas que usan el dominio — sin tener que tocar las `CREATE TABLE` ni ejecutar múltiples `ALTER TABLE`.

## Qué lo distingue del DOMAIN de PostgreSQL

El `DOMAIN` de PostgreSQL existe desde mucho antes pero es más esencial: tipo base + vínculos, sin sistema de annotations. Oracle añadió un nivel de metadatos (`display`, `description`, ordering etc.) que herramientas de BI, reporting y UI generation pueden leer para generar automáticamente etiquetas, ordering visual, descripciones de campo.
