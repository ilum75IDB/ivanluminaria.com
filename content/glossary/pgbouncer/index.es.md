---
title: "PgBouncer"
description: "Connection pooler ligero para PostgreSQL que reduce el coste de las conexiones manteniendo un pool reducido de conexiones reales compartidas entre múltiples clientes."
translationKey: "glossary_pgbouncer"
aka: "PgBouncer (PostgreSQL Connection Pooler)"
articles:
  - "/posts/postgresql/pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600"
---

PgBouncer es un connection pooler ligero para PostgreSQL, escrito en C con I/O asíncrono. Se sitúa entre los clientes y la base de datos, manteniendo un pool reducido de conexiones reales hacia PostgreSQL y reutilizándolas entre muchos clientes concurrentes, eliminando el coste de fork y autenticación por cada nueva conexión.

## Cómo funciona

PgBouncer intercepta las conexiones entrantes y las mapea sobre un subconjunto de conexiones reales ya abiertas hacia PostgreSQL. Soporta tres modos de pooling:

- **Session pooling**: una conexión real se asigna al cliente durante toda la sesión.
- **Transaction pooling**: la conexión real se devuelve al pool tras cada COMMIT o ROLLBACK. Es el modo más eficiente, pero incompatible con ciertas funcionalidades con estado (prepared statements en el servidor, `SET LOCAL`, advisory locks).
- **Statement pooling**: liberación tras cada instrucción individual. Raramente usado en producción.

La configuración mínima se realiza mediante un archivo `.ini`:

```ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
```

## Cuándo se usa

PgBouncer es adecuado cuando el número de conexiones de cliente supera lo que PostgreSQL puede sostener de forma estable (típicamente más de 200-300 conexiones activas), o cuando cargas de trabajo sin estado como workers o microservicios abren y cierran conexiones con alta frecuencia. No reemplaza una gestión correcta de conexiones en la capa de aplicación, pero atenúa sus efectos bajo carga elevada.

En el modo transaction pooling, parámetros como `server_reset_query` y el manejo de prepared statements requieren atención específica para evitar comportamientos inesperados.
