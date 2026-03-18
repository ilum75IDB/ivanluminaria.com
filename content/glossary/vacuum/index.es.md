---
title: "VACUUM"
description: "Comando PostgreSQL que recupera el espacio ocupado por dead tuples, haciéndolo reutilizable para nuevas inserciones sin devolverlo al sistema operativo."
translationKey: "glossary_vacuum"
aka: "PostgreSQL VACUUM"
articles:
  - "/posts/postgresql/vacuum-autovacuum-postgresql"
---

**VACUUM** es el comando PostgreSQL que recupera el espacio ocupado por los dead tuples (filas muertas) y lo pone disponible para nuevas inserciones. No devuelve espacio al sistema operativo, no reorganiza la tabla y no compacta nada — marca las páginas como reescribibles.

## Cómo funciona

`VACUUM tabla` escanea la tabla, identifica los dead tuples que ya no son visibles para ninguna transacción y marca su espacio como reutilizable. Es una operación ligera que no bloquea las escrituras y puede ejecutarse en paralelo con las queries normales. `VACUUM FULL` en cambio reescribe físicamente toda la tabla con un lock exclusivo — para usar muy raramente y solo en emergencias.

## Para qué sirve

Sin VACUUM, las tablas con alto tráfico de UPDATE y DELETE acumulan dead tuples que ocupan espacio en disco y ralentizan los escaneos secuenciales. VACUUM es el mecanismo de limpieza esencial que equilibra el coste del modelo MVCC de PostgreSQL.

## Por qué es crítico

El autovacuum ejecuta VACUUM automáticamente, pero con los valores por defecto de PostgreSQL puede activarse con poca frecuencia en tablas de alto tráfico. En una tabla con 10 millones de filas, el default espera 2 millones de dead tuples antes de actuar — suficiente para degradar visiblemente el rendimiento.
