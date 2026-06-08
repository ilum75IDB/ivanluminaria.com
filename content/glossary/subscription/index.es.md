---
title: "Subscription"
description: "Objeto PostgreSQL del subscriber que establece la conexión al publisher y gestiona el ciclo de vida de la replicación lógica: snapshot inicial, streaming, reconexión."
translationKey: "glossary_subscription"
aka: "PostgreSQL Logical Replication Subscription"
articles:
  - "/posts/postgresql/replica-logica-in-postgresql-scenari-d-uso-configurazione-e-monitoraggio"
---

**Subscription** es el objeto que, en el lado **subscriber** (la base de datos destino), establece la conexión al publisher PostgreSQL, especifica la publication a la que suscribirse y gestiona todo el ciclo de vida de la replicación lógica: snapshot inicial de los datos, streaming de las modificaciones incrementales, reconexión automática en caso de interrupción.

## Cómo se crea

Se declara con `CREATE SUBSCRIPTION`, indicando la conexión al publisher y la publication a consumir:

```sql
CREATE SUBSCRIPTION mi_sub
  CONNECTION 'host=pg-primary user=replica_user dbname=app'
  PUBLICATION mi_pub;
```

En el momento de la creación se realiza un snapshot inicial de las tablas, luego comienza el streaming continuo vía WAL.

## Estado y monitorización

La vista `pg_stat_subscription` expone el estado de cada subscription activa: posición actual de aplicación, latencia, último evento recibido. Es el punto de entrada para el troubleshooting de lag o de bloqueos.

## Límites operativos

Una subscription **no puede** ser pausada/reanudada de forma nativa antes de la 14 — se deshabilita con `ALTER SUBSCRIPTION ... DISABLE`. En caso de **conflictos** (fila ya presente en el destino, violación de constraint) el streaming se detiene y debe resolverse manualmente antes de reanudarse.
