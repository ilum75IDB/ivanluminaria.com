---
title: "default_statistics_target"
description: "The PostgreSQL parameter that controls the granularity of statistics collected by ANALYZE (size of MCV list and histogram)."
translationKey: "glossary_postgresql_default_statistics_target"
aka: "default_statistics_target (PostgreSQL)"
articles:
  - "/posts/postgresql/explain-analyze-postgresql"
---

**default_statistics_target** is the PostgreSQL parameter that controls the **granularity of the statistics** that `ANALYZE` builds for each column. The default value is 100.

## How it works

ANALYZE builds two statistical structures per column, used by the optimizer:

- **Most common values (MCV)**: the list of the most frequent values, with their respective frequencies
- **Histogram**: the distribution of the remaining values, divided into equal-population buckets

`default_statistics_target` determines how many elements these structures can hold. With the value `100`: up to 100 values in the MCV list and up to 100 buckets in the histogram.

**The number of sampled rows is a separate matter and depends on the target**: it's roughly `300 × default_statistics_target`. With the default of 100, ANALYZE reads ~30,000 rows per column; with a target of 500, ~150,000. So raising the target increases both the granularity of the statistics **and** the cost of ANALYZE.

## When to increase it

For small tables or tables with uniform distribution, 100 samples are sufficient. For large tables with skewed distribution — where a few values dominate most rows — 100 samples can give a distorted picture, leading the optimizer to wrong cardinality estimates.

You can increase the target at the column level:

    ALTER TABLE orders ALTER COLUMN status SET STATISTICS 500;
    ANALYZE orders;

Values between 500 and 1000 significantly improve estimate quality on columns with non-uniform distribution.

## Practical limits

Beyond 1000 the benefit is marginal and `ANALYZE` itself becomes slower, because it needs to sample more rows and build larger structures. It's a fine-tuning adjustment: apply it only to columns that actually cause wrong estimates, not to every column in every table.
