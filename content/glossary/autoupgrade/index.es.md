---
title: "AutoUpgrade"
description: "Utilidad Java (autoupgrade.jar) que desde Oracle 21c es la herramienta única para análisis pre-upgrade, correcciones y upgrade de la base de datos. Reemplaza a preupgrade.jar, ya no distribuido."
translationKey: "glossary_autoupgrade"
aka: "AutoUpgrade Utility (autoupgrade.jar)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

AutoUpgrade es la utilidad Java distribuida con Oracle Database que a partir de la 21c se ha convertido en la herramienta única para gestionar todo el ciclo de vida del upgrade: análisis pre-upgrade, corrección automática de los problemas detectados, ejecución del upgrade y fix-up post-upgrade. Reemplaza definitivamente a `preupgrade.jar`, ya no distribuido en las releases recientes.

## Cómo funciona

AutoUpgrade opera en cuatro modos principales, controlados por el parámetro `-mode`:

- **`analyze`** — sólo lectura, produce un informe de compatibilidad sin modificar nada. Es el modo a usar en producción semanas antes de la ventana de upgrade.
- **`fixups`** — aplica las correcciones automáticas a los problemas resolubles sin intervención humana (ej. recompilación de objetos inválidos, eliminación de componentes deprecados).
- **`deploy`** — ejecuta el upgrade completo desde el source al target database.
- **`upgrade`** — ejecuta sólo la fase de upgrade del diccionario, saltando fixups y post-upgrade tasks.

```bash
# Análisis pre-upgrade (sólo lectura, seguro en producción)
java -jar $ORACLE_HOME_21C/rdbms/admin/autoupgrade.jar \
  -preupgrade "target_version=21,dir=/tmp/preupg" -mode analyze

# Upgrade completo desde un config file
java -jar $ORACLE_HOME_21C/rdbms/admin/autoupgrade.jar \
  -config upgrade.cfg -mode deploy
```

## Cuándo se utiliza

En cada escenario de upgrade Oracle desde la versión 12.2 o superior hacia 19c, 21c, 23ai. El caso de uso más común es el modo `analyze` como primer paso de cada proyecto de migración: produce un informe detallado de objetos inválidos, parámetros obsoletos, componentes a eliminar e incompatibilidades aplicativas. El informe debe leerse y discutirse con los desarrolladores aplicativos antes de planificar la ventana de downtime — muchas de las correcciones requieren cambios al código del cliente que no pueden aplicarse durante el fin de semana del cutover.
