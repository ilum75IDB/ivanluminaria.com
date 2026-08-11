---
title: "replication_group_members"
description: "MySQL system view listing active nodes in a Group Replication cluster with each member's state and role."
translationKey: "glossary_replication_group_members"
aka: "performance_schema.replication_group_members"
articles:
  - "/posts/mysql/mysql-8-0-patching-gtid-rhel"
---

`replication_group_members` is a view exposed by `performance_schema` that provides a real-time snapshot of the membership in a MySQL Group Replication cluster. Each row represents one node and reports its current state and role within the distributed consensus protocol. On a standalone server or one using traditional replication (asynchronous or semisync), the view returns no rows.

## How it works

The view aggregates information exchanged through the group communication plugin (GCS/Paxos). The main columns are:

| Column | Description |
|---|---|
| `MEMBER_ID` | Node's unique UUID |
| `MEMBER_HOST` / `MEMBER_PORT` | Network coordinates |
| `MEMBER_STATE` | `ONLINE`, `RECOVERING`, `UNREACHABLE`, `ERROR`, `OFFLINE` |
| `MEMBER_ROLE` | `PRIMARY` or `SECONDARY` |

```sql
SELECT MEMBER_HOST, MEMBER_PORT, MEMBER_STATE, MEMBER_ROLE
FROM performance_schema.replication_group_members;
```

A node in `RECOVERING` state is applying transaction backfill received from the donor. `UNREACHABLE` means the other members have lost contact but have not yet expelled the node from the group.

## Operational context

This view is the first checkpoint during maintenance operations on a Group Replication cluster: rolling patching, planned failover, post-restart verification. Before stopping a node, confirm that all members are `ONLINE` and that exactly one `PRIMARY` exists (Single-Primary mode). In Multi-Primary mode, all `ONLINE` nodes show `PRIMARY`.

The view does not replace continuous monitoring: alerting on `UNREACHABLE` or `ERROR` states requires polling it periodically or integrating it with an orchestration layer (ProxySQL, MySQL Router, Orchestrator).
