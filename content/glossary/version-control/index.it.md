---
title: "Version Control"
description: "Sistema che traccia ogni modifica al codice sorgente, permettendo di visualizzare la cronologia, annullare cambiamenti e collaborare senza sovrascritture. Git è lo standard attuale."
translationKey: "glossary_version-control"
aka: "Controllo versione, VCS"
articles:
  - "/posts/project-management/ai-github-project-management"
---

Il **Version Control** (controllo versione) è un sistema che registra ogni modifica ai file di un progetto, mantenendo una cronologia completa di chi ha cambiato cosa, quando e perché. Git è il sistema di version control più usato al mondo.

## Come funziona

Ogni modifica viene registrata come "commit" con un messaggio descrittivo, un autore e un timestamp. Il sistema mantiene l'intera storia del progetto: è possibile tornare a qualsiasi versione precedente, confrontare versioni diverse e capire l'evoluzione del codice nel tempo. Con Git, ogni sviluppatore ha una copia completa della storia sul proprio computer.

## A cosa serve

Senza version control, il codice vive su cartelle condivise dove le sovrascritture accidentali sono la norma e nessuno sa quale sia la versione "buona". Con il version control, ogni modifica è tracciata e reversibile, i conflitti tra sviluppatori vengono gestiti in modo strutturato, e la storia del progetto è una risorsa, non un mistero.

## Quando si usa

Sempre, su qualsiasi progetto software con più di un file o più di uno sviluppatore. L'assenza di version control è il primo segnale di un progetto fuori controllo. GitHub, GitLab e Bitbucket sono piattaforme che aggiungono collaborazione (Pull Request, Issue tracker) sopra Git.
