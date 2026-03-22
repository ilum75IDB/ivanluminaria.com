---
title: "pg_stat_statements"
description: "Estensione PostgreSQL che raccoglie statistiche di esecuzione per tutte le query SQL, strumento fondamentale per la diagnostica delle performance."
translationKey: "glossary_pg-stat-statements"
aka: "pgss"
articles:
  - "/posts/postgresql/pg-stat-statements"
---

**pg_stat_statements** è un'estensione di PostgreSQL — inclusa nella distribuzione ufficiale ma non attiva di default — che tiene traccia delle statistiche di esecuzione di tutte le query SQL che passano dal server. Le query vengono normalizzate (i valori letterali sostituiti con parametri) per raggruppare le esecuzioni dello stesso pattern.

## Come funziona

L'estensione richiede di essere caricata come shared library all'avvio del server tramite il parametro `shared_preload_libraries`. Una volta attiva, registra per ogni query: numero di esecuzioni, tempo totale e medio, righe restituite, blocchi letti da disco e da cache. Il parametro `pg_stat_statements.max` controlla quante query distinte vengono tracciate (default 5000).

## A cosa serve

È lo strumento principale per identificare le query più costose su un server PostgreSQL. Ordinando per `total_exec_time` si ottiene immediatamente la classifica delle query che consumano più risorse. Combinato con EXPLAIN ANALYZE, permette un workflow diagnostico completo: pg_stat_statements identifica il problema, EXPLAIN spiega la causa.

## Quando si usa

Dovrebbe essere attivo su qualsiasi installazione PostgreSQL di produzione. L'overhead è trascurabile (1-2% di CPU). Senza pg_stat_statements, qualsiasi attività di performance tuning si basa su ipotesi anziché su dati.
