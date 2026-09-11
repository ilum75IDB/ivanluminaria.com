---
title: "Data Quality"
description: "Medida en que los datos son precisos, completos, coherentes, válidos y oportunos. Proceso continuo de monitoreo y remediación, no una verificación puntual."
translationKey: "glossary_data_quality"
aka: "Calidad del dato"
articles:
  - "/posts/data-warehouse/data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati"
---

La Data Quality mide en qué medida los datos de un sistema son fiables para respaldar decisiones y análisis. Cinco dimensiones la definen: precisión, completitud, coherencia, validez y oportunidad. Ninguna de ellas está garantizada de forma permanente: se degradan con el tiempo por integraciones defectuosas, errores humanos, cambios de esquema o fuentes externas fuera de control.

## Cómo funciona

Un proceso de Data Quality se articula en tres fases recurrentes: **profiling**, **monitoring** y **remediation**.

El profiling analiza la distribución de los datos para detectar anomalías estructurales (valores nulos, duplicados, formatos inconsistentes). El monitoring aplica reglas continuas sobre los pipelines — umbrales de nulidad, rangos esperados, cardinalidad — y genera alertas cuando una métrica cae por debajo del nivel aceptable. La remediation corrige los datos en origen (fix en la fuente) o en destino (transformaciones de limpieza en el pipeline ETL/ELT).

```sql
-- Ejemplo: control de completitud sobre una columna crítica
SELECT
  COUNT(*) AS total,
  COUNT(customer_id) AS no_nulos,
  ROUND(COUNT(customer_id) * 100.0 / COUNT(*), 2) AS pct_completitud
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '7 days';
```

## Contexto operativo

En los data warehouses, la Data Quality es un requisito previo de la governance: sin ella, los informes y los modelos de ML producen resultados poco fiables independientemente de la calidad de la arquitectura subyacente. Las herramientas especializadas (Great Expectations, dbt tests, Soda Core) integran los controles directamente en los pipelines, bloqueando los datos no conformes antes de que lleguen a las capas analíticas. El principal trade-off es entre latencia y rigor: controles más granulares aumentan la cobertura pero ralentizan los jobs de carga.
