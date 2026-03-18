---
title: "GIN Index"
description: "Generalized Inverted Index — tipo di indice PostgreSQL ottimizzato per ricerche full-text, pattern matching con trigrammi e query su array e JSONB."
translationKey: "glossary_gin-index"
aka: "Generalized Inverted Index"
articles:
  - "/posts/postgresql/like-optimization-postgresql"
---

Un **GIN Index** (Generalized Inverted Index) è un tipo di indice PostgreSQL progettato per indicizzare valori composti: array, documenti JSONB, testo con trigrammi e ricerche full-text. A differenza del B-Tree, un GIN crea un mapping inverso: da ogni elemento (parola, trigramma, chiave JSON) ai record che lo contengono.

## Come funziona

Per ogni valore distinto nel dato indicizzato, il GIN mantiene una lista di puntatori alle righe che contengono quel valore. Nel caso di `pg_trgm`, il testo viene scomposto in trigrammi (sequenze di 3 caratteri) e ogni trigramma viene indicizzato. Una ricerca `LIKE '%ABC%'` viene tradotta in un'intersezione di trigrammi, evitando la scansione sequenziale.

## A cosa serve

GIN risolve il problema delle ricerche "contiene" (`LIKE '%valore%'`) su colonne di testo, che con un B-Tree richiederebbero una scansione sequenziale dell'intera tabella. Su tabelle di milioni di righe, la differenza è tra secondi e millisecondi.

## Quando si usa

GIN è ideale su tabelle append-only o con basso churn (pochi UPDATE/DELETE), perché il costo di manutenzione dell'indice è più alto rispetto a un B-Tree. La creazione in produzione va fatta con `CREATE INDEX CONCURRENTLY` per evitare lock sulle scritture.
