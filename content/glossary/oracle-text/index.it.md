---
title: "Oracle Text"
description: "Componente Oracle Database per l'indicizzazione e la ricerca full-text su colonne CLOB, BLOB e VARCHAR2, senza licenza separata."
translationKey: "glossary_oracle_text"
aka: "Oracle Text (Oracle interMedia Text, ConText)"
articles:
  - "/posts/oracle/oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente"
---

Oracle Text è il motore di ricerca full-text integrato in Oracle Database. Permette di indicizzare e interrogare grandi volumi di testo strutturato e non strutturato direttamente all'interno del database, senza dipendenze esterne e senza licenza aggiuntiva rispetto alla Standard o Enterprise Edition.

## Come funziona

Oracle Text costruisce indici specializzati (di tipo `CONTEXT`, `CTXCAT`, `CTXRULE` o `CTXPATH`) sulle colonne testuali. L'indice `CONTEXT` è il più comune: tokenizza il testo, applica stemming e stoplist, e memorizza le posizioni dei token in strutture interne ottimizzate per la ricerca.

Le query avvengono tramite l'operatore `CONTAINS` nella clausola `WHERE`:

```sql
SELECT doc_id, title
FROM documents
WHERE CONTAINS(body, 'database AND performance', 1) > 0
ORDER BY SCORE(1) DESC;
```

L'indice va sincronizzato manualmente o schedulato con `CTX_DDL.SYNC_INDEX` dopo operazioni DML, perché non è transazionale in tempo reale.

## Quando si usa

Oracle Text è indicato quando:

- il volume di testo supera quello gestibile con `LIKE` o `REGEXP_LIKE` senza degrado delle prestazioni;
- servono funzionalità avanzate come ricerca per prossimità, fuzzy matching, espansione tematica o highlight dei risultati;
- i documenti risiedono già in Oracle Database e spostare i dati verso un motore esterno (Elasticsearch, Solr) introdurrebbe complessità architetturale non giustificata.

Il limite principale è la sincronizzazione dell'indice: in scenari ad alto tasso di scrittura, il lag tra DML e aggiornamento dell'indice va pianificato esplicitamente.
