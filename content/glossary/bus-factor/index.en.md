---
title: "Bus Factor"
description: "Number of team members who, if simultaneously lost, would block the project. A measure of how concentrated critical knowledge is in a few heads."
translationKey: "glossary_bus_factor"
aka: "Truck Factor, Lottery Factor"
articles:
  - "/posts/project-management/team-di-progetto-che-reggono"
---

**Bus Factor** (also known as Truck Factor or Lottery Factor) is an empirical metric that answers the question: *"How many team members have to be simultaneously lost before the project grinds to a halt?"*. The somewhat macabre name comes from the hypothetical scenario of a colleague hit by a bus — but it applies equally to extended leave, illness, resignations, or transfers.

## How to calculate it

There's no exact mathematical formula, just a reasoned estimate starting from a few questions:

- Who is the only person who knows how to configure the production cluster?
- Who is the only person who knows the functional domain of a given area?
- Who wrote the most critical piece of code without documenting it?
- Who maintains the relationship with a key stakeholder on the customer side?

If the answer to each question is "one person", the bus factor is 1 on that competence. The team's bus factor is the minimum across all individual critical-competence bus factors.

## Typical values

- **Bus factor = 1**: critical risk. A single person holds knowledge that would block the project. Common in small teams or "guru-style" work.
- **Bus factor = 2**: fragile. Covered if one person is out, but if both are gone the project stalls.
- **Bus factor ≥ 3**: resilient. Knowledge is distributed enough to absorb multiple absences.

The pragmatic target in real projects is to keep the bus factor ≥ 3 on truly critical competences, accepting lower values on more peripheral areas.

## How to raise the bus factor

Four tools, all low-cost but requiring calendar time:

- **Minimal documentation**: not encyclopedias, but 2-5 page operational runbooks on critical procedures
- **Pair working**: two people on the same activity, alternating between "hands on keyboard" and "observes and asks"
- **Rotation**: whoever has always done X moves to Y this month, and vice versa. Even just for a week
- **Recurring knowledge transfer**: 30 minutes on the calendar every week on a specific topic, recorded

## Signs that the bus factor is low

- When one person goes on leave, the team visibly slows down
- Some activities are systematically assigned to the same person
- A critical procedure has never been documented
- The lead is the only one who knows the "why" of certain architectural choices
