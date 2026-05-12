---
title: "ENUM (MySQL)"
description: "Tipo de dato de MySQL que admite un conjunto predefinido de valores cadena, almacenado internamente como un índice numérico de 1-2 bytes."
translationKey: "glossary_mysql_enum"
aka: "MySQL ENUM type"
articles:
  - "/posts/mysql/enum-mysql-semplifica-o-complica"
---

**ENUM (MySQL)** es un tipo de dato que admite solo un conjunto predefinido de valores cadena, declarado en el momento de creación de la columna. Es una de las features características de MySQL — pocos otros DBMS mainstream tienen un tipo enumerado nativo.

## Cómo funciona

Cuando declaras `status ENUM('NEW','ACTIVE','CLOSED')`, MySQL asigna a cada valor un índice numérico: 'NEW'=1, 'ACTIVE'=2, 'CLOSED'=3. En disco se almacena el índice entero, no la cadena. La conversión ocurre en lectura. Bajo los 256 valores declarados ENUM ocupa 1 byte por fila; entre 256 y 65535, ocupa 2 bytes.

## Para qué sirve

ENUM ofrece tres ventajas concretas: almacenamiento compacto (1-2 bytes en lugar de N caracteres de un VARCHAR), restricción "solo estos valores" declarada a nivel de schema sin necesidad de un CHECK separado, lectura legible en las queries (`WHERE status = 'ACTIVE'`) sin JOIN contra una tabla de lookup.

## Cuándo usarlo

Es la elección correcta cuando el dominio de los valores es realmente cerrado y estable en el tiempo: días de la semana, estados binarios o ternarios fijos, polaridad, tipologías reguladas por ley. Es perfecto también dentro de una lookup table pequeña (5-50 filas), donde sus límites se vuelven irrelevantes.

## Límites a conocer

- **Case-insensitive**: `'ACTIVE'` y `'active'` son el mismo valor (comportamiento diferente respecto a PostgreSQL)
- **Ordenamiento por posición de declaración**, no alfabético — un `ORDER BY` puede producir resultados sorprendentes
- **Modificar el ENUM** (añadir un valor en el medio, renombrar, reordenar) requiere un rebuild de la tabla, costoso en tablas grandes
