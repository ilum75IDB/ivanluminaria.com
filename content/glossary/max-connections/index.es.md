---
title: "max_connections"
description: "Parámetro de PostgreSQL que fija el número máximo de conexiones simultáneas. Cada conexión tiene un coste real en memoria y en la planificación del sistema operativo."
translationKey: "glossary_max_connections"
aka: "max_connections (límite de conexiones PostgreSQL)"
articles:
  - "/posts/postgresql/pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600"
---

`max_connections` es el parámetro de `postgresql.conf` que determina cuántas conexiones de cliente puede aceptar PostgreSQL de forma simultánea. No es un límite arbitrario: cada conexión activa lanza un proceso backend dedicado, con un coste fijo en memoria compartida y en la planificación del sistema operativo.

## Cómo funciona

PostgreSQL sigue un modelo de proceso por conexión: cada cliente que se conecta genera un proceso backend independiente mediante fork. `max_connections` establece el techo máximo de esos procesos. Al alcanzar el límite, el servidor rechaza nuevas conexiones con un error explícito.

```sql
-- Consultar el valor actual
SHOW max_connections;

-- Conexiones activas en este momento
SELECT count(*) FROM pg_stat_activity;
```

Modificar el parámetro requiere reiniciar el servidor, ya que determina la asignación inicial de memoria compartida, en particular para las tablas de bloqueos y los buffers por proceso.

## Contexto operativo

Un valor elevado de `max_connections` no es gratuito: cada slot reserva aproximadamente 5–10 MB de memoria compartida aunque la conexión esté inactiva. Con 500 conexiones se habla de varios gigabytes reservados antes de que llegue una sola consulta.

El patrón recomendado es mantener `max_connections` bajo (típicamente 100–200 para cargas OLTP) y delegar el multiplexado a un connection pooler como PgBouncer en modo transaction pooling. De este modo, miles de clientes de aplicación comparten un número reducido de conexiones reales hacia PostgreSQL.

## Notas

Aumentar `max_connections` obliga también a revisar `work_mem` y `shared_buffers`: la memoria disponible se reparte entre todos los procesos backend activos. Subir el límite sin considerar el footprint global puede provocar presión de memoria o, en el peor caso, un OOM del sistema operativo.
