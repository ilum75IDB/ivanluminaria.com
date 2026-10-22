---
title: "PGA (Program Global Area)"
description: "PGA este zona de memorie privată alocată de Oracle per sesiune. O configurare greșită degradează silențios operațiile de sort și hash join, îngreunând diagnosticarea."
translationKey: "glossary_pga"
aka: "Program Global Area"
articles:
  - "/posts/oracle/ai-mostra-sintomo-board-chiede-causa"
---

PGA (Program Global Area) este o zonă de memorie privată pe care Oracle o alocă pentru fiecare proces server sau sesiune. Spre deosebire de SGA (System Global Area), partajată între toate sesiunile, PGA este exclusivă: conține spațiul de lucru pentru operații de sort, hash join, bitmap merge și variabilele de sesiune.

## Cum funcționează

Oracle gestionează PGA în mod automat (`PGA_AGGREGATE_TARGET`) sau manual. În modul automat, baza de date estimează memoria disponibilă și o distribuie între sesiunile active. Când PGA alocată depășește ținta, Oracle scrie datele pe disc (temp tablespace), degradând performanța.

```sql
-- Verificarea configurației curente a PGA
SELECT name, value
FROM v$pgastat
WHERE name IN (
  'aggregate PGA target parameter',
  'aggregate PGA auto target',
  'total PGA inuse',
  'cache hit percentage'
);
```

Parametrul `WORKAREA_SIZE_POLICY` controlează dacă gestionarea este `AUTO` sau `MANUAL`. În modul manual, parametri precum `SORT_AREA_SIZE` și `HASH_AREA_SIZE` definesc limitele per sesiune.

## Context operațional

O PGA subdimensionată produce spill frecvent pe disc: interogările cu ORDER BY, GROUP BY sau hash join devin lente fără ca alertele standard (CPU, I/O agregat) să indice clar cauza. Degradarea se corelează de obicei cu vârfuri de sesiuni concurente, nu cu interogări individuale.

O PGA modificată fără înregistrare în change log reprezintă una dintre cauzele cele mai greu de depistat în regresiile de performanță: simptomul apare în producție, dar originea se regăsește într-o modificare de parametru efectuată cu săptămâni înainte — exact scenariul în care instrumentele de observability singure nu sunt suficiente.
