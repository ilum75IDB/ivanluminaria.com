---
title: "Transaction Pooling"
description: "Modo de pooling en el que el backend se asigna al cliente solo durante una transacción, maximizando la reutilización de conexiones reales a la base de datos."
translationKey: "glossary_transaction_pooling"
aka: "Transaction-level pooling"
articles:
  - "/posts/postgresql/pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600"
---

El Transaction Pooling es el modo de pooling más agresivo disponible en herramientas como PgBouncer: una conexión física al backend de PostgreSQL se asigna a un cliente únicamente durante el tiempo necesario para completar una transacción. En cuanto se produce el COMMIT o el ROLLBACK, el backend vuelve al pool y queda disponible para cualquier otro cliente en espera.

## Cómo funciona

Desde el punto de vista del cliente, la conexión parece persistente. Internamente, el pooler detecta los límites de transacción y reasigna el backend físico en cada ciclo. Con 1000 clientes conectados y transacciones de corta duración, pueden bastar entre 20 y 50 conexiones reales hacia PostgreSQL.

El parámetro clave en PgBouncer es `pool_mode = transaction`, configurable de forma global o por base de datos:

```ini
[databases]
mydb = host=127.0.0.1 port=5432 pool_mode=transaction
```

## Cuándo usarlo y sus limitaciones

Es la opción estándar para aplicaciones web con alta concurrencia de conexiones: habitualmente un backend con su propio pool de conexiones situado detrás de PgBouncer, que a su vez conecta con PostgreSQL. Reduce drásticamente el número de procesos backend activos, disminuyendo el consumo de memoria y el overhead de context switching.

Las limitaciones son concretas: cualquier funcionalidad que dependa del estado de sesión en el servidor — prepared statements del lado del servidor, variables de sesión con `SET`, advisory locks, cursores `WITH HOLD` — deja de funcionar correctamente en Transaction Pooling, porque la sesión backend cambia entre transacciones. La solución pasa por usar Session Pooling para esas cargas de trabajo o por deshabilitar las funcionalidades incompatibles en la capa de aplicación.
