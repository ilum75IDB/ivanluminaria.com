---
title: "Oracle"
layout: "list"
date: "2026-03-10T08:03:00+01:00"
description: "Oracle Database: security, performance and architecture on the longest-running and most complex enterprise database on the market."
image: "oracle.cover.jpg"
---

I have seen a DBA shut down a production system with a `DROP TABLESPACE` run on the wrong window. I have seen four-second queries turn into four-hour queries after an upgrade, because someone had touched `optimizer_features_enable` "it was the same anyway". I have seen backups that would not restore, audits disabled "temporarily" for five years, and indexes created by hand on a Friday afternoon in production.

And I have seen the exact opposite: Oracle instances that have been running for twenty years without a minute of unplanned downtime, handling huge workloads and surviving three major upgrades without a scratch.

The difference has never been the version. It has always been **who was running it**.

------------------------------------------------------------------------

I have been working with Oracle since 1996. In nearly thirty years I have seen Oracle 7, 8i, 9i, 10g, 11g, 12c, 19c, 21c, 23ai come and go — along with paradigms, trends, consultants selling the feature of the month as the answer to every problem.

The heart of the engine, though, has stayed the same: **solid, complex, unforgiving to those who do not know it deeply.**

You do not learn Oracle from tutorials. You learn it:

- from **production incidents** at three in the morning, when the manual is of little use and a colleague who has already seen that behaviour is worth more
- from **migrations** where the execution plan changes the day after go-live and nobody understands why
- from **execution plans** that turn pathological after a `DBMS_STATS.GATHER_SCHEMA_STATS` run with default parameters
- from the **`v$`** views that tell the truth even when the application is lying
- from the **tuning packs** that are actually useful, and those you have paid for and will never switch on

------------------------------------------------------------------------

## 🔧 What I look at when I arrive on a new instance

When a customer calls me because "the database is slow" or "something is off", there are five things I look at before touching any parameter. It is not a checklist from a certification course — it is what I have learned to look at after wasting too much time on the wrong places.

| What | Where I look | Why |
|---|---|---|
| **The real workload** | AWR, ASH, `v$active_session_history` | Understand who really burns CPU, I/O and `db time` — often it is not what the customer suspects |
| **What whoever came before me changed** | `v$parameter` with `ismodified`, `dba_hist_parameter` | "Non-standard" parameters are the first sign of past debugging left without documentation |
| **Who does what** | `dba_audit_trail`, `unified_audit_trail`, scheduled jobs | Find the night jobs, the real application connections, the untracked DBA accesses |
| **Data Guard status** | `v$dataguard_stats`, `v$archive_dest_status` | If there is a standby, check it is actually aligned — do not trust the dashboards |
| **Space and growth** | `dba_tablespaces`, `dba_hist_tbspc_space_usage` | Figure out where you are heading before you hit the wall, not after |

Once I have read these five things, I have 70% of the picture. The other questions come afterwards — and they come focused.

------------------------------------------------------------------------

## 📚 What I talk about here

Real stories, concrete numbers and lessons learned on Oracle in production. Architecture, performance, security, migrations, SQL tuning, PL/SQL, storage management and design decisions that separate an installation that works from one that merely survives.

No brochure theory. Just what I have seen work — and what I have seen fail — in real environments: insurance, telco, public administration, banking, pharma.

------------------------------------------------------------------------

With Oracle, knowing the syntax is not enough.

You need to understand how the engine thinks — and have the humility to admit that, sometimes, the engine is right.
