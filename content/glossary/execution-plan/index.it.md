---
title: "Execution Plan"
description: "Piano di esecuzione — la sequenza di operazioni scelta dal database optimizer per risolvere una query SQL."
translationKey: "glossary_execution_plan"
aka: "Piano di Esecuzione"
articles:
  - "/posts/postgresql/explain-analyze-postgresql"
  - "/posts/postgresql/pg-stat-statements"
---

**Execution plan** (piano di esecuzione) è la sequenza di operazioni che il database sceglie per risolvere una query SQL. Quando scrivi una SELECT con JOIN, filtri WHERE e ordinamenti, l'optimizer valuta decine di strategie possibili e ne sceglie una basandosi sulle statistiche disponibili.

## Come funziona

Il piano è rappresentato come un albero di nodi: ogni nodo è un'operazione (scan, join, sort, aggregate) che riceve dati dai nodi figli e li passa al nodo padre. In PostgreSQL si visualizza con `EXPLAIN` (piano stimato) o `EXPLAIN ANALYZE` (piano reale con tempi effettivi e conteggi righe).

L'optimizer decide per ogni nodo quale strategia usare: sequential scan o index scan per l'accesso alle tabelle, nested loop, hash join o merge join per le giunzioni, sort o hash per i raggruppamenti.

## Perché è importante

La lettura corretta di un piano di esecuzione è la competenza più importante per il tuning delle query. Non basta guardare il tempo totale: bisogna confrontare le righe stimate con quelle reali nodo per nodo, verificare i buffer I/O e identificare dove l'optimizer ha fatto scelte sbagliate.

Una stima errata anche di un solo nodo può propagarsi a cascata su tutto il piano, trasformando una query da millisecondi a minuti.

## Cosa può andare storto

I problemi più frequenti nei piani di esecuzione:

- **Stime di cardinalità sbagliate**: l'optimizer pensa che una tabella restituisca 100 righe e ne arrivano 2 milioni
- **Join sbagliato**: un nested loop scelto dove serviva un hash join, a causa di statistiche obsolete
- **Indice ignorato**: un sequential scan su una tabella grande perché le statistiche non riflettono la distribuzione reale dei dati
- **Spill su disco**: operazioni di sort o hash che non stanno in `work_mem` e finiscono su disco
