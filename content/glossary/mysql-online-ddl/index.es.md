---
title: "Online DDL"
description: "Mecanismo MySQL/InnoDB que permite ejecutar operaciones de ALTER TABLE sin bloquear las escrituras concurrentes, con límites precisos según la operación."
translationKey: "glossary_mysql_online_ddl"
aka: "MySQL Online DDL"
articles:
  - "/posts/mysql/enum-mysql-semplifica-o-complica"
---

**Online DDL** es el mecanismo de MySQL y del motor de almacenamiento InnoDB que permite ejecutar muchas operaciones de `ALTER TABLE` sin bloquear las escrituras concurrentes sobre la tabla. Se introdujo en MySQL 5.6 y se amplió progresivamente en las versiones siguientes.

## Cómo funciona

MySQL evalúa automáticamente la operación solicitada y elige entre tres algoritmos: `INSTANT` (modifica solo los metadatos, fracción de segundo), `INPLACE` (modifica la tabla sin copiarla, soporta DML en paralelo), `COPY` (rebuild completo, bloquea las escrituras). El algoritmo usado depende del tipo de ALTER y de la versión de MySQL.

## Para qué sirve

Reducir drásticamente el downtime durante mantenimientos de schema en bases de datos en producción. Operaciones como añadir una columna al final, añadir un índice, modificar un default se han vuelto prácticamente instantáneas. Operaciones más pesadas (cambio de tipo columna, reconstrucción de un índice primario) siguen requiriendo rebuild, pero a menudo con concurrencia preservada.

## Cuándo prestar atención

Online DDL no es gratis: incluso `INPLACE` genera carga significativa en I/O y replication lag. En tablas de cientos de millones de filas, incluso operaciones "online" pueden producir horas de lag en las réplicas. Además, ciertas operaciones (ej. modificar una columna ENUM añadiendo valores en el medio) caen aún en `ALGORITHM=COPY` y bloquean las escrituras. Vale la pena siempre especificar explícitamente `ALGORITHM=INPLACE, LOCK=NONE` para estar seguros del comportamiento, y probar antes en una réplica.
