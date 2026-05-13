---
title: "OID (Object Identifier)"
description: "Identificador numérico interno usado por PostgreSQL para referirse a objetos del sistema (tablas, tipos, funciones). Entero sin signo de 4 bytes."
translationKey: "glossary_postgresql_oid"
aka: "PostgreSQL OID, Object Identifier"
articles:
  - "/posts/postgresql/enum-postgresql-paga-o-pesa"
---

El **OID** (Object Identifier) es un identificador numérico interno que PostgreSQL usa para referirse a objetos del sistema: tablas, tipos de dato, funciones, esquemas, roles. Es un entero sin signo de 4 bytes gestionado por PostgreSQL mismo, distinto de las claves primarias de las tablas de usuario.

## Cómo funciona

Cada objeto del catálogo de sistema (ej. `pg_class` para tablas, `pg_type` para tipos, `pg_enum` para valores ENUM) tiene una columna `oid` que funciona como identificador único. Los OID son asignados automáticamente por el motor y usados como claves en los JOIN entre catálogos del sistema. PostgreSQL expone varias funciones de conversión (`oid::regclass`, `oid::regtype`, etc.) para obtener el nombre legible de un objeto a partir de su OID.

## Para qué sirve

Para identificar cada objeto de la base de datos de forma única y estable a través del dump-restore. Para los tipos ENUM, cada valor declarado en `CREATE TYPE ... AS ENUM` recibe un OID, que se guarda en las filas de la tabla que usa el tipo. Esto permite almacenar el valor en solo 4 bytes manteniendo al mismo tiempo el vínculo con el nombre legible y el orden posicional.

## Cuándo se usa

Raramente de forma directa en las aplicaciones — el OID es un detalle de implementación que la mayoría de las consultas no ve. Se vuelve relevante cuando se analizan los catálogos del sistema (`information_schema`, `pg_catalog`), cuando se escriben herramientas de introspección o monitoring, y cuando se debuggea el comportamiento de tipos complejos como los ENUM o los domains.
