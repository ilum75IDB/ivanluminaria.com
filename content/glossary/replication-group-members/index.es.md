---
title: "replication_group_members"
description: "Vista del sistema MySQL que lista los nodos activos en un clúster Group Replication con el estado y rol de cada miembro."
translationKey: "glossary_replication_group_members"
aka: "performance_schema.replication_group_members"
articles:
  - "/posts/mysql/articolo-mysql-patching-mysql-8-0-dal-backup-alla-verifica-passo-per-passo"
---

`replication_group_members` es una vista expuesta por `performance_schema` que ofrece una instantánea en tiempo real de la composición de un clúster MySQL Group Replication. Cada fila corresponde a un nodo del grupo e indica su estado actual y el rol que desempeña dentro del protocolo de consenso distribuido. En un servidor standalone o con replicación tradicional (asíncrona o semisync), la vista no devuelve filas.

## Cómo funciona

La vista agrega la información intercambiada a través del plugin de comunicación de grupo (GCS/Paxos). Las columnas principales son:

| Columna | Descripción |
|---|---|
| `MEMBER_ID` | UUID único del nodo |
| `MEMBER_HOST` / `MEMBER_PORT` | Coordenadas de red |
| `MEMBER_STATE` | `ONLINE`, `RECOVERING`, `UNREACHABLE`, `ERROR`, `OFFLINE` |
| `MEMBER_ROLE` | `PRIMARY` o `SECONDARY` |

```sql
SELECT MEMBER_HOST, MEMBER_PORT, MEMBER_STATE, MEMBER_ROLE
FROM performance_schema.replication_group_members;
```

Un nodo en estado `RECOVERING` está aplicando el backfill de transacciones recibido del donor. `UNREACHABLE` indica que los demás miembros han perdido el contacto, pero aún no han expulsado al nodo del grupo.

## Contexto operativo

Esta vista es el primer punto de control durante operaciones de mantenimiento en un clúster Group Replication: patching en rolling, failover planificado, verificación post-reinicio. Antes de detener un nodo conviene confirmar que todos los miembros estén `ONLINE` y que exista un único `PRIMARY` (modo Single-Primary). En modo Multi-Primary, todos los nodos `ONLINE` muestran `PRIMARY`.

La vista no reemplaza la monitorización continua: para alertas sobre estados `UNREACHABLE` o `ERROR` es necesario consultarla periódicamente o integrarla con una capa de orquestación (ProxySQL, MySQL Router, Orchestrator).
