---
description: "PostgreSQL: arquitectura, rendimiento y diseño en uno de los sistemas de bases de datos open source más avanzados y longevos."
layout: "list"
title: "PostgreSQL"
image: "postgresql.cover.jpg"
---

He visto PostgreSQL en producción con `shared_buffers` a 128MB en máquinas con 256GB de RAM — "porque hemos seguido el default". He visto `autovacuum` deshabilitado porque "ralentizaba el sistema", y tres meses después una tabla de 500 millones de filas con el 80% de bloat y consultas que no terminaban nunca. He visto réplicas streaming rotas silenciosamente durante semanas, y nos dimos cuenta solo cuando el master se cayó y el failover no arrancó.

Y he visto exactamente lo contrario: clusters Postgres que aguantan miles de conexiones concurrentes, gestionan terabytes de datos y sobreviven a upgrades mayores sin un minuto de downtime percibido.

La diferencia no está en el código. Está en **quien ha tenido el valor de tocar los defaults en vez de sufrirlos**.

------------------------------------------------------------------------

PostgreSQL no es solo una base de datos open source. Es el resultado de casi cuatro décadas de evolución académica e industrial.

Nacido en 1986 en la Universidad de Berkeley como evolución de Ingres, el proyecto POSTGRES introdujo conceptos que en su momento eran vanguardia: **extensibilidad, tipos de datos personalizados, reglas y un modelo relacional avanzado**. En 1996 llegó el soporte SQL y el nombre pasó a PostgreSQL. El mundo, sin embargo, siguió llamándolo simplemente "Postgres". Y está bien así.

Después de veinte años trabajando con él, una cosa he aprendido: PostgreSQL **premia a quien lo estudia y castiga a quien lo deja en defaults**. Es un motor diseñado para ser tuneado, no para ser instalado y olvidado. Las suposiciones del desarrollo las desmonta la realidad de la producción:

- **VACUUM y autovacuum** no son opcionales — son como lavarse los dientes
- **`shared_buffers`** en el default de 128MB es razonable solo en un portátil
- **`work_mem`** mal configurado multiplicado por las conexiones activas te provoca un OOM en el peor momento
- **Las réplicas** necesitan monitoring activo — el streaming se rompe en silencio
- **Las extensiones** pueden cambiar el comportamiento del catálogo y bloquear los upgrades

------------------------------------------------------------------------

## 🔧 Los parámetros que nunca dejo por defecto

Cuando pongo en producción un cluster Postgres, hay cinco parámetros que nunca dejo en su valor de salida. No porque el default esté mal en términos absolutos, sino porque está pensado para correr en cualquier sitio — y "cualquier sitio" no es nunca tu máquina de producción.

| Parámetro | Qué regula | Cómo lo configuro |
|---|---|---|
| **`shared_buffers`** | Caché compartida de Postgres | Típicamente el 25% de la RAM — no más, la caché del filesystem hace el resto |
| **`effective_cache_size`** | Lo que el planner cree que hay en caché | 50-75% de la RAM — no asigna nada, influye en las decisiones del optimizador |
| **`work_mem`** | Memoria para sort y hash por operación | Bajo (4-16MB) si hay muchas conexiones, alto solo para cargas analíticas dedicadas |
| **`autovacuum_*`** | Limpieza automática de dead tuples | Nunca deshabilitado. Eventualmente tuneado (`naptime`, `cost_limit`) para ser más agresivo en tablas calientes |
| **`wal_level` + `max_wal_senders`** | Nivel de detalle WAL, slots para réplicas | `replica` o `logical` según el caso, senders dimensionados sobre las réplicas reales más margen |

Cinco parámetros. Veinte minutos de análisis. Meses de problemas de rendimiento evitados.

------------------------------------------------------------------------

## 📚 De qué hablo aquí

Historias reales y decisiones técnicas sobre PostgreSQL en producción. Arquitectura, VACUUM y bloat, tuning de parámetros, réplica streaming y lógica, estrategias de upgrade, backups con pg_basebackup y WAL archiving, extensiones que sirven de verdad (y las que se podían evitar).

Nada de recetas preempaquetadas. Solo lo que he visto funcionar en entornos reales — postal, banca, administración pública, telco — donde Postgres aguanta miles de instancias en paralelo y no puede permitirse aproximaciones.

------------------------------------------------------------------------

Elegir PostgreSQL no es solo elegir una base de datos open source.

Es elegir un motor diseñado para ser extendido, analizado y comprendido — y aceptar que sin un poco de estudio los defaults no te llevarán muy lejos.
