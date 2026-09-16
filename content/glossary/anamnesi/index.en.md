---
title: "Anamnesis"
description: "Systematic collection of symptoms, recent events, and system configuration as the starting point for diagnosing a technical problem."
translationKey: "glossary_anamnesi"
aka: "System history gathering"
articles:
  - "/posts/project-management/il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire"
---

In medicine, anamnesis is the structured gathering of a patient's clinical history before any diagnosis is attempted. Applied to IT systems, the term describes the same process directed at machines, databases, and applications: systematically collecting observed symptoms, recent changes, configuration details, and operational context before forming any hypothesis about the root cause.

## How it works

A technical anamnesis follows a precise, sequential set of questions:

- **What changed recently?** Deployments, package upgrades, configuration parameter edits, maintenance windows.
- **When did the symptom first appear?** Exact timestamps, correlation with scheduled events (backups, batch jobs, load spikes).
- **Who had access and what did they do?** Access logs, command history, tickets opened in the hours before the incident.
- **What is the current configuration?** Software version, hardware resources, network topology, external dependencies.

Only after gathering this information does it make sense to formulate diagnostic hypotheses. Skipping this step almost always leads to chasing the wrong cause.

## When to use it

Anamnesis is the first step whenever a problem is not immediately reproducible or its cause is not obvious: sudden slowdowns, intermittent errors, anomalous behavior following an update. It is especially critical in production environments, where diagnosis time has a direct cost, and in legacy systems where documentation is sparse and institutional knowledge is spread across multiple people.

A thorough anamnesis reduces the risk of applying fixes that address the symptom without touching the root cause.
