---
title: "ZDM"
description: "Zero Downtime Migration — Oracle's tool for automating migrations to OCI by combining Data Guard and Data Pump under an orchestration layer."
translationKey: "glossary_zdm"
aka: "Zero Downtime Migration"
articles:
  - "/posts/oracle/oracle-cloud-migration"
---

**ZDM** (Zero Downtime Migration) is the tool Oracle provides for automating Oracle database migrations to OCI (Oracle Cloud Infrastructure) or to higher-version on-premises databases. The name is somewhat optimistic — downtime isn't zero, but it's minimized.

## How it works

ZDM is essentially an orchestrator that combines existing Oracle technologies under a single automated workflow. It supports two modes:

- **Physical migration** (Data Guard-based): creates a standby of the source database on the target, synchronizes it via redo transport, then performs a switchover. Downtime in the order of minutes.
- **Logical migration** (Data Pump-based): performs logical export and import with incremental synchronization via GoldenGate or Data Pump. More flexible but slower.

## When to use it

ZDM is suited for standard migrations where source and target infrastructure are configured conventionally. The advantage is automation: it reduces the chance of human error in repetitive steps.

## When not to use it

For complex configurations — RAC with cross-engine DB links, non-standard external dependencies, PL/SQL procedures with HTTP calls — ZDM's automation layer can become an obstacle. In these cases, configuring Data Guard manually provides more control over details and the sequence of operations.

## Requirements

ZDM requires a dedicated host (the "ZDM service host") with SSH access to both the source database and the target. The source must be Oracle 11.2.0.4 or higher, and the target can be on OCI or on-premises.
