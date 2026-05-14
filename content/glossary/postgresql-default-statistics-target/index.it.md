---
title: "default_statistics_target"
description: "Il parametro PostgreSQL che controlla la granularita' delle statistiche raccolte da ANALYZE (dimensione di MCV e istogramma)."
translationKey: "glossary_postgresql_default_statistics_target"
aka: "default_statistics_target (PostgreSQL)"
articles:
  - "/posts/postgresql/explain-analyze-postgresql"
---

**default_statistics_target** è il parametro PostgreSQL che controlla la **granularità delle statistiche** costruite da `ANALYZE` su ogni colonna. Il valore di default è 100.

## Come funziona

ANALYZE costruisce per ogni colonna due strutture statistiche usate dall'optimizer:

- **Most common values (MCV)**: la lista dei valori più frequenti con le rispettive frequenze
- **Istogramma**: la distribuzione dei valori rimanenti, divisa in bucket di uguale popolazione

`default_statistics_target` determina quanti elementi possono avere queste strutture. Con valore `100`: fino a 100 valori nella lista MCV e fino a 100 bucket nell'istogramma.

**Il numero di righe campionate è separato e dipende dal target**: vale circa `300 × default_statistics_target`. Con il default di 100, ANALYZE legge ~30.000 righe per colonna; con un target di 500, ~150.000. Quindi alzare il target aumenta sia la granularità delle statistiche **sia** il costo di ANALYZE.

## Quando aumentarlo

Per tabelle piccole o con distribuzione uniforme, 100 campioni sono sufficienti. Per tabelle grandi con distribuzione asimmetrica (skewed) — dove pochi valori dominano la maggior parte delle righe — 100 campioni possono dare una rappresentazione distorta, portando l'optimizer a stime di cardinalità sbagliate.

Si può aumentare il target a livello di singola colonna:

    ALTER TABLE orders ALTER COLUMN status SET STATISTICS 500;
    ANALYZE orders;

Valori tra 500 e 1000 migliorano sensibilmente la qualità delle stime su colonne con distribuzione non uniforme.

## Limiti pratici

Oltre 1000 il beneficio è marginale e l'`ANALYZE` stesso diventa più lento, perché deve campionare più righe e costruire strutture più grandi. È una regolazione fine: va applicata solo alle colonne che effettivamente causano stime errate, non a tutte le colonne di tutte le tabelle.
