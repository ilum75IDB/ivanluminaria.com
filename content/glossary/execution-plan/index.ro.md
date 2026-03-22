---
title: "Execution Plan"
description: "Plan de executie — secventa de operatii aleasa de optimizatorul bazei de date pentru a rezolva o interogare SQL."
translationKey: "glossary_execution_plan"
aka: "Plan de Executie"
articles:
  - "/posts/postgresql/explain-analyze-postgresql"
  - "/posts/postgresql/pg-stat-statements"
---

Un **execution plan** (plan de executie) este secventa de operatii pe care baza de date o alege pentru a rezolva o interogare SQL. Cand scrii un SELECT cu JOIN-uri, filtre WHERE si sortari, optimizatorul evalueaza zeci de strategii posibile si alege una pe baza statisticilor disponibile.

## Cum functioneaza

Planul este reprezentat ca un arbore de noduri: fiecare nod este o operatie (scan, join, sort, aggregate) care primeste date de la nodurile copil si le transmite nodului parinte. In PostgreSQL se vizualizeaza cu `EXPLAIN` (plan estimat) sau `EXPLAIN ANALYZE` (plan real cu timpii efectivi si contoarele de randuri).

Optimizatorul decide pentru fiecare nod ce strategie sa foloseasca: sequential scan sau index scan pentru accesul la tabele, nested loop, hash join sau merge join pentru jonctiuni, sort sau hash pentru grupari.

## De ce conteaza

Citirea corecta a unui plan de executie este cea mai importanta competenta pentru optimizarea interogarilor. Nu este suficient sa te uiti la timpul total: trebuie sa compari randurile estimate cu cele reale nod cu nod, sa verifici bufferele de I/O si sa identifici unde optimizatorul a facut alegeri gresite.

O estimare eronata chiar si pe un singur nod se poate propaga in cascada pe intregul plan, transformand o interogare de milisecunde intr-una de minute.

## Ce poate merge prost

Cele mai frecvente probleme in planurile de executie:

- **Estimari de cardinalitate gresite**: optimizatorul crede ca un tabel returneaza 100 de randuri si ajung 2 milioane
- **Join gresit**: un nested loop ales acolo unde era nevoie de un hash join, din cauza statisticilor invechite
- **Index ignorat**: un sequential scan pe un tabel mare pentru ca statisticile nu reflecta distributia reala a datelor
- **Spill pe disc**: operatii de sort sau hash care nu incap in `work_mem` si sfarsesc prin a scrie pe disc
