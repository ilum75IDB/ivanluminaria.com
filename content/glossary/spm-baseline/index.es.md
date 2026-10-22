---
title: "SPM Baseline"
description: "Baseline de Oracle SQL Plan Management: congela un plan de ejecución aprobado para una consulta, evitando que el optimizador lo sustituya por uno menos eficiente."
translationKey: "glossary_spm_baseline"
aka: "SQL Plan Management Baseline"
articles:
  - "/posts/oracle/oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback"
---

Una SPM Baseline es una construcción de Oracle SQL Plan Management que ancla un plan de ejecución concreto a una consulta. Una vez que un plan se marca como baseline aceptada, el Cost-Based Optimizer (CBO) lo utiliza de forma exclusiva, aunque encuentre un plan alternativo con un coste estimado menor, hasta que dicha alternativa sea aceptada explícitamente.

## Cómo funciona

Cada plan se identifica mediante un `SQL_HANDLE` (vinculado al texto de la consulta) y un `PLAN_NAME` (vinculado al plan específico). Oracle mantiene una SQL Plan History: los planes nuevos entran en el historial automáticamente, pero no se convierten en baseline hasta que se aceptan de forma explícita. Solo los planes marcados como `ACCEPTED` son elegibles en tiempo de ejecución.

```sql
-- Cargar una baseline desde la caché de cursores para una consulta específica
DECLARE
  l_plans PLS_INTEGER;
BEGIN
  l_plans := DBMS_SPM.LOAD_PLANS_FROM_CURSOR_CACHE(
    sql_id => 'abc123xyz',
    plan_hash_value => 987654321
  );
END;
/

-- Verificar las baselines activas
SELECT sql_handle, plan_name, accepted, enabled, fixed
FROM   dba_sql_plan_baselines
WHERE  sql_text LIKE '%nombre_tabla%';
```

Activar `FIXED = YES` añade un bloqueo más estricto: el CBO no puede considerar ningún plan alternativo independientemente de nuevas estadísticas o hints.

## Cuándo se usa

El escenario más habitual es una actualización de base de datos (p. ej., de 11g R2 a 19c): los planes validados en staging se capturan y cargan como baselines antes del go-live en producción, de modo que la nueva versión del optimizador no pueda introducir regresiones. También resulta útil tras una actualización masiva de estadísticas o un cambio estructural (nuevo índice, particionado) que pudiera desestabilizar consultas críticas.

El principal inconveniente es el mantenimiento: las baselines deben revisarse periódicamente. Un plan congelado sobre una tabla que crece un orden de magnitud puede volverse subóptimo con el tiempo.
