---
title: "Tablespace"
description: "Unidad lógica de almacenamiento en Oracle que agrupa uno o más datafiles físicos. Permite organizar, gestionar y optimizar el espacio en disco para tablas, índices y particiones."
translationKey: "glossary_tablespace"
articles:
  - "/posts/oracle/oracle-partitioning"
---

Un **Tablespace** es la unidad lógica de organización del almacenamiento en Oracle Database. Cada tablespace está compuesto por uno o más datafiles físicos en disco, y cada objeto de la base de datos (tabla, índice, partición) reside en un tablespace.

## Cómo funciona

Oracle separa la gestión lógica (tablespace) de la física (datafile). Un DBA puede crear tablespaces dedicados para propósitos diferentes: uno para datos activos, uno para índices, uno para archivo. Esto permite distribuir la carga de I/O en discos diferentes y aplicar políticas de gestión diferenciadas (ej. read-only para datos históricos).

## Para qué sirve

En el contexto del partitioning, los tablespaces permiten estrategias avanzadas de gestión del ciclo de vida: mover particiones antiguas a tablespaces de archivo económicos, ponerlas en read-only para reducir la carga de backup, y recuperar espacio activo sin eliminar datos. Un `ALTER TABLE MOVE PARTITION ... TABLESPACE ts_archive` es una operación DDL que tarda menos de un segundo.

## Cuándo se usa

Cada instalación Oracle usa tablespaces. El diseño de tablespaces se vuelve crítico cuando se gestionan tablas de cientos de GB con partitioning, porque una buena distribución en tablespaces separados habilita backups incrementales eficientes y gestión del ciclo de vida de los datos.
