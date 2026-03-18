---
title: "COALESCE"
description: "Función SQL que devuelve el primer valor no NULL de una lista de expresiones."
translationKey: "glossary_coalesce"
aka: "NVL (Oracle), IFNULL (MySQL)"
articles:
  - "/posts/data-warehouse/ragged-hierarchies"
---

**COALESCE** es una función SQL estándar que acepta una lista de expresiones y devuelve la primera que no es NULL. Si todas las expresiones son NULL, devuelve NULL.

## Sintaxis

``` sql
COALESCE(expresion1, expresion2, expresion3, ...)
```

Equivale a una cadena de CASE WHEN:

``` sql
CASE WHEN expresion1 IS NOT NULL THEN expresion1
     WHEN expresion2 IS NOT NULL THEN expresion2
     WHEN expresion3 IS NOT NULL THEN expresion3
     ELSE NULL END
```

## Uso en las jerarquías

En el contexto de las ragged hierarchies, COALESCE se usa a menudo para rellenar los niveles faltantes:

``` sql
COALESCE(top_group_name, group_name, client_name) AS top_group_name
```

Esto funciona como workaround en los reportes, pero tiene limitaciones importantes: debe repetirse en cada consulta, no distingue los valores originales de los de fallback, y complica el código.

## Alternativas por base de datos

- **Oracle**: `NVL(a, b)` para dos valores, `COALESCE` para más de dos
- **MySQL**: `IFNULL(a, b)` para dos valores, `COALESCE` para más de dos
- **PostgreSQL**: solo `COALESCE` (SQL estándar)

## Enfoque recomendado en el DWH

En un data warehouse, es preferible usar COALESCE en el ETL para poblar la tabla dimensional con valores NOT NULL (self-parenting), en lugar de usarla repetidamente en los reportes. La lógica de gestión de NULLs debe estar en el modelo, no en la presentación.
