---
title: "Flashback Table"
description: "Comando Oracle que restaura una tabla completa a un punto anterior en el tiempo usando datos de undo, sin interrumpir las sesiones activas en otras tablas."
translationKey: "glossary_flashback_table"
aka: "Oracle Flashback Table"
articles:
  - "/posts/oracle/oracle-flashback-recupero-dati-logici-senza-downtime-da-query-a-database"
---

`FLASHBACK TABLE` es un comando DDL/DML de Oracle que revierte una tabla completa — incluidos sus datos — a un snapshot anterior, aprovechando los segmentos de undo todavía disponibles en la instancia. A diferencia de una restauración tradicional, opera a nivel lógico y no requiere downtime de la base de datos.

## Cómo funciona

El comando lee los bloques de undo generados por las transacciones posteriores al punto objetivo y los aplica en orden inverso sobre la tabla. Para que funcione, la tabla debe tener `ROW MOVEMENT` habilitado (necesario para reasignar los ROWID durante el proceso) y los datos de undo deben seguir presentes en el tablespace UNDO — no sobrescritos por transacciones más recientes.

```sql
-- Prerequisito: habilitar ROW MOVEMENT
ALTER TABLE pedidos ENABLE ROW MOVEMENT;

-- Restaurar a un timestamp específico
FLASHBACK TABLE pedidos TO TIMESTAMP
  TO_TIMESTAMP('2025-06-10 14:30:00', 'YYYY-MM-DD HH24:MI:SS');

-- Restaurar a un SCN específico
FLASHBACK TABLE pedidos TO SCN 9823741;
```

## Cuándo se usa

El escenario habitual es la recuperación ante un error aplicativo o humano: un `DELETE` o `UPDATE` ejecutado sin el `WHERE` correcto, o un `TRUNCATE` accidental (este último solo es recuperable si la tabla fue eliminada con DROP y se usa `FLASHBACK DROP`). El comando es adecuado cuando:

- la ventana temporal es reducida (acotada por el valor de `UNDO_RETENTION` configurado);
- se necesita restaurar una sola tabla sin afectar a las demás;
- las sesiones activas en otras tablas no deben interrumpirse.

Dos limitaciones principales: la operación falla si los datos de undo ya han sido sobrescritos, y no gestiona dependencias referenciales — si la tabla tiene foreign keys hacia otras tablas que también fueron modificadas en el intervalo, la restauración puede generar violaciones de integridad que deben resolverse manualmente.
