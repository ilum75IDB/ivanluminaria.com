---
title: "Use Case"
description: "Tehnică de analiză a cerințelor introdusă de Ivar Jacobson care descrie sistemul din punctul de vedere al actorului care îl folosește, nu al obiectelor care îl compun."
translationKey: "glossary_use_case"
aka: "Use Case (Jacobson)"
articles:
  - "/posts/project-management/da-rivali-a-co-autori-uml-rup"
---

**Use case**-ul este o tehnică de analiză a cerințelor introdusă de **Ivar Jacobson** la sfârșitul anilor '80 în metoda sa *Objectory*, și ulterior încorporată în UML ca una dintre cele nouă diagrame standard ale anului 1997. Descrie sistemul **din punctul de vedere al actorului care îl folosește** (utilizator, sistem extern, scheduler), nu al obiectelor software care îl compun.

## Cum funcționează

Un use case este compus din:

- un **actor** (cine inițiază interacțiunea)
- un **obiectiv** (ce vrea să obțină actorul)
- un **scenariu principal** (secvența tipică de pași)
- eventuale **scenarii alternative** (ce se întâmplă în caz de eroare sau variantă)

Exemplu clasic: *"Ca client înregistrat vreau să anulez o comandă, pentru că m-am răzgândit în privința achiziției."* Actorul este clientul înregistrat, obiectivul este anularea unei comenzi, scenariile descriu pașii (login, căutare comandă, confirmare) și excepțiile (comandă deja expediată, sesiune expirată).

## De ce a schimbat analiza cerințelor

Înainte de use case, analiza tindea să descrie sistemul în termeni de **funcții** (ce face) sau de **date** (ce conține). Jacobson a propus în schimb să se pornească de la **comportamentul observabil pentru cel care folosește sistemul** — o schimbare de perspectivă simplă dar revoluționară, pentru că a pus în conversație developer și business într-un limbaj comun.

## Moștenirea în metodologiile Agile

**User story** din Agile este un use case despuiat de formalismul academic. Sintaxa *"ca [actor] vreau să [fac X] pentru a [obține Y]"* (Mike Cohn) este distilarea conversațională a use case-ului lui Jacobson. Aceeași arhitectură narativă, același rol de punte între business și tehnic — doar mai scurtă și mai puțin structurată.
