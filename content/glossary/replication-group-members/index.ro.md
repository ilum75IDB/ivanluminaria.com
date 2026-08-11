---
title: "replication_group_members"
description: "Vedere de sistem MySQL care listează nodurile active dintr-un cluster Group Replication cu starea și rolul fiecărui membru."
translationKey: "glossary_replication_group_members"
aka: "performance_schema.replication_group_members"
articles:
  - "/posts/mysql/mysql-8-0-patching-gtid-rhel"
---

`replication_group_members` este o vedere expusă de `performance_schema` care oferă o imagine în timp real a compoziției unui cluster MySQL Group Replication. Fiecare rând corespunde unui nod din grup și indică starea sa curentă și rolul pe care îl îndeplinește în protocolul de consens distribuit. Pe un server standalone sau cu replicare tradițională (asincronă sau semisync), vederea nu returnează niciun rând.

## Cum funcționează

Vederea agregă informațiile schimbate prin plugin-ul de comunicare de grup (GCS/Paxos). Coloanele principale sunt:

| Coloană | Descriere |
|---|---|
| `MEMBER_ID` | UUID unic al nodului |
| `MEMBER_HOST` / `MEMBER_PORT` | Coordonate de rețea |
| `MEMBER_STATE` | `ONLINE`, `RECOVERING`, `UNREACHABLE`, `ERROR`, `OFFLINE` |
| `MEMBER_ROLE` | `PRIMARY` sau `SECONDARY` |

```sql
SELECT MEMBER_HOST, MEMBER_PORT, MEMBER_STATE, MEMBER_ROLE
FROM performance_schema.replication_group_members;
```

Un nod în starea `RECOVERING` aplică backfill-ul de tranzacții primit de la donor. `UNREACHABLE` înseamnă că ceilalți membri au pierdut contactul, dar nodul nu a fost încă expulzat din grup.

## Context operațional

Această vedere este primul punct de control în timpul operațiunilor de mentenanță pe un cluster Group Replication: patching în rolling, failover planificat, verificare post-repornire. Înainte de a opri un nod este recomandat să se confirme că toți membrii sunt `ONLINE` și că există un singur `PRIMARY` (modul Single-Primary). În modul Multi-Primary, toate nodurile `ONLINE` afișează `PRIMARY`.

Vederea nu înlocuiește monitorizarea continuă: pentru alerte pe stările `UNREACHABLE` sau `ERROR` este necesară interogarea periodică sau integrarea cu un strat de orchestrare (ProxySQL, MySQL Router, Orchestrator).
