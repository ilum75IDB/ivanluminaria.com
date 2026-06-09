---
title: "WAL"
description: "Write-Ahead Log — registro secuencial de todos los cambios en una base de datos PostgreSQL, escrito antes que los archivos de datos. Base de durability, crash recovery, replicación física y lógica."
translationKey: "glossary_wal"
aka: "Write-Ahead Log"
articles:
  - "/posts/postgresql/replica-logica-in-postgresql-scenari-d-uso-configurazione-e-monitoraggio"
---

El **WAL** (Write-Ahead Log) es el registro secuencial de todos los cambios aplicados a la base de datos PostgreSQL: cada INSERT, UPDATE, DELETE, DDL se escribe aquí **antes** de que las modificaciones se apliquen a los archivos de datos reales. Es la base de durability, crash recovery, replicación física y replicación lógica.

## Por qué "Write-Ahead"

La regla es: una transacción se considera committed solo cuando su registro WAL ha sido `fsync`-ado a disco. Incluso si el servidor crashea inmediatamente después, el archivo de datos puede ser reconstruido reproduciendo los registros WAL desde el último checkpoint. Esta garantía permite a PostgreSQL tolerar crashes súbitos sin corrupción de la base de datos.

## Estructura en disco

Los registros WAL se agrupan en **segmentos** de 16 MB por defecto (configurable vía `wal_segment_size`) en el directorio `pg_wal/`. Cada segmento tiene un nombre hexadecimal de 24 caracteres (por ejemplo `000000010000000000000042`) que codifica timeline + offset LSN — el **Log Sequence Number**, el identificador monotónico de posición en el WAL.

## Replicación lógica y WAL

La replicación lógica de PostgreSQL **decodifica** los registros WAL (originalmente en formato físico) en cambios lógicos fila por fila (INSERT/UPDATE/DELETE con valores de columna) mediante el plugin `pgoutput`. Es este paso de "logical decoding" lo que permite a los subscribers aplicar las modificaciones sobre tablas incluso con un layout físico diferente (por ejemplo PostgreSQL 13 → 15 con tablespace cambiado). Sin WAL no hay replicación.
