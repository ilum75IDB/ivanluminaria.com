---
title: "COALESCE"
description: "A SQL function that returns the first non-NULL value from a list of expressions."
translationKey: "glossary_coalesce"
aka: "NVL (Oracle), IFNULL (MySQL)"
articles:
  - "/posts/data-warehouse/ragged-hierarchies"
---

**COALESCE** is a standard SQL function that accepts a list of expressions and returns the first one that is not NULL. If all expressions are NULL, it returns NULL.

## Syntax

``` sql
COALESCE(expression1, expression2, expression3, ...)
```

It's equivalent to a CASE WHEN chain:

``` sql
CASE WHEN expression1 IS NOT NULL THEN expression1
     WHEN expression2 IS NOT NULL THEN expression2
     WHEN expression3 IS NOT NULL THEN expression3
     ELSE NULL END
```

## Use in hierarchies

In the context of ragged hierarchies, COALESCE is often used to fill missing levels:

``` sql
COALESCE(top_group_name, group_name, client_name) AS top_group_name
```

This works as a report workaround, but has significant limitations: it must be repeated in every query, it doesn't distinguish original values from fallback ones, and it complicates the code.

## Database alternatives

- **Oracle**: `NVL(a, b)` for two values, `COALESCE` for more than two
- **MySQL**: `IFNULL(a, b)` for two values, `COALESCE` for more than two
- **PostgreSQL**: `COALESCE` only (standard SQL)

## Recommended approach in the DWH

In a data warehouse, it's better to use COALESCE in the ETL to populate the dimension table with NOT NULL values (self-parenting), rather than using it repeatedly in reports. NULL handling logic belongs in the model, not in the presentation layer.
