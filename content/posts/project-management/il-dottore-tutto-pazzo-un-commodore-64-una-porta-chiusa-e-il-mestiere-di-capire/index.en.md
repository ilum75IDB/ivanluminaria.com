---
title: "A child like any other: how a Commodore 64 and a master key shaped thirty years of database work"
seoTitle: "From Commodore 64 to database engineering: a career origin story"
description: "A BASIC program, a locked door, and a passepartout. How curiosity in front of a blinking cursor became thirty years of databases, banks, and production systems."
date: 2099-12-31
draft: true
translationKey: "il_dottore_tutto_pazzo_un_commodore_64_una_porta_chiusa_e_il_mestiere_di_capire"
tags: ["career", "origin-story", "commodore-64", "database-engineering"]
categories: ["project-management"]
image: "il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire.cover.jpg"
webo_status: da_tradurre
webo_generated_at: 2026-09-16
---

## A child like any other

As a child, like many others, I wanted to be a vet. I loved animals and nature, and taking care of them seemed like the finest job in the world.

You probably had a ready answer to the question "what do you want to be when you grow up?" too. And yours probably took a different turn at some point.

Mine did in 1983, when my father bought a Commodore 64.

## READY.

If you're roughly my age, you remember it: the biscuit-coloured slab plugged into the television, the keys that clacked like a typewriter, the blue screen with the light-blue border and the text an entire generation still knows by heart.

```text
    **** COMMODORE 64 BASIC V2 ****

 64K RAM SYSTEM  38911 BASIC BYTES FREE

READY.
```

Below it, a cursor blinking and waiting for instructions.

Those who had a cassette recorder remember PRESS PLAY ON TAPE, the coloured stripes on the screen border, and the hope that the game would load on the first try. Those who stopped by the newsagent remember tapes with ten games on them and titles translated into a mangled local language that took some deciphering. We were all in the same boat, and the boat took five minutes to load.

Along with the computer, my father had books full of BASIC programs to type in. Pages of lines numbered in tens, and at the end, if you'd copied correctly, a game. If you'd copied wrong, after two hours of typing, the Commodore told you with a frankness all its own: `?SYNTAX ERROR IN 340`. Line 340 was perfect, identical to the book. The cause was in line 330, where a semicolon had become a colon. Without knowing it, I was learning the first rule of every diagnosis: the symptom shows up in one place, the cause is usually a little further up.

The rules were clear: copy the listing exactly, and the vet plan stays for later.

## The crazy doctor

One of those programs was called "The Crazy Doctor." It asked you a series of questions — a kind of medical history — and at the end, based on your answers, it delivered a tongue-in-cheek diagnosis.

One day, when I was around ten, I was angry with my father. Instead of slamming a door, I opened the program and modified it: whenever he answered, the doctor would always conclude that he was "mean and unpleasant." I can't show you the original listing; this is a reconstruction, just to give you the idea:

```basic
500 REM THE DIAGNOSIS
510 IF N$="DAD" THEN PRINT "YOU ARE MEAN AND UNPLEASANT": END
520 PRINT "YOU HAVE AN ACUTE ATTACK OF..."
```

The Commodore didn't have accented characters — a genuine quirk of the era. Respect was in short supply that afternoon, even in the code.

My father couldn't get angry, because it was the doctor talking. Perfect diplomatic immunity, built in BASIC by a child who didn't even know what diplomatic immunity was. And above all he was pleased: I had done something that wasn't in the book. I had understood someone else's program well enough to change it.

From that day on, his books stopped being pages to copy and became companions on the road. Every listing was a mechanism to take apart and understand.

## He gets the computer to solve his homework instead of studying

In middle school I was writing my own programs. They solved geometry and algebra problems: you entered the data, and the program worked through every step until the result.

My teacher didn't see the point, and she had her reasons. Those were the early years of computers entering family homes, and for many adults they were still mysterious objects. She told my father to take the computer away, otherwise I'd never learn mathematics. Her verdict: "He gets the computer to solve his problems instead of studying."

Today I understand her. Faced with a technology she barely knew, she was trying to protect my learning, and from the outside a kid with a computer solving equations looks like someone who found a shortcut.

The shortcut didn't exist. The Commodore knew nothing about triangles: I had to teach it every single step. Knowing how to solve a geometry problem on paper is one thing; knowing how to explain it to a machine, step by step, leaving nothing to intuition, is another — and it requires understanding the subject far more deeply. When you think about it, the same holds true when the one who needs to understand is a person.

## The locked door

My father came back from that meeting and took the teacher seriously. He moved the Commodore into his and my mother's bedroom and locked the door.

A locked door says two things: that something valuable is inside, and that someone has decided it isn't for you. My father meant the second. I only heard the first.

Almost in withdrawal, I studied the situation like a listing that wouldn't run. Three things were needed: an afternoon without parents, an accomplice, and a key. The afternoons were there — my parents would go out and leave me and my brother at home. I bribed the accomplice with an ice cream: my first negotiation, and still one of the most cost-effective. The key I bought at the hardware shop: a passepartout.

The door opened. Every time my parents were out I set up the Commodore, and the cursor started blinking again. Before they got back I packed everything away and put it exactly as it was. My father only found out months later.

I'm not telling this as something to imitate. I'm telling it for the three lessons I found in it, looking back. The key locked the computer; curiosity stayed free. A passepartout opens many doors because it comes from someone who has understood how locks are made. And whoever opens a door takes responsibility for what they find inside.

## The patient has changed

At thirteen I told my father I was going to write video games for a living. I never wrote a single one. In 1994 I enrolled in Computer Engineering at Roma Tre, and from there came thirty years of databases and systems holding up banks, insurance companies, and telecoms.

The child who wanted to care for animals found his trade, in his own way. A system that slows down or stops sends symptoms, rarely explanations. The work starts with a case history — like the crazy doctor's — and ends with a diagnosis to explain step by step, like the geometry programs, to whoever has to make a decision.

Behind every system there are people: the team keeping it running, the one called in the middle of the night, the one who has to answer to a board of directors the next morning. Taking care of a system means, first of all, letting those people do their jobs without worry.

I still run into locked doors. The passepartout is the same: understand how the lock is made. With one important difference: today the keys are handed to me by clients, and keeping them safe is the part of the job I take most seriously.

There is one phrase that, in day-to-day work, signals a locked door more reliably than any alert: "we've always done it this way." I hear it in front of a batch job nobody has touched in years, an inherited configuration, a check that keeps running with no one remembering why. It's an understandable phrase, often said by capable and tired people. And it's usually right there that line 330 is hiding.

The doctor, in the meantime, has become considerably less crazy.

## Just like you

The credit for this path belongs to ordinary people.

First of all, my father. In 1983 he brought a computer home when very few people knew what to do with one. He let his son get his hands into the programs from his books, and took a "mean and unpleasant" verdict with a certain satisfaction, because he had seen something the book didn't contain. And even by locking that door, without meaning to, he taught me how much what was inside was worth — and not to stop at a "no" before understanding why.

Then a teacher who, with the tools of those years, was trying to protect my learning. And a brother who kept a secret for months, for the price of an ice cream.

If you also started out in front of a blinking cursor, you know what I'm talking about. And if today you're looking at a line 340 that seems perfect, there's only one useful question: where is line 330?
