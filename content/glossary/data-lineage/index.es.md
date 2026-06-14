---
title: "Data Lineage"
description: "Data Lineage: rastrear el recorrido completo de un dato desde el origen hasta el destino, a través de transformaciones y sistemas intermedios, para auditoría y troubleshooting."
translationKey: "glossary_data_lineage"
aka: "Data Provenance, Trazabilidad de Datos"
articles:
  - "/posts/data-warehouse/data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati"
---

El Data Lineage es la capacidad de reconstruir el recorrido completo de un dato: dónde se origina, por qué sistemas transita, qué transformaciones sufre y dónde termina. En un data warehouse moderno, donde los datos atraviesan pipelines ETL/ELT, staging layers y marts dimensionales, esta trazabilidad es un requisito operativo, no un complemento opcional.

## Cómo funciona

El lineage se captura en dos niveles de granularidad:

- **Column-level lineage**: rastrea cada columna individual a través de las transformaciones SQL. Herramientas como dbt exponen este nivel de forma nativa mediante su grafo de dependencias.
- **Table-level lineage**: mapea las dependencias entre tablas o datasets, suficiente para impact analysis y documentación.

Con dbt, cada modelo `.sql` genera automáticamente metadatos de lineage accesibles mediante `dbt docs generate`. A nivel de plataforma, Apache Atlas y OpenLineage (estándar abierto) permiten agregar lineage de fuentes heterogéneas.

```sql
-- dbt model: marts/finance/revenue.sql
-- El lineage rastrea automáticamente la dependencia de staging.orders y staging.payments
SELECT
  o.order_id,
  p.amount AS revenue
FROM {{ ref('stg_orders') }} o
JOIN {{ ref('stg_payments') }} p ON o.order_id = p.order_id
```

## Cuándo se usa

Tres escenarios justifican la inversión en Data Lineage:

1. **Auditoría regulatoria** (GDPR, SOX, DORA): demostrar el origen y las transformaciones de datos sensibles o financieros exige un lineage documentado y verificable.
2. **Troubleshooting**: un KPI incorrecto en un informe se puede rastrear hacia arriba — qué transformación introdujo el error, qué tabla fuente estaba corrupta.
3. **Impact analysis**: antes de modificar una tabla fuente, conocer cuántos modelos downstream dependen de ella evita regresiones silenciosas.

El coste de implementación escala con la granularidad: el lineage a nivel de columna requiere herramientas dedicadas o plataformas que lo soporten de forma nativa.
