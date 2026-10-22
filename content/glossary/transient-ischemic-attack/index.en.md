---
title: "Transient Ischemic Attack"
description: "A TIA (Transient Ischemic Attack) is a brief, self-resolving system failure that signals an underlying structural problem, not a clean bill of health."
translationKey: "glossary_transient_ischemic_attack"
aka: "TIA, mini-stroke (system metaphor)"
articles:
  - "/posts/project-management/il-restart-ha-risolto-il-problema-e-ancora-li"
---

In medicine, a Transient Ischemic Attack (TIA) is a short-lived neurological episode that resolves on its own within 24 hours, leaving no detectable permanent damage. In IT project management and systems operations, the term is borrowed as a metaphor for brief, apparently self-healing failures that actually signal an unresolved structural issue beneath the surface.

## The metaphor mechanism

Just as a clinical TIA often precedes a full stroke, a system TIA — a crash fixed by a restart, a timeout that vanished on its own, a latency spike that quietly subsided — is a warning signal, not a resolution. The system recovered, but the root cause is still there. Treating the episode as closed because "it fixed itself" is precisely the reasoning that turns a warning into a full incident.

## Operational context

In IT projects, TIAs surface as:

- nightly application restarts that "fix everything" with no one knowing why
- slow queries that return to normal speed after a connection pool restart
- intermittent message queue errors that disappear before anyone files a ticket

The correct response is not to celebrate recovery, but to open a post-mortem even when the system is back online. An undiagnosed TIA is technical debt with an unknown expiry date.

## Notes

The term is deliberately provocative: using it in a retrospective or incident report shifts the team's focus from "it's back up" to "why did it go down in the first place."
