---
categories:
- project-management
date: 2099-12-31
description: A personal story about curiosity, a locked door, and a mad doctor program
  that changed everything. How a C64 in 1983 shaped thirty years of database work.
draft: true
image: il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire.cover.jpg
seoTitle: 'From Commodore 64 to database engineering: a personal story'
tags:
- personal
- career
- origin-story
- commodore-64
title: 'A kid like any other: from a Commodore 64 to thirty years of databases'
translationKey: il_dottore_tutto_pazzo_un_commodore_64_una_porta_chiusa_e_il_mestiere_di_capire
webo_generated_at: 2026-09-16
webo_status: da_tradurre
---

## A kid like any other

As a child, like many others, I wanted to be a vet. I loved animals and nature, and taking care of them seemed like the best job in the world.

You probably had a ready answer too, at that age, when someone asked what you wanted to be when you grew up. And yours probably took a different turn at some point.

Mine did in 1983, when my father bought a Commodore 64.

## READY.

If you're roughly my age, you remember it: the hazelnut-coloured slab plugged into the television, the keys that clicked like a typewriter, the blue screen with the light-blue border and the text an entire generation still knows by heart.

```text
    **** COMMODORE 64 BASIC V2 ****

 64K RAM SYSTEM  38911 BASIC BYTES FREE

READY.
```

Below it, a cursor blinking and waiting for instructions.

Those who had the cassette recorder remember PRESS PLAY ON TAPE, the coloured stripes flickering on the screen border, and the hope that the game would load on the first try. Those who stopped by the newsstand remember the tapes with ten games on them and titles translated into a barely decipherable English. We were all in the same boat, and the boat took five minutes to load.

Along with the computer, my father had books full of BASIC programs to copy out. Pages of lines numbered in tens, and at the end, if you'd typed everything correctly, a game. If you'd typed it wrong, after two hours of work, the Commodore would tell you with its own particular brand of honesty: `?SYNTAX ERROR IN 340`. Line 340 was perfect, identical to the book. The cause was in line 330, where a semicolon had become a colon. Without knowing it, I was learning the first rule of every diagnosis: the symptom shows up in one place, the cause is usually a little further up.

The rules of the game were clear: copy the listing exactly, and the vet plan stays on track for the future.

## The mad doctor

One of those programs was called "The Mad Doctor." It asked you a series of questions — a kind of medical history — and at the end, based on your answers, it delivered a comic, tongue-in-cheek diagnosis.

One day, I was about ten years old and furious with my father. Instead of slamming a door, I opened the program and modified it: whenever he answered, the doctor would always conclude that he was "mean and unpleasant." I can't show you the original listing; this is a reconstruction, just to give you the idea:

```basic
500 REM THE DIAGNOSIS
510 IF N$="DAD" THEN PRINT "YOU ARE MEAN AND UNPLEASANT": END
520 PRINT "YOU HAVE AN ACUTE ATTACK OF..."
```

The Commodore didn't have accented characters — that's authentic period detail. Respect was in short supply in the code that afternoon too.

My father couldn't get angry, because it was the doctor talking. Perfect diplomatic immunity, built in BASIC by a kid who didn't even know what diplomatic immunity meant. And above all he was pleased: I had done something the book didn't contain. I had understood someone else's program well enough to change it.

From that day on, his books stopped being pages to copy and became companions on the road. Every listing was a mechanism to take apart and figure out how it worked.

## He gets the computer to solve his homework instead of studying

In middle school I was writing my own programs. They solved geometry and algebra problems: you entered the data, and the program worked through every step and showed the result.

My teacher didn't see the point, and she had her reasons. Those were the early years of computers entering family homes, and for many adults they were still mysterious objects. She told my father to take the computer away from me, otherwise I would never learn mathematics. Her verdict: "He gets the computer to solve his problems instead of studying."

Today I understand her. Faced with a technology she barely knew, she wanted to protect my learning, and from the outside a kid with a computer that solves equations looks like someone who found a shortcut.

The shortcut didn't exist. The Commodore knew nothing about triangles: I had to teach it every single step. Knowing how to solve a geometry problem in your notebook is one thing; knowing how to explain it to a machine, step by step, leaving nothing to intuition, is something else entirely — and it requires understanding the subject far more deeply. When you think about it, the same is true when the person who needs to understand is a human being.

## The locked door

My father came back from that meeting and took the teacher seriously. He moved the Commodore into his and my mother's bedroom and locked the door.

A locked door says two things: that there's something valuable inside, and that someone has decided it's not for you. My father meant the second. I only heard the first.

Almost in withdrawal, I studied the situation like a listing that wouldn't run. Three things were needed: an afternoon without parents, an accomplice, and a key. The afternoons were easy — my parents would go out and it was just me and my brother at home. I bribed the accomplice with an ice cream: my first negotiation, and still one of the most cost-effective ones I've ever made. The key I bought at the hardware store: a skeleton key.

The door opened. Every time my parents were out I would set up the Commodore, and the cursor would start blinking again. Before they got back I would pack everything away and put it exactly as it had been. My father only found out months later.

I'm not telling this as something to imitate. I'm telling it for the three lessons I found in it, looking back. The key locked the computer; curiosity stayed free. A skeleton key opens many doors because it comes from someone who has understood how locks are made. And whoever opens a door takes responsibility for what they find inside.

## The patient has changed

At thirteen I told my father I was going to write video games for a living. I never wrote a single one. In 1994 I enrolled in Computer Engineering at Roma Tre, and from there came thirty years of databases and systems that keep banks, insurance companies, and telecoms running.

The kid who wanted to take care of animals found his trade, in his own way. A system that slows down or stops sends symptoms, rarely explanations. The work starts with a history-taking, like the mad doctor's, and ends with a diagnosis to explain step by step — like the geometry programs — to whoever has to make a decision.

Behind every system there are people: the team that keeps it running, the one who gets called in the middle of the night, the one who has to answer to a board of directors the next morning. Taking care of a system means, first of all, letting those people do their work without worry.

I still run into locked doors. The skeleton key is the same: understand how the lock is made. With one important difference: today the keys are handed to me by clients, and keeping them safe is the part of the job I take most seriously.

There's a phrase that, in day-to-day work, signals a locked door more reliably than any alert: "we've always done it this way." I hear it in front of a batch job nobody has touched in years, an inherited configuration, a check that keeps running without anyone remembering why. It's an understandable thing to say, often said by good people who are tired. And it's usually right there that line 330 is hiding.

The doctor, in the meantime, has become considerably less mad.

## Just like you

The credit for this path belongs to ordinary people.

First of all, my father. In 1983 he brought a computer into the house when very few people knew what to do with one. He let his son get his hands into the programs in his books, and took a "mean and unpleasant" verdict with a certain satisfaction, because he had seen something the book didn't contain. And even by locking that door, without meaning to, he taught me how much what was inside was worth — and not to stop at a "no" before understanding why.

Then a teacher who, with the tools of that era, was trying to protect my learning. And a brother who kept a secret for months, for the price of an ice cream.

If you also started out in front of a blinking cursor, you know what I'm talking about. And if today you're looking at a line 340 that seems perfect, there's only one useful question: where is line 330?

## Glossary
- **[BASIC](/en/glossary/basic/)** — Beginner's All-purpose Symbolic Instruction Code: an interpreted programming language widespread on home computers of the 1980s, designed to be accessible without specialist training.
- **[Listing](/en/glossary/basic/)** — in the context of home computing, the complete printed or on-screen text of a program's source code, typically published in magazines or books for manual entry.
- **[Skeleton key](/en/glossary/listato/)** (passpartout) — a key cut to open multiple different locks; used here both literally and as a metaphor for transferable technical understanding.
- **Syntax error** — an error signalled by an interpreter or compiler when source code does not conform to the grammar rules of the language; on the C64, reported with the line number of the detected anomaly.
- **Diagnosis** — in database and systems engineering, the process of identifying the root cause of a malfunction starting from observed symptoms, analogous to clinical diagnosis in medicine.
