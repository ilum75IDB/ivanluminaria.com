---
title: "replication_group_members"
description: "Vista di sistema MySQL che elenca i nodi attivi in un cluster Group Replication con stato e ruolo di ciascun membro."
translationKey: "glossary_replication_group_members"
aka: "performance_schema.replication_group_members"
articles:
  - "/posts/mysql/mysql-8-0-patching-gtid-rhel"
---

`replication_group_members` è una vista esposta da `performance_schema` che fotografa in tempo reale la composizione di un cluster MySQL Group Replication. Ogni riga corrisponde a un nodo del gruppo e riporta il suo stato corrente e il ruolo che ricopre nel consenso distribuito. Su un server standalone o con replica tradizionale (asincrona o semisync) la vista è vuota.

## Come funziona

La vista aggrega le informazioni scambiate tramite il plugin di comunicazione di gruppo (GCS/Paxos). I campi principali sono:

| Colonna | Descrizione |
|---|---|
| `MEMBER_ID` | UUID univoco del nodo |
| `MEMBER_HOST` / `MEMBER_PORT` | Coordinate di rete |
| `MEMBER_STATE` | `ONLINE`, `RECOVERING`, `UNREACHABLE`, `ERROR`, `OFFLINE` |
| `MEMBER_ROLE` | `PRIMARY` o `SECONDARY` |

```sql
SELECT MEMBER_HOST, MEMBER_PORT, MEMBER_STATE, MEMBER_ROLE
FROM performance_schema.replication_group_members;
```

Un nodo in stato `RECOVERING` sta applicando i transaction backfill ricevuti dal donor; `UNREACHABLE` indica che gli altri membri hanno perso il contatto ma non hanno ancora espulso il nodo dal gruppo.

## Contesto operativo

La vista è il primo punto di controllo durante operazioni di manutenzione su un cluster Group Replication: patching rolling, failover pianificato, verifica post-restart. Prima di procedere con lo stop di un nodo è buona norma accertarsi che tutti i membri siano `ONLINE` e che esista un solo `PRIMARY` (in modalità Single-Primary). In modalità Multi-Primary tutti i nodi `ONLINE` mostrano `PRIMARY`.

La vista non sostituisce il monitoraggio continuo: per alerting su `UNREACHABLE` o `ERROR` è necessario interrogarla periodicamente o integrarla con uno strumento di orchestrazione (ProxySQL, MySQL Router, Orchestrator).
