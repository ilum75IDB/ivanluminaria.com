---
title: "ANALYZE"
description: "Il comando PostgreSQL che aggiorna le statistiche delle tabelle usate dall'optimizer per scegliere il piano di esecuzione."
translationKey: "glossary_analyze"
tags: ["glossario"]
---

`ANALYZE` è il comando PostgreSQL che raccoglie statistiche sulla distribuzione dei dati nelle tabelle e le salva nel catalogo `pg_statistic` (leggibile tramite la vista `pg_stats`). L'optimizer usa queste statistiche per stimare la cardinalità — quante righe restituirà ogni operazione — e scegliere il piano di esecuzione più efficiente.

Le statistiche raccolte includono: valori più frequenti (most common values), istogrammi di distribuzione, numero di valori distinti e percentuale di NULL per ogni colonna. Senza statistiche aggiornate, l'optimizer è costretto a indovinare, e le stime sbagliate portano a piani di esecuzione disastrosi — come scegliere un nested loop su milioni di righe pensando che siano centinaia.

PostgreSQL esegue ANALYZE automaticamente tramite l'autovacuum, ma la soglia di default (50 righe + 10% delle righe vive) può essere troppo alta per tabelle che crescono rapidamente. Dopo import massivi o cambiamenti significativi nella distribuzione dei dati, un ANALYZE manuale è la prima azione diagnostica da fare.

## Articoli correlati

- [EXPLAIN ANALYZE non basta: come leggere davvero un piano di esecuzione PostgreSQL](/it/posts/postgresql/explain-analyze-postgresql/)
