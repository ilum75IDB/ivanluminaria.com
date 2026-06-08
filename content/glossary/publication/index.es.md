---
title: "Publication"
description: "Objeto PostgreSQL de replicación lógica que define el conjunto de tablas (y filas, desde la 15) cuyos cambios se ponen a disposición de los subscribers."
translationKey: "glossary_publication"
aka: "PostgreSQL Logical Replication Publication"
articles:
  - "/posts/postgresql/replica-logica-in-postgresql-scenari-d-uso-configurazione-e-monitoraggio"
---

**Publication** es un objeto de la replicación lógica PostgreSQL que define un conjunto de tablas cuyos cambios se ponen a disposición para la replicación. Reside en el **publisher** (la base de datos origen) y puede ser consumida por uno o más subscribers independientes, cada uno con su propia subscription.

## Cómo se crea

Se declara con `CREATE PUBLICATION` especificando las tablas a incluir. Desde la versión 15 es posible añadir también una cláusula `WHERE` para filtrar las filas replicadas:

```sql
CREATE PUBLICATION mi_pub
  FOR TABLE clientes, pedidos
  WHERE (status = 'active');
```

## Qué no contiene

Una publication transporta cambios **DML** (INSERT, UPDATE, DELETE, TRUNCATE) pero **no DDL**: las modificaciones de esquema (ALTER TABLE, CREATE INDEX) deben aplicarse manualmente en ambos lados de la replicación, o mediante herramientas de orquestación externas. Las **sequences** tampoco se replican por defecto.

## Cuándo se usa

Típicamente en escenarios de migración cross-versión de PostgreSQL, integración CDC hacia un data warehouse, o replicación selectiva de subconjuntos de tablas en nodos de staging. Una misma publication puede alimentar varios subscribers en paralelo, cada uno con su propio ritmo de consumo.
