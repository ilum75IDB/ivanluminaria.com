---
title: "ASSERTION"
description: "Constructo SQL estándar para expresar vínculos cross-tabla validados a nivel transaccional por el motor del database. Anunciado en Oracle 26ai."
translationKey: "glossary_sql_assertion"
aka: "SQL ASSERTION (cross-table constraint)"
articles:
  - "/posts/oracle/enum-oracle-workaround-fino-a-23ai"
---

La **`ASSERTION`** es un constructo previsto por el estándar SQL — desde los años 90 — para expresar vínculos que **atraviesan múltiples tablas**, validados directamente por el motor del database a nivel transaccional. Sobre el papel es una solución elegante a problemas que hoy se resuelven con trigger o con check aplicativos. En la práctica, hasta 2026, ningún DBMS mainstream lo había implementado realmente. Oracle lo ha anunciado para la 26ai.

## Cómo funciona (sobre el papel)

`CREATE ASSERTION nombre CHECK (<condición>)` define una condición que el database garantiza siempre verdadera. A diferencia de un `CHECK` de tabla (que evalúa una sola fila en el momento del INSERT/UPDATE), una `ASSERTION` puede hacer referencia a **múltiples tablas**, hacer agregaciones, contar filas. Ejemplo: "al menos una fila en `estados_x` debe tener `activo='Y'`", o "la suma de importes en `linea_pedido` no puede superar el `total` en `pedido`".

## Por qué ha tardado tanto

Implementar las `ASSERTION` de manera eficiente es difícil. En cada modificación de las tablas implicadas el motor debe revalidar la aserción — y hacerlo sin serializar todas las transacciones requiere mecanismos sofisticados de incremental checking o de lock cross-tabla. Ningún vendor ha encontrado nunca la fórmula ganadora. Oracle 26ai será el primer intento serio en un DBMS comercial de relevancia.

## Qué cambia para quien modela enumeraciones

Para las taxonomías gestionadas con lookup table, las `ASSERTION` abren un escenario nuevo: vínculos que hoy viven como trigger aplicativos (ej. "la taxonomía no puede quedar sin estados activos") se volverán expresables en DDL, validados a nivel transaccional, gestionados por el motor. Es material que se desarrolla cuando la implementación 26ai esté disponible en test.
