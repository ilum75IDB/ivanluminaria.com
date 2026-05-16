---
title: "VALIDATE / NOVALIDATE"
description: "Modos Oracle de aplicación de un vínculo al momento de la creación o modificación: VALIDATE controla todas las filas existentes, NOVALIDATE salta el control."
translationKey: "glossary_oracle_validate_novalidate"
aka: "Constraint validation modes (Oracle)"
articles:
  - "/posts/oracle/enum-oracle-19c-26ai-domini"
---

**`VALIDATE`** y **`NOVALIDATE`** son los dos modos con los que Oracle Database aplica un vínculo (CHECK, FK, UNIQUE, NOT NULL, y desde 23ai también `SQL DOMAIN`) en el momento de la **creación o modificación del vínculo mismo**. La diferencia concierne solo a las **filas ya presentes** en la tabla: todo lo que se inserta o actualiza después siempre es controlado por el motor.

## Cómo funciona

Se especifica como opción de cláusula en `CREATE TABLE`, `ALTER TABLE ADD CONSTRAINT`, `ALTER TABLE MODIFY` o `ALTER DOMAIN`. `VALIDATE` (default) hace una **escansión completa** de la tabla para verificar que cada fila respete el vínculo; si incluso una sola viola, la operación falla con `ORA-02293`. `NOVALIDATE` salta la escansión y acepta el estado actual "tal como está": el vínculo se marca como aplicado hacia adelante, pero el diccionario de datos lo señala como **no validado** (`STATUS = ENABLED NOVALIDATE` en `DBA_CONSTRAINTS`).

## Cuándo se usa NOVALIDATE

Típicamente en **tablas muy grandes** en ventanas de mantenimiento ajustadas, donde la escansión de validación costaría horas de bloqueo. Se aplica `NOVALIDATE`, se garantiza la integridad hacia adelante, y se hace un cleanup posterior vía script batch en background. Común en:

- Migración esquema en tablas históricas de cientos de millones de filas
- Adición de un CHECK sobre una columna `status` de una fact table DWH
- Conversión de viejos `CHECK` inline a `SQL DOMAIN` en muchas tablas (Oracle 23ai+)

## Qué controlar después

Una vez que el vínculo está `ENABLED NOVALIDATE`, el optimizador **no lo usa para optimizar consultas** (ej. para podar condiciones imposibles), porque no tiene garantía de que las filas históricas lo respeten. Para recuperar el plan óptimo, tras haber limpiado los datos históricos, conviene ejecutar un `ALTER TABLE ... ENABLE VALIDATE CONSTRAINT` que devuelve el vínculo a estado plenamente válido.
