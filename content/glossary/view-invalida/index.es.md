---
title: "Vista inválida"
description: "Vista de MySQL cuyo cuerpo SQL referencia objetos que ya no existen o no son accesibles: tablas renombradas, columnas eliminadas, permisos revocados."
translationKey: "glossary_view_invalida"
aka: "Vista rota, Broken view"
articles:
  - "/posts/mysql/mysql-8-0-patching-gtid-rhel"
---

Una **vista inválida** es una vista cuyo cuerpo SQL referencia objetos que ya no existen o no son accesibles: tablas renombradas, columnas eliminadas, permisos revocados. MySQL no invalida automáticamente las vistas cuando se modifica la tabla subyacente, por lo que el error permanece silencioso hasta la primera ejecución de la vista o durante un `mysqldump`.

## Cómo funciona

MySQL almacena el texto SQL de la vista en `information_schema.VIEWS` en el momento de su creación, pero no mantiene dependencias rastreadas en tiempo de ejecución. Si una tabla referenciada se renombra o una columna se elimina con `ALTER TABLE ... DROP COLUMN`, la vista sigue existiendo en el catálogo sin ninguna señal de error.

```sql
-- Verificación rápida del estado de las vistas en la base de datos actual
SELECT table_name, is_updatable
FROM information_schema.VIEWS
WHERE table_schema = DATABASE();

-- El acceso a la vista expone la invalidez
SELECT * FROM nombre_vista;
-- ERROR 1356 (HY000): View 'db.nombre_vista' references invalid table(s) or column(s)
```

## Contexto operativo

El problema aparece típicamente en tres escenarios: durante un ciclo de **patching** o migración de esquema, tras un `RENAME TABLE` ejecutado sin actualizar las vistas dependientes, o durante un dump con `mysqldump --routines` que intenta exportar la definición de la vista. En este último caso el dump puede completarse, pero la restauración falla o genera advertencias difíciles de rastrear. Antes de cualquier operación de mantenimiento, la práctica habitual es realizar una verificación sistemática con `CHECK TABLE nombre_vista` o consultando `information_schema`.
