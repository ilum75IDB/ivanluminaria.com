---
title: "Plan fixed"
description: "Plan de ejecución Oracle marcado con FIXED=YES en una SQL Plan Baseline: el optimizador lo selecciona siempre, ignorando cualquier plan alternativo."
translationKey: "glossary_piano_fixed"
aka: "Fixed Plan (SQL Plan Baseline)"
articles:
  - "/posts/oracle/oracle-sql-plan-management-stabilizzare-i-piani-di-esecuzione-per-prevenire"
---

Un **plan fixed** es un plan de ejecución almacenado en una SQL Plan Baseline y marcado con el atributo `FIXED = YES`. A diferencia de los planes simplemente aceptados (`ACCEPTED = YES`), un plan fixed tiene prioridad absoluta: el optimizador de Oracle lo selecciona siempre para esa sentencia SQL, aunque durante la compilación encuentre planes alternativos con un coste estimado menor.

## Cómo funciona

Cuando el optimizador procesa una consulta, comprueba si existe una SQL Plan Baseline asociada a su SQL signature. Si la baseline contiene al menos un plan con `FIXED = YES`, el optimizador ignora cualquier otro plan —aceptado o no— y utiliza exclusivamente el plan fixed.

Para marcar un plan como fixed se utiliza `DBMS_SPM`:

```sql
DECLARE
  v_result PLS_INTEGER;
BEGIN
  v_result := DBMS_SPM.ALTER_SQL_PLAN_BASELINE(
    sql_handle      => 'SQL_abc123def456',
    plan_name       => 'SQL_PLAN_abc123def456_1',
    attribute_name  => 'fixed',
    attribute_value => 'YES'
  );
END;
/
```

## Cuándo se usa

El plan fixed es la herramienta adecuada cuando la estabilidad del plan es más crítica que las optimizaciones automáticas del optimizador:

- **Regresiones post-upgrade**: tras una actualización de Oracle o de las estadísticas, fijar un plan conocido como bueno evita que el optimizador elija rutas peores.
- **Consultas críticas en producción**: para sentencias con SLAs estrictos, cualquier variabilidad en el plan de ejecución es inaceptable.
- **Entornos con estadísticas inestables**: las tablas con datos muy volátiles pueden generar planes distintos en cada recopilación de estadísticas; el plan fixed neutraliza esa variabilidad.

El principal inconveniente es la rigidez: si las características de los datos cambian de forma significativa (nuevos índices, particionamiento, volúmenes muy distintos), el plan fixed puede volverse subóptimo sin que el optimizador pueda intervenir. Debe monitorizarse y revisarse periódicamente.
