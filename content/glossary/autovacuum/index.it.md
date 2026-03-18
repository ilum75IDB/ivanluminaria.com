---
title: "Autovacuum"
description: "Daemon PostgreSQL che esegue automaticamente VACUUM e ANALYZE sulle tabelle quando il numero di dead tuples supera una soglia configurabile."
translationKey: "glossary_autovacuum"
aka: "Autovacuum Daemon"
articles:
  - "/posts/postgresql/vacuum-autovacuum-postgresql"
---

L'**Autovacuum** è un daemon di PostgreSQL che esegue automaticamente VACUUM e ANALYZE sulle tabelle quando il numero di dead tuples supera una soglia calcolata come: `threshold + scale_factor × n_live_tup`. Con i default (threshold=50, scale_factor=0.2), su una tabella con 10 milioni di righe si attiva dopo 2 milioni di dead tuples.

## Come funziona

Il daemon controlla periodicamente `pg_stat_user_tables` e lancia un worker per ogni tabella che supera la soglia. Il numero massimo di worker simultanei è controllato da `autovacuum_max_workers` (default 3). Il parametro `autovacuum_vacuum_cost_delay` controlla quanto il vacuum rallenta sé stesso per non sovraccaricare l'I/O.

## A cosa serve

È il custode silenzioso che impedisce alle tabelle di gonfiarsi per accumulo di dead tuples. Non va mai disabilitato — è la peggior cosa che si possa fare a un PostgreSQL in produzione. Va configurato per tabella: le tabelle ad alto traffico necessitano scale_factor bassi (0.01-0.05) e cost_delay ridotti.

## Cosa può andare storto

Con i default, l'autovacuum è troppo conservativo per tabelle ad alto traffico. 3 worker per decine di tabelle attive non bastano. Lo scale_factor al 20% su tabelle grandi genera milioni di dead tuples prima dell'intervento. Il tuning per-tabella con `ALTER TABLE ... SET (autovacuum_vacuum_scale_factor = 0.01)` è essenziale.
