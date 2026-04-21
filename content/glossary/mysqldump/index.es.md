---
title: "mysqldump"
description: "Utilidad de backup lógico incluida en cada instalación de MySQL, produce un archivo SQL secuencial para recrear esquema y datos."
translationKey: "glossary_mysqldump"
aka: "MySQL dump"
articles:
  - "/posts/mysql/mysqldump-mysqlpump-mydumper"
  - "/posts/mysql/mysql-pre-upgrade-assessment"
---

**mysqldump** es la utilidad de backup lógico incluida de serie en cada instalación de MySQL y MariaDB. Produce un archivo SQL que contiene todas las instrucciones (CREATE TABLE, INSERT) necesarias para reconstruir completamente el esquema y los datos de una base de datos.

## Cómo funciona

mysqldump se conecta al servidor MySQL y lee las tablas una por una, generando las instrucciones SQL correspondientes como salida. La operación es rigurosamente single-threaded: una tabla tras otra, una fila tras otra. El archivo producido puede comprimirse externamente (gzip, zstd) pero la herramienta en sí no ofrece compresión nativa.

Con la opción `--single-transaction`, el dump ocurre dentro de una transacción con isolation level REPEATABLE READ, que garantiza un snapshot consistente en tablas InnoDB sin adquirir locks sobre las escrituras.

## Para qué sirve

mysqldump es la herramienta estándar para:

- Backup lógico de bases de datos pequeñas y medianas
- Migraciones entre versiones diferentes de MySQL
- Exportación de tablas individuales o bases de datos para transferencia entre entornos
- Creación de dumps legibles e inspeccionables manualmente

## Cuándo se convierte en problema

En bases de datos por encima de 10-15 GB, el dump single-threaded se convierte en un cuello de botella. Una base de datos de 60 GB puede requerir 3-4 horas de dump y otras tantas de restore. La falta de paralelismo es la limitación estructural: no hay forma de acelerar el proceso si no es pasando a herramientas como mydumper.
