---
title: "Type safety"
description: "Propiedad de un sistema de tipos que impide, en parse-time, el uso de valores incompatibles con el tipo declarado de columna, parámetro o variable."
translationKey: "glossary_type_safety"
aka: "Seguridad de tipos, type checking"
articles:
  - "/posts/postgresql/enum-postgresql-paga-o-pesa"
---

La **type safety** es la propiedad de un sistema de tipos que impide, en parse-time o compile-time, el uso de valores no compatibles con el tipo declarado. En el contexto de bases de datos significa que el motor rechaza las operaciones que violan las restricciones de tipo, antes incluso de ejecutar la consulta.

## Cómo funciona

Cuando una columna, un parámetro de función o una variable están declarados con un tipo específico (ej. `INTEGER`, un domain personalizado, un ENUM), el motor verifica en el momento del parse que cada valor asignado o comparado sea compatible. Las operaciones que mezclan tipos incompatibles sin un cast explícito generan un error antes de la ejecución, evitando bugs que solo aparecerían en tiempo de ejecución.

## Para qué sirve

Para mover la detección de errores del runtime al parse-time, reduciendo el riesgo de datos corruptos o inconsistentes en producción. En PostgreSQL, por ejemplo, un ENUM es un tipo independiente: una función que acepta un `estado_suscripcion` no podrá jamás ser llamada con una cadena libre. En MySQL, donde el ENUM es una decoración de una columna `VARCHAR`, esta garantía no existe — la restricción está solo en la columna, no en el tipo.

## Cuándo se usa

Es útil en todos los sistemas donde la integridad semántica de los datos cuenta más que la comodidad de escritura: billing, finanzas, datos de clientes, cualquier dominio en el que un valor "fuera de dominio" representa un error de negocio y no una variante aceptable. La type safety end-to-end es uno de los rasgos distintivos de PostgreSQL y una de las razones por las que se elige en contextos enterprise.
