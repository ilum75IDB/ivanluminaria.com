---
title: "Parallel DML"
description: "Funcionalidad de Oracle que distribuye INSERT, UPDATE, DELETE y MERGE entre múltiples procesos esclavos. Requiere habilitación explícita a nivel de sesión."
translationKey: "glossary_parallel_dml"
aka: "Parallel DML (Oracle Parallel Execution)"
articles:
  - "/posts/data-warehouse/etl-oracle-da-4-ore-a-25-minuti-con-staging-tables-merge-e-parallel-dml"
---

El Parallel DML es la funcionalidad de Oracle que distribuye las operaciones de escritura — INSERT, UPDATE, DELETE y MERGE — entre múltiples procesos esclavos coordinados por un único query coordinator. A diferencia del Parallel Query, que se activa automáticamente en tablas con un grado de paralelismo definido, el Parallel DML exige una habilitación explícita a nivel de sesión para que los hints sean respetados.

## Cómo funciona

La habilitación se realiza con un comando DDL sobre la sesión activa:

```sql
ALTER SESSION ENABLE PARALLEL DML;
```

Solo después de este comando los hints `/*+ PARALLEL(tabla, grado) */` tienen efecto sobre las operaciones DML. Sin la habilitación a nivel de sesión, Oracle descarta los hints de forma silenciosa, sin emitir errores ni advertencias, lo que dificulta el diagnóstico durante el análisis de rendimiento.

```sql
INSERT /*+ PARALLEL(target_table, 8) */ INTO target_table
SELECT * FROM staging_table;
```

Cada proceso esclavo trabaja sobre una partición lógica de los datos. El COMMIT final consolida todas las escrituras de forma atómica. Hasta ese momento, la tabla destino no está disponible para otras sesiones DML.

## Cuándo se usa

El Parallel DML es la opción adecuada para cargas ETL en entornos de Data Warehouse donde se procesan decenas o cientos de millones de filas dentro de ventanas de procesamiento ajustadas. La mejora de rendimiento escala con el ancho de banda de I/O disponible y el grado de paralelismo configurado en la tabla o especificado en el hint.

Restricciones a tener en cuenta:

- No aplicable a tablas con triggers habilitados
- Incompatible con ciertos tipos de restricciones de integridad referencial
- La sesión no debe tener transacciones DML abiertas antes de la habilitación
