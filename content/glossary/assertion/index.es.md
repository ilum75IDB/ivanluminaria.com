---
title: "ASSERTION"
description: "Restricción de integridad declarativa SQL que valida un predicado sobre el estado completo de la base de datos, abarcando múltiples tablas."
translationKey: "glossary_assertion"
aka: "Restricción declarativa multi-tabla"
articles:
  - "/posts/oracle/articolo-oracle-assertions-in-oracle-26ai"
---

Un ASSERTION es una restricción de integridad declarativa introducida por SQL-92 que expresa un predicado booleano sobre el estado completo de la base de datos. A diferencia de `CHECK` — limitado a una sola fila o, como máximo, a una sola tabla — un ASSERTION puede abarcar múltiples tablas y agregaciones, y se viola cuando el predicado evalúa a `FALSE` tras cualquier operación DML o DDL.

## Cómo funciona

El ASSERTION se define con `CREATE ASSERTION` y se asocia a un esquema. El motor lo evalúa al final de cada transacción (o, según la implementación, tras cada sentencia): si el predicado devuelve `FALSE`, la transacción es rechazada con ROLLBACK automático.

```sql
CREATE ASSERTION max_pedidos_por_cliente
CHECK (
  NOT EXISTS (
    SELECT cliente_id
    FROM pedidos
    GROUP BY cliente_id
    HAVING COUNT(*) > 1000
  )
);
```

El predicado puede referenciar cualquier tabla visible en el esquema, usando subconsultas, agregaciones y joins. El enforcement lo gestiona el motor, no la capa de aplicación.

## Cuándo se usa

Los ASSERTION cubren reglas de negocio que no pueden expresarse con `CHECK` ni con `FOREIGN KEY`: límites agregados, invariantes cross-tabla, restricciones temporales distribuidas entre múltiples entidades. El coste es real: cada transacción que toca las tablas referenciadas puede desencadenar la reevaluación del predicado, con impacto en el rendimiento en escenarios de escritura intensiva.

SQL-92 los estandarizó, pero durante décadas ningún RDBMS enterprise mainstream los implementó de forma nativa. Oracle 23ai/26ai es el primer motor de producción a gran escala en hacerlo.
