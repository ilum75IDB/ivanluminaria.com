---
title: "Rolling Restart"
description: "Sequential node restart procedure that keeps a cluster service available throughout the operation, applying configuration changes without downtime."
translationKey: "glossary_rolling_restart"
aka: null
articles:
  - "/posts/mysql/articolo-mysql-saturazione-swap-su-innodb-cluster-3-nodi-analisi-e-fix-dei-param"
---

A **rolling restart** is the technique of restarting cluster nodes one at a time, keeping the remaining nodes running so the service stays available to clients throughout the operation. The cluster must maintain quorum at every step to continue handling writes and electing a primary.

## How it works

On a 3-node InnoDB Cluster, the typical sequence is:

1. Identify the node to restart (a secondary is the safest starting point).
2. Confirm the cluster is `ONLINE` and all members are in sync.
3. Restart the node (`systemctl restart mysqld` or equivalent).
4. Wait for the node to rejoin the group before moving to the next one.

```bash
# Check cluster status before each step
mysqlsh -- cluster status
```

The restarted node reconnects to the group via Group Replication and catches up on missed transactions through distributed recovery. Only after its status returns to `ONLINE` should the next node be restarted.

## When to use it

A rolling restart is the standard procedure whenever MySQL configuration parameters in `my.cnf` require a process restart — for example changes to `innodb_buffer_pool_size`, `innodb_log_file_size`, or Group Replication settings. It is also the preferred approach for applying OS patches or minor version upgrades without scheduling a formal maintenance window.

The main constraint is time: if a restarted node has a significant transaction backlog to recover, the distributed recovery phase can take several minutes, stretching the total operational window.
