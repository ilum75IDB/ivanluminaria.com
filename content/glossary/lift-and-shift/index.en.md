---
title: "Lift-and-Shift"
description: "Cloud migration strategy that moves systems without changing their architecture or code, deferring any optimization to the post-migration phase."
translationKey: "glossary_lift_and_shift"
aka: "Rehost migration"
articles:
  - "/posts/oracle/latenza-wan-e-change-control-gxp-il-costo-reale-del-lift-and-shift"
---

Lift-and-shift is a cloud migration approach that replicates the source environment — servers, databases, applications — onto the target platform without altering architecture, configuration, or code. The primary goal is to minimize the validation perimeter and compress time-to-go-live, deliberately accepting that the migrated system will not be optimized for its new context.

## How it works

The source system is reproduced 1:1 on the target platform: VMs are converted or recreated with identical specifications, databases are migrated via backup/restore or replication tooling without schema refactoring, and network dependencies are faithfully reconstructed. In regulated environments (GxP, SOX, PCI-DSS), this approach limits the validation delta because application behavior remains nominally unchanged.

## When it is used

Lift-and-shift is the predominant choice when:

- migration timelines are constrained by contractual or licensing deadlines
- the system is legacy and internal expertise for safe refactoring is unavailable
- IQ/OQ/PQ validation scope must be kept narrow due to budget or schedule constraints

The main limitation is structural: cloud operational costs (compute, storage, networking) remain high because the system does not leverage elasticity, managed services, or cloud-native architectures. WAN latency and change control constraints in GxP environments can amplify these costs significantly, as analyzed in the linked article.
