---
title: "wsrep_cluster_size"
description: "Galera status variable reporting the number of active nodes in the cluster. Dropping below quorum halts writes on all surviving nodes."
translationKey: "glossary_wsrep_cluster_size"
aka: "Galera cluster size status variable"
articles:
  - "/posts/mysql/galera-cluster-quorum-split-brain-e-bootstrap-di-emergenza-con-due-nodi-giu"
---

`wsrep_cluster_size` is a status variable exposed by the wsrep (Galera) plugin that reports how many nodes are currently connected and synchronized in the cluster. It is not a configuration parameter: its value is dynamic and changes in real time as the cluster topology shifts.

## How it works

Read the value with a simple query:

```sql
SHOW STATUS LIKE 'wsrep_cluster_size';
```

In a correctly operating 3-node cluster the expected result is `3`. Galera calculates quorum using the formula `⌊N/2⌋ + 1`: with 3 nodes the minimum quorum is 2. If `wsrep_cluster_size` drops to `1`, the surviving node cannot reach quorum, sets `wsrep_cluster_status` to `non-Primary`, and rejects writes to prevent split-brain.

## Operational context

Checking `wsrep_cluster_size` is the first step when an application reports write errors on a Galera cluster. A value lower than the expected node count does not necessarily signal a critical outage: two out of three nodes still hold quorum and the cluster remains in `Primary` state. The problem arises only when the majority is lost.

In 2-node clusters (a configuration discouraged in production) any single node loss brings `wsrep_cluster_size` to `1` and immediately blocks writes, requiring either a manual bootstrap or an arbitrator node (garbd).

## Notes

`wsrep_cluster_size` reflects the size of the current cluster view (Primary Component), not the total number of configured nodes. A node in `Donor/Desynced` or `Joiner` state may temporarily not appear in the count, or may lower it, during an SST/IST transfer.
