---
title: "Control File"
description: "Archivo binario de Oracle que registra la estructura física del database: rutas de datafiles, redo logs, SCN actual e información de checkpoint. Imprescindible para la fase MOUNT."
translationKey: "glossary_control_file"
aka: null
articles:
  - "/posts/oracle/quali-sono-i-files-critici-di-un-db-oracle"
---

El Control File es un archivo binario de pequeño tamaño que Oracle mantiene actualizado de forma continua. Contiene los metadatos estructurales del database: rutas de los datafiles, rutas de los redo log groups, SCN actual e información de checkpoint. Sin él, la instancia no puede superar la fase de MOUNT.

## Qué registra

Cada vez que Oracle ejecuta un CHECKPOINT o añade un archivo a la estructura del database, el Control File se actualiza de forma síncrona. Los campos principales incluyen:

- **Nombre del database y DBID**
- **Ruta y estado de cada datafile** (online, offline, read-only)
- **Configuración de los redo log groups**
- **SCN de checkpoint** — utilizado durante el recovery para determinar el punto de consistencia
- **Metadatos de backup de RMAN** (cuando se usa Recovery Manager)

## Multiplexación y riesgo de pérdida

Oracle permite — y recomienda — mantener copias idénticas del Control File en rutas físicamente separadas. La configuración se realiza mediante el parámetro `CONTROL_FILES`:

```sql
ALTER SYSTEM SET CONTROL_FILES =
  '/u01/oradata/orcl/control01.ctl',
  '/u02/fast_recovery_area/orcl/control02.ctl'
SCOPE=SPFILE;
```

Todas las copias se escriben en paralelo en cada actualización. Si una copia está corrupta o falta, el database arranca igualmente usando las copias válidas. La pérdida de **todas** las copias sin un backup reciente requiere un recovery manual complejo.

## Contexto operativo

Durante el startup, Oracle lee el Control File en la fase MOUNT para localizar los datafiles antes de abrirlos (fase OPEN). En un entorno Data Guard, el Control File del standby también contiene metadatos de sincronización con el primary. En los backups de RMAN, el Control File (o un Catalog separado) actúa como registro central de todos los backup sets e image copies.
