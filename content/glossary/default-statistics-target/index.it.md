---
title: "default_statistics_target"
description: "Il parametro PostgreSQL che controlla quanti campioni l'optimizer raccoglie per stimare la distribuzione dei dati in una colonna."
translationKey: "glossary_default_statistics_target"
tags: ["glossario"]
---

`default_statistics_target` è il parametro PostgreSQL che definisce il numero di campioni raccolti dal comando ANALYZE per costruire le statistiche di ogni colonna. Il valore di default è 100, che significa che PostgreSQL campiona 100 valori per costruire istogrammi e liste di valori frequenti.

Per tabelle piccole o con distribuzione uniforme, 100 campioni sono sufficienti. Per tabelle grandi con distribuzione asimmetrica (skewed) — dove pochi valori dominano la maggior parte delle righe — 100 campioni possono dare una rappresentazione distorta, portando l'optimizer a stime di cardinalità sbagliate.

Si può aumentare il target a livello di singola colonna con `ALTER TABLE ... ALTER COLUMN ... SET STATISTICS N`. Valori tra 500 e 1000 migliorano sensibilmente la qualità delle stime su colonne con distribuzione non uniforme. Oltre 1000 il beneficio è marginale e l'ANALYZE stesso diventa più lento. È una regolazione fine che fa la differenza nelle query con join complessi su tabelle con milioni di righe.

## Articoli correlati

- [EXPLAIN ANALYZE non basta: come leggere davvero un piano di esecuzione PostgreSQL](/it/posts/postgresql/explain-analyze-postgresql/)
