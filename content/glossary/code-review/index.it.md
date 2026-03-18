---
title: "Code Review"
description: "Pratica di revisione del codice da parte di un collega prima del merge, per catturare bug, migliorare la qualità e condividere conoscenza nel team."
translationKey: "glossary_code-review"
articles:
  - "/posts/project-management/ai-github-project-management"
---

La **Code Review** è la pratica per cui un collega esamina il codice scritto da un altro sviluppatore prima che venga incorporato nel branch principale. Su GitHub avviene dentro le Pull Request.

## Come funziona

Lo sviluppatore apre una Pull Request con le sue modifiche. Un reviewer assegnato esamina il diff del codice, lascia commenti, suggerisce miglioramenti e alla fine approva o richiede modifiche. Il processo è asincrono: non servono riunioni, il review avviene sullo strumento. Solo dopo l'approvazione il codice viene fuso nel branch principale.

## A cosa serve

La code review cattura bug che i test automatici non trovano, migliora la qualità del codice, e — aspetto spesso sottovalutato — diffonde la conoscenza del codebase nel team. Se solo una persona conosce un modulo e se ne va, il progetto ha un problema. Con le code review, almeno due persone conoscono ogni pezzo di codice.

## Quando si usa

Su ogni Pull Request, senza eccezioni. Non è una formalità: è un investimento in qualità. Il tempo speso in review è sempre inferiore al tempo che si spenderebbe per correggere bug in produzione scoperti troppo tardi.
