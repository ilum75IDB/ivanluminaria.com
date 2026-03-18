---
title: "pg_trgm"
description: "Estensione PostgreSQL che fornisce funzioni e operatori per la ricerca di similarità basata su trigrammi, abilitando l'uso di indici GIN per LIKE con wildcard."
translationKey: "glossary_pg-trgm"
articles:
  - "/posts/postgresql/like-optimization-postgresql"
---

**pg_trgm** è un'estensione di PostgreSQL che implementa la ricerca basata su trigrammi — sequenze di tre caratteri consecutivi estratte dal testo. Abilita l'uso di indici GIN e GiST per accelerare ricerche `LIKE '%valore%'` e `ILIKE`, che altrimenti richiederebbero scansioni sequenziali.

## Come funziona

L'estensione scompone ogni stringa in trigrammi: ad esempio, "hello" diventa {"  h", " he", "hel", "ell", "llo", "lo "}. Un indice GIN con operator class `gin_trgm_ops` indicizza questi trigrammi. Quando si esegue un `LIKE '%ell%'`, PostgreSQL cerca i trigrammi corrispondenti nell'indice invece di scansionare l'intera tabella.

## A cosa serve

pg_trgm risolve uno dei problemi più comuni in PostgreSQL: la ricerca "contiene" su colonne di testo grandi. Senza pg_trgm, un `LIKE '%valore%'` su una tabella di milioni di righe richiede una scansione completa. Con pg_trgm e un indice GIN, la stessa ricerca usa l'indice e risponde in millisecondi.

## Quando si usa

Si attiva con `CREATE EXTENSION IF NOT EXISTS pg_trgm` e si crea l'indice con `USING gin (colonna gin_trgm_ops)`. È ideale su tabelle con basso churn (pochi UPDATE/DELETE). La creazione dell'indice va fatta con `CONCURRENTLY` in produzione per evitare lock.
