---
title: "From rivals to co-authors: how Booch, Rumbaugh and Jacobson invented UML (and what's left of it today)"
seoTitle: "Three Amigos, UML and RUP: the history and what's left today"
description: "The story of the Three Amigos of UML and RUP: how Booch, Rumbaugh and Jacobson, from rivals, unified object-oriented modeling. And what's left of it today."
date: "2026-06-30T08:03:00+01:00"
draft: false
translationKey: "da_rivali_a_co_autori_uml_rup"
tags: ["methodology"]
categories: ["project-management"]
image: "da-rivali-a-co-autori-uml-rup.cover.jpg"
---

The other day, in an internal training room at an insurance client, I opened a project document from 2003 to show an example of application architecture. UML diagrams, RUP phases with their coloured dots, schematic use cases, sequences of interactions between actors and systems. A colleague a few years younger walked up to the whiteboard and asked me, no detours: *"What are these acronyms? I've seen them in some courses but I've never really understood them."*

The question made me smile — not because it was strange, but because it was the same one I would have asked twenty years ago if someone had put that poster in front of me. **UML and RUP are two acronyms that made an era**, and that today live a double life: marginal in the current conversation about project management, but still alive in precise niches where documentary rigour is mandatory. And behind those acronyms lies one of the most curious stories in software engineering of the last thirty years — the story of **three rivals who chose to stand in the same room**.

It's worth telling.

---

## The 1990s: three tribes, three vocabularies

To understand UML, you need to step back to the late 1980s, when object-oriented was becoming the dominant paradigm in programming. But there was a problem: every research group and every tooling company had invented **its own way of visually representing classes, relationships, objects**. And the three main approaches, each with its prophet, eyed each other across the trenches.

**Grady Booch**, American, had been working since the mid-'80s at **Rational Software** (the company founded by Mike Devlin and Paul Levy in 1981). He had published the *Booch Method* in the early '90s: a notation rich in symbols — clouds, arrows, labels — that became hard to draw by hand but extraordinarily expressive when supported by a graphical tool. It was for developers.

**James Rumbaugh**, also American, worked in the research labs of **General Electric**. In 1991 he published *Object Modeling Technique* (OMT), a drier approach more oriented toward data modeling than behaviour representation. It worked well in contexts where the database was at the centre of the system. It was for architects.

**Ivar Jacobson**, Swedish, had worked at **Ericsson** before founding his own company, *Objectory AB*. His original contribution was the concept of the **use case**: describing the system from the point of view of the actor who uses it, not the object that composes it. It was for those who talked to the business.

Three tribes, three vocabularies, **three different sets of symbols to draw the same class**. Separate conferences, competing books, customers who had to choose which tribe to follow. The competition, in the words of those who lived through that period, was at times fierce — there were technical papers from one camp openly criticising the choices of the other two. Nothing personal, but three communities watching each other from across the river.

---

## The turning point: October 1994

In mid-1994, Rational Software makes the move that changes everything. Mike Devlin, the CEO, has understood that fragmentation is becoming a brake on enterprise adoption of object-oriented — and that none of the three methods will ever win on its own. He decides then to **put the protagonists together**.

In October 1994, **James Rumbaugh leaves General Electric and moves to Rational**. The news makes noise: two of the three prophets of object-oriented modeling now work in the same company. Booch and Rumbaugh, who up to the day before had signed articles responding to each other in specialist journals, now have offices down the same corridor.

A year later, in 1995, Rational acquires **Objectory AB**, and **Ivar Jacobson** joins the group. It's done: the three men who had dominated the OO debate for five years are in the same company. The specialist press, with a mix of curiosity and irony, names them **the Three Amigos** — not without a touch of scepticism: will three people so different really manage to work together?

The three, interviewed years later, told the beginnings without emphasis. *"For the first few months everyone defended their own notation. Then, gradually, we realised that no single approach was enough. And it was obvious that the market wouldn't tolerate three competing standards forever."*

---

## UML, November 1997

Between 1995 and 1997 the Three Amigos work on merging the three methods. Booch brings symbolic richness for structural modeling, Rumbaugh brings the discipline of data and state modeling, Jacobson brings use cases as a bridge to the business. Thus is born **UML — Unified Modeling Language**.

The standardisation path goes through **OMG (Object Management Group)** [1], the non-profit consortium that already administered other object-oriented standards (such as CORBA). UML 1.0 is submitted to the OMG in January 1997; **UML 1.1 is adopted as a formal OMG standard in November 1997**.

In that first version UML offered **nine types of diagrams** organised in two families: **structural** (class diagram, object diagram, component diagram, deployment diagram) to describe static structure, and **behavioural** (use case, sequence, collaboration, statechart, activity) to describe dynamic behaviour. Since then the spec has grown — UML 2.5 (the current one) has thirteen types of diagrams — but the core has remained.

A standard is measured not by who creates it, but by who uses it. And **UML was adopted rapidly** — in the three years that followed it became the dominant language for architectural documentation in banking, telco, public sector and insurance, where enterprise tenders explicitly required it in their contract specifications.

---

## RUP, 1998: the enterprise process

UML was the **language**, but a **process** was needed to tell how to use it. Rational Software responds in 1998 with **RUP — Rational Unified Process** [2]. An iterative software development method, based on previous contributions from Booch and Jacobson, organised in **four sequential phases with internal iterations** in each phase:

- **Inception** — vision, business case, scope
- **Elaboration** — architecture, detailed requirements, risk mitigation
- **Construction** — iterative implementation
- **Transition** — deploy, beta, rollout

Unlike the classic *waterfall*, RUP was **iterative**: you didn't finish a phase before starting the next, you went back and forth multiple times. Unlike the *lightweight* methods that would arrive a few years later, however, it was **heavyweight** — a typical enterprise RUP project foresaw six months of Elaboration before writing a line of production code. Formal documents, traced artefacts, documented milestones, possible audits.

It was the right answer for the context in which it was born. In the years 1998-2005, RUP was massively adopted in European banking, in public administration, in telecommunications systems. **IBM acquires Rational in 2003** for 2.1 billion dollars — an operation that valued, in fact, RUP as a strategic asset as much as UML.

---

## February 2001: the Agile Manifesto changes the wind

While RUP reached its peak adoption, **across the river** something completely different was being born. Between February 11th and 13th, 2001, **seventeen developers meet at a ski resort in Utah** — Snowbird — and sign a poster of a few lines that would become the **Agile Manifesto** [3].

Four pairs of values, each in the form "X over Y":

- *Individuals and interactions over processes and tools*
- *Working software over comprehensive documentation*
- *Customer collaboration over contract negotiation*
- *Responding to change over following a plan*

It was exactly the reverse of RUP. Where RUP put processes at the centre, Agile put people. Where RUP asked for six months of documents before code, Agile asked for working software every two weeks. Where RUP formalised contracts, Agile asked for continuous conversations with the client.

None of the seventeen signatories, it's worth saying, attacked RUP explicitly. The Manifesto names no competing method. But the message was clear, and in the ten years that followed the wind changed. **Scrum**, **XP** (Extreme Programming), **Kanban** became the standard vocabulary of the development team. RUP, in many contexts, stopped being proposed in new projects.

A note worth making: many of Agile's ideas **weren't born from scratch**. **User stories** are use cases stripped of Jacobson's academic formalism, short **sprints** are RUP's Elaborations shortened, and even the BDD ceremony called *"Three Amigos meeting"* — developer, tester and business analyst discussing a user story together before starting it — is an explicit homage to the group of Booch, Rumbaugh and Jacobson. Agile didn't so much contradict UML, **it more freed its ideas from the weight of the process**. It's material that's worth its own article, in the future.

It's not dead. But the wind has changed.

---

## What remains today, twenty years on

Twenty years after the Agile Manifesto, where do we find ourselves?

**UML is still alive**, but differently from how the Three Amigos imagined. It's no longer the universal language to describe a system's architecture — that role has often been taken by freer diagrams, by architecture decision records (ADRs) in markdown, by sketches in Mermaid or draw.io that don't respect formal UML syntax but carry its spirit. **UML as a formal notation survives** in public administration tender specifications, in ISO certification projects, and in academic contexts where teaching object-oriented modeling is still part of the curriculum.

**RUP, on the other hand, has found its niche** — and it's a niche that's anything but marginal. It lives on, alive and well, in sectors where **documentary rigour is mandatory by law or by audit**:

- **Aviation and aerospace** — DO-178C-certified avionic systems, where every requirement must be traced from collection to test
- **Medical** — devices under IEC 62304, where the software development process is certified alongside the product
- **Patents and pharmaceutical R&D** — where the traceability of the innovation process has legal value
- **Critical banking** — core payment systems where formal documentation is part of the regulatory contract

In these contexts, **a pure agile method doesn't pass the audit**. You need to be able to demonstrate to an external auditor, years after release, why a certain architectural choice was made and what alternatives had been considered. RUP — or one of its direct descendants — is still the standard way of doing that.

For the rest, **Scrum and Kanban dominate**. The [15-minute daily stand-ups](/en/posts/project-management/standup-meeting-15-minuti/) I described in another article are the Agile ritual par excellence, and they wouldn't exist if those seventeen in Utah hadn't signed that poster in 2001.

---

## The lesson I take away from the Three Amigos

The lesson I'm left with from this story — the one I tried to explain to my colleague in front of the whiteboard that day — is not UML, and it's not RUP.

It's that **three people who were doing the same thing in a competitive way decided, at some point, to stand in the same room**. They stopped publishing articles answering each other, they stopped defending every detail of their own notation, and they looked for the piece of common value. It wasn't painless — it took two years of confrontation inside Rational before UML 1.0 was ready. But it happened.

And it's a lesson that, in today's project management, is worth far more than any syntactic detail of UML. When a development team splits into factions each defending its own preferred framework — Scrum vs Kanban, microservices vs monolith, REST vs GraphQL — the lesson of the Three Amigos is that the value of a method is not measured in its theoretical superiority, but in its **ability to stand in the same room with other different methods** and produce something new.

There is no superior method. There are different contexts, and methods suited to different contexts. UML and RUP are suited where documentary rigour is mandatory. Scrum and Kanban are suited where iteration speed is mandatory. Both survive, side by side, because both serve.

And stories like that of the Three Amigos serve to remind us of this, every now and then.

---

## Official sources

1. Object Management Group — [Unified Modeling Language (UML) specification](https://www.omg.org/spec/UML/)
2. Rational Unified Process — [overview and phases (IBM/Rational documentation archive)](https://www.ibm.com/docs/en/rational-soft-arch/9.7.0?topic=overview-rational-unified-process)
3. Beck, Beedle, van Bennekum et al. — [Manifesto for Agile Software Development (February 2001)](https://agilemanifesto.org/)

---

## Glossary

- **[Three Amigos](/en/glossary/three-amigos/)** — Nickname given by specialist press to Grady Booch, James Rumbaugh and Ivar Jacobson, the three creators of UML who worked at Rational Software between 1994 and 1998. From rivals they became co-authors of a unified standard.
- **[UML](/en/glossary/uml/)** — Unified Modeling Language. Standard object-oriented modeling language, adopted by OMG in November 1997 from the merger of three previous methods (Booch Method, OMT, Objectory). Includes structural and behavioural diagrams.
- **[RUP](/en/glossary/rup/)** — Rational Unified Process. Iterative software development method released by Rational in 1998, organised in four phases (Inception, Elaboration, Construction, Transition). Heavyweight and document-intensive, today lives in regulated niches (aviation, medical, critical banking).
- **[Use Case](/en/glossary/use-case/)** — Requirements analysis technique introduced by Ivar Jacobson that describes the system from the point of view of the actor who uses it, not from the objects that compose it. One of the three pillars that fed UML.
- **[Agile Manifesto](/en/glossary/agile-manifesto/)** — A few-line document signed at Snowbird, Utah, on February 11-13, 2001 by seventeen developers. Four pairs of values that shifted the focus of software development from heavyweight practices (RUP-like) to lightweight practices (Scrum, XP, Kanban).
