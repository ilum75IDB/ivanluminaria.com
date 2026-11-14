---
title: "SQL Plan Baseline"
description: "Conjunto de planes de ejecución aceptados para un SQL statement concreto, almacenado en el repositorio SPM de Oracle para garantizar la estabilidad del rendimiento."
translationKey: "glossary_sql_plan_baseline"
aka: "SPM Baseline, Plan Baseline"
articles:
  - "/posts/oracle/oracle-sql-plan-management-stabilizzare-i-piani-di-esecuzione-per-prevenire"
---

Una SQL Plan Baseline es un conjunto de uno o más planes de ejecución aprobados para un SQL statement específico, gestionado por el componente Oracle **SQL Plan Management (SPM)**. Cuando una baseline está activa, el optimizer selecciona únicamente entre los planes que contiene, aunque durante la compilación identifique alternativas aparentemente más eficientes.

## Cómo funciona

En el momento del parsing, el optimizer compara el plan generado con los almacenados en la baseline. Si el plan ya está marcado como `ACCEPTED = YES`, se utiliza directamente. Si es nuevo, se añade a la baseline con estado `NOT ACCEPTED` y permanece en cuarentena hasta que un DBA — o el proceso automático de evolución de planes — lo verifique y promueva.

```sql
-- Carga manual de una baseline desde la Cursor Cache
DECLARE
  l_plans PLS_INTEGER;
BEGIN
  l_plans := DBMS_SPM.LOAD_PLANS_FROM_CURSOR_CACHE(
    sql_id => 'abc123xyz',
    plan_hash_value => 987654321
  );
END;
/
```

## Cuándo se utiliza

Las baselines son la herramienta principal para **bloquear regresiones de plan** tras actualizaciones de base de datos, recolección de nuevas estadísticas o cambios estructurales en índices. Son preferibles a los hints inline porque no requieren modificaciones en el código de la aplicación y se gestionan íntegramente desde el lado del DBA. La limitación principal es que cada baseline está vinculada al `SQL_ID` exacto: cualquier variación en el texto de la consulta — incluso espacios o mayúsculas — genera un `SQL_ID` distinto y requiere una baseline separada.
