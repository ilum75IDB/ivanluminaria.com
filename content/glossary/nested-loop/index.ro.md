---
title: "Nested Loop (Join)"
description: "Cum functioneaza nested loop join si cand optimizatorul il alege — sau il alege din greseala."
translationKey: "glossary_nested_loop"
tags: ["glosar"]
---

Nested loop este cea mai simpla strategie de join: pentru fiecare rand din tabelul extern, baza de date cauta randurile corespunzatoare in tabelul intern. Functioneaza ca un dublu ciclu for imbricat — de aici numele.

Este alegerea ideala cand tabelul extern are putine randuri si tabelul intern are un index pe coloana de join. In acest scenariu, nested loop este imbatabil: putine iteratii, acces direct prin index, memorie minima. Un join pe 100 de randuri externe cu un index B-tree pe tabelul intern este practic instantaneu.

Devine un dezastru cand optimizatorul il alege pe seturi mari de date din greseala — de obicei pentru ca statisticile subestimeaza numarul de randuri. Un nested loop pe 2 milioane de randuri externe inseamna 2 milioane de cautari in tabelul intern, si fara index fiecare cautare este un scan complet. In aceste cazuri, un hash join sau un merge join ar fi cu ordine de marime mai rapide.

## Articole corelate

- [EXPLAIN ANALYZE nu este suficient: cum sa citesti cu adevarat un plan de executie PostgreSQL](/ro/posts/postgresql/explain-analyze-postgresql/)
