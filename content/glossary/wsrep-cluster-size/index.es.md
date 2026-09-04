---
title: "wsrep_cluster_size"
description: "Variable de estado de Galera que indica el número de nodos activos en el clúster. Caer por debajo del quórum bloquea las escrituras en todos los nodos supervivientes."
translationKey: "glossary_wsrep_cluster_size"
aka: "Galera cluster size status variable"
articles:
  - "/posts/mysql/galera-cluster-quorum-split-brain-e-bootstrap-di-emergenza-con-due-nodi-giu"
---

`wsrep_cluster_size` es una variable de estado expuesta por el plugin wsrep (Galera) que indica cuántos nodos están actualmente conectados y sincronizados en el clúster. No es un parámetro de configuración: su valor es dinámico y cambia en tiempo real conforme varía la topología del clúster.

## Cómo funciona

El valor se consulta con una simple query:

```sql
SHOW STATUS LIKE 'wsrep_cluster_size';
```

En un clúster de 3 nodos operando correctamente, el resultado esperado es `3`. Galera calcula el quórum con la fórmula `⌊N/2⌋ + 1`: con 3 nodos el quórum mínimo es 2. Si `wsrep_cluster_size` baja a `1`, el nodo superviviente no alcanza el quórum, establece `wsrep_cluster_status` en `non-Primary` y rechaza las escrituras para evitar el split-brain.

## Contexto operativo

Verificar `wsrep_cluster_size` es el primer paso cuando una aplicación reporta errores de escritura en un clúster Galera. Un valor inferior al total de nodos esperados no indica necesariamente una interrupción crítica: dos de tres nodos mantienen el quórum y el clúster permanece en estado `Primary`. El problema surge únicamente cuando se pierde la mayoría.

En clústeres de 2 nodos (configuración desaconsejada en producción), la pérdida de cualquier nodo lleva `wsrep_cluster_size` a `1` y bloquea las escrituras de inmediato, requiriendo un bootstrap manual o el uso de un nodo árbitro (garbd).

## Notas

`wsrep_cluster_size` refleja el tamaño de la vista actual del clúster (Primary Component), no el número total de nodos configurados. Un nodo en estado `Donor/Desynced` o `Joiner` puede no aparecer temporalmente en el conteo, o reducirlo, durante una transferencia SST/IST.
