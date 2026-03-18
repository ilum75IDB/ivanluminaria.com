---
title: "Hash Join"
description: "Come funziona l'hash join e perché è la scelta migliore per join su grandi volumi di dati."
translationKey: "glossary_hash_join"
tags: ["glossario"]
---

L'hash join è una strategia di join progettata per grandi volumi di dati. Funziona in due fasi: prima il database legge la tabella più piccola e costruisce una hash table in memoria, indicizzando le righe per la colonna di join. Poi scansiona la tabella più grande e per ogni riga cerca la corrispondenza nella hash table con un lookup O(1).

Il vantaggio è che non servono indici e la complessità è lineare — proporzionale alla somma delle righe delle due tabelle, non al prodotto come nel nested loop. Lo svantaggio è che richiede memoria per la hash table: se la tabella più piccola non sta in `work_mem`, il database deve scrivere batch su disco (batched hash join), rallentando l'operazione.

L'optimizer sceglie l'hash join quando entrambe le tabelle sono grandi e non ci sono indici utili, oppure quando le statistiche indicano che il numero di righe da combinare è troppo alto per un nested loop efficiente. È una delle strategie più comuni nei data warehouse e nei report che aggregano milioni di righe.

## Articoli correlati

- [EXPLAIN ANALYZE non basta: come leggere davvero un piano di esecuzione PostgreSQL](/it/posts/postgresql/explain-analyze-postgresql/)
