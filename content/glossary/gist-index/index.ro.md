---
title: "GiST Index"
description: "Generalized Search Tree — familie de indexuri PostgreSQL pentru date cu structură geometrică, de intervale sau similaritate, indispensabilă pentru interogări spațiale și pe intervale."
translationKey: "glossary_gist_index"
aka: "Generalized Search Tree"
articles:
  - "/posts/postgresql/postgresql-indici-quando-fanno-male"
---

**GiST** (*Generalized Search Tree*) este o familie de indexuri PostgreSQL gândită pentru date care nu pot fi ordonate liniar: geometrii, intervale, vectori de similaritate, full-text. Este un arbore echilibrat care organizează datele pe *bounding box-uri* ierarhice în loc de ordonare lexicografică.

## Cum funcționează

În timp ce un B-tree ordonează valorile de la "minim" la "maxim" și face căutare dihotomică, GiST grupează datele în regiuni (bounding box-uri) imbricate. Fiecare nod al arborelui reprezintă o regiune care conține toate datele din copiii săi. Când se caută o valoare, GiST elimină regiuni întregi cu o comparație de suprapunere — fără să coboare în nodurile care nu pot conține rezultatul.

Această structură permite indexarea:

- **Geometriilor**: puncte, poligoane, linii (cu PostGIS)
- **Intervalelor**: `int4range`, `tsrange`, `daterange` și alte tipuri range
- **Full-text**: vectori `tsvector` pentru căutare textuală
- **Similarității**: cu extensii precum `pg_trgm` pentru căutări aproximative

## La ce servește

Rezolvă interogări "spațiale" sau pe intervale pe care un B-tree nu le poate gestiona:

- Găsește toate punctele într-un dreptunghi sau rază
- Găsește toate înregistrările cu un interval care se suprapune cu alt interval
- Găsește texte similare cu o interogare, chiar și cu erori de tastare
- Caută prin containment: `range1 @> range2` sau `geom1 && geom2`

## Când se folosește

Se folosește cu `CREATE INDEX ... USING GIST (coloana)`. Este complementul natural al GIN: GIN pentru containment de array-uri/JSONB, GiST pentru geometrie/intervale/similaritate. Pe tabele cu mult churn are cost de scriere similar cu GIN — deci trebuie evaluat de la caz la caz.
