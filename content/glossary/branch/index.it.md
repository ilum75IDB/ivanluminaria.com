---
title: "Branch"
description: "Ramo di sviluppo indipendente in un sistema di version control. Permette di lavorare su modifiche isolate senza influenzare il codice principale fino al merge."
translationKey: "glossary_branch"
articles:
  - "/posts/project-management/ai-github-project-management"
---

Un **Branch** (ramo) è una linea di sviluppo indipendente in un repository Git. Ogni branch contiene una copia del codice su cui si può lavorare senza influenzare il branch principale (main) o il lavoro di altri sviluppatori.

## Come funziona

Quando uno sviluppatore crea un branch (es. `fix/issue-234-errore-calcolo`), Git crea un puntatore alla versione corrente del codice. Da quel momento, le modifiche fatte sul branch restano isolate. Al termine del lavoro, le modifiche vengono proposte al team tramite Pull Request e, dopo approvazione, unite (merged) nel branch principale.

## A cosa serve

I branch eliminano il problema delle sovrascritture accidentali e dei conflitti non gestiti. Ogni sviluppatore lavora nella propria area isolata: non sovrascrive il lavoro degli altri e non rompe il codice funzionante. Il branch principale resta sempre in uno stato "buono" perché riceve solo codice approvato.

## Quando si usa

Un branch si crea per ogni task, bug fix o funzionalità. La convenzione di naming aiuta a identificare lo scopo: `fix/` per bug, `feature/` per nuove funzionalità, `hotfix/` per correzioni urgenti. Il branch viene eliminato dopo il merge per mantenere il repository pulito.
