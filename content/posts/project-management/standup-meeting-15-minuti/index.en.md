---
title: "Standup meetings: why they only work if they last 15 minutes"
description: "A standup that starts well and in three weeks becomes a 45-minute meeting. How to enforce the 15-minute constraint and why it's the only thing that makes daily meetings actually work."
date: "2026-01-27T08:03:00+01:00"
draft: false
translationKey: "standup_meeting_15_minuti"
tags: ["standup", "agile", "meeting", "team-management", "scrum"]
categories: ["Project Management"]
image: "standup-meeting.cover.jpg"
---

First Monday of the project. New team, new methodology, new hopes. The PM proposes a daily standup. Everyone nods. "Fifteen minutes, standing up, three questions. Simple."

The first week works. At 9:15 it starts, by 9:28 everyone is back at their desk. Each person speaks for two minutes, blockers are flagged, people move on. Pure efficiency.

The second week someone raises a hand mid-round: "Can I quickly explain the problem I'm having with the integration?" Five minutes of technical discussion between two people. The other six stand there listening to something that doesn't concern them.

The third week the standup lasts thirty-five minutes. Someone brings a laptop. Someone else sits down. The three-question round has become a status meeting with open discussions, improvised demos and architectural debates.

By the fourth week the team starts skipping the standup. "It lasts half an hour anyway, I don't have time."

I've seen this sequence at least ten times in my career. It's not bad luck. It's a pattern.

------------------------------------------------------------------------

## ⏱️ Why the 15-minute constraint is non-negotiable

A standup has one purpose: **synchronise the team**. It is not an analysis meeting. It is not a problem-solving session. It is not a design workshop. It is a quick alignment checkpoint.

And the time constraint is what makes it so.

When a standup lasts 15 minutes, specific things happen:

- People prepare **before** the meeting, because they know they have two minutes
- Problems are **flagged**, not solved. Resolution happens afterwards, between the people involved
- The team maintains the perception that the standup is **useful and respectful of their time**
- Nobody walks in thinking "here we go, another half hour wasted"

When the standup runs past 20 minutes, the mechanism breaks:

| Duration | Effect on the team |
|---|---|
| 10-15 min | High focus, active participation, positive perception |
| 15-20 min | Acceptable, but some people start drifting |
| 20-30 min | People not involved in the long threads mentally check out |
| 30-45 min | The team sees the standup as a waste of time. Absences begin |
| 45+ min | The standup is dead. It has become a status meeting dressed up as an agile practice |

The most dangerous thing is not the overrun itself. It's that it happens gradually. Three extra minutes today, five tomorrow. Nobody notices until it's too late.

------------------------------------------------------------------------

## ❓ The three questions — and nothing else

The classic standup is built on three questions:

1. **What did I do yesterday?**
2. **What will I do today?**
3. **Is anything blocking me?**

Simple. But simplicity is treacherous, because the temptation to expand is constant.

"What I did yesterday" doesn't mean retelling your day. It means saying: "I finished the lookup table migration" or "I worked on bug #247, haven't resolved it yet." Ten seconds, not three minutes.

"What I'll do today" is not a detailed plan. It's a statement of intent: "Today I'll finish bug #247 and start integration testing."

"Is anything blocking me" is the most important question. Because this is where dependencies surface, bottlenecks appear, problems that one person alone cannot solve. But — and this is crucial — **the blocker is flagged, not resolved live**.

When someone says "I'm blocked because I don't have access to the staging environment", the correct response is not a fifteen-minute discussion about who should grant access, how to configure it and why it didn't work yesterday. The correct response is: "OK, let's talk after the standup, you and me."

This discipline is what keeps the standup under 15 minutes. Without it, every blocker becomes a meeting inside the meeting.

------------------------------------------------------------------------

## 💀 When the standup dies

I've identified a fairly precise list of the ways a standup can die. I list them not out of pessimism, but because recognising them is the only way to prevent them.

### The thread killer

One person describes a complex technical problem. Another person responds. A dialogue starts between two people, while six others stand idle. The facilitator doesn't intervene because "it's an important topic". Fifteen minutes gone.

### The improvised demo

"Wait, let me show you what I did." Screen share, application walkthrough, UI detail explanations. Interesting? Maybe. Relevant to the standup? No.

### The manager who asks questions

The PM or team lead starts probing: "Is that feature at 60% or 70%? When do you expect to finish? Have you talked to the client?" The standup turns into an individual status report.

### The missing facilitator

Without someone keeping the pace, the standup becomes a free-form conversation. Free-form conversations are lovely at the pub, not at 9:15 in the morning when eight people have work to do.

### The open laptop

When people bring laptops to the standup, the implicit message is: "This meeting doesn't deserve my full attention." And they're right — if the standup lasts 40 minutes, it doesn't.

------------------------------------------------------------------------

## 🛠️ How to make a standup actually work

After twenty years of projects, here's my recipe. It's not elegant, it's not textbook, but it works.

### 1. Visible timer

A timer on the shared screen (or a phone placed on the table) that starts when the standup begins. Everyone sees it. When it hits 15 minutes, the standup ends. Full stop.

It's not authoritarian. It's a team agreement. The timer is not the enemy — it's the guardian of everyone's time.

### 2. Facilitator with the mandate to cut

You need a person — rotating or permanent — whose sole job is to say: "OK, we'll dig into that after. Next." It's not rudeness. It's respect for the six people who are waiting.

The best facilitator does it naturally: "Interesting, let's discuss right after. Marco, your turn."

### 3. Standing up, for real

It's not folklore. Standing has a concrete psychological effect: people want to finish quickly. When you sit down, you relax. When you stand, you tend towards brevity.

If the team is remote, the principle translates to: cameras on, no multitasking. The signal should be: "These 15 minutes have my full attention."

### 4. No laptops, no screen sharing

The standup is verbal. If something requires a demo, a diagram, a visual explanation — that's not standup material. That's a separate meeting, with the right people.

### 5. Parking lot

Every time a topic comes up that deserves deeper discussion, the facilitator writes it on a visible list — the "parking lot". After the standup, the people involved stay and discuss. Everyone else goes to work.

The parking lot is the most underrated tool in standup management. It lets you say "we'll discuss that later" without the topic being forgotten.

------------------------------------------------------------------------

## 📊 The standup in numbers

Let's do a calculation nobody ever does.

A team of 8 people. Daily standup. 220 working days per year.

| Scenario | Duration | Hours/person/year | Total team hours/year |
|---|---|---|---|
| 15-minute standup | 15 min | 55 hours | 440 hours |
| 30-minute standup | 30 min | 110 hours | 880 hours |
| 45-minute standup | 45 min | 165 hours | 1,320 hours |

The difference between a well-managed standup and one that's out of control is **880 hours per year**. For a team of 8 people. That's 110 working days. Nearly five person-months.

And that's without counting the indirect effect: a 45-minute standup doesn't just steal 45 minutes. It steals the 10-15 minutes of focus needed afterwards to get back into the flow.

------------------------------------------------------------------------

## 🔄 Remote standups vs in-person

Since 2020 standups are often remote. The medium changes, but the principles stay the same. With a few extra precautions.

### Remote is worse (if you're not careful)

- Audio latency creates overlaps that stretch the time
- Multitasking is invisible (but real)
- The lack of body language makes it harder for the facilitator to know when to cut
- Screen sharing is one click away, and the temptation to use it is strong

### How to manage a remote standup

| Practice | Reason |
|---|---|
| Predefined speaking order | Avoids the "who's next?" and awkward silences |
| Cameras on | Signals presence and attention |
| Chat for the parking lot | Captures topics in real time without interrupting |
| Shared timer on screen | Same principle as in-person standups |
| Everyone muted except the speaker | Eliminates background noise and interrupt temptation |

The most effective trick I've found for remote standups is the **relay round**: each person, after speaking, names the next one. "I'm done. Sara, you're up." This keeps attention active and gives rhythm to the meeting.

------------------------------------------------------------------------

## 🎯 The standup is a tool, not a ritual

What has always struck me is how easily the standup becomes an empty ritual. You do it because "that's what you do", because "we're agile", because "the framework says so". But nobody asks any more: is it working?

A standup works when the team perceives it as useful. When at 9:15 people show up willingly, say their piece in two minutes, listen to others, and by 9:30 they're at their desk knowing exactly what's happening in the project.

A standup doesn't work when people see it as an obligation. When they sigh looking at the clock. When they check their phones. When they think "I could have used that half hour to work."

The difference between the two scenarios is almost always the same: whether the 15-minute constraint is respected or not.

You don't need sophisticated frameworks. You don't need certifications. You need a timer, a facilitator with a backbone, and the awareness that people's time has value.

Fifteen minutes. Three questions. Parking lot for the rest.

Everything else is noise.

------------------------------------------------------------------------

## Glossary

**[Daily Standup](/en/glossary/daily-standup/)** — Daily meeting of maximum 15 minutes where each team member answers three questions: what I did yesterday, what I will do today, what is blocking me.

**[Parking Lot](/en/glossary/parking-lot/)** — Visible list of topics that emerge during a meeting and deserve further discussion but are deferred to respect the timebox.

**[Facilitator](/en/glossary/facilitatore/)** — Person responsible for guiding a meeting by maintaining focus, respecting the timebox, and ensuring everyone has a voice.

**[Timeboxing](/en/glossary/timeboxing/)** — Time management technique that assigns a fixed, non-negotiable interval to an activity, forcing conclusion within the established limit.

**[Scrum](/en/glossary/scrum/)** — Agile framework for project management that organizes work into fixed-length sprints, with defined roles and structured ceremonies.
