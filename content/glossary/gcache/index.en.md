---
title: "gcache"
description: "Circular on-disk buffer used by Galera Cluster to store recent writesets and prefer IST over SST after short node outages."
translationKey: "glossary_gcache"
aka: "Galera Cache"
articles:
  - "/posts/mysql/galera-cluster-quorum-split-brain-e-bootstrap-di-emergenza-con-due-nodi-giu"
---

The gcache is a circular on-disk buffer that every node in a Galera Cluster maintains locally. It holds recently replicated writesets and acts as the operational memory for incremental synchronization between nodes.

## How it works

When a node rejoins the cluster after a short absence, Galera checks whether the missing writesets are still present in the donor node's gcache. If they are, an **Incremental State Transfer (IST)** is performed: the donor sends only the missing writesets, without copying the entire dataset. If the gcache does not cover the gap, the cluster falls back to a **State Snapshot Transfer (SST)**, a far more expensive operation that transfers a full database snapshot.

The key parameter is `gcache.size`, configurable inside `wsrep_provider_options`:

```ini
wsrep_provider_options = "gcache.size=2G"
```

The default value is 128 MB, which is often insufficient in write-heavy environments.

## Operational context

Sizing the gcache correctly is the primary lever to avoid unwanted SST operations. The practical rule is to estimate the writeset volume produced during the expected downtime window (maintenance, restart, network instability) and set `gcache.size` above that threshold. A gcache that is too small forces SST even after absences of just a few minutes; one that is too large wastes disk space without proportional benefit.

The gcache physical file is located by default at `<datadir>/galera.cache`, and its size on disk matches exactly the configured value, pre-allocated at startup.
