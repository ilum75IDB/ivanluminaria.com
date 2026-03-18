---
title: "B-Tree"
description: "Structură de date de arbore echilibrat, tipul implicit de index în majoritatea bazelor de date relaționale. Eficient pentru căutări de egalitate și interval, dar inadecvat pentru LIKE cu wildcard inițial."
translationKey: "glossary_b-tree"
articles:
  - "/posts/postgresql/like-optimization-postgresql"
---

**B-Tree** (Balanced Tree) este cea mai comună structură de date pentru indexuri în bazele de date relaționale și este tipul implicit de index în PostgreSQL, MySQL și Oracle. Menține datele sortate într-o structură de arbore echilibrat care garantează timpi de căutare logaritmici.

## Cum funcționează

Un B-Tree organizează cheile în noduri sortate, cu fiecare nod conținând pointeri către noduri copil. Căutarea pornește de la rădăcină și coboară către frunze, înjumătățind spațiul de căutare la fiecare nivel. Pentru o tabelă cu 6 milioane de rânduri, un B-Tree necesită tipic 3-4 nivele de adâncime, adică 3-4 citiri de pagină pentru a găsi o valoare.

## La ce folosește

B-Tree-urile sunt optime pentru căutări de egalitate (`WHERE col = 'valoare'`), intervale (`WHERE col BETWEEN x AND y`), sortare și căutări cu prefix (`LIKE 'ABC%'`). Nu pot fi însă folosite pentru căutări cu wildcard inițial (`LIKE '%ABC%'`), deoarece ordonarea B-Tree nu ajută la găsirea substringurilor în poziții arbitrare.

## Când se folosește

B-Tree este alegerea corectă pentru majoritatea indexurilor. Când e nevoie de o căutare "conține" pe text, trebuie trecut la un index GIN cu extensia pg_trgm. Alegerea între B-Tree și GIN depinde de tipul query-ului și de profilul de încărcare al tabelei.
