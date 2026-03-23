---
title: "Cutover"
description: "The critical moment in a migration when the production system is definitively moved from the old to the new infrastructure."
translationKey: "glossary_cutover"
articles:
  - "/posts/oracle/oracle-cloud-migration"
---

The **cutover** is the moment when a production system is moved from the old infrastructure to the new one. It's the most visible phase of a migration — the one everyone remembers, for better or worse.

## Anatomy of a cutover

A well-planned cutover follows a detailed runbook with numbered steps, estimated times, success criteria and rollback procedures for each step. Typical components:

1. **Application stop** — closing connections and verifying no sessions are active
2. **Final synchronization** — in a Data Guard migration, verifying transport lag and apply lag are at zero
3. **Switchover/migration** — the technical operation that transfers the service
4. **Validation** — connectivity tests, verification queries, functional tests
5. **Gradual opening** — progressive readmission of users

## Downtime and windows

A cutover's downtime is the time between the last user disconnecting and the first user reconnecting. With Data Guard switchover, downtime can be in the order of minutes. With Data Pump, it can be hours or days.

The cutover window is planned during periods of lowest usage: nights, weekends, holidays. But "lowest usage" doesn't mean "zero usage" — in manufacturing companies with 24/7 shifts, there's no moment when the database isn't needed by someone.

## Rollback

Every cutover must have a rollback plan. With Data Guard, rollback is a second switchover — relatively straightforward. With Data Pump, rollback means restarting the original database and accepting the loss of transactions that occurred after the migration began. The quality of the rollback plan is inversely proportional to the probability of needing it — but woe to those who don't have one.
