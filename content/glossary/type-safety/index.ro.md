---
title: "Type safety"
description: "Proprietate a unui sistem de tipuri care împiedică, la parse-time, folosirea de valori incompatibile cu tipul declarat al coloanei sau parametrului."
translationKey: "glossary_type_safety"
aka: "Siguranța tipurilor, type checking"
articles:
  - "/posts/postgresql/enum-postgresql-paga-o-pesa"
---

**Type safety** este proprietatea unui sistem de tipuri care împiedică, la parse-time sau compile-time, folosirea de valori incompatibile cu tipul declarat. În contextul bazelor de date înseamnă că motorul respinge operațiile care încalcă constrângerile de tip, înainte chiar de a executa interogarea.

## Cum funcționează

Când o coloană, un parametru de funcție sau o variabilă sunt declarate cu un tip specific (de ex. `INTEGER`, un domain custom, un ENUM), motorul verifică în momentul parse-ului că fiecare valoare atribuită sau comparată este compatibilă. Operațiile care amestecă tipuri incompatibile fără un cast explicit generează o eroare înainte de execuție, evitând bug-uri care s-ar manifesta doar la runtime.

## La ce folosește

La mutarea detecției erorilor de la runtime la parse-time, reducând riscul de date corupte sau inconsistente în producție. În PostgreSQL, de exemplu, un ENUM este un tip de sine stătător: o funcție care acceptă un `stare_abonament` nu va putea fi niciodată apelată cu un șir liber. În MySQL, unde ENUM este o decorare a unei coloane `VARCHAR`, această garanție nu există — restricția este doar pe coloană, nu pe tip.

## Când se folosește

Este utilă în toate sistemele unde integritatea semantică a datelor contează mai mult decât comoditatea scrierii: billing, finanțe, date despre clienți, orice domeniu în care o valoare "în afara domeniului" reprezintă o eroare de business și nu o variantă acceptabilă. Type safety end-to-end este una dintre trăsăturile distinctive ale PostgreSQL și unul dintre motivele pentru care este aleasă în contextele enterprise.
