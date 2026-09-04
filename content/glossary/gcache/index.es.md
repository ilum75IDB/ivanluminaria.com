---
title: "gcache"
description: "Buffer circular en disco que cada nodo de Galera Cluster mantiene para almacenar writesets recientes y favorecer IST frente a SST en reinicios breves."
translationKey: "glossary_gcache"
aka: "Galera Cache"
articles:
  - "/posts/mysql/galera-cluster-quorum-split-brain-e-bootstrap-di-emergenza-con-due-nodi-giu"
---

El gcache es un buffer circular en disco que cada nodo de un Galera Cluster mantiene de forma local. Almacena los writesets replicados recientemente y actúa como memoria operativa del proceso de sincronización incremental entre nodos.

## Cómo funciona

Cuando un nodo se reincorpora al cluster tras una ausencia breve, Galera verifica si los writesets faltantes siguen presentes en el gcache del nodo donante. Si es así, se ejecuta una **Incremental State Transfer (IST)**: el donante envía únicamente los writesets ausentes, sin copiar el dataset completo. Si el gcache no cubre el intervalo faltante, el cluster recurre a una **State Snapshot Transfer (SST)**, operación mucho más costosa que transfiere una snapshot completa de la base de datos.

El parámetro clave es `gcache.size`, configurable en `wsrep_provider_options`:

```ini
wsrep_provider_options = "gcache.size=2G"
```

El valor predeterminado es 128 MB, habitualmente insuficiente en entornos con alto volumen de escrituras.

## Contexto operativo

Dimensionar correctamente el gcache es la principal palanca para evitar SST no deseadas. La regla práctica consiste en estimar el volumen de writesets generado durante el período de inactividad previsto (mantenimiento, reinicio, inestabilidad de red) y configurar `gcache.size` por encima de ese umbral. Un gcache demasiado pequeño fuerza SST incluso tras ausencias de pocos minutos; uno demasiado grande ocupa espacio en disco sin beneficio proporcional.

El archivo físico del gcache se encuentra por defecto en `<datadir>/galera.cache` y su tamaño en disco coincide exactamente con el valor configurado, preasignado en el arranque.
