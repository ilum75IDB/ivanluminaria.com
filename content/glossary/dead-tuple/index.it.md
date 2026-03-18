---
title: "Dead Tuple"
description: "Riga obsoleta in una tabella PostgreSQL, marcata come non più visibile dopo un UPDATE o DELETE ma non ancora rimossa fisicamente dal disco."
translationKey: "glossary_dead-tuple"
aka: "Tupla morta"
articles:
  - "/posts/postgresql/vacuum-autovacuum-postgresql"
---

Un **Dead Tuple** è una riga in una tabella PostgreSQL che è stata aggiornata (UPDATE) o cancellata (DELETE) ma non è ancora stata rimossa fisicamente. Resta nelle pagine dati, occupando spazio su disco e rallentando le scansioni.

## Come funziona

Quando PostgreSQL esegue un UPDATE, non sovrascrive la riga originale: crea una nuova versione e marca la vecchia come "morta". La vecchia riga resta fisicamente nella pagina dati finché il VACUUM non la pulisce. I dead tuples sono il prezzo del modello MVCC — necessari per garantire l'isolamento transazionale.

## A cosa serve

I dead tuples sono un indicatore chiave della salute di una tabella. La vista `pg_stat_user_tables` mostra `n_dead_tup` e `last_autovacuum` — se i dead tuples crescono più velocemente di quanto l'autovacuum riesca a pulire, la tabella ha un problema. Un dead_tuple_percent sopra il 20-30% è un segnale di allarme.

## Cosa può andare storto

Su una tabella con 500.000 update al giorno e il default di autovacuum (scale_factor 0.2), il VACUUM si attiva ogni 4 giorni. Nel frattempo i dead tuples si accumulano, le tabelle si gonfiano e le query rallentano progressivamente — il pattern "lunedì bene, venerdì disastro".
