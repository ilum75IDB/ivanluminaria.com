---
title: "FLUSH PRIVILEGES"
seoTitle: "FLUSH PRIVILEGES: cuándo es necesario en MySQL y MariaDB"
description: "FLUSH PRIVILEGES recarga en memoria las tablas de privilegios de MySQL y MariaDB. Cuándo es necesario y por qué no hace falta tras GRANT o CREATE USER."
translationKey: "glossary_flush-privileges"
articles:
  - "/posts/mysql/mysql-users-and-hosts"
---

**FLUSH PRIVILEGES** es un comando MySQL/MariaDB que fuerza al servidor a recargar en memoria las tablas de privilegios desde la base de datos `mysql`. Hace inmediatamente efectivos los cambios en los permisos.

## Cómo funciona

MySQL mantiene en memoria una caché de las tablas de grant (`mysql.user`, `mysql.db`, `mysql.tables_priv`). Cuando se usan `CREATE USER` y `GRANT`, MySQL actualiza tanto las tablas como la caché automáticamente. Pero si las tablas de grant se modifican directamente con `INSERT`, `UPDATE` o `DELETE`, la caché no se actualiza. `FLUSH PRIVILEGES` fuerza la recarga de la caché desde las tablas.

## Para qué sirve

El comando es necesario después de: eliminación directa de usuarios de la tabla `mysql.user`, cambios manuales de privilegios vía DML, o después de un `DROP USER` de usuarios anónimos como parte del hardening de seguridad. Sin el FLUSH, los cambios no tienen efecto hasta el próximo reinicio del servidor.

## Cuándo se usa

Después de cualquier modificación directa a las tablas de grant. Si se usan exclusivamente `CREATE USER`, `GRANT`, `REVOKE` y `DROP USER`, el FLUSH no es técnicamente necesario porque estos comandos actualizan la caché automáticamente. Sin embargo, ejecutarlo después de un `DROP USER` de usuarios anónimos es buena práctica para garantizar la consistencia.
