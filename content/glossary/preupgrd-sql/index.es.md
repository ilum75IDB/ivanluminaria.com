---
title: "preupgrd.sql"
description: "Script Oracle de pre-upgrade que se ejecuta en la instancia origen: detecta objetos inválidos, parámetros obsoletos e incompatibilidades antes del cutover."
translationKey: "glossary_preupgrd_sql"
aka: "Oracle Pre-Upgrade Information Tool"
articles:
  - "/posts/oracle/oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback"
---

`preupgrd.sql` es el script de pre-upgrade distribuido con Oracle 19c (y versiones anteriores con nombres similares). Se ejecuta sobre la instancia **origen**, antes de iniciar cualquier procedimiento de migración, y genera un informe textual que refleja el estado de la base de datos frente a los requisitos de la versión de destino.

## Qué hace

El script consulta el diccionario de datos y vistas internas para detectar:

- objetos en estado `INVALID` que podrían bloquear la fase de recompilación post-upgrade
- parámetros de inicialización deprecados o eliminados en la versión destino
- funcionalidades obsoletas aún activas (p. ej., desajustes en `COMPATIBLE`, `DB_BLOCK_SIZE` fuera de rango)
- problemas de timezone, character set y componentes opcionales no migrables de forma automática

La salida se escribe en `$ORACLE_BASE/cfgtoollogs/db_unique_name/preupgrade/` como archivos de texto y, en versiones recientes, como scripts SQL correctivos listos para ejecutar.

```bash
sqlplus / as sysdba @$ORACLE_HOME/rdbms/admin/preupgrd.sql
```

## Cuándo se usa

`preupgrd.sql` debe ejecutarse **semanas antes** del cutover, no la noche de la migración. El DBA analiza el informe para planificar las correcciones: recompilar objetos inválidos, eliminar parámetros obsoletos, actualizar componentes opcionales. En entornos de producción críticos — como bases de datos financieras de 8 TB — el informe se convierte en entrada directa para el plan de ROLLBACK y para estimar la ventana de mantenimiento.

## Notas operativas

Oracle distribuye versiones actualizadas del script con cada PSU/RU. Antes de ejecutarlo, hay que verificar que se usa la copia presente en el `ORACLE_HOME` de la **versión de destino**, no de la origen: ahí reside la lógica de validación actualizada.
