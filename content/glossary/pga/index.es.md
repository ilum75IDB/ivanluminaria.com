---
title: "PGA (Program Global Area)"
description: "La PGA es el área de memoria privada que Oracle asigna por sesión. Una configuración incorrecta degrada silenciosamente los sort y hash join, dificultando el diagnóstico."
translationKey: "glossary_pga"
aka: "Program Global Area"
articles:
  - "/posts/oracle/ai-mostra-sintomo-board-chiede-causa"
---

La PGA (Program Global Area) es un área de memoria privada que Oracle asigna a cada proceso servidor o sesión. A diferencia de la SGA (System Global Area), que es compartida entre todas las sesiones, la PGA es exclusiva: contiene el espacio de trabajo para operaciones de sort, hash join, bitmap merge y las variables de sesión.

## Cómo funciona

Oracle gestiona la PGA en modo automático (`PGA_AGGREGATE_TARGET`) o manual. En modo automático, la base de datos estima la memoria disponible y la distribuye entre las sesiones activas. Cuando la PGA asignada supera el objetivo, Oracle vuelca los datos a disco (temp tablespace), degradando el rendimiento.

```sql
-- Verificar la configuración actual de PGA
SELECT name, value
FROM v$pgastat
WHERE name IN (
  'aggregate PGA target parameter',
  'aggregate PGA auto target',
  'total PGA inuse',
  'cache hit percentage'
);
```

El parámetro `WORKAREA_SIZE_POLICY` controla si la gestión es `AUTO` o `MANUAL`. En modo manual, parámetros como `SORT_AREA_SIZE` y `HASH_AREA_SIZE` definen los límites por sesión.

## Contexto operativo

Una PGA subdimensionada provoca volcados frecuentes a disco: las consultas con ORDER BY, GROUP BY o hash join se vuelven lentas sin que las alertas estándar (CPU, I/O agregado) lo evidencien con claridad. La degradación suele correlacionarse con picos de sesiones concurrentes, no con consultas individuales.

Una PGA modificada sin registro en el change log es una de las causas más difíciles de detectar en regresiones de rendimiento: el síntoma aparece en producción, pero el origen se remonta a un cambio de parámetro realizado semanas antes, un escenario donde las herramientas de observability por sí solas resultan insuficientes.
