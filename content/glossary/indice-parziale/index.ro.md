---
title: "Index Parțial"
description: "Index PostgreSQL care acoperă doar o submulțime din rândurile tabelului, definit cu WHERE în CREATE INDEX. Reduce spațiul și timpul de mentenanță."
translationKey: "glossary_indice_parziale"
aka: "Partial Index"
articles:
  - "/posts/postgresql/postgresql-indici-quando-fanno-male"
---

Un **index parțial** (*partial index*) este un index PostgreSQL care acoperă doar o submulțime din rândurile tabelului, definit cu o clauză `WHERE` în `CREATE INDEX`. Rândurile care nu satisfac condiția nu sunt indexate și nu ocupă spațiu în index.

## Cum funcționează

Sintaxa e simplă:

```sql
CREATE INDEX idx_active
ON comenzi (data_creare)
WHERE stare = 'activ';
```

Indexul conține doar rândurile cu `stare = 'activ'`. Toate celelalte sunt ignorate. Planner-ul folosește acest index doar pentru interogări care includ aceeași condiție `WHERE stare = 'activ'` (sau o condiție mai restrictivă).

## La ce servește

Rezolvă un scenariu foarte comun: majoritatea interogărilor operative filtrează mereu pe o condiție (de ex. `activ = true`, `arhivat = false`, `data > x`), iar rândurile care nu satisfac acea condiție nu sunt căutate niciodată. Indexarea lor e o risipă.

Beneficiile concrete:

- **Spațiu**: indexul e mai mic, uneori cu mult. Pe un tabel unde 35% din rânduri sunt "active", indexul parțial ocupă 35% din spațiu.
- **Mentenanță**: mai puțină muncă pentru VACUUM, mai puțină write-amplification la INSERT/UPDATE pe rândurile excluse.
- **Performanță**: indexul e mai mic de parcurs și încape mai ușor în cache.

## Când se folosește

Se folosește când:

- Interogările operative filtrează sistematic pe o condiție binară
- Rândurile care nu satisfac condiția sunt multe (>50%) și nerelevante pentru workload-ul fierbinte
- Interogările pe cealaltă submulțime sunt rare și acceptabile cu un seq scan

Nu se folosește dacă interogările filtrează pe condiții dinamice sau variabile: planner-ul nu va folosi niciodată indexul parțial.
