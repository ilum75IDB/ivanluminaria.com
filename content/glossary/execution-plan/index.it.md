---
title: "Execution Plan (Piano di Esecuzione)"
description: "Cos'è un piano di esecuzione e come l'optimizer del database decide la strategia per eseguire una query."
translationKey: "glossary_execution_plan"
tags: ["glossario"]
---

Il piano di esecuzione è la sequenza di operazioni che il database sceglie per risolvere una query SQL. Quando scrivi una SELECT con JOIN, filtri WHERE e ordinamenti, l'optimizer valuta decine di strategie possibili — quale indice usare, quale tipo di join, in che ordine leggere le tabelle — e ne sceglie una basandosi sulle statistiche disponibili.

In PostgreSQL si visualizza con `EXPLAIN` (solo il piano stimato) o `EXPLAIN ANALYZE` (piano reale con tempi effettivi). Il piano è rappresentato come un albero di nodi: ogni nodo è un'operazione (scan, join, sort, aggregate) che riceve dati dai nodi figli e li passa al nodo padre.

La lettura corretta di un piano di esecuzione è la competenza più importante per il tuning delle query. Non basta guardare il tempo totale: bisogna confrontare le righe stimate con quelle reali nodo per nodo, verificare i buffer I/O e identificare dove l'optimizer ha fatto scelte sbagliate.

## Articoli correlati

- [EXPLAIN ANALYZE non basta: come leggere davvero un piano di esecuzione PostgreSQL](/it/posts/postgresql/explain-analyze-postgresql/)
