---
title: "LRU list"
description: "Estructura de dos zonas de InnoDB que gestiona la expulsión de páginas del buffer pool, protegiendo los datos calientes de los full scan ocasionales."
translationKey: "glossary_lru_list"
aka: "LRU list (young list + old list)"
articles:
  - "/posts/mysql/innodb-buffer-pool-dimensionamento-hit-ratio-e-warm-up-dopo-restart"
---

La LRU list es la estructura de datos con la que InnoDB decide qué páginas mantener en el buffer pool y cuáles descartar cuando la memoria está llena. A diferencia de un LRU clásico de lista única, InnoDB emplea una variante de dos zonas que separa las páginas "calientes" de las recién cargadas, reduciendo el riesgo de que una operación de escaneo masivo expulse datos accedidos con frecuencia.

## Cómo funciona

La lista se divide en dos subzonas contiguas:

- **Young list** (cabeza, ~5/8 de la lista): contiene las páginas accedidas recientemente varias veces. Son las páginas "calientes" que InnoDB intenta mantener en caché el mayor tiempo posible.
- **Old list** (cola, ~3/8 de la lista): punto de entrada para cada página cargada por primera vez desde disco. Una página permanece en la old list durante al menos `innodb_old_blocks_time` milisegundos (valor por defecto: 1000 ms) antes de poder ser promovida a la young list.

Cuando el buffer pool está saturado, InnoDB elimina las páginas desde la cola de la old list (las más "frías"). La promoción de old a young solo ocurre si la página vuelve a ser accedida tras el período de espera configurado.

## Contexto operativo

El mecanismo de dos zonas protege la young list durante los full scan: las páginas leídas secuencialmente entran en la old list pero, si no se vuelven a acceder dentro del timeout, son expulsadas sin desplazar nunca los datos calientes. Esto resulta especialmente relevante en escenarios como:

- informes nocturnos o trabajos ETL que ejecutan `SELECT` sobre tablas grandes
- `mysqldump` o backups lógicos que leen tablas completas
- consultas analíticas ocasionales en instancias OLTP

Los parámetros clave a monitorizar y ajustar son `innodb_old_blocks_pct` (porcentaje reservado para la old list, por defecto 37) e `innodb_old_blocks_time`. Un valor demasiado bajo de `innodb_old_blocks_time` hace ineficaz la protección; uno demasiado alto puede retrasar la promoción de páginas genuinamente calientes.
