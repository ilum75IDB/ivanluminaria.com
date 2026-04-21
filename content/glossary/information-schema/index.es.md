---
title: "information_schema"
description: "Esquema de sistema de MySQL/MariaDB en solo lectura que expone metadatos sobre bases de datos, tablas, índices, usuarios y estado del servidor. Base de cualquier assessment y análisis estructural."
translationKey: "glossary_information_schema"
aka: "Information Schema, INFORMATION_SCHEMA"
articles:
  - "/posts/mysql/mysql-pre-upgrade-assessment"
---

**information_schema** es el esquema virtual estándar SQL que MySQL y MariaDB exponen como interfaz de introspección: no contiene datos aplicativos, sino metadatos sobre el estado del servidor (bases de datos presentes, tablas, columnas, índices, usuarios, privilegios, parámetros de sesión).

## Cómo funciona

Las tablas de `information_schema` son vistas sobre los catálogos internos de la base de datos. Las más usadas son:

- `TABLES` — una fila por tabla, con tamaño, tipo de engine, número de filas estimado
- `COLUMNS` — una fila por columna, con tipo de dato, nullability, collation
- `STATISTICS` — una fila por índice y por columna incluida, con cardinalidad estimada
- `SCHEMATA` — una fila por base de datos
- `PROCESSLIST` — sesiones activas (equivalente a `SHOW PROCESSLIST`)
- `INNODB_*` — métricas y estado del engine InnoDB

## Para qué sirve

Es el punto de partida de cualquier assessment: sizing de la base de datos, identificación de las tablas más grandes, auditoría de índices, análisis de tipos de dato, control de collations mixtas. Muchos scripts de monitoreo y herramientas BI leen `information_schema` para construir cuadros de estado.

## Limitaciones a tener en cuenta

Los valores de `data_length`, `index_length` y `table_rows` son **estimaciones** actualizadas periódicamente por InnoDB y dependen del último `ANALYZE TABLE`. En tablas muy volátiles pueden subestimar un 10-15%. Para datos críticos (plan de migración, plan de capacidad) es buena práctica contrastar con el tamaño físico de los ficheros `.ibd` (`du -sh /var/lib/mysql/<schema>/*.ibd`).
