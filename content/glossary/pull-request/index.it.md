---
title: "Pull Request"
description: "Meccanismo di proposta e revisione delle modifiche al codice su piattaforme come GitHub. Permette code review, discussione e approvazione prima del merge nel branch principale."
translationKey: "glossary_pull-request"
aka: "PR, Merge Request"
articles:
  - "/posts/project-management/ai-github-project-management"
---

Una **Pull Request** (PR) è una richiesta formale di incorporare le modifiche da un branch di sviluppo nel branch principale del repository. È il meccanismo centrale di collaborazione su GitHub e piattaforme simili.

## Come funziona

Lo sviluppatore lavora su un branch dedicato (es. `fix/issue-234-errore-calcolo`), completa le modifiche, e apre una PR. La PR mostra il diff del codice, permette ai colleghi di commentare riga per riga, richiedere modifiche o approvare. Solo dopo l'approvazione il codice viene unito (merged) nel branch principale. Questo garantisce che il codice "buono" resti sempre buono.

## A cosa serve

La PR trasforma lo sviluppo da un'attività individuale a un processo di team. Previene sovrascritture accidentali, cattura bug prima che arrivino in produzione, e crea una cronologia completa di chi ha fatto cosa, quando e perché. In progetti caotici, è la differenza tra controllo e disordine.

## Quando si usa

Su ogni modifica al codice, senza eccezioni. Anche le correzioni piccole passano per una PR, perché il valore non è solo nella review ma nella tracciabilità. Su piattaforme GitLab la stessa funzionalità si chiama Merge Request.
