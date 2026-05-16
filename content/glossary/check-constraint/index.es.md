---
title: "CHECK constraint"
description: "Restricción SQL estándar que limita los valores admitidos en una columna mediante una expresión booleana."
translationKey: "glossary_check_constraint"
aka: "CHECK constraint"
articles:
  - "/posts/mysql/enum-mysql-semplifica-o-complica"
  - "/posts/postgresql/enum-postgresql-paga-o-pesa"
  - "/posts/oracle/enum-oracle-workaround-fino-a-23ai"
---

El **CHECK constraint** es una restricción SQL estándar que limita los valores admitidos en una columna o tabla mediante una expresión booleana. Cuando un `INSERT` o `UPDATE` produciría un valor que viola la expresión, la base de datos rechaza la operación.

## Cómo funciona

Se declara a nivel de columna o de tabla en el `CREATE TABLE` o se añade después con `ALTER TABLE ADD CONSTRAINT`. La expresión puede ser cualquier condición booleana válida: `status IN ('NEW','ACTIVE','CLOSED')`, `precio > 0`, `fecha_fin >= fecha_inicio`. La restricción se evalúa en cada escritura sobre la columna.

## Para qué sirve

Garantizar la integridad del dato directamente en el schema, sin tener que validar a nivel aplicativo. Particularmente útil para:

- Limitar un campo a un conjunto de valores (alternativa a ENUM)
- Restricciones inter-columna (ej. coherencia de fechas, sumas que deben corresponder)
- Validación de formato básica (ej. emails, códigos fiscales)

## Cuándo se usa en MySQL

Cuidado con la versión: antes de **MySQL 8.0.16** los CHECK constraint se parseaban y se ignoraban silenciosamente. Solo desde la 8.0.16 se aplican de verdad. Es algo que ha sorprendido a muchos desarrolladores migrados de PostgreSQL u Oracle, donde los CHECK funcionan desde siempre.

Respecto a ENUM, CHECK es más flexible (renombrar un valor es solo un `ALTER CONSTRAINT`) pero más verboso. Va bien para conjuntos de 5-15 valores que se tocan de vez en cuando, sin necesidad de atributos adicionales.
