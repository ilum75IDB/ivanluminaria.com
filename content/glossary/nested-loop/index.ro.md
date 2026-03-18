---
title: "Nested Loop"
description: "Nested Loop Join — strategia de join care scaneaza tabelul intern pentru fiecare rand al tabelului extern, ideala pentru seturi mici de date cu index."
translationKey: "glossary_nested_loop"
aka: "Nested Loop Join"
articles:
  - "/posts/postgresql/explain-analyze-postgresql"
---

**Nested loop** este cea mai simpla strategie de join: pentru fiecare rand din tabelul extern, baza de date cauta randurile corespunzatoare in tabelul intern. Functioneaza ca un dublu ciclu `for` imbricat — de aici numele.

## Cum functioneaza

Optimizatorul alege un tabel ca "extern" (outer) si unul ca "intern" (inner). Pentru fiecare rand din tabelul extern, executa o cautare in tabelul intern pe coloana de join. Daca tabelul intern are un index pe coloana de join, fiecare cautare este un acces direct via B-tree. Fara index, fiecare cautare devine un sequential scan complet.

## Cand este alegerea corecta

Nested loop este imbatabil cand tabelul extern are putine randuri si tabelul intern are un index pe coloana de join. Un join pe 100 de randuri externe cu un index B-tree pe tabelul intern este practic instantaneu: putine iteratii, acces direct, memorie minima.

Este de asemenea strategia preferata pentru lookup-urile de dimensiuni in data warehouse-uri, unde un fact table filtrat (putine randuri) se uneste cu un dimension table indexat.

## Ce poate merge prost

Devine un dezastru cand optimizatorul il alege pe seturi mari de date din greseala — de obicei pentru ca statisticile subestimeaza numarul de randuri. Un nested loop pe 2 milioane de randuri externe inseamna 2 milioane de cautari in tabelul intern. Fara index, fiecare cautare este un scan complet.

In aceste cazuri un hash join sau un merge join ar fi cu ordine de marime mai rapide. Cauza principala este aproape intotdeauna o estimare de cardinalitate gresita: statistici invechite sau un `default_statistics_target` prea mic.
