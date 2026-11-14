---
title: "Data Warehouse (DWH)"
description: "Sistema de base de datos optimizado para el análisis de datos históricos, que agrega información de fuentes operacionales heterogéneas priorizando lecturas masivas y agregaciones."
translationKey: "glossary_data_warehouse"
aka: "DWH, Enterprise Data Warehouse (EDW)"
articles:
  - "/posts/data-warehouse/la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto"
---

Un Data Warehouse es un sistema de almacenamiento diseñado para consolidar datos provenientes de múltiples fuentes operacionales — CRM, ERP, sistemas de facturación, logs de aplicaciones — en un único repositorio optimizado para el análisis. No reemplaza las bases de datos transaccionales: las complementa, leyendo de ellas mediante pipelines ETL o ELT.

## Cómo funciona

El patrón de acceso es el opuesto al OLTP: pocas escrituras masivas (batch o micro-batch) y un volumen muy alto de lecturas que recorren millones de filas. El esquema es típicamente desnormalizado — star schema o snowflake schema — para minimizar los JOIN y maximizar el rendimiento de las consultas analíticas.

```sql
-- Consulta analítica típica sobre un DWH telco
SELECT
    d.mes,
    r.region,
    SUM(f.ingresos_eur)  AS ingresos_totales,
    COUNT(f.cliente_id)  AS clientes_activos
FROM fact_ingresos f
JOIN dim_fecha   d ON f.fecha_id  = d.fecha_id
JOIN dim_region  r ON f.region_id = r.region_id
WHERE d.anio = 2024
GROUP BY d.mes, r.region
ORDER BY d.mes, ingresos_totales DESC;
```

Las materialized views son una herramienta habitual para pre-calcular agregaciones costosas y servirlas con latencia mínima.

## Cuándo utilizarlo

Un DWH es la elección correcta cuando la carga analítica empieza a degradar el rendimiento de los sistemas operacionales, cuando es necesario historizar datos que los sistemas fuente no conservan, o cuando múltiples fuentes heterogéneas deben consultarse de forma unificada. No es adecuado para escenarios que requieren datos en tiempo real con latencia inferior al segundo: en esos casos se evalúan arquitecturas lambda o kappa con una capa de streaming.

## Notas

La distinción entre un DWH y un Data Lake tiene que ver principalmente con la estructura: el DWH impone un esquema rígido en el momento de la escritura (schema-on-write), mientras que el Data Lake acepta datos crudos y aplica el esquema en la lectura (schema-on-read). Muchas arquitecturas modernas combinan ambos en el patrón conocido como Data Lakehouse.
