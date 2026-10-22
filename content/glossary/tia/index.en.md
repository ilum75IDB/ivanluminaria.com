---
title: "TIA (This Is Acceptable)"
description: "TIA stands for 'This Is Acceptable': the implicit tolerance threshold by which a team decides to live with a known issue rather than fix it."
translationKey: "glossary_tia"
aka: "This Is Acceptable"
articles:
  - "/posts/project-management/il-restart-ha-risolto-il-problema-e-ancora-li"
---

TIA — *This Is Acceptable* — is the decision, often unformalized, to accept a defect, a workaround, or an anomalous behavior as part of a system's normal operation. It is not a fix: it is a tolerance threshold that the team, consciously or not, has stopped questioning.

## How it works in practice

A TIA emerges when an issue is reported, partially analyzed, and then filed away with a note like "good enough for now." The weekly restart that clears the problem every Monday morning, the slow query that "only runs at night," the error log that "doesn't affect users" — these are all undeclared TIAs. The risk is that over time they become invisible: part of the de facto infrastructure rather than the designed one.

## When it becomes a problem

An undocumented TIA is technical debt in disguise. When the context shifts — new data volumes, staff turnover, a version upgrade — the accepted behavior stops being acceptable, but no one remembers why it was tolerated in the first place. The lack of traceability turns a reasonable decision into an operational blind spot. Explicitly documenting a TIA (with date, context, and review conditions) is the difference between a deliberate choice and a time bomb.

## Operational notes

If a TIA must exist, it must be written down: an open ticket, a recorded decision, an assigned owner, a review deadline. A TIA without an owner is not a decision — it is a forgotten problem.
