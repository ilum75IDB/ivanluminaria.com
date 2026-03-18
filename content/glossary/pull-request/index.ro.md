---
title: "Pull Request"
description: "Mecanism de propunere și revizuire a modificărilor de cod pe platforme precum GitHub. Permite code review, discuție și aprobare înainte de merge în branch-ul principal."
translationKey: "glossary_pull-request"
aka: "PR, Merge Request"
articles:
  - "/posts/project-management/ai-github-project-management"
---

Un **Pull Request** (PR) este o cerere formală de incorporare a modificărilor dintr-un branch de dezvoltare în branch-ul principal al repository-ului. Este mecanismul central de colaborare pe GitHub și platforme similare.

## Cum funcționează

Dezvoltatorul lucrează pe un branch dedicat (ex. `fix/issue-234-eroare-calcul`), completează modificările și deschide un PR. PR-ul arată diff-ul codului, permite colegilor să comenteze rând cu rând, să ceară modificări sau să aprobe. Doar după aprobare codul se unește (merge) în branch-ul principal. Aceasta garantează că codul "bun" rămâne bun.

## La ce folosește

PR-ul transformă dezvoltarea dintr-o activitate individuală într-un proces de echipă. Previne suprascrierile accidentale, surprinde bug-uri înainte să ajungă în producție și creează un istoric complet al cine a făcut ce, când și de ce. În proiectele haotice, este diferența dintre control și dezordine.

## Când se folosește

La fiecare modificare de cod, fără excepții. Chiar și corecțiile mici trec printr-un PR, pentru că valoarea nu e doar în review ci în trasabilitate. Pe platformele GitLab aceeași funcționalitate se numește Merge Request.
