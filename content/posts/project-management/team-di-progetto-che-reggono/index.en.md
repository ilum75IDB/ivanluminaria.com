---
title: "5 rules I've seen work in project teams that hold"
description: "A PM who kept a spreadsheet of bathroom-break minutes, and another one who filtered the noise and let the team work. Five rules observed from both sides of the table — as a consultant and as a lead — that keep showing up in project teams that hold under pressure."
date: "2026-05-19T08:03:00+01:00"
draft: false
translationKey: "team_di_progetto_che_reggono"
tags: ["project-management", "team", "leadership", "psychological-safety", "knowledge-transfer", "micromanagement"]
categories: ["Project Management"]
image: "team-di-progetto-che-reggono.cover.jpg"
---

Over fifteen years ago I had a PM who kept an Excel sheet with the minutes each of us spent in the bathroom. I'm not making this up. A shared sheet, updated by hand, with columns for date, name, time left, time back, duration. He'd show it at the weekly status meeting, as a comment on project progress — as if the minutes away from the desk explained anything about the delays.

The outcome was predictable. Mornings the team came in silent, footsteps in the corridor got quick and furtive, people staggered their breaks so they wouldn't overlap with a colleague at the restroom. Two people quit within six months. The project shipped — but in the following months half the team was rotating, and every new hire had to be trained from scratch.

I'm not telling this story to moralize. I'm telling it because it's useful to set against another, more recent one. A PM on a project at an Italian commercial bank who, when escalation emails started pouring in from upstairs, read them himself, translated them into a single technical question for us, and spared the team the whirlwind. At year's end that team had produced twice the work with half the meetings.

The rules I'll list here aren't my ten commandments as an enlightened PM. They're patterns I've seen recur across thirty years of projects — first sitting on the other side of the table as a consultant, then with the lead's hat on. There are five of them, they're simple, and when they're in place they make the difference between a team that holds under pressure and a team that falls apart at the first turn.

## 1️⃣ Give people permission to say "I don't know"

In a team, silence is almost never concentration. It's fear of being wrong. Fear that saying "I don't know" is equivalent to declaring you aren't up to the role, the salary, the expectations. So people bluff. They accept tasks they don't know how to tackle, spend days on them without asking, and the problem surfaces when there's no margin left to solve it.

On a project for a mobile telco operator, a few years back, a senior developer had been stuck for three weeks on an LDAP configuration he'd never touched before. Status meetings, stakeholder emails, rescheduling — and nobody knew the block was right there. Until a new PM, who joined mid-project, opened the retro with a blunt question: *"Who has something they're stuck on and can't unblock?"*. The senior raised his hand and said *"this LDAP thing, I've never really done it, I'm flailing"*. A colleague from another team, in the room by chance, said *"come over, I'll show you in half an hour"*. Forty-five minutes later the block was gone.

Three weeks versus forty-five minutes. The difference wasn't technical competence: the know-how was there, inside the company, two rooms away. The difference was the possibility of admitting you didn't know. When that permission is missing, the team pays the price of bluffing. When it's there, information circulates and blockers last minutes instead of weeks.

The technical term is {{< glossary term="psychological-safety" >}}Psychological Safety{{< /glossary >}}. It doesn't mean a soft climate where nobody ever critiques: it means a climate where you can admit not knowing without consequences to your professional standing. It's the prerequisite for everything else.

## 2️⃣ Shield the team from noise

A PM must not be a meeting multiplier. They must be a filter. In any project of a certain size there's a constant stream of requests coming from outside the team: stakeholders asking for a status update every day, directors wanting "a quick sync" every morning, vendors sending escalation emails to half the company, sales asking for slides for a meeting "to prepare by tomorrow".

If all of this reaches the team directly, the team stops working. They start working on responding to external {{< glossary term="micromanagement" >}}micromanagement{{< /glossary >}}, which is the same mechanism as the PM timing bathroom breaks — just delegated to miscellaneous stakeholders.

On the bank project I mentioned at the start, the PM had found an almost craftsman-like balance: status requests he intercepted himself, answering with a weekly A4 report he sent out Monday morning to all concerned parties, and he managed to stop 90% of ad-hoc requests at the source. What reached the team, filtered, was only the one technical question that genuinely needed deeper work. The outcome: the team got back eight hours of meeting slots per week. Eight hours per person, times seven people, add up to over one person-month of work recovered every month.

Shielding doesn't mean walling the team off or deflecting everything. It means distinguishing noise from signal — and signal is recognizable because it carries new information or real decisions, not because it arrives tagged "urgent".

## 3️⃣ Put people where they perform, not where they're needed

The antipattern is common: *"we need someone to do X, let's grab whoever on the team has the most calendar time"*. But having free time doesn't automatically make that person the right one. Often someone who "would be needed" on X is someone who would perform far better on Y, with X better covered by someone else.

On a project for an Italian Public Administration entity, a colleague had been assigned to handle the user-ticketing frontline. Technically skilled, well-prepared, but she struggled with direct contact with frustrated users; she went home drained every evening. Her output was good but never excellent. After three months the lead stepped back, looked at the team's real skills and interests, and reassigned her to data analysis — where she turned out to be very strong, producing reports nobody had been able to build before. The frontline was covered by a junior who'd been on something completely different until then: that direct contact was training him, growing him, making him feel useful.

The outcome: two people who were previously performing at 60% were now at 100%, and the project benefited without any new hires. The rule isn't "reassign everyone", it's subtler: take stock every few months, talk to people, observe where they spend energy and where they gain it. A good PM redistributes based on observation, not based on the initial org chart.

## 4️⃣ Circulate knowledge, not people

The first question a PM should ask themselves is: *"If the team lost one person tomorrow, how long would the project stall?"*. The answer — measured in days, not comforting words — is called {{< glossary term="bus-factor" >}}bus factor{{< /glossary >}}. A bus factor of 1 means critical knowledge sits in a single head, and that head can fall ill, take leave, or change company. A bus factor of 3 means the same knowledge is spread across at least three people on the team.

The tools to raise the bus factor are simple and well known — minimal but up-to-date documentation, pair working on critical activities, periodic rotation of responsibilities — and all three require the PM to put calendar time into it, not just an encouragement email.

On a project at a national postal and logistics operator with around 1,500 MySQL and PostgreSQL production instances, operational pressure was high: whenever a DBA went on leave, the rest of the team suffered because a specific piece of knowledge was missing. We introduced a very simple ritual: every Tuesday at 14:30, a 30-minute {{< glossary term="knowledge-transfer" >}}knowledge transfer{{< /glossary >}} session on a specific topic (a cluster configuration, a recovery procedure, troubleshooting of a specific service), given in rotation by a team member. Sessions recorded, indexed in an internal wiki, searchable.

Six months later, when a DBA went on paternity leave for three months, the colleague covering for him was already operational from day one — he'd never personally touched those systems, but he had attended or watched the recorded KT sessions on the critical procedures. The ritual isn't "every now and then we do a bit of training". The ritual is a half-hour blocked on the calendar, every week, producing a shared team asset. It's one of the highest cost-benefit practices I've seen applied on a project.

## 5️⃣ Recognize the work, not just the results

Project results depend on variables the team often doesn't control: customer decisions, scope changes, vendor delays, regulatory constraints that land mid-track. The work, on the other hand, is under the team's control. The work is what went into the day: hours of analysis, hours of coding, hours of discussion, hours of testing.

If a PM only recognizes results, when results slip for external reasons people get demotivated. They worked well, maybe worked a lot, and they hear *"the go-live slipped anyway"*. Next time they'll work less, because they've learned that their effort doesn't count when the external outcome doesn't arrive. The technical term is the distinction between {{< glossary term="outcome-vs-output" >}}outcome and output{{< /glossary >}}: output is what the team produced, outcome is the final result measured by the business.

On a multi-country insurance project, the team had completed the development of a new commissions-management module on time and at the expected quality. Then, due to business decisions affecting another part of the system, the go-live slipped by three months and the commissions module sat in waiting. The project lead called the team into a fifteen-minute meeting and said, very precisely: *"You delivered what you were supposed to deliver, on time and at the quality we agreed on. The go-live depends on factors that aren't in your hands. Thank you for the work."*. Then she listed, one by one, the toughest pieces of work the team had tackled in the previous months — three or four specific, concrete sentences.

It may sound small. It was huge. That team kept its pace through the three months of waiting, and when the go-live did happen it went well. The rule isn't "hand out medals". The rule is to distinguish what the team did well (output) from what the business decided (outcome), and to explicitly recognize the former when the latter doesn't arrive.

## 🧭 The PM as custodian of the conditions

One summer many years ago, in Rome, with one of those heatwaves that nail you to the asphalt, I decided to go to the office in bermuda shorts. I knew perfectly well it wasn't the most appropriate outfit for a professional setting, but the heat was really off the charts. As I walked in, in the corridor, I ran into my manager. He looked me up and down and, smiling, said: *"Off to the beach today?"*. And I, on instinct, tapped my temple with my index finger and said: *"Do you pay me for how I dress or for what's in here?"*. He burst out laughing, gave me a pat on the shoulder, and kept walking toward his office. From that day on we went on having an excellent professional relationship, even though our paths later took us in different directions.

That pat on the shoulder is an image that stuck with me. In another context — that of the bathroom-minutes spreadsheet — the same scene would have ended in a formal HR report and a note in the annual review. The manager who chose to laugh that morning had understood something simple: a person's value on a project doesn't live in bermuda shorts or in a suit, it lives in the ideas they produce and the work they make flow. That choice — to laugh instead of to sanction — is exactly the custodian-of-the-conditions craft.

These five rules aren't a commandment list for a commanding PM. They're observations on what happens when certain conditions are in place and when they're missing. Underneath all of them runs a common thread: the PM isn't the general leading the troops, they're more like the custodian of the conditions. Their job is to make sure every person on the team has the permission, the space and the tools to do their own work well.

The success of a project belongs to the team that produced it, not to the PM. And responsibility for failures belongs to the PM more than to the team, because the conditions were under their control. This reversal — which sounds counterintuitive to some — is the part that makes the difference. When a team feels that whoever leads them takes responsibility for the conditions and doesn't take credit for the successes, they hold up better under pressure, bluff less, help each other more.

Every team member contributes to the shared success with their part: technical, relational, organizational, domain-knowledge. The PM contributes with the conditions. If the conditions are missing, everyone's contribution crumbles; when they're in place, the team holds. All five rules above are concrete ways to put those conditions in place and keep them over time.

And no, you don't keep a spreadsheet of bathroom-break minutes. That's the exact opposite of a PM's job. It's a sign you haven't understood the craft.

------------------------------------------------------------------------

## Glossary

**[Psychological Safety](/en/glossary/psychological-safety/)** — Team climate in which people feel free to admit mistakes, say "I don't know", and raise problems without fearing consequences to their professional standing. It doesn't mean a soft climate without criticism — it means professional safety around telling the technical truth.

**[Bus Factor](/en/glossary/bus-factor/)** — Number of team members who, if simultaneously lost, would block the project. A bus factor of 1 is a critical risk: knowledge is concentrated in a single head. Target: keep the bus factor ≥ 3 for critical skills.

**[Micromanagement](/en/glossary/micromanagement/)** — Management style based on pointwise control of the team's daily activities, often accompanied by constant status requests and measurement of time spent on individual operations. It causes motivation loss, turnover, and discourages initiative.

**[Outcome vs Output](/en/glossary/outcome-vs-output/)** — Distinction between what the team concretely produces (output: code, documents, deliverables) and the final result measured by the business (outcome: go-live, revenue, KPI). Output is under the team's control; outcome also depends on external variables.

**[Knowledge Transfer](/en/glossary/knowledge-transfer/)** — Structured process of transferring knowledge between people or teams, critical to raising the bus factor and reducing single-person dependencies. It can be synchronous (pairing sessions) or asynchronous (documentation, recorded videos).