---
title: "Nested Loop"
description: "Nested Loop Join — strategia di join che scansiona la tabella interna per ogni riga della tabella esterna, ideale per dataset piccoli con indice."
translationKey: "glossary_nested_loop"
aka: "Nested Loop Join"
articles:
  - "/posts/postgresql/explain-analyze-postgresql"
---

**Nested loop** è la strategia di join più semplice: per ogni riga della tabella esterna, il database cerca le righe corrispondenti nella tabella interna. Funziona come un doppio ciclo `for` annidato — da qui il nome.

## Come funziona

L'optimizer sceglie una tabella come "esterna" (outer) e una come "interna" (inner). Per ogni riga della tabella esterna, esegue una ricerca nella tabella interna sulla colonna di join. Se la tabella interna ha un indice sulla colonna di join, ogni ricerca è un accesso diretto via B-tree. Senza indice, ogni ricerca diventa un sequential scan completo.

## Quando è la scelta giusta

Il nested loop è imbattibile quando la tabella esterna ha poche righe e la tabella interna ha un indice sulla colonna di join. Un join su 100 righe esterne con un indice B-tree sulla tabella interna è praticamente istantaneo: poche iterazioni, accesso diretto, memoria minima.

È anche la strategia preferita per le lookup sulle dimensioni nei data warehouse, dove si unisce una fact table filtrata (poche righe) con una dimension table indicizzata.

## Cosa può andare storto

Diventa un disastro quando l'optimizer lo sceglie su dataset grandi per errore — tipicamente perché le statistiche sottostimano il numero di righe. Un nested loop su 2 milioni di righe esterne significa 2 milioni di lookup nella tabella interna. Senza indice, ogni lookup è uno scan completo.

In questi casi un hash join o un merge join sarebbero ordini di grandezza più veloci. La causa è quasi sempre una stima di cardinalità sbagliata: statistiche obsolete o `default_statistics_target` troppo basso.
