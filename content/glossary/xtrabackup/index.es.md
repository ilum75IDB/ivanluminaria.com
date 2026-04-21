---
title: "xtrabackup"
description: "Herramienta de backup físico hot para MySQL/MariaDB desarrollada por Percona. Copia los ficheros InnoDB con la base de datos en ejecución, gestionando las transacciones activas mediante el redo log."
translationKey: "glossary_xtrabackup"
aka: "Percona XtraBackup"
articles:
  - "/posts/mysql/mysql-pre-upgrade-assessment"
---

**xtrabackup** es la principal herramienta open source para backup físico hot de MySQL, MariaDB y Percona Server, desarrollada y mantenida por Percona. A diferencia de `mysqldump` y `mydumper` — que producen dumps lógicos — copia directamente los ficheros de datos InnoDB en el sistema de ficheros mientras la base de datos está en ejecución, sin requerir downtime.

## Cómo funciona

El proceso tiene dos fases:

1. **Backup**: `xtrabackup` copia los ficheros `.ibd` de InnoDB y simultáneamente lee el redo log para registrar todas las modificaciones que ocurren durante la copia. El resultado es un conjunto de ficheros de datos + un fichero de redo log que representan un estado *inconsistente* de la base de datos (los ficheros se copiaron en momentos ligeramente distintos) pero *reconstruible*.
2. **Prepare**: antes del restore, `xtrabackup --prepare` ejecuta un crash recovery aplicando el redo log a los ficheros de datos, llevándolos a un estado consistente.

## Cuándo es la mejor opción

En datasets superiores a ~100 GB el tiempo de backup de xtrabackup es típicamente 5-10 veces más rápido que `mysqldump` y 2-4 veces más rápido que `mydumper`, porque salta completamente la regeneración de `INSERT`s. La ventaja es aún más marcada en fase de restore, donde una copia binaria + crash recovery tarda minutos frente a las horas de un restore lógico.

Es la opción obligada cuando la ventana de mantenimiento es estrecha, para snapshots pre-upgrade y para migraciones lift-and-shift hacia nuevos storages.

## Restricciones a tener en cuenta

- Las tablas **MyISAM** se bloquean durante su copia (FLUSH TABLES WITH READ LOCK): en bases de datos con MyISAM residual esto puede causar bloqueos aplicativos de minutos
- El backup requiere acceso directo al sistema de ficheros del servidor MySQL
- El restore requiere aplicar el redo log antes de poder arrancar la instancia (fase `--prepare`)
