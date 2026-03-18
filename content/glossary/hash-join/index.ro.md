---
title: "Hash Join"
description: "Hash Join — strategie de join optimizata pentru volume mari de date, bazata pe o hash table construita in memorie."
translationKey: "glossary_hash_join"
aka: "Hash Join"
articles:
  - "/posts/postgresql/explain-analyze-postgresql"
---

**Hash join** este o strategie de join proiectata pentru volume mari de date. Functioneaza in doua faze: mai intai construieste o structura de date in memorie, apoi o foloseste pentru a gasi corespondentele eficient.

## Cum functioneaza

Baza de date citeste tabelul mai mic (build side) si construieste o hash table in memorie, indexand randurile dupa coloana de join. Apoi scaneaza tabelul mai mare (probe side) si pentru fiecare rand cauta corespondenta in hash table cu un lookup O(1).

Complexitatea este liniara — proportionala cu suma randurilor din ambele tabele, nu cu produsul ca in nested loop. Nu sunt necesare indexuri: hash table-ul inlocuieste temporar indexul.

## Cand este alegerea corecta

Optimizatorul alege hash join cand ambele tabele sunt mari si nu exista indexuri utile, sau cand statisticile indica ca numarul de randuri de combinat este prea mare pentru un nested loop eficient. Este una dintre cele mai comune strategii in data warehouse-uri si rapoarte care agrega milioane de randuri.

## Ce poate merge prost

Punctul slab este memoria. Hash table-ul trebuie sa incapa in `work_mem`: daca tabelul mai mic nu incape, baza de date scrie loturi pe disc (batched hash join), cu o degradare semnificativa a performantei.

- **work_mem prea mic**: hash table-ul este impartit in loturi pe disc, multiplicand I/O-ul
- **Estimari gresite**: optimizatorul alege ca build side tabelul gresit pentru ca statisticile indica mai putine randuri decat realitatea
- **Skew in date**: daca o valoare in coloana de join domina majoritatea randurilor, un bucket al hash table-ului devine enorm in timp ce restul raman goale
