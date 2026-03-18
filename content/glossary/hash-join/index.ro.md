---
title: "Hash Join"
description: "Cum functioneaza hash join si de ce este cea mai buna alegere pentru join-uri pe volume mari de date."
translationKey: "glossary_hash_join"
tags: ["glosar"]
---

Hash join este o strategie de join proiectata pentru volume mari de date. Functioneaza in doua faze: mai intai baza de date citeste tabelul mai mic si construieste o hash table in memorie, indexand randurile dupa coloana de join. Apoi scaneaza tabelul mai mare si pentru fiecare rand cauta corespondenta in hash table cu un lookup O(1).

Avantajul este ca nu sunt necesare indexuri si complexitatea este liniara — proportionala cu suma randurilor din ambele tabele, nu cu produsul ca in nested loop. Dezavantajul este ca necesita memorie pentru hash table: daca tabelul mai mic nu incape in `work_mem`, baza de date trebuie sa scrie loturi pe disc (batched hash join), incetinind operatia.

Optimizatorul alege hash join cand ambele tabele sunt mari si nu exista indexuri utile, sau cand statisticile indica ca numarul de randuri de combinat este prea mare pentru un nested loop eficient. Este una dintre cele mai comune strategii in data warehouse-uri si rapoarte care agrega milioane de randuri.

## Articole corelate

- [EXPLAIN ANALYZE nu este suficient: cum sa citesti cu adevarat un plan de executie PostgreSQL](/ro/posts/postgresql/explain-analyze-postgresql/)
