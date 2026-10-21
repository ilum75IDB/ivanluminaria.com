---
categories:
- oracle
date: '2026-11-10'
description: Migrating the database to cloud and optimizing afterward sounds reasonable.
  In a GxP system, every post-go-live change opens a revalidation cycle. Here's why.
draft: false
image: latenza-wan-e-change-control-gxp-il-costo-reale-del-lift-and-shift.cover.jpg
seoTitle: 'Lift-and-shift and GxP systems: the real cost of phase two'
tags:
- cloud-migration
- database
- gxp-compliance
- change-control
- oracle
- lift-and-shift
title: 'Lift-and-shift now, optimize later: what ''later'' actually costs in a validated
  system'
translationKey: latenza_wan_e_change_control_gxp_il_costo_reale_del_lift_and_shift
webo_generated_at: 2026-10-21
webo_status: scheduled
---

# Lift-and-shift now, optimize later: what «later» actually costs in a validated system

*Why the cheapest moment to rethink your database in a cloud migration is before the move — and what happens when, after go-live, every change must go through GxP change control.*

---

## The business case was sound

The document the investment committee had approved was well put together. A mid-sized pharmaceutical company, three manufacturing sites, a company-owned data center with a hosting contract about to expire and a server fleet that had reached end of support. At the center: an Oracle database of roughly 6 TB running the quality management system, the QC laboratory LIMS, and batch release reporting. The plan was clear — move everything to cloud infrastructure in nine months, lift-and-shift, same version, same application architecture, no rewrites. Optimization and modernization in a second phase, already budgeted for the following year.

The choice had solid logic behind it, and whoever made it hadn't miscalculated the numbers in front of them. The data center contract set the deadline. A full application rewrite would have required a complete system revalidation, with timelines incompatible with that deadline. *«Let's get out of the data center first, then optimize at our own pace»* was, at that table, the most reasonable thing anyone could have said.

Go-live arrived on schedule. The system worked. Six weeks later, the Quality Director asked why the batch release report — previously running in three minutes — was now taking eleven.

## Eleven minutes, and where they come from

The answer wasn't in the database. The LIMS application servers had stayed at one of the manufacturing sites — connected to lab instruments that couldn't be moved — while the database had gone to the cloud. A sensible choice on paper: the application stayed close to the instruments, the database went where it cost less to manage.

The release report, written fifteen years earlier for a LAN, didn't execute one query — it executed hundreds of thousands of them, one per analytical result row, inside an application loop. In the AWR the signature is unmistakable: the *SQL\*Net roundtrips to/from client* statistic extremely high relative to useful *user calls*, with time dominated by the *SQL\*Net message from client* wait event — the database sitting idle, waiting for the client.

The numbers, once laid out, are straightforward:

- roughly **180,000 round-trips** per report execution;
- on LAN, approximately **0.3 ms** latency per round-trip → 54 seconds of network time out of three minutes total;
- between the manufacturing site and the cloud region, approximately **3 ms** → 540 seconds of network alone, nine minutes;
- the remaining work (roughly two minutes) identical before and after.

Three minutes become eleven without a single query getting worse. The database, in the cloud, was actually faster. *(Representative figures for analogous contexts — TO BE VERIFIED before publication: actual site-to-region latency and round-trip count need to be calibrated against a documentable case.)*

Meanwhile the monthly bill had come in 35% above the business case. Instances had been sized to the historical on-premises peak, with margin, because nobody wanted to risk performance degradation in a validated system; storage had been selected at the tier that guaranteed the IOPS of the old array; backups had been replicated with the same retention policy as before, now billed per gigabyte. *(Percentage TO BE VERIFIED.)*

## Why «later» costs more than «before»

Up to this point it's a story anyone who has done a cloud migration will recognize: a chatty application, a latency that was previously invisible, a cautious sizing decision. The sector-specific part arrives when phase two opens.

The database and the LIMS are **validated computerized systems**: they support GxP decisions, and fall under EU GMP Annex 11 and, for products destined for the US market, under 21 CFR Part 11. Every change to a validated system goes through change control, risk assessment, documented testing, and Quality approval. Rewriting the report loop as a set-based query, pushing the calculation to the database side, revising instance sizing — each of these changes, on a live production system, opens a revalidation cycle.

Before the migration, those same changes would have traveled **inside** the migration validation itself — which had to happen regardless. The test package, the protocol, the signatures: all of it was already planned and paid for. After go-live, every intervention becomes its own project, with its own protocol, its own signatures, its own maintenance window negotiated with manufacturing.

That's the point the business case couldn't see. **Phase two was budgeted as technical work. In practice it's validation work**, and its cost is proportional to the number of interventions, not their technical complexity. In this specific case, the phase two estimate grew from four to eleven calendar months once Quality lined up the required changes. *(TO BE VERIFIED.)*

Nobody in this story did poor work. The infrastructure team migrated exactly what they'd been asked to migrate, on time. The application team kept the code unchanged to avoid invalidating the validation. Quality did its job. The weak point was in the phrase itself: *«we'll optimize later»* assumes that later carries the same price tag as before.

## The move and the sealed boxes

Anyone who has moved house at least once knows the phenomenon. The move has a date, and the date commands. In the last two weeks the boxes fill up without choosing: *«I'll take everything, then sort it out in the new place»*. In the new place, the unopened boxes go to the basement. They're still there five years later, and now the basement costs money per square meter.

The moment when choosing costs least is **before** sealing the box — when you already have it in your hands. Afterward, opening it means going down to the basement, moving the others, finding the time. In the cloud the basement bills every month; in a validated system, opening a box also requires someone else's signature.

## Four questions to ask before writing «phase two» into the plan

None of these questions is an argument against lift-and-shift, which often remains the right choice when there's a real deadline. They're meant to help decide **what** to carry as-is and what is worth rethinking while the cost of rethinking it is still the cost of the migration.

**1. Which components are staying outside the cloud, and how much do they talk to the database?**
An application that stays on-site and a database that goes to a region turns every round-trip into WAN latency. Counting round-trips for critical transactions — from the AWR, before the migration — takes an afternoon. Multiplying them by the measured latency between the two sites gives you the time the system will lose, before it loses it.

**2. Was sizing calculated on measured load or on fear of load?**
On old hardware you bought once for five years, and the margin was free after purchase. In the cloud, margin is billed every hour. Sizing to measured load, with an explicit plan to grow, is a different decision from sizing *«like before, with a bit of headroom»*.

**3. Which phase two interventions touch a validated system, and how much does validating them after go-live cost compared to doing it during?**
This is the question that moves the conversation from the technical plan to the economic one. If the answer is *«we'd validate them during the migration anyway»*, phase two costs a fraction of what it will cost on a live production system.

**4. Who signs off on phase two, and with what already-approved budget?**
A phase two without an owner and without a deliberated budget is, in practice, a basement. Naming who is accountable and with what resources — before go-live — is the only way to prevent it from remaining an intention.

## What this article leaves out

Two topics deserve their own article and are deliberately left out here: **Oracle licensing in the cloud** (the vCPU counting rules on hyperscalers shift the business case numbers considerably) and **data residency** for quality and pharmacovigilance data. Anyone who has dealt with these in a GxP migration probably has a piece of this story that's missing here.

## A question worth carrying with you

The next time a migration plan contains the phrase *«optimization in a subsequent phase»*, it's worth asking:

*«How many round-trips does our most critical transaction make — and how much will it cost to change it afterward, compared to changing it now?»*

For those who have already been through a migration with applications left on-premises and the database in the cloud: what was the first sign that «later» was going to cost more than expected?

## Official sources

*Narrative article: Official sources section not required (no commands, syntax, or parameters cited).*

## Glossary
- **[Lift-and-shift](/en/glossary/lift-and-shift/)** — Cloud migration strategy that moves systems to the target infrastructure without architectural changes, preserving the existing application stack and database version.
- **[GxP](/en/glossary/awr/)** — Umbrella term for Good Practice regulations (GMP, GLP, GCP) governing pharmaceutical and life sciences industries; systems supporting GxP decisions are subject to validation requirements.
- **[Validated computerized system](/en/glossary/lift-and-shift/)** — A software or IT system formally verified to consistently perform its intended function within a regulated environment; changes require documented change control and re-qualification.
- **[AWR](/en/glossary/awr/)** (Oracle) — Automatic Workload Repository: periodic snapshots of workload metrics used as the basis for AWR reports and ADDM analysis.
- **[Round-trip](/en/glossary/sql-net-roundtrips-to-from-client/)** (database) — A complete client-server-client exchange: the client sends a request, the server processes it, and the result is returned. In chatty applications, high round-trip counts amplify network latency directly into response time.
