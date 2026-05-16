---
title: "Lookup table"
description: "Tabla de referencia conectada vía foreign key que almacena los valores válidos de una enumeración, junto con eventuales atributos descriptivos."
translationKey: "glossary_lookup_table"
aka: "Tabla de lookup, tabla de referencia"
articles:
  - "/posts/mysql/enum-mysql-semplifica-o-complica"
  - "/posts/postgresql/enum-postgresql-paga-o-pesa"
  - "/posts/oracle/enum-oracle-workaround-fino-a-23ai"
---

La **lookup table** es una tabla de referencia que almacena los valores válidos de un dominio enumerado, conectada a las tablas que la usan mediante una foreign key. Es la vía "puramente base de datos" para modelar una enumeración, alternativa a tipos nativos como ENUM o a CHECK constraint.

## Cómo está hecha

El schema canónico incluye al menos tres columnas: un `id` sustituto (típicamente `SMALLINT` o `TINYINT`) como primary key, un `codigo` textual (la clave natural, normalmente única), y una `descripcion` extendida. A menudo se añaden atributos como `orden` para el sort visual, `activo` para el soft-delete, y timestamps de audit.

## Para qué sirve

La ventaja principal respecto a ENUM es la flexibilidad: renombrar una descripción es un `UPDATE` en una fila, sin migración ni rebuild de la tabla que la referencia. Se pueden añadir atributos (etiquetas localizadas, orden, flags) sin tocar el schema de las tablas hijas. Es adecuada cuando los valores cambian en el tiempo o cuando hacen falta metadatos asociados.

## Cuándo se usa

Es la elección correcta cuando:
- Los valores se modifican con cierta frecuencia (añadir, renombrar, desactivar)
- Hacen falta atributos adicionales (traducciones, orden, flags)
- Se quieren gestionar los valores en runtime sin DDL (paneles admin)
- El número de valores crece con el tiempo, más allá de 20-30

El precio a pagar es el JOIN necesario en las queries, que sin embargo se optimiza fácilmente con índices compuestos y vistas dedicadas.
