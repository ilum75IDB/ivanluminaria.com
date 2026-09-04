---
title: "RMAN Incremental Backup"
description: "Estrategia de backup Oracle RMAN que copia solo los bloques modificados desde el último backup de nivel igual o superior. Level 0 es la base, level 1 es el delta."
translationKey: "glossary_rman_incremental_backup"
aka: "RMAN Incremental Backup (Oracle Recovery Manager)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

El RMAN Incremental Backup copia únicamente los bloques de datos que han cambiado desde el último backup de nivel igual o superior, en lugar de duplicar los datafiles completos. Esto reduce de forma significativa tanto la ventana de backup como el volumen transferido, convirtiéndolo en la herramienta estándar para sincronizar bases de datos de gran tamaño durante migraciones.

## Cómo funciona

El mecanismo se basa en dos niveles:

- **Level 0**: equivale funcionalmente a un backup completo y actúa como base de la cadena incremental. Se copian todos los bloques.
- **Level 1**: copia solo los bloques modificados tras el último backup de level 0 o level 1.

RMAN rastrea los bloques modificados a través del **Change Tracking File** (cuando está habilitado), evitando el escaneo completo de los datafiles en cada ejecución.

```bash
# Backup incremental level 0 (base)
rman target /
BACKUP INCREMENTAL LEVEL 0 DATABASE;

# Backup incremental level 1 (delta)
BACKUP INCREMENTAL LEVEL 1 DATABASE;

# Aplicar el delta a una copia imagen
RECOVER COPY OF DATABASE WITH TAG 'incr_merge';
```

## Cuándo se utiliza

En escenarios de migración — como el paso de Oracle 12c a 21c en una base de datos de 12 TB — el flujo habitual es:

1. Realizar un backup level 0 (o una copia física inicial) en el sistema origen.
2. Aplicar backups level 1 sucesivos para reducir el gap de datos a medida que se acerca la ventana de cutover.
3. En el momento del downtime, aplicar el último incremental y abrir la base de datos de destino.

Este esquema comprime el downtime final a pocos minutos independientemente del tamaño de la base de datos. La principal limitación es la dependencia de la cadena: un backup level 1 no puede aplicarse sin un level 0 válido previo.
