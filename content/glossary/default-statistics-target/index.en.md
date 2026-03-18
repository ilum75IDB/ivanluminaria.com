---
title: "default_statistics_target"
description: "The PostgreSQL parameter that controls how many samples the optimizer collects to estimate data distribution in a column."
translationKey: "glossary_default_statistics_target"
tags: ["glossary"]
---

`default_statistics_target` is the PostgreSQL parameter that defines the number of samples collected by the ANALYZE command to build statistics for each column. The default value is 100, meaning PostgreSQL samples 100 values to build histograms and most common values lists.

For small tables or tables with uniform distribution, 100 samples are sufficient. For large tables with skewed distribution — where a few values dominate most rows — 100 samples can give a distorted picture, leading the optimizer to wrong cardinality estimates.

You can increase the target at the column level with `ALTER TABLE ... ALTER COLUMN ... SET STATISTICS N`. Values between 500 and 1000 significantly improve estimate quality on columns with non-uniform distribution. Beyond 1000 the benefit is marginal and ANALYZE itself becomes slower. It is a fine-tuning adjustment that makes a real difference in queries with complex joins on tables with millions of rows.

## Related articles

- [EXPLAIN ANALYZE is not enough: how to really read a PostgreSQL execution plan](/en/posts/postgresql/explain-analyze-postgresql/)
