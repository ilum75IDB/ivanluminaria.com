---
title: "AWR"
description: "Automatic Workload Repository — Oracle Database's built-in diagnostic tool for collecting and analyzing performance statistics."
translationKey: "glossary_awr"
aka: "Automatic Workload Repository"
articles:
  - "/posts/oracle/oracle-awr-ash"
  - "/posts/oracle/oracle-cloud-migration"
---

**AWR** (Automatic Workload Repository) is a built-in Oracle Database component that automatically collects system performance statistics at regular intervals (every 60 minutes by default) and retains them for a configurable period.

## How it works

AWR captures periodic snapshots that include:

- Session statistics and wait events
- SQL metrics (top SQL by execution time, I/O, CPU)
- Memory structure statistics (SGA, PGA)
- I/O statistics by datafile and tablespace

## What it's for

The AWR report is the primary tool for diagnosing performance issues in Oracle. By comparing two snapshots you can identify:

- Queries consuming excessive resources
- Changes in execution plans
- I/O, CPU or memory bottlenecks
- Performance regressions after application deployments

## When to use it

AWR is the first tool to consult when you receive a slowness report. Together with **ASH** (Active Session History), it lets you reconstruct what happened in the database during a specific time window, even after the problem has resolved.
