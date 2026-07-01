---
title: "Rolling Restart"
description: "Procedimiento de reinicio secuencial de nodos de un clúster que mantiene el servicio activo y aplica cambios de configuración sin downtime."
translationKey: "glossary_rolling_restart"
aka: "Reinicio secuencial, reinicio rotativo"
articles:
  - "/posts/mysql/articolo-mysql-saturazione-swap-su-innodb-cluster-3-nodi-analisi-e-fix-dei-param"
---

El **rolling restart** es la técnica que consiste en reiniciar los nodos de un clúster de uno en uno, manteniendo siempre activos los demás para que el servicio permanezca disponible para los clientes durante toda la operación. El clúster debe conservar el quórum en cada paso para seguir gestionando escrituras y elegir un primary.

## Cómo funciona

En un InnoDB Cluster de 3 nodos, la secuencia habitual es:

1. Identificar el nodo a reiniciar (preferiblemente un secondary).
2. Verificar que el clúster esté `ONLINE` y que todos los miembros estén sincronizados.
3. Reiniciar el nodo (`systemctl restart mysqld` o equivalente).
4. Esperar a que el nodo vuelva a unirse al grupo antes de continuar con el siguiente.

```bash
# Verificar el estado del clúster antes de cada paso
mysqlsh -- cluster status
```

El nodo reiniciado se reconecta al grupo mediante Group Replication y recupera las transacciones pendientes a través de distributed recovery. Solo después de confirmar que su estado vuelve a ser `ONLINE` se procede con el siguiente nodo.

## Cuándo se usa

El rolling restart es el procedimiento estándar cuando es necesario aplicar cambios en los parámetros de configuración de MySQL (`my.cnf`) que requieren reiniciar el proceso, como modificaciones en `innodb_buffer_pool_size`, `innodb_log_file_size` o parámetros de Group Replication. También es el método habitual para aplicar parches del sistema operativo o actualizaciones de versión menores sin necesidad de programar una ventana de mantenimiento formal.

La principal limitación es el tiempo: si el nodo reiniciado tiene un backlog de transacciones considerable, la fase de distributed recovery puede prolongarse varios minutos, alargando la ventana operativa total.
