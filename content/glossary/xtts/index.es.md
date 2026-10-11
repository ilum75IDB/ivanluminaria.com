---
title: "XTTS (Cross-Platform Transportable Tablespaces)"
description: "Método Oracle para migrar bases de datos de varios terabytes entre versiones distintas minimizando el downtime mediante backups incrementales RMAN cíclicos."
translationKey: "glossary_xtts"
aka: "Cross-Platform Transportable Tablespaces"
articles:
  - "/posts/oracle/oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback"
---

XTTS (Cross-Platform Transportable Tablespaces) es la técnica Oracle que permite mover tablespaces entre plataformas y versiones de base de datos distintas — por ejemplo de Oracle 11gR2 en Linux x86 a Oracle 19c en OCI — transportando los datafiles directamente en lugar de realizar un export/import lógico. Para bases de datos del orden de los terabytes, este enfoque reduce el downtime del cutover final de días a pocas horas.

## Cómo funciona

El proceso se articula en tres fases diferenciadas:

1. **Backup RMAN level 0** — copia completa de los datafiles de los tablespaces origen, transferida al destino y restaurada.
2. **Incrementales cíclicos (level 1)** — ejecutados varias veces en las semanas previas al cutover, reducen progresivamente el delta entre origen y destino.
3. **Cutover final** — el último incremental se aplica con el tablespace origen en modo read-only; el plug-in en el destino completa la migración.

```bash
# Ejemplo: generación del script RMAN para backup level 0
$ORACLE_HOME/perl/bin/perl xttdriver.pl --backup_to_dest \
  --tablespaces USERS,FINANCE \
  --level 0
```

El script `xttdriver.pl` (disponible en Oracle MOS) orquesta el backup, la conversión de endianness y la transferencia de archivos.

## Cuándo se usa

XTTS es la opción adecuada cuando:

- La base de datos supera varios cientos de GB y un export con Data Pump requeriría ventanas de mantenimiento inaceptables.
- La migración cruza versiones mayores (p. ej. 11g → 19c) o plataformas con endianness diferente.
- El SLA exige un downtime máximo medible en horas, no en días.

La principal limitación es la complejidad operativa: requiere coordinación precisa entre los DBAs de origen y destino, verificación de compatibilidad del character set y gestión separada de los objetos no transportables (secuencias, sinónimos, grants), que deben migrarse de forma independiente mediante Data Pump.
