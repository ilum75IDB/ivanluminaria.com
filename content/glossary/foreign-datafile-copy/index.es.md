---
title: "Foreign datafile copy"
description: "Datafile que RMAN materializa en la base de datos de destino a partir de un backset transportable, antes de que las tablespaces sean conectadas mediante plug-in."
translationKey: "glossary_foreign_datafile_copy"
aka: "Foreign Datafile Copy (RMAN cross-platform transportable backup)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

Un *foreign datafile copy* es el datafile que RMAN materializa en la base de datos de destino a partir de un backupset producido con la cláusula `FOR TRANSPORT`, antes de que las tablespaces correspondientes sean conectadas mediante plug-in en la PDB target. Es el objeto intermedio del mecanismo de transportable backup — lo que hace posible aplicar backup incrementales RMAN a datafiles que en el target aún no pertenecen a ninguna tablespace registrada.

## Cómo funciona

El flujo típico es en dos fases. Primero se genera el backupset transportable en el source, habitualmente con la base de datos abierta usando `ALLOW INCONSISTENT`:

```bash
# En el source
rman target /
BACKUP INCREMENTAL LEVEL 0
  FOR TRANSPORT ALLOW INCONSISTENT
  TABLESPACE DATA_01, DATA_02
  FORMAT '/backup/rman/xtts_l0_%U';
```

En el target, el backupset se restaura como *foreign datafile copy* — todavía no es una tablespace, sino un fichero ya posicionado en el sistema de ficheros del CDB target:

```bash
# En el target
RESTORE FOREIGN TABLESPACE DATA_01, DATA_02 TO NEW
  FROM BACKUPSET '/backup/rman/xtts_l0_1_1';
```

Cada incremental sucesivo se aplica al foreign datafile copy con `RECOVER FOREIGN DATAFILECOPY`, enumerando explícitamente las rutas físicas de los ficheros target:

```bash
RECOVER FOREIGN DATAFILECOPY '/u02/oradata/pdb1/data_01.dbf',
                             '/u02/oradata/pdb1/data_02.dbf'
  FROM BACKUPSET '/backup/rman/xtts_l1_2_1';
```

**Límite operativo importante**: cada `RECOVER FOREIGN DATAFILECOPY` acepta un único backupset a la vez. Un script que intente encolar varios backupsets en un único comando falla.

## Cuándo se utiliza

En migraciones vía Transportable Tablespaces (TTS) cross-version combinadas con backup incremental — patrón usado para mover volúmenes del orden de terabytes cuando la ventana de downtime es demasiado ajustada para un Data Pump completo. El foreign datafile copy es la "landing zone" que permite aplicar la cadena de incrementales en el target mientras el source database sigue en escritura, reduciendo el downtime final sólo al último apply del delta más el plug-in de los metadatos.
