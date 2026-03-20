---
title: "mysqlpump"
description: "Evolución de mysqldump introducida en MySQL 5.7 con paralelismo a nivel de tabla, deprecada por Oracle en MySQL 8.0.34."
translationKey: "glossary_mysqlpump"
aka: "MySQL pump"
articles:
  - "/posts/mysql/mysqldump-mysqlpump-mydumper"
---

**mysqlpump** es la utilidad de backup lógico introducida por Oracle en MySQL 5.7 como evolución de mysqldump. La diferencia principal es el soporte para paralelismo a nivel de tabla y compresión nativa del output (zlib, lz4, zstd).

## Cómo funciona

mysqlpump puede hacer dump de múltiples tablas simultáneamente usando threads paralelos, configurables con `--default-parallelism`. La compresión se aplica directamente durante el dump, sin necesidad de pipes externos hacia gzip. También soporta el dump selectivo de usuarios y cuentas MySQL.

Sin embargo, el paralelismo opera solo a nivel de tabla entera: si una sola tabla es mucho más grande que las demás, un thread se arrastra solo mientras los otros ya han terminado.

## El problema de la consistencia

Con el paralelismo activo, mysqlpump no garantiza consistencia entre tablas diferentes — tablas exportadas por threads diferentes pueden reflejar momentos diferentes en el tiempo. Esta es una limitación crítica para backups de producción en bases de datos relacionales con foreign keys.

## Estado actual

Oracle declaró mysqlpump deprecado en MySQL 8.0.34 y lo eliminó completamente en MySQL 8.4. Para quien busca paralelismo en el backup lógico, mydumper es la alternativa recomendada.
