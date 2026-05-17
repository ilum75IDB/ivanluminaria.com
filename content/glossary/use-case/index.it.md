---
title: "Use Case"
description: "Tecnica di analisi dei requisiti introdotta da Ivar Jacobson che descrive il sistema dal punto di vista dell'attore che lo usa, non degli oggetti che lo compongono."
translationKey: "glossary_use_case"
aka: "Use Case (Jacobson)"
articles:
  - "/posts/project-management/da-rivali-a-co-autori-uml-rup"
---

Lo **use case** è una tecnica di analisi dei requisiti introdotta da **Ivar Jacobson** alla fine degli anni '80 nel suo metodo *Objectory*, e poi incorporata in UML come uno dei nove diagrammi standard del 1997. Descrive il sistema **dal punto di vista dell'attore che lo usa** (utente, sistema esterno, scheduler), non degli oggetti software che lo compongono.

## Come funziona

Uno use case è composto da:

- un **attore** (chi inizia l'interazione)
- un **obiettivo** (cosa l'attore vuole ottenere)
- uno **scenario principale** (la sequenza di passi tipica)
- eventuali **scenari alternativi** (cosa succede in caso di errore o variante)

Esempio classico: *"Come cliente registrato voglio cancellare un ordine, perché ho cambiato idea sull'acquisto."* L'attore è il cliente registrato, l'obiettivo è cancellare un ordine, gli scenari descrivono i passi (login, ricerca ordine, conferma) e le eccezioni (ordine già spedito, sessione scaduta).

## Perché ha cambiato l'analisi dei requisiti

Prima dello use case, l'analisi tendeva a descrivere il sistema in termini di **funzioni** (cosa fa) o di **dati** (cosa contiene). Jacobson ha proposto di partire invece dal **comportamento osservabile per chi usa il sistema** — un cambio di prospettiva semplice ma rivoluzionario, perché ha messo in conversazione developer e business in un linguaggio comune.

## L'eredità nelle metodologie Agile

La **user story** dell'Agile è uno use case asciugato del formalismo accademico. La sintassi *"come [attore] voglio [fare X] per [ottenere Y]"* (Mike Cohn) è il distillato conversazionale dello use case di Jacobson. Stessa architettura narrativa, stesso ruolo di ponte tra business e tecnico — solo più breve e meno strutturato.
