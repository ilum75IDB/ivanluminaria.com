---
title: "Change Control"
description: "Proces formal GxP pentru gestionarea modificărilor la hardware, software și proceduri: evaluarea riscurilor, protocol de testare, documentație și semnături autorizate."
translationKey: "glossary_change_control"
aka: "Proces de Management al Schimbărilor"
articles:
  - "/posts/oracle/latenza-wan-e-change-control-gxp-il-costo-reale-del-lift-and-shift"
---

Change control-ul este procesul formal obligatoriu în sistemele validate GxP (Good Practice) care reglementează orice modificare adusă infrastructurii, software-ului sau procedurilor operaționale. În mediile reglementate din industria farmaceutică, medicală sau biotehnologică, implementarea unei modificări fără un change control aprobat constituie o deviere documentabilă cu consecințe regulatorii directe.

## Cum funcționează

Ciclul tipic cuprinde patru faze secvențiale:

1. **Cerere de modificare** — descrierea tehnică a modificării propuse, justificarea și sistemele afectate.
2. **Evaluarea riscurilor** — analiza impactului asupra statusului de validare existent (IQ/OQ/PQ), integrității datelor și continuității operaționale.
3. **Protocol de testare** — definirea testelor care trebuie executate înainte de go-live, cu criterii de acceptare explicite.
4. **Aprobare și implementare** — semnături autorizate din partea rolurilor desemnate (QA, IT, business owner) și documentație post-implementare.

Fiecare fază generează artefacte trasabile care trebuie păstrate în sistemul de management documentar pentru audituri interne și inspecții regulatorii.

## Context operațional

Change control-ul devine un blocaj critic în proiectele de migrare cloud (lift-and-shift), deoarece fiecare componentă migrată — bază de date, middleware, sistem de operare — poate necesita o cerere de modificare separată. În mediile Oracle care rulează sisteme GxP, chiar și o actualizare minoră de patch poate declanșa un ciclu complet de re-validare dacă afectează funcționalități deja calificate. Timpul mediu de aprobare în organizațiile de dimensiuni medii variază între 2 și 8 săptămâni pentru modificări cu risc mediu — un factor pe care planurile de migrare îl subestimează în mod sistematic.
