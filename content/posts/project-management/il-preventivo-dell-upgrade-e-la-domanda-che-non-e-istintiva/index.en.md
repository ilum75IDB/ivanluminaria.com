---
categories:
- project-management
date: '2026-10-06'
description: Why upgrading CPU, RAM or IOPS rarely solves a mission-critical database
  slowdown — and what to check before signing the purchase order.
draft: false
image: il-preventivo-dell-upgrade-e-la-domanda-che-non-e-istintiva.cover.jpg
seoTitle: Why adding CPU or RAM rarely fixes a slow database
tags:
- performance-tuning
- database-strategy
- oracle
- data-warehouse
- incident-response
title: More resources, same root cause
translationKey: il_preventivo_dell_upgrade_e_la_domanda_che_non_e_istintiva
webo_generated_at: 2026-09-30
webo_status: scheduled
---

*Why adding CPU, RAM or IOPS rarely fixes a mission-critical database that's slowing down — and what to look at before signing the purchase order.*

---

## The purchase order on the table

There's a moment that repeats itself almost identically across banks, insurance companies, utilities and telcos. A CIO — or a CTO, or a Head of Data Platform — is looking at a quote for an infrastructure upgrade. It might be a new Exadata, a larger PDB on OCI, a migration to a cloud instance with more guaranteed IOPS, or additional RAM on a physical machine that had run out of headroom.

The number in the bottom right corner sits somewhere between a few hundred thousand and a few million euros. The rationale written two pages above sounds reasonable: *the system is struggling, the team says it needs more capacity, the vendor confirms it, SLAs with enterprise clients are about to be breached*. The board wants a quick answer, the CFO wants to know when the signature is coming.

The instinctive reaction, in that moment, is to approve.

It's instinctive for an understandable reason: **adding resources is the easiest decision to explain in twenty seconds to the executive committee**. It's measurable (more gigs, more cores, more IOPS), it's comparable (the vendor sends you the price list), it's traceable (at year-end the CFO knows exactly what was spent). It gives the precise impression of *having done something*.

And in some cases — probably fewer than people think, but not zero — it actually works. If the system was genuinely under-provisioned for the load, more capacity solves it. On paper it's the rational choice.

The problem is what happens in the **other** cases.

## What happens when that wasn't the cause

A database that slows down is, practically always, a symptom. The symptom shows up at a specific point: a nightly query that blows past its window, an analytical batch that takes three times as long, a front-end application that responds slowly during peak hours, a sporadic incident that resolves itself after ten minutes. **The real cause, in a system that has been layered over ten or twenty years, almost always sits one level further back** from where the symptom appears.

It might be an execution plan degraded by a stale statistic. It might be a data model that grew faster than it was designed for — a table that went from 200 million to 2 billion rows with the same indexes from ten years ago. It might be a storage configuration changed six months earlier that moved a file to a slower tier. It might be a new query, introduced by an application that arrived last year, scanning a large table every three minutes without anyone noticing. It might be a RAC configuration that, below a certain concurrency level, triggers cross-cutting wait events that never show up in daily monitoring.

In all these cases, adding resources produces a measurable and temporary effect. The system, with more CPU or more IOPS, manages to mask the bottleneck for weeks, sometimes a couple of months. Then the bottleneck shifts. The degraded plan hasn't changed, the table keeps growing, the poorly designed query keeps running — and in the meantime the load has grown too, as it always does in real systems. The symptom comes back, at a slightly different point, often made worse by the fact that the infrastructure is now more expensive to keep running.

When that happens, the internal conversation becomes a second problem. Because the CIO who just signed that purchase order now has to explain to the board that the problem the upgrade was supposed to fix is back. And the board — legitimately — asks the question the CIO dreads most: *"so what now? Another upgrade?"*

## A case, and the numbers beside it

A concrete example, with sector and order of magnitude (real numbers, anonymised client). A critical analytical batch in a telco context, running Oracle on OCI with Autonomous Database, was taking **four hours** every night. Over the previous three years, the response had been: more CPU, more IOPS, more SGA memory. Each time, the batch dropped by twenty minutes for a few weeks, then crept back to the four-hour mark. A cross-layer analysis — execution plans, historical wait events in AWR, correlation with source table growth, review of the most expensive joins, targeted rewrite of three PL/SQL steps — brought the batch time **under thirty minutes**. The infrastructure resources stayed exactly as they were.

In another context, a Data Warehouse spanning four European countries with over 60,000 lines of PL/SQL, the pattern was similar: the nightly ingestion window was stretching quarter by quarter, and the recurring request was for more machine. After an intervention on the data model, the indexes, and the reorganisation of some staging tables, **the full daily ingestion came back under two hours** — without touching the infrastructure layer.

The point isn't that hardware never helps. The point is that when the real cause lies in the software, the model or the plan, hardware buys time. Time is useful — sometimes it's indispensable to get through to the next maintenance weekend — but it's time, not a solution. And when you buy it believing you've fixed things, the second incident arrives at the worst possible moment, with the question: *"after the first one, what did we actually do?"*

## Line 330 is still there

There's an image I use often, and anyone who started programming forty years ago understands it without explanation. When the Commodore 64 hit an error it displayed a polite message: `?SYNTAX ERROR IN 340`. You'd go and check line 340 — it was perfect. The cause was in line 330 — a semicolon that a few minutes earlier had become a colon. *(I wrote about that experience at length — and how it shaped the work I do today — in [The mad doctor: a Commodore 64, a closed door, and the craft of understanding](/en/posts/project-management/il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire/).)*

For the kids of that era, that experience taught a principle that holds unchanged on enterprise systems today: **the place where the computer complains is almost never the place where the error lives**. Adding hardware at the point where the system complains is the adult equivalent of editing line 340. The program keeps not working, because line 330 is still waiting.

In mission-critical databases the mechanism is the same. Only the scale changes. And the cost of getting it wrong.

## The questions that come before the signature

None of these questions are meant to talk anyone out of signing an upgrade. In some cases, I'll say it again, the upgrade is the right answer and should be done. The questions are there to **decide case by case whether it really is**, before the quote becomes a purchase order.

**1. What changed in the days or weeks before the first symptom appeared?**
A system that has worked for years and is now struggling almost always has a triggering event. A patch, an application release, a recalculated statistic, a table that crossed a size threshold, a storage configuration change, a new module that started calling the database differently. If the timeline of *what changed* hasn't been reconstructed in a credible way, the upgrade is buying time on a cause that's still unknown.

**2. What technical evidence supports the hypothesis that more capacity is needed?**
An AWR with clear evidence that the dominant wait events are CPU-bound or I/O-bound supports an upgrade. An ASH showing sessions blocked on application-level locks, or a degraded execution plan doing a full scan on an indexable table, points somewhere else. The difference is in the data, not in gut feeling.

**3. Who, inside the team or alongside it, is looking at the system as a whole?**
The DBA sees the database, the developer sees the application, the sysadmin sees the infrastructure, the network team sees the network. Each one sees their own piece correctly. The real cause, when it's cross-cutting, lives in the intersection — and none of these roles, by definition, has full visibility across that intersection. The question "who reads the system as a whole?" isn't rhetorical: if the answer is *"nobody in a structured way"*, the upgrade is deciding before anyone has understood.

**4. If the upgrade only worked for three months, what would plan B be?**
This is the question the most experienced CIOs ask last. If the answer is *"we'd do another one"*, the strategy is clear and the risk is worth taking. If the answer is *"we haven't thought about it"*, it's worth pausing for a moment.

## The comparison a CFO understands in thirty seconds

A structured Health Check — five days of cross-layer analysis, a report with timeline, evidence and a prioritised roadmap — costs an order of magnitude less than the average enterprise infrastructure upgrade quote (indicatively €8K for the Health Check versus €300K–€500K for a mid-sized Exadata upgrade — *reference figures TO BE VERIFIED against the client's specific price lists*).

The logic for a CFO is straightforward: **before signing a six-figure spend, an independent second opinion costs a fraction of the quote and reduces the probability of signing twice for the same problem**. It's not a discount on the infrastructure spend — it's insurance that when the signature arrives, it arrives on the right decision.

The value for the CIO is even more direct: it brings a defensible decision to the board. *"We commissioned an independent analysis, we compared its conclusions with the vendor's proposal, and the final choice is consistent with both"* is a sentence that closes the point in three lines of meeting minutes. *"We signed because the vendor recommended it"* opens a different kind of conversation — the one the CIO would rather not be having six months later, if the problem comes back.

## A question to take away

There's no universal principle on infrastructure upgrades. There are contexts where it's the right call and should be made without hesitation; there are others where it's time bought at a high price. The difference doesn't lie in the technology or the vendor. It lies in the quality of the diagnosis that precedes the signature.

If a significant purchase order is on your desk this week, there's one question worth asking before you approve:

*"Does the analysis behind this spend credibly distinguish between the real cause of the slowdown and the point where the slowdown is visible — or is it assuming they're the same thing?"*

If the answer has any hesitation in it, line 330 might still be there.
