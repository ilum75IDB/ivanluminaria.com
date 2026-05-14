---
title: "ALTER TYPE ADD VALUE"
description: "Comando PostgreSQL que añade un valor a un ENUM existente. Operación de metadata, transaccional, sin rebuild de la tabla que usa el tipo."
translationKey: "glossary_postgresql_alter_type_add_value"
aka: "Extensión de ENUM PostgreSQL"
articles:
  - "/posts/postgresql/enum-postgresql-paga-o-pesa"
---

`ALTER TYPE ... ADD VALUE` es el comando PostgreSQL que añade un nuevo valor a un tipo enumerativo ya existente. Es una de las modificaciones DDL más frecuentes sobre un ENUM, y es una **de las diferencias principales** respecto a MySQL: en PostgreSQL no requiere un rebuild de la tabla que usa el tipo.

## Cómo funciona

Sintaxis: `ALTER TYPE nombre_tipo ADD VALUE 'nuevo_valor' [BEFORE|AFTER 'otro_valor']`. Sin la cláusula posicional, el nuevo valor se añade al final de la lista. Con `BEFORE` o `AFTER`, se inserta en la posición especificada, afectando el orden usado por `ORDER BY` sobre esa columna. Disponible desde PostgreSQL 9.1; el posicionamiento `BEFORE`/`AFTER` llegó con 9.6.

## Para qué sirve

Para extender el vocabulario de un ENUM sin tener que recrear el tipo. Es una operación de **solo metadata**: PostgreSQL actualiza el catálogo `pg_enum` sin tocar las tablas que usan el tipo, incluso si contienen miles de millones de filas. Se ejecuta en milisegundos, dentro de una transacción, con posibilidad de rollback si algo sale mal en el deploy.

## Cuándo se usa

Es la modificación natural al ciclo de vida de un ENUM PostgreSQL: nuevo producto, nuevo canal, nueva política de negocio → un nuevo valor que añadir al conjunto. A diferencia de `ADD VALUE`, en PostgreSQL **no existe un `DROP VALUE` nativo**: eliminar un valor requiere recrear el tipo desde cero y migrar las columnas que lo usan. Esta asimetría es el principal límite operativo del tipo ENUM en PostgreSQL.
