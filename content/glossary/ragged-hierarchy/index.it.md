---
title: "Ragged hierarchy"
description: "Gerarchia in cui non tutti i rami raggiungono la stessa profondità: alcuni livelli intermedi sono assenti."
translationKey: "glossary_ragged_hierarchy"
aka: "Gerarchia sbilanciata, Unbalanced hierarchy"
articles:
  - "/posts/data-warehouse/ragged-hierarchies"
---

Una **ragged hierarchy** (gerarchia sbilanciata) è una struttura gerarchica in cui non tutti i rami raggiungono la stessa profondità. Alcuni livelli intermedi sono assenti per determinate entità.

## Esempio concreto

In una gerarchia a tre livelli Top Group → Group → Client:

- Alcuni clienti hanno tutti e tre i livelli (gerarchia completa)
- Alcuni clienti hanno un Group ma nessun Top Group
- Alcuni clienti non hanno né Group né Top Group (clienti diretti)

Il risultato è una struttura con "buchi" che causa problemi nei report di aggregazione: righe con NULL, totali spezzati, drill-down incompleti.

## Perché è un problema nel DWH

I tool di BI e le query SQL si aspettano gerarchie complete per funzionare correttamente. Un GROUP BY su una colonna con NULL produce risultati inattesi: le righe con NULL vengono raggruppate separatamente, i totali non tornano, e lo stesso gruppo può apparire su più righe.

## Come si risolve

La tecnica standard è il **self-parenting**: chi non ha un padre diventa padre di sé stesso. Questo bilancia la gerarchia a monte, nell'ETL, eliminando i NULL dalla tabella dimensionale. Flag aggiuntivi (`is_direct_client`, `is_standalone_group`) permettono di distinguere le entità bilanciate artificialmente da quelle con gerarchia naturale.
