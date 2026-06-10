---
title: "Online Redo Log"
description: "Archivos circulares de Oracle que registran cada cambio en la base de datos antes de escribirlos en los datafiles: base del mecanismo de recovery ante caídas."
translationKey: "glossary_online_redo_log"
aka: "Redo Log, Online Redo Log Files"
articles:
  - "/posts/oracle/quali-sono-i-files-critici-di-un-db-oracle"
---

El Online Redo Log es la estructura que Oracle utiliza para garantizar la durabilidad de las transacciones. Cada modificación — INSERT, UPDATE, DELETE, DDL — genera una **redo entry** que se escribe en el redo log *antes* de aplicarse a los datafiles. Ante un crash, Oracle relee estas entradas para devolver la base de datos a un estado consistente.

## Cómo funciona

Los redo logs se organizan en **grupos** (mínimo dos; tres o más recomendados en producción). Oracle escribe de forma circular: llena el grupo activo, realiza un **log switch** y pasa al siguiente. Cada grupo puede tener varios **miembros** — copias físicas idénticas en discos distintos — para redundancia.

El proceso en segundo plano **LGWR** (Log Writer) vuelca el redo buffer en memoria al log activo en cuatro situaciones: en cada COMMIT, cuando el buffer alcanza el 30% de capacidad, cada 3 segundos, o antes de que **DBWR** escriba los bloques sucios.

```sql
-- Consultar el estado de los grupos de redo log
SELECT group#, members, bytes/1024/1024 AS mb, status
FROM v$log
ORDER BY group#;

-- Consultar los miembros físicos
SELECT group#, member, status
FROM v$logfile
ORDER BY group#;
```

## Contexto operativo

Dimensionar correctamente los grupos de redo log es crítico: grupos demasiado pequeños provocan log switches frecuentes, lo que degrada el rendimiento y aumenta la carga sobre ARCH (el proceso de archivado, cuando la base de datos opera en modo **ARCHIVELOG**). Grupos demasiado grandes alargan los tiempos de recovery.

Un log switch cada 15–30 minutos es un punto de partida habitual. En entornos con alta carga de escritura — cargas masivas, pipelines ETL — los switches más frecuentes son esperables; la respuesta habitual es aumentar el tamaño de los grupos o añadir más grupos.

Si un grupo no puede sobrescribirse porque ARCH aún no ha archivado el log anterior, la base de datos queda bloqueada a la espera. Este es uno de los cuellos de botella más comunes en producción relacionados con la configuración del redo log.
