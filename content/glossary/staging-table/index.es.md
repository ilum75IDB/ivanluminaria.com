---
title: "Staging Table"
description: "Tabla temporal que actúa como área de aterrizaje para datos brutos en un proceso ETL, separando la ingestión de la transformación y la carga final."
translationKey: "glossary_staging_table"
aka: "Área de staging, landing table"
articles:
  - "/posts/data-warehouse/etl-oracle-da-4-ore-a-25-minuti-con-staging-tables-merge-e-parallel-dml"
---

Una staging table es una tabla intermedia que recibe los datos brutos desde la fuente antes de que sean transformados y cargados en el destino final. Separa con claridad las tres fases de un proceso ETL, haciendo que cada fase sea independiente, monitorizable y reanudable tras un fallo.

## Cómo funciona

Los datos se copian primero en bloque en la staging table — habitualmente sin restricciones de integridad referencial activas para maximizar el rendimiento de los INSERT — y solo después se aplican los controles de calidad, las transformaciones y el MERGE hacia las tablas de destino.

```sql
-- 1. Carga bruta en la staging table (sin restricciones activas)
INSERT /*+ APPEND */ INTO stg_orders
SELECT * FROM ext_orders_source;

-- 2. Transformación y MERGE en la tabla de destino
MERGE INTO orders tgt
USING stg_orders src
  ON (tgt.order_id = src.order_id)
WHEN MATCHED THEN UPDATE SET tgt.status = src.status
WHEN NOT MATCHED THEN INSERT (order_id, status) VALUES (src.order_id, src.status);
```

Operar en bulk sobre la staging table en lugar de fila a fila reduce drásticamente el número de COMMITs y la presión sobre el redo log.

## Cuándo se usa

Las staging tables son la solución adecuada cuando el volumen de datos hace inviable la transformación en vuelo durante la ingestión. Son especialmente útiles cuando:

- el proceso ETL debe ser reanudable (basta con relanzar desde el último TRUNCATE/INSERT sobre la staging);
- el sistema fuente no tolera consultas lentas ni transacciones de larga duración;
- se quiere aplicar Parallel DML en la fase de MERGE sin bloquear la fuente.

El principal trade-off es el espacio en disco adicional y la latencia introducida por la doble escritura, asumible en prácticamente todos los contextos batch.
