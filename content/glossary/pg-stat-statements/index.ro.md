---
title: "pg_stat_statements"
description: "Extensie PostgreSQL care colectează statistici de execuție pentru toate query-urile SQL, instrument fundamental pentru diagnosticarea performanței."
translationKey: "glossary_pg-stat-statements"
aka: "pgss"
articles:
  - "/posts/postgresql/pg-stat-statements"
---

**pg_stat_statements** este o extensie PostgreSQL — inclusă în distribuția oficială dar neactivă implicit — care ține evidența statisticilor de execuție pentru toate query-urile SQL care trec prin server. Query-urile sunt normalizate (valorile literale înlocuite cu parametri) pentru a grupa execuțiile aceluiași pattern.

## Cum funcționează

Extensia necesită încărcarea ca shared library la pornirea serverului prin parametrul `shared_preload_libraries`. Odată activă, înregistrează pentru fiecare query: numărul de execuții, timpul total și mediu, rândurile returnate, blocurile citite de pe disc și din cache. Parametrul `pg_stat_statements.max` controlează câte query-uri distincte sunt urmărite (implicit 5000).

## La ce servește

Este instrumentul principal pentru identificarea query-urilor celor mai costisitoare pe un server PostgreSQL. Sortând după `total_exec_time` se obține imediat clasamentul query-urilor care consumă cele mai multe resurse. Combinat cu EXPLAIN ANALYZE, permite un workflow diagnostic complet: pg_stat_statements identifică problema, EXPLAIN explică cauza.

## Când se folosește

Ar trebui să fie activ pe orice instalare PostgreSQL de producție. Overhead-ul este neglijabil (1-2% CPU). Fără pg_stat_statements, orice activitate de performance tuning se bazează pe presupuneri în loc de date.
