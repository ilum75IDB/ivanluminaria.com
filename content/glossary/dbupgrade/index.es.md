---
title: "dbupgrade"
description: "Utilidad Oracle que actualiza el diccionario de datos del sistema durante un upgrade de versión, sustituyendo al antiguo catupgrd.sql desde la 12c."
translationKey: "glossary_dbupgrade"
aka: "dbupgrade (sucesor de catupgrd.sql)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

`dbupgrade` es el script de shell introducido por Oracle a partir de la versión 12c para reemplazar a `catupgrd.sql`. Su función es llevar el diccionario de datos del sistema al nivel de la nueva versión de Oracle instalada, recompilando los componentes internos y actualizando vistas, paquetes y metadatos del sistema.

## Cómo funciona

El DBA ejecuta `dbupgrade` después de arrancar la base de datos en modo upgrade (`STARTUP UPGRADE`). Internamente orquesta la misma secuencia de scripts SQL que antes ejecutaba `catupgrd.sql` de forma manual, pero con gestión de errores integrada, paralelismo configurable y logs estructurados por componente.

```bash
# Arranque de la base de datos en modo upgrade
sqlplus / as sysdba <<EOF
STARTUP UPGRADE;
EXIT;
EOF

# Ejecución del upgrade del diccionario de datos
cd $ORACLE_HOME/bin
./dbupgrade -n 4 -l /u01/upgrade_logs
```

El parámetro `-n` controla el número de procesos paralelos; `-l` especifica el directorio de logs. Al finalizar, la base de datos se reinicia en modo normal y se ejecuta `utlrp.sql` para recompilar los objetos inválidos.

## Cuándo se utiliza

`dbupgrade` es obligatorio en cualquier upgrade in-place de Oracle o tras restaurar la base de datos sobre un `ORACLE_HOME` de versión superior. Forma parte del flujo de DBUA (Database Upgrade Assistant) y puede invocarse manualmente para upgrades desatendidos o automatizados mediante scripts. En entornos con bases de datos de gran tamaño — como un upgrade de 12c a 21c sobre tablespaces de 12 TB — el grado de paralelismo elegido tiene un impacto directo en la duración total del proceso.
