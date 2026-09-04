---
title: "Primary Component (PC)"
description: "The Primary Component is the subset of Galera nodes that holds the quorum and is allowed to accept writes, preventing split-brain scenarios."
translationKey: "glossary_primary_component"
aka: "PC, quorum partition"
articles:
  - "/posts/mysql/galera-cluster-quorum-split-brain-e-bootstrap-di-emergenza-con-due-nodi-giu"
---

In a Galera cluster, not all nodes are equal at all times: only those forming the **Primary Component** are authorised to process writes. The PC is the subset of nodes that has achieved quorum — a majority of the cluster's total votes — and can therefore continue operating safely. Nodes excluded from the PC enter `non-Primary` state and stop accepting DML statements.

## How it works

Galera uses a membership protocol built on **wsrep** (Write-Set Replication). Each node exchanges heartbeats and votes with the others. When a network partition or a crash isolates a group of nodes, each group independently calculates whether it holds more than half of the total cluster votes.

- The group with **more than half the votes** becomes (or remains) the Primary Component.
- The minority group transitions to `non-Primary` state: client connections receive an error and no writes are accepted.

This mechanism is the main safeguard against **split-brain**: two partitions cannot both believe they are the PC and silently diverge.

## Operational context

The critical edge case is a **two-node cluster**: if one node goes down, the survivor holds exactly 50% of the votes and cannot reach quorum. It enters `non-Primary` state even if it is fully healthy. The standard solution is to add a third node or a lightweight arbitrator (`garbd`) so that one side can always exceed 50%.

In maintenance or emergency bootstrap scenarios, it is possible to manually force PC formation:

```sql
SET GLOBAL wsrep_provider_options='pc.bootstrap=YES';
```

This must be done carefully: if another partition is still active and holds more recent data, promoting the wrong node risks losing committed transactions.
