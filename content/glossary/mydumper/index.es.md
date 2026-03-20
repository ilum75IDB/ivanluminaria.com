---
title: "mydumper"
description: "Herramienta open source de backup lógico para MySQL/MariaDB con paralelismo real a nivel de chunk, con restore paralelo mediante myloader."
translationKey: "glossary_mydumper"
aka: "myloader"
articles:
  - "/posts/mysql/mysqldump-mysqlpump-mydumper"
---

**mydumper** es una herramienta open source de backup lógico para MySQL y MariaDB que implementa paralelismo real: no solo entre tablas diferentes, sino también dentro de la misma tabla, dividiéndola en chunks basados en la primary key.

## Cómo funciona

mydumper se conecta al servidor MySQL, adquiere un snapshot consistente con `FLUSH TABLES WITH READ LOCK` (o `--trx-consistency-only` para evitar locks globales en InnoDB), luego distribuye el trabajo entre threads múltiples. Cada tabla grande se rompe en chunks — por defecto basados en los rangos de la primary key — y cada chunk se exporta por un thread separado.

La salida no es un único archivo SQL sino un directorio con un archivo por cada tabla (o por cada chunk), más los archivos de metadatos, esquema y stored procedures.

## El restore con myloader

El compañero de mydumper es `myloader`, que carga los archivos en paralelo desactivando los checks de foreign keys y reconstruyendo los índices al final. Este enfoque hace el restore significativamente más rápido comparado con la carga secuencial de un único archivo SQL.

## Cuándo se usa

mydumper es la opción recomendada para bases de datos de producción por encima de 10 GB donde la velocidad de dump y restore es crítica. En una base de datos de 60 GB con 8 threads, un dump que con mysqldump requiere 3-4 horas se completa en 20-25 minutos.
