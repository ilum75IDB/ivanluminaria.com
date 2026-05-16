---
title: "ALTER DOMAIN"
description: "Comando Oracle 23ai que modifica un SQL Domain (vínculo CHECK, DEFAULT, annotations) propagando el cambio a todas las columnas que usan el dominio."
translationKey: "glossary_oracle_alter_domain"
aka: "ALTER DOMAIN (Oracle 23ai)"
articles:
  - "/posts/oracle/enum-oracle-workaround-fino-a-23ai"
---

`ALTER DOMAIN` es el comando Oracle Database 23ai que **modifica un SQL Domain existente** — el vínculo `CHECK`, el valor de `DEFAULT`, las `ANNOTATIONS` — propagando el cambio a todas las columnas que declararon ese dominio como tipo. Es lo que convierte al SQL Domain en una alternativa real a la lookup table, no en un simple `CHECK` reutilizable.

## Cómo funciona

`ALTER DOMAIN nombre_dominio CONSTRAINT chk_X CHECK (VALUE IN (...))` actualiza el vínculo del dominio. Oracle busca automáticamente todas las columnas declaradas con `nombre_dominio` (en cualquier tabla y esquema, según los permisos) y aplica el nuevo vínculo. Las filas existentes pueden ser validadas (`VALIDATE`) o dejadas como están (`NOVALIDATE`), a discreción de quien gestiona la migración.

## Para qué sirve

Sustituir docenas de `ALTER TABLE` con una sola operación. Cuando el dominio de una columna se usa en 20 tablas y hay que añadir un nuevo valor admitido, antes de la 23ai había que modificar 20 `CHECK` distintos — con `ALTER DOMAIN` es una sola instrucción. Vale también para modificaciones al `DEFAULT` o a las `ANNOTATIONS`.

## Qué cambia respecto a ALTER TABLE

`ALTER TABLE ... MODIFY CONSTRAINT` actúa sobre un único vínculo de una única tabla. `ALTER DOMAIN` actúa sobre todas las columnas, en todas las tablas, que heredan el dominio. Es la diferencia entre una operación local y una operación de schema-wide governance.
