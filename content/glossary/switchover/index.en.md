---
title: "Switchover"
description: "A planned Data Guard operation that reverses the roles between primary and standby without data loss, reversible and controlled."
translationKey: "glossary_switchover"
articles:
  - "/posts/oracle/oracle-cloud-migration"
---

A **switchover** is a planned Oracle Data Guard operation that reverses the roles between the primary and standby databases. The primary becomes the standby, the standby becomes the primary. No data is lost, no transaction fails — it's a clean, controlled transition.

## Switchover vs Failover

The distinction is fundamental:

| | Switchover | Failover |
|---|---|---|
| **When** | Planned (maintenance, migration) | Emergency (primary failure) |
| **Data loss** | Zero | Possible (depends on mode) |
| **Reversibility** | Yes, with another switchover | No, standby becomes primary permanently |
| **Time** | Minutes (typically 1-3) | Seconds to minutes |

## How to execute

With Data Guard Broker, the switchover is a single command:

    DGMGRL> SWITCHOVER TO standby_db;

The broker automatically manages the sequence: stopping redo transport, applying the last redo on the standby, reversing roles, restarting redo transport in the opposite direction.

## Use in migrations

Switchover is the preferred strategy for Oracle cross-site migrations. You configure Data Guard between the source and target environments, let it synchronize, and at cutover time you execute the switchover. If something goes wrong on the new infrastructure, a second switchover brings everything back to the starting point — a safety net that Data Pump cannot offer.
