---
title: "MERGE"
description: "Instrucción SQL que combina INSERT y UPDATE en una única operación atómica (upsert), eliminando el doble acceso a la tabla propio de los ETL heredados."
translationKey: "glossary_merge"
aka: "UPSERT, MERGE INTO"
articles:
  - "/posts/data-warehouse/etl-oracle-da-4-ore-a-25-minuti-con-staging-tables-merge-e-parallel-dml"
---

`MERGE` es una instrucción SQL estándar (ISO/IEC 9075) que unifica la lógica de INSERT y UPDATE en una única operación atómica. El motor accede a la tabla de destino una sola vez, compara cada fila fuente con su contraparte en el destino y decide en tiempo real si insertar, actualizar o — donde esté soportado — eliminar.

## Cómo funciona

La sintaxis básica tiene tres cláusulas principales: `USING` (fuente de datos), `ON` (condición de join) y `WHEN MATCHED` / `WHEN NOT MATCHED` (acciones condicionales).

```sql
MERGE INTO pedidos_dw tgt
USING staging_pedidos src
  ON (tgt.pedido_id = src.pedido_id)
WHEN MATCHED THEN
  UPDATE SET tgt.importe = src.importe,
             tgt.estado  = src.estado
WHEN NOT MATCHED THEN
  INSERT (pedido_id, importe, estado)
  VALUES (src.pedido_id, src.importe, src.estado);
```

Toda la operación queda envuelta en una única transacción: o todo tiene éxito (COMMIT implícito o explícito), o nada se escribe (ROLLBACK automático ante cualquier error).

## Cuándo se usa

`MERGE` es la herramienta natural para los flujos ETL/ELT que cargan datos incrementales en un data warehouse: la staging table aporta las filas nuevas o modificadas, y `MERGE` las aplica a la tabla de destino sin necesidad de un SELECT previo para discriminar entre INSERT y UPDATE.

Frente al patrón heredado `SELECT → IF EXISTS → INSERT/UPDATE`:

- **Elimina la race condition** entre lectura y escritura en entornos concurrentes.
- **Reduce los round-trips** hacia la base de datos.
- **Admite paralelización** (p. ej., `PARALLEL DML` en Oracle) sobre tablas particionadas.

El principal inconveniente es la portabilidad: la sintaxis varía entre Oracle, SQL Server, PostgreSQL (que usa `INSERT ... ON CONFLICT`) y MySQL (`INSERT ... ON DUPLICATE KEY UPDATE`), lo que dificulta la reutilización entre distintos vendors sin una capa de abstracción.
