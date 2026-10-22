---
title: "default_pool_size"
description: "Parámetro de PgBouncer que define el número de conexiones reales a PostgreSQL mantenidas por cada par base de datos/usuario, clave para el dimensionamiento del pool."
translationKey: "glossary_default_pool_size"
aka: null
articles:
  - "/posts/postgresql/pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600"
---

`default_pool_size` es un parámetro fundamental en PgBouncer, un pooler de conexiones ligero y de alto rendimiento para PostgreSQL. Este parámetro determina el número máximo de conexiones *reales* que PgBouncer mantiene abiertas hacia el servidor PostgreSQL para cada combinación única de base de datos y usuario. Es el centro para dimensionar correctamente el pool de conexiones y asegurar una gestión eficiente de los recursos.

## Qué hace y cómo funciona

PgBouncer actúa como un intermediario entre las aplicaciones cliente y el servidor PostgreSQL. En lugar de que PostgreSQL abra una nueva conexión para cada solicitud del cliente, PgBouncer mantiene un pool de conexiones preexistentes y las reutiliza. El parámetro `default_pool_size` controla el tamaño de este pool para cada par específico (base de datos, usuario).

Por ejemplo, si `default_pool_size` se establece en `20` y PgBouncer gestiona conexiones para `db1` con `user_a` y `db2` con `user_b`, mantendrá hasta 20 conexiones para `(db1, user_a)` y otras 20 para `(db2, user_b)`. Este mecanismo reduce la sobrecarga de crear y cerrar conexiones, mejorando el rendimiento y la escalabilidad. El parámetro se aplica independientemente del `pool_mode` (Session, Transaction, Statement).

Aquí hay un ejemplo de configuración en `pgbouncer.ini`:

```ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb
anotherdb = host=127.0.0.1 port=5432 dbname=anotherdb

[pgbouncer]
default_pool_size = 20
pool_mode = transaction
```

## Impacto y dimensionamiento

El dimensionamiento correcto de `default_pool_size` es crucial para el rendimiento general del sistema:

*   **Valor demasiado bajo**: Si el número de conexiones disponibles en el pool es insuficiente para las solicitudes concurrentes, los clientes tendrán que esperar a que una conexión se libere. Esto introduce latencia, reduce el rendimiento y puede causar cuellos de botella.
*   **Valor demasiado alto**: Un `default_pool_size` excesivo lleva a PgBouncer a abrir demasiadas conexiones a PostgreSQL. Esto puede sobrecargar el propio servidor de base de datos, consumiendo memoria y CPU para la gestión de conexiones, y potencialmente anulando los beneficios del pooling.

El dimensionamiento óptimo depende de varios factores: la carga de trabajo (número de consultas por segundo, duración de las transacciones), el número de clientes concurrentes, el `pool_mode` utilizado (el pooling de transacciones generalmente permite pools más pequeños y eficientes) y los recursos de hardware del servidor PostgreSQL. Es aconsejable monitorear las estadísticas de PgBouncer (por ejemplo, `SHOW STATS`, `SHOW POOLS`) para observar `waiting_clients` y la utilización del pool, y ajustar el valor según las necesidades reales.
