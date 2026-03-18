---
title: "Branch"
description: "Linie de dezvoltare independentă într-un sistem de version control. Permite lucrul pe modificări izolate fără a afecta codul principal până la merge."
translationKey: "glossary_branch"
articles:
  - "/posts/project-management/ai-github-project-management"
---

Un **Branch** (ramură) este o linie de dezvoltare independentă într-un repository Git. Fiecare branch conține o copie a codului pe care se poate lucra fără a afecta branch-ul principal (main) sau munca altor dezvoltatori.

## Cum funcționează

Când un dezvoltator creează un branch (ex. `fix/issue-234-eroare-calcul`), Git creează un pointer la versiunea curentă a codului. Din acel moment, modificările făcute pe branch rămân izolate. La finalul lucrului, modificările se propun echipei prin Pull Request și, după aprobare, se unesc (merge) în branch-ul principal.

## La ce folosește

Branch-urile elimină problema suprascrierilor accidentale și a conflictelor negestionate. Fiecare dezvoltator lucrează în propria zonă izolată: nu suprascrie munca celorlalți și nu strică codul funcțional. Branch-ul principal rămâne mereu într-o stare "bună" pentru că primește doar cod aprobat.

## Când se folosește

Se creează un branch pentru fiecare task, bug fix sau funcționalitate. Convenția de naming ajută la identificarea scopului: `fix/` pentru bug-uri, `feature/` pentru funcționalități noi, `hotfix/` pentru corecții urgente. Branch-ul se șterge după merge pentru a menține repository-ul curat.
