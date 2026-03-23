---
title: "BYOL"
description: "Bring Your Own License — Oracle program that allows reusing existing on-premises licenses on OCI cloud without additional licensing costs."
translationKey: "glossary_byol"
aka: "Bring Your Own License"
articles:
  - "/posts/oracle/oracle-cloud-migration"
---

**BYOL** (Bring Your Own License) is an Oracle program that allows organizations to transfer software licenses purchased for on-premises infrastructure to Oracle Cloud Infrastructure (OCI), without having to purchase new cloud licenses.

## How it works

When an organization already owns Oracle licenses — typically Enterprise Edition with options like RAC, Data Guard or Partitioning — it can "bring them along" in the migration to OCI. The support contract (Software Update License & Support) is maintained, and the licenses are associated with cloud resources instead of physical servers.

On OCI, each OCPU corresponds to one processor license, with a transparent 1:1 ratio. This makes the calculation predictable and compliant with Oracle licensing policies.

## Why it matters in migrations

BYOL is often the decisive factor in choosing OCI over other cloud providers. On AWS or Azure, Oracle applies different licensing rules: each vCPU counts as half a processor, and options like RAC are either unsupported or require additional licenses. An Oracle audit on a non-OCI cloud can turn an apparent saving into a very significant unexpected cost.

## What it covers

- Oracle Database (all editions)
- Database options (RAC, Data Guard, Partitioning, Advanced Compression, etc.)
- Oracle Middleware and other Oracle products with eligible licenses

BYOL is not automatic: it must be requested and configured when provisioning OCI resources, specifying the existing licenses in the contract.
