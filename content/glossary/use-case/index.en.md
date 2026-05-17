---
title: "Use Case"
description: "Requirements analysis technique introduced by Ivar Jacobson that describes the system from the point of view of the actor who uses it, not from the objects that compose it."
translationKey: "glossary_use_case"
aka: "Use Case (Jacobson)"
articles:
  - "/posts/project-management/da-rivali-a-co-autori-uml-rup"
---

The **use case** is a requirements analysis technique introduced by **Ivar Jacobson** in the late 1980s in his *Objectory* method, and then incorporated into UML as one of the nine standard diagrams of 1997. It describes the system **from the point of view of the actor who uses it** (user, external system, scheduler), not the software objects that compose it.

## How it works

A use case is composed of:

- an **actor** (who initiates the interaction)
- a **goal** (what the actor wants to achieve)
- a **main scenario** (the typical sequence of steps)
- possible **alternative scenarios** (what happens in case of error or variant)

Classic example: *"As a registered customer I want to cancel an order, because I've changed my mind about the purchase."* The actor is the registered customer, the goal is to cancel an order, the scenarios describe the steps (login, order search, confirm) and the exceptions (order already shipped, expired session).

## Why it changed requirements analysis

Before the use case, analysis tended to describe the system in terms of **functions** (what it does) or **data** (what it contains). Jacobson proposed instead starting from the **observable behaviour for those who use the system** — a simple shift of perspective, but a revolutionary one, because it put developer and business in conversation in a common language.

## The legacy in Agile methodologies

The Agile **user story** is a use case stripped of academic formalism. The syntax *"as a [actor] I want to [do X] in order to [achieve Y]"* (Mike Cohn) is the conversational distillation of Jacobson's use case. Same narrative architecture, same role of bridge between business and technical — just shorter and less structured.
