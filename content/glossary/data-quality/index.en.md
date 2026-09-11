---
title: "Data Quality"
description: "Measure of how accurate, complete, consistent, valid, and timely data is. A continuous monitoring and remediation process, not a one-off check."
translationKey: "glossary_data_quality"
aka: null
articles:
  - "/posts/data-warehouse/data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati"
---

Data Quality measures how reliable data is for supporting decisions and analysis. Five dimensions define it: accuracy, completeness, consistency, validity, and timeliness. None of them are permanently guaranteed — they degrade over time due to faulty integrations, human errors, schema changes, or uncontrolled external sources.

## How it works

A Data Quality process runs in three recurring phases: **profiling**, **monitoring**, and **remediation**.

Profiling analyzes data distribution to detect structural anomalies (null values, duplicates, inconsistent formats). Monitoring applies continuous rules across pipelines — null thresholds, expected ranges, cardinality checks — and raises alerts when a metric drops below an acceptable level. Remediation fixes data upstream (source-side fix) or downstream (cleansing transformations in the ETL/ELT pipeline).

```sql
-- Example: completeness check on a critical column
SELECT
  COUNT(*) AS total,
  COUNT(customer_id) AS non_null,
  ROUND(COUNT(customer_id) * 100.0 / COUNT(*), 2) AS pct_completeness
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '7 days';
```

## Operational context

In data warehouses, Data Quality is a prerequisite for governance: without it, reports and ML models produce unreliable output regardless of how well the underlying architecture is designed. Dedicated tools (Great Expectations, dbt tests, Soda Core) embed checks directly into pipelines, blocking non-conforming data before it reaches analytical layers. The main trade-off is between latency and rigor: more granular checks increase coverage but slow down loading jobs.
