---
title: "Nested Loop (Join)"
description: "Come funziona il nested loop join e quando l'optimizer lo sceglie — o lo sceglie per errore."
translationKey: "glossary_nested_loop"
tags: ["glossario"]
---

Il nested loop è la strategia di join più semplice: per ogni riga della tabella esterna, il database cerca le righe corrispondenti nella tabella interna. È come un doppio ciclo for annidato — da qui il nome.

È la scelta ideale quando la tabella esterna ha poche righe e la tabella interna ha un indice sulla colonna di join. In questo scenario, il nested loop è imbattibile: poche iterazioni, accesso diretto via indice, memoria minima. Un join su 100 righe esterne con un indice B-tree sulla tabella interna è praticamente istantaneo.

Diventa un disastro quando l'optimizer lo sceglie su dataset grandi per errore — tipicamente perché le statistiche sottostimano il numero di righe. Un nested loop su 2 milioni di righe esterne significa 2 milioni di lookup nella tabella interna, e senza indice ogni lookup è uno scan completo. In questi casi, un hash join o un merge join sarebbero ordini di grandezza più veloci.

## Articoli correlati

- [EXPLAIN ANALYZE non basta: come leggere davvero un piano di esecuzione PostgreSQL](/it/posts/postgresql/explain-analyze-postgresql/)
