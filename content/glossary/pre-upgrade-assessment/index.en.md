---
title: "Pre-upgrade Assessment"
description: "Structured measurement of a database's size, growth rate, backup times and restore times before an upgrade. Used to size the maintenance window and define a realistic rollback."
translationKey: "glossary_pre_upgrade_assessment"
aka: "Upgrade Readiness Check, Database Sizing & Timing Assessment"
articles:
  - "/posts/mysql/mysql-pre-upgrade-assessment"
---

**Pre-upgrade Assessment** is a technical document, but above all a risk-governance tool. It translates the operational question "can we complete the upgrade within the maintenance window?" into measured numbers, not eyeballed guesses.

## The four fundamental figures

A complete assessment answers four concrete questions:

1. **Current sizes**: how much does each database weigh today, by schema, by table, on real disk vs. `information_schema` estimate
2. **Growth rate**: how fast data grows over time, measured via historicized snapshots and/or binary log volume
3. **Backup times**: how long a full backup takes, measured on every tool that might be used (`mysqldump`, `mydumper`, `xtrabackup`, `pg_dump`, `expdp`…)
4. **Restore times**: how long it takes to rebuild the database from scratch — the most important and most frequently forgotten number

## Why restore times matter more than backup times

Backups run in the background, often outside the maintenance window. Restores instead are inside the window, inside the rollback plan, inside the service-restoration SLA. A dataset that backs up in 30 minutes may take 4 hours to logically restore: if the rollback plan doesn't account for it, the window isn't enough.

## When to do it

- Before a **major upgrade** (MySQL 5.7→8.0, Oracle 12c→19c, PostgreSQL 14→16)
- Before an **infrastructure migration** (new storage, new hypervisor, cloud migration)
- Before a **re-platforming** from on-premises to cloud
- As an **annual periodic audit** on production databases, to verify that measured times are still valid after data growth

## What to deliver to the PM

A single table, not thirty slides. Columns: server, current size, estimated growth, backup time, restore time (primary tool), worst-case restore time (mysqldump or equivalent). The PM should be able to attach it to the cutover plan without any rework.
