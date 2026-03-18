---
title: "RPO"
description: "Recovery Point Objective — the maximum amount of data an organisation can afford to lose in a disaster, measured in time."
translationKey: "glossary_rpo"
aka: "Recovery Point Objective"
articles:
  - "/posts/oracle/oracle-data-guard"
---

**RPO** (Recovery Point Objective) is the maximum amount of data an organisation can afford to lose in case of failure or disaster. It is measured in time: an RPO of 1 hour means accepting the loss of at most the last hour of transactions.

## How it's determined

RPO depends on the backup and replication strategy:

| Strategy | Typical RPO |
|----------|------------|
| Nightly tape backup | 12-24 hours |
| Backup + archived logs on remote storage | 1-4 hours |
| Asynchronous Data Guard (MaxPerformance) | A few seconds |
| Synchronous Data Guard (MaxAvailability) | Zero |

## RPO vs RTO

RPO and RTO are complementary but distinct:

- **RPO**: how much data you can lose (looks backward in time)
- **RTO**: how long it takes to restore service (looks forward in time)

An organisation can have RPO=0 (zero data loss) but RTO=4 hours (it takes 4 hours to restart), or vice versa.

## Why it matters

RPO determines the investment needed in replication infrastructure. Going from RPO=24 hours to RPO=0 can cost orders of magnitude more, but the cost must be weighed against the value of lost data — as in the case of six hours of unissued insurance policies.
