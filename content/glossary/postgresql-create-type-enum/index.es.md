---
title: "CREATE TYPE AS ENUM"
description: "Statement DDL de PostgreSQL que crea un tipo enumerativo como objeto de primera clase, reutilizable en varias columnas y modificable con ALTER TYPE."
translationKey: "glossary_postgresql_create_type_enum"
aka: "Tipo ENUM de PostgreSQL"
articles:
  - "/posts/postgresql/enum-postgresql-paga-o-pesa"
---

`CREATE TYPE ... AS ENUM` es el statement DDL de PostgreSQL que declara un tipo enumerativo, es decir un dominio cerrado de valores textuales admitidos. A diferencia de MySQL, en PostgreSQL el ENUM es un **tipo de dato independiente**, no una decoración de una columna `VARCHAR`.

## Cómo está hecho

Sintaxis base: `CREATE TYPE nombre_tipo AS ENUM ('valor1','valor2',...)`. Una vez creado, el tipo puede usarse como tipo de una o más columnas (`estado estado_suscripcion`), como tipo de parámetro de funciones y procedimientos, y en declaraciones de índices parciales. Internamente PostgreSQL almacena cada valor como un OID de 4 bytes, manteniendo el orden posicional declarado en el `CREATE TYPE`.

## Para qué sirve

Para imponer, a nivel de esquema, la pertenencia de un valor a un conjunto cerrado. Es más estricto que un `CHECK` constraint porque define un **tipo** — por lo que la restricción viaja con la columna incluso a través de funciones, vistas y parámetros de procedimiento. Las consultas con `WHERE estado = 'ACTIVA'` son legibles y rápidas, sin necesidad de JOIN con tablas lookup.

## Cuándo se usa

Es la elección correcta cuando el conjunto de valores es **estable en el tiempo** (días de la semana, estados binarios, polaridades técnicas) y la semántica debe ser controlada por el esquema. Desaconsejado cuando el vocabulario evoluciona con frecuencia o hacen falta atributos extra (etiquetas localizadas, orden de visualización, flags), porque PostgreSQL no ofrece `ALTER TYPE DROP VALUE` nativo: eliminar un valor requiere recrear el tipo y migrar las columnas.
