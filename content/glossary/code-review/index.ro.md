---
title: "Code Review"
description: "Practica de revizuire a codului de către un coleg înainte de merge, pentru a surprinde bug-uri, îmbunătăți calitatea și partaja cunoștințele în echipă."
translationKey: "glossary_code-review"
articles:
  - "/posts/project-management/ai-github-project-management"
---

**Code Review** este practica prin care un coleg examinează codul scris de un alt dezvoltator înainte ca acesta să fie incorporat în branch-ul principal. Pe GitHub are loc în interiorul Pull Request-urilor.

## Cum funcționează

Dezvoltatorul deschide un Pull Request cu modificările sale. Un reviewer atribuit examinează diff-ul codului, lasă comentarii, sugerează îmbunătățiri și în final aprobă sau cere modificări. Procesul este asincron: nu sunt necesare ședințe, review-ul are loc pe instrument. Doar după aprobare codul se fuzionează în branch-ul principal.

## La ce folosește

Code review-ul surprinde bug-uri pe care testele automate nu le găsesc, îmbunătățește calitatea codului și — aspect adesea subestimat — răspândește cunoașterea codebase-ului în echipă. Dacă doar o persoană cunoaște un modul și pleacă, proiectul are o problemă. Cu code review-urile, cel puțin două persoane cunosc fiecare bucată de cod.

## Când se folosește

La fiecare Pull Request, fără excepții. Nu e o formalitate: e o investiție în calitate. Timpul petrecut în review e întotdeauna mai mic decât timpul care s-ar petrece corectând bug-uri în producție descoperite prea târziu.
