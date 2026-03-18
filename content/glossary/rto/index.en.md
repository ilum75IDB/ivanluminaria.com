---
title: "RTO"
description: "Recovery Time Objective — the maximum acceptable time to restore a service after a failure or disaster."
translationKey: "glossary_rto"
aka: "Recovery Time Objective"
articles:
  - "/posts/oracle/oracle-data-guard"
---

**RTO** (Recovery Time Objective) is the maximum acceptable time to restore service after a failure or disaster. It is measured from the moment of failure to the moment the system is operational again.

## How it's determined

RTO depends on the recovery strategy and available infrastructure:

| Strategy | Typical RTO |
|----------|------------|
| Restore from tape backup | 4-12 hours |
| Restore from disk backup | 1-4 hours |
| Data Guard with manual switchover | 1-5 minutes |
| Data Guard with Fast-Start Failover | 10-30 seconds |

## RTO vs RPO

- **RTO**: how long it takes to restart (looks forward)
- **RPO**: how much data you can lose (looks backward)

They are independent metrics. A backup restore can have RTO=2 hours and RPO=24 hours. A synchronous Data Guard can have RTO=30 seconds and RPO=0.

## The business impact

RTO has a direct and measurable impact: every minute of downtime translates into blocked operations, unserved customers, lost revenue. The difference between RTO=6 hours and RTO=42 seconds — as in the case of moving from single instance to Data Guard — can be worth more than the cost of the entire infrastructure.
