---
title: "OFA"
description: "OFA (Optimal Flexible Architecture) es la convención de Oracle para organizar los archivos de una instancia con rutas predecibles, portables y fáciles de mantener."
translationKey: "glossary_ofa"
aka: "Optimal Flexible Architecture"
articles:
  - "/posts/oracle/quali-sono-i-files-critici-di-un-db-oracle"
---

OFA (Optimal Flexible Architecture) es la convención de naming y layout de directorios recomendada por Oracle para organizar los archivos de una instancia: datafiles, control files, redo logs, archived logs y backups. No es obligatoria a nivel de motor, pero seguirla hace que el entorno sea predecible para cualquier persona que deba operar en él, incluidas herramientas como DBCA y RMAN.

## Cómo funciona

OFA define una jerarquía de directorios con raíz en un mount point dedicado, típicamente con la forma `/u01/app/oracle/oradata/<DB_NAME>/`. Los archivos se distribuyen en subdirectorios por tipo:

```
/u01/app/oracle/                  # ORACLE_BASE
  product/19.0.0/dbhome_1/        # ORACLE_HOME
  oradata/ORCL/                   # datafiles y control files
  fast_recovery_area/ORCL/        # FRA: archived logs, backups, flashback logs
  admin/ORCL/adump/               # audit trail
```

Los datafiles siguen el patrón `<tablespace_name>_<n>.dbf`, los redo logs siguen `redo<group>_<member>.log`. El naming sistemático permite identificar de un vistazo el rol de cada archivo.

## Cuándo se aplica

OFA es más relevante durante la instalación y el aprovisionamiento: DBCA la aplica por defecto, y RMAN la presupone al configurar los paths de backup. Los entornos que se desvían de OFA tienden a acumular deuda operativa: los scripts de mantenimiento escritos para una instancia no funcionan en otra, y el troubleshooting nocturno se vuelve más lento. En entornos multi-instancia o RAC, respetar OFA es prácticamente indispensable para mantener la operación bajo control.
