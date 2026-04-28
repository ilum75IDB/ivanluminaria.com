---
title: "Índice Parcial"
description: "Índice PostgreSQL que cubre solo un subconjunto de las filas de la tabla, definido con WHERE en el CREATE INDEX. Reduce espacio y tiempo de mantenimiento."
translationKey: "glossary_indice_parziale"
aka: "Partial Index"
articles:
  - "/posts/postgresql/postgresql-indici-quando-fanno-male"
---

Un **índice parcial** (*partial index*) es un índice PostgreSQL que cubre solo un subconjunto de las filas de la tabla, definido con una cláusula `WHERE` en el `CREATE INDEX`. Las filas que no cumplen la condición no se indexan y no ocupan espacio en el índice.

## Cómo funciona

La sintaxis es simple:

```sql
CREATE INDEX idx_activos
ON pedidos (fecha_creacion)
WHERE estado = 'activo';
```

El índice contiene solo las filas con `estado = 'activo'`. Todas las demás se ignoran. El planner usa este índice solo para consultas que incluyen la misma condición `WHERE estado = 'activo'` (o una condición más restrictiva).

## Para qué sirve

Resuelve un escenario muy común: la mayoría de las consultas operativas siempre filtra por una condición (p.ej. `activo = true`, `archivado = false`, `fecha > x`), y las filas que no cumplen esa condición no se buscan nunca. Indexarlas es un desperdicio.

Los beneficios concretos:

- **Espacio**: el índice es más pequeño, a veces mucho. En una tabla donde el 35% de las filas es "activa", el índice parcial ocupa el 35% del espacio.
- **Mantenimiento**: menos trabajo para VACUUM, menos write-amplification en INSERT/UPDATE de las filas excluidas.
- **Rendimiento**: el índice es más pequeño de recorrer y suele caber en caché con más facilidad.

## Cuándo se usa

Se usa cuando:

- Las consultas operativas filtran sistemáticamente por una condición binaria
- Las filas que no cumplen la condición son muchas (>50%) y no relevantes para el workload caliente
- Las consultas sobre el otro subconjunto son raras y aceptables con un seq scan

No usarlo si las consultas filtran por condiciones dinámicas o variables: el planner nunca usará el índice parcial.
