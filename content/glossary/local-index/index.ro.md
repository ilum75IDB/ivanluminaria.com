---
title: "Local Index"
description: "Index Oracle partițional cu aceeași cheie ca tabela, unde fiecare partiție a tabelei are partiția de index corespunzătoare. Mai ușor de întreținut decât un index global."
translationKey: "glossary_local-index"
articles:
  - "/posts/oracle/oracle-partitioning"
---

Un **Local Index** este un index Oracle creat pe o tabelă partițională, care este automat partiționat cu aceeași cheie și aceleași limite ca tabela. Fiecare partiție a tabelei are o partiție de index corespunzătoare.

## Cum funcționează

Când se creează un index cu clauza `LOCAL`, Oracle creează o partiție de index pentru fiecare partiție a tabelei. Dacă tabela are 100 de partiții lunare, indexul va avea 100 de partiții corespunzătoare. Operațiile DDL pe o partiție (DROP, TRUNCATE, SPLIT) invalidează doar partiția de index corespunzătoare, nu întregul index.

## La ce folosește

Local Index este alegerea preferată pentru indexuri pe tabele partiționale deoarece menține independența partițiilor. Un `DROP PARTITION` durează mai puțin de o secundă și nu invalidează niciun alt index. Cu un index global, aceeași operație ar invalida întregul index, necesitând ore de rebuild.

## Când se folosește

Se folosește când indexul include cheia de partiție sau când interogările filtrează întotdeauna pe coloana de partiție. Pentru lookup-uri punctuale pe coloane non-partiție (ex. cheie primară), e nevoie de un index global. Regula: local unde e posibil, global doar unde e necesar.
