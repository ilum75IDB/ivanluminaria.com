---
title: "Data Lineage"
description: "Data Lineage: tracking the full journey of a data point from source through transformations to destination, enabling audit, troubleshooting, and impact analysis."
translationKey: "glossary_data_lineage"
aka: "Data Provenance, Data Traceability"
articles:
  - "/posts/data-warehouse/data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati"
---

Data Lineage is the ability to reconstruct the complete journey of a data point: where it originates, which systems it passes through, what transformations it undergoes, and where it lands. In a modern data warehouse — where data flows across ETL/ELT pipelines, staging layers, and dimensional marts — this traceability is a hard requirement, not a nice-to-have.

## How it works

Lineage is captured at two granularity levels:

- **Column-level lineage**: tracks every individual column through SQL transformations. Tools like dbt expose this natively via their dependency graph.
- **Table-level lineage**: maps dependencies between tables or datasets, sufficient for impact analysis and documentation.

With dbt, each `.sql` model automatically generates lineage metadata accessible via `dbt docs generate`. At the platform level, Apache Atlas and OpenLineage (an open standard) aggregate lineage from heterogeneous sources.

```sql
-- dbt model: marts/finance/revenue.sql
-- Lineage automatically tracks the dependency on staging.orders and staging.payments
SELECT
  o.order_id,
  p.amount AS revenue
FROM {{ ref('stg_orders') }} o
JOIN {{ ref('stg_payments') }} p ON o.order_id = p.order_id
```

## When to use it

Three scenarios justify the investment in Data Lineage:

1. **Regulatory audit** (GDPR, SOX, DORA): proving the origin and transformations of sensitive or financial data requires documented, verifiable lineage.
2. **Troubleshooting**: a wrong KPI in a report can be traced upstream — which transformation introduced the error, which source table was corrupted.
3. **Impact analysis**: before modifying a source table, knowing how many downstream models depend on it prevents silent regressions.

Implementation cost scales with granularity: column-level lineage requires dedicated tooling or platforms that support it natively.
