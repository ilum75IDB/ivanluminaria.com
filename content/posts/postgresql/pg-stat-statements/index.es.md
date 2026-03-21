---
title: "pg_stat_statements: lo primero que instalar en cualquier PostgreSQL"
description: "Un PostgreSQL en producción durante dos años sin pg_stat_statements. Cuando lo activamos, tres queries consumían el 80% de los recursos — cada una se resolvía con un solo índice. Cómo instalar, consultar y leer los resultados de la extensión más importante para la diagnóstica de PostgreSQL."
date: "2026-04-21T10:00:00+01:00"
draft: false
translationKey: "pg_stat_statements"
tags: ["monitoring", "performance", "pg_stat_statements", "diagnostics", "tuning"]
categories: ["postgresql"]
image: "pg-stat-statements.cover.jpg"
---

El ticket decía: "La base de datos va lenta desde hace unos días, pero no sabemos qué query es el problema."

PostgreSQL 15 en producción, un gestional para una empresa manufacturera con unos cuatrocientos usuarios. El servidor tenía 64 GB de RAM, 16 cores, discos NVMe — hardware más que adecuado para la carga. Sin embargo, los tiempos de respuesta de la aplicación habían subido de 200 milisegundos a 2-3 segundos, y la tendencia iba a peor.

Lo primero que le pregunté al DBA fue: "Enséñame la salida de pg_stat_statements."

Silencio. Luego: "No lo tenemos activado."

Dos años de producción. Cuatrocientos usuarios. Ninguna herramienta de diagnóstica de queries instalada. Es como conducir de noche sin faros — mientras la carretera es recta no te das cuenta de nada, pero en la primera curva terminas en la cuneta.

---

## Qué hace pg_stat_statements

{{< glossary term="pg-stat-statements" >}}pg_stat_statements{{< /glossary >}} es una extensión de PostgreSQL — incluida en la distribución oficial pero no activa por defecto — que lleva el registro de las estadísticas de ejecución de todas las queries SQL que pasan por el servidor.

Para cada query, registra:

- Cuántas veces se ejecutó (`calls`)
- Cuánto tiempo total consumió (`total_exec_time`)
- Cuánto tiempo de media por ejecución (`mean_exec_time`)
- Cuántas filas devolvió (`rows`)
- Cuántos bloques leyó de disco (`shared_blks_read`) y de la caché (`shared_blks_hit`)

Las queries se normalizan: los valores literales se reemplazan con `$1`, `$2`, etc. Esto significa que `SELECT * FROM users WHERE id = 42` y `SELECT * FROM users WHERE id = 99` son la misma query para pg_stat_statements. Es exactamente lo que quieres — te interesa el patrón, no los valores individuales.

---

## Instalación: cinco minutos que lo cambian todo

La instalación requiere una modificación en `postgresql.conf` y un reinicio del servicio. No hay forma de evitar el reinicio — la extensión debe cargarse como shared library al arranque del proceso.

```ini
# postgresql.conf
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.max = 10000
pg_stat_statements.track = all
```

El parámetro `pg_stat_statements.max` define cuántas queries distintas se rastrean. El valor por defecto es 5000, pero en bases de datos con muchas queries diferentes conviene subirlo. `pg_stat_statements.track` establecido a `all` rastrea también las queries ejecutadas dentro de funciones PL/pgSQL — sin este parámetro, las queries en stored procedures no se registran.

Después del reinicio:

```sql
CREATE EXTENSION pg_stat_statements;
```

A partir de ese momento, cada query que pasa por el servidor queda registrada. No hace falta tocar la aplicación, no hace falta modificar queries, nada. Es completamente transparente.

¿El overhead? Despreciable. He hecho benchmarks en varios entornos y el impacto está en el rango del 1-2% de CPU adicional. En cualquier base de datos de producción, es un coste que se recupera en el primer problema diagnosticado.

---

## Las tres queries que se comían el servidor

Volvamos al cliente. Después del reinicio con la extensión activa, esperé 24 horas para recoger una muestra representativa de la carga. Luego lancé la query que siempre lanzo primero:

```sql
SELECT
    substring(query, 1, 80) AS query_truncada,
    calls,
    round(total_exec_time::numeric, 2) AS total_time_ms,
    round(mean_exec_time::numeric, 2) AS mean_time_ms,
    rows,
    round((100 * total_exec_time / sum(total_exec_time) OVER ())::numeric, 2) AS porcentaje
FROM pg_stat_statements
WHERE userid != (SELECT usesysid FROM pg_user WHERE usename = 'postgres')
ORDER BY total_exec_time DESC
LIMIT 20;
```

Esta query ordena todas las queries rastreadas por tiempo total consumido y muestra el porcentaje sobre el total. Es el punto de partida — te dice inmediatamente dónde va el tiempo de la base de datos.

El resultado era impresionante:

| # | Query (truncada) | Calls | Total time | Mean time | % |
|---|-----------------|-------|------------|-----------|---|
| 1 | `SELECT o.*, c.name FROM orders o JOIN customers c ON...` | 847.000 | 1.240.000 ms | 1,46 ms | 42% |
| 2 | `SELECT p.*, s.qty FROM products p LEFT JOIN stock s...` | 312.000 | 680.000 ms | 2,18 ms | 23% |
| 3 | `SELECT * FROM audit_log WHERE created_at > $1 AND...` | 28.000 | 440.000 ms | 15,71 ms | 15% |

Tres queries. El 80% del tiempo total de la base de datos.

La primera se ejecutaba 847.000 veces en 24 horas — unas diez veces por segundo. El tiempo medio era bajo (1,46 ms) pero el volumen la convertía en la más costosa en términos absolutos. Faltaba un índice en la columna de join de la tabla `customers`.

La segunda tenía un LEFT JOIN que hacía un sequential scan en la tabla `stock` — 2 millones de filas, cada vez. Un índice en la columna de join llevó el mean_time de 2,18 ms a 0,12 ms.

La tercera era la que más me preocupaba. 15 milisegundos de media en una tabla de auditoría con 50 millones de filas. La query filtraba por `created_at` y `action_type`, pero el índice existente era solo sobre `created_at`. Un índice compuesto `(created_at, action_type)` resolvió el problema.

Tres índices. Veinte minutos de trabajo. El tiempo medio de respuesta de la aplicación bajó de 2,3 segundos a 180 milisegundos.

---

## Las queries diagnósticas que uso siempre

Después de años de uso, tengo un conjunto de queries que lanzo regularmente. Las comparto porque son las que me habría gustado tener cuando empecé con PostgreSQL.

### Top queries por tiempo total

Es la query que mostré antes. Te dice dónde va el tiempo de la base de datos. La uso como primer paso en cualquier sesión diagnóstica.

### Top queries por tiempo medio

```sql
SELECT
    substring(query, 1, 80) AS query_truncada,
    calls,
    round(mean_exec_time::numeric, 2) AS mean_time_ms,
    round(total_exec_time::numeric, 2) AS total_time_ms,
    rows
FROM pg_stat_statements
WHERE calls > 100
ORDER BY mean_exec_time DESC
LIMIT 20;
```

Esta es complementaria a la primera. Encuentra las queries individualmente lentas — las que quizás se ejecutan pocas veces pero cada una tarda segundos. El filtro `calls > 100` evita pescar queries puntuales que no son representativas.

### Queries con más I/O a disco

```sql
SELECT
    substring(query, 1, 80) AS query_truncada,
    calls,
    shared_blks_read AS bloques_disco,
    shared_blks_hit AS bloques_cache,
    round(
        100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0), 2
    ) AS cache_hit_ratio
FROM pg_stat_statements
WHERE shared_blks_read > 1000
ORDER BY shared_blks_read DESC
LIMIT 20;
```

Esta es fundamental para entender qué queries están martilleando el disco. Un `cache_hit_ratio` por debajo del 90% en una query frecuente es una señal de alarma — significa que los datos no caben en `shared_buffers` y cada ejecución va a leer del filesystem.

### Queries con peor ratio filas devueltas / bloques leídos

```sql
SELECT
    substring(query, 1, 80) AS query_truncada,
    calls,
    rows AS filas_devueltas,
    shared_blks_hit + shared_blks_read AS bloques_totales,
    round(rows::numeric / nullif(shared_blks_hit + shared_blks_read, 0), 4) AS eficiencia
FROM pg_stat_statements
WHERE calls > 50
  AND (shared_blks_hit + shared_blks_read) > 0
ORDER BY eficiencia ASC
LIMIT 20;
```

Esta encuentra las queries que leen muchísimos bloques para devolver pocas filas — la señal clásica de un sequential scan donde haría falta un index scan. Una eficiencia cercana a cero en una query frecuente es casi siempre un índice que falta.

---

## Reset de las estadísticas: cuándo y por qué

Las estadísticas de pg_stat_statements son acumulativas desde el último reset. Si el servidor lleva seis meses encendido, estás viendo la media de seis meses — que podría ocultar un problema reciente.

```sql
SELECT pg_stat_statements_reset();
```

¿Cuándo hacer el reset? Depende de la situación:

- **Después de un deploy aplicativo**: las queries cambian, los datos viejos no sirven
- **Después de una intervención de tuning**: quieres ver el efecto de los índices creados, no la media con el "antes"
- **Periódicamente**: algunos equipos hacen un reset semanal o mensual y guardan los datos en una tabla histórica antes del reset

Un enfoque que uso frecuentemente es guardar un snapshot antes del reset:

```sql
CREATE TABLE pgss_snapshot AS
SELECT now() AS snapshot_time, *
FROM pg_stat_statements;

SELECT pg_stat_statements_reset();
```

Así tienes el histórico y las estadísticas frescas.

---

## pg_stat_statements + EXPLAIN: el workflow completo

pg_stat_statements te dice *cuál* query es el problema. EXPLAIN te dice *por qué* es un problema. Usarlos juntos es el workflow diagnóstico más potente que ofrece PostgreSQL.

El proceso que sigo es siempre el mismo:

1. **Identifico las top queries** con pg_stat_statements (por tiempo total, por tiempo medio, o por I/O)
2. **Copio la query normalizada** y reemplazo los `$1`, `$2` con valores reales
3. **Lanzo EXPLAIN (ANALYZE, BUFFERS)** para ver el plan de ejecución
4. **Busco las señales de alarma**: sequential scan en tablas grandes, nested loop con muchas filas, sort en disco
5. **Intervengo**: creo un índice, reescribo la query, actualizo las estadísticas con ANALYZE

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT o.*, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.created_at > '2026-01-01';
```

Lo importante es el ciclo: después de la intervención, haces un reset de pg_stat_statements, esperas unas horas, y verificas que la query haya mejorado realmente en los números reales — no solo en el EXPLAIN.

---

## Por qué no está activo por defecto

Una pregunta que me hacen a menudo: si pg_stat_statements es tan útil, ¿por qué PostgreSQL no lo activa por defecto?

La respuesta es filosófica más que técnica. PostgreSQL tiene una cultura de minimalismo — el core hace la base de datos, todo lo demás es extensión. El overhead de pg_stat_statements es despreciable, pero el proyecto prefiere no imponer nada. Es la misma razón por la que `shared_buffers` tiene un valor por defecto de 128 MB — un valor ridículo para cualquier producción, pero el proyecto no quiere asumir cuánto hardware tienes.

La consecuencia práctica es que toda instalación PostgreSQL debería configurarse explícitamente. Y pg_stat_statements debería ser la primera línea de la checklist post-instalación — antes de afinar shared_buffers, antes de configurar el autovacuum, antes de todo lo demás.

Sin pg_stat_statements estás volando a ciegas. Puedes hacer tuning todo lo que quieras, pero estás adivinando dónde intervenir.

---

## El día después

El día después de crear los tres índices, volví a consultar pg_stat_statements. La distribución de la carga había cambiado completamente. Las tres queries que antes consumían el 80% del tiempo ahora estaban al 12% — y la query más costosa se había convertido en un report que se ejecutaba una vez al día y del que nadie se había quejado nunca.

El DBA me preguntó: "¿Pero por qué nadie nos había dicho que instaláramos esta extensión?"

La respuesta es que pg_stat_statements no es un secreto. Está en la documentación oficial, está en cada tutorial de performance tuning, la recomienda cada DBA PostgreSQL que conozco. Pero si no la instalas, no sabes lo que no sabes. Y si no sabes lo que no sabes, todo parece funcionar — hasta que deja de funcionar.

Cinco minutos de instalación. Veinte minutos de análisis. Tres índices. Una base de datos que pasó de "lenta desde hace unos días" a "la más rápida que hemos tenido" — que en realidad simplemente significa "tan rápida como debería haber sido desde el principio."

------------------------------------------------------------------------

## Glosario

**[pg_stat_statements](/es/glossary/pg-stat-statements/)** — Extensión PostgreSQL que recopila estadísticas de ejecución de todas las queries SQL: tiempos, conteos, filas devueltas y bloques leídos. Herramienta fundamental para la diagnóstica de rendimiento.

**[shared_buffers](/es/glossary/shared-buffers/)** — Área de memoria compartida de PostgreSQL que sirve como caché para los bloques de datos leídos del disco. El parámetro más importante para el tuning de memoria, con un valor por defecto de 128 MB casi siempre inadecuado para producción.

**[Execution Plan](/es/glossary/execution-plan/)** — Secuencia de operaciones (scan, join, sort) que la base de datos elige para resolver una query SQL. Se visualiza con EXPLAIN y EXPLAIN ANALYZE.

**[Sequential Scan](/es/glossary/sequential-scan/)** — Operación de lectura donde PostgreSQL lee todos los bloques de una tabla de principio a fin sin usar índices. Eficiente en tablas pequeñas, problemática en tablas grandes cuando solo se necesita un subconjunto de filas.

**[ANALYZE](/es/glossary/postgresql-analyze/)** — Comando PostgreSQL que recopila estadísticas sobre la distribución de los datos en las tablas, usadas por el optimizer para elegir el plan de ejecución.
