---
title: "SQL Plan Management (SPM)"
description: "Funcionalidad de Oracle que estabiliza los planes de ejecución mediante baselines aprobadas, evitando regresiones de rendimiento causadas por el optimizer."
translationKey: "glossary_sql_plan_management"
aka: "SPM, SQL Plan Baseline"
articles:
  - "/posts/oracle/oracle-sql-plan-management-stabilizzare-i-piani-di-esecuzione-per-prevenire"
---

SQL Plan Management (SPM) es una funcionalidad de Oracle Database que permite controlar qué planes de ejecución puede utilizar el optimizer para una sentencia SQL concreta. El mecanismo central es el **SQL Plan Baseline**: un repositorio de planes verificados y aceptados que el optimizer consulta antes de adoptar cualquier plan recién generado.

## Cómo funciona

Con SPM activo, el optimizer puede generar planes alternativos, pero los marca como no aceptados. Un plan nuevo solo entra en producción tras una aceptación explícita — manual o mediante evolución automática — y únicamente si demuestra un rendimiento igual o superior al del baseline existente.

```sql
-- Carga manual de un plan desde la Cursor Cache al baseline
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

Cada entrada del baseline se identifica mediante el par `SQL_HANDLE` + `PLAN_NAME` y se almacena en el tablespace `SYSAUX`, con persistencia independiente de cambios en estadísticas o parámetros del sistema.

## Cuándo se utiliza

SPM es la herramienta de referencia cuando:

- una actualización de estadísticas, un parche del optimizer o una actualización de Oracle introduce regresiones de plan en consultas críticas;
- se necesita congelar el comportamiento de una consulta específica en entornos con SLAs estrictos;
- se migra entre versiones de Oracle y se requiere estabilidad de plan durante el período de transición.

La principal limitación operativa es la gestión del ciclo de vida de los baselines: los baselines acumulados deben revisarse periódicamente para no bloquear optimizaciones legítimas que el optimizer podría aprovechar.
