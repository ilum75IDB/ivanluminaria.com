---
title: "Indice CATSEARCH"
description: "Indice Oracle Text per archivi misti: risolve predicati SQL su attributi strutturati e ricerca full-text in un'unica operazione dentro l'indice."
translationKey: "glossary_indice_catsearch"
aka: "CATSEARCH index, Oracle Text CATSEARCH"
articles:
  - "/posts/oracle/oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente"
---

L'indice CATSEARCH è un tipo specializzato di Oracle Text progettato per domini in cui ogni documento porta con sé attributi strutturati — mittente, data, categoria, stato — e testo libero da ricercare contemporaneamente. A differenza di un approccio ibrido che combina un indice B-tree su colonne strutturate con un indice full-text separato, CATSEARCH fonde entrambe le dimensioni in un'unica struttura.

## Come funziona

L'indice viene creato con `CTXSYS.CTXCAT` come tipo di indice e accetta una lista di colonne strutturate da includere nella sub-index. Oracle Text costruisce internamente un catalogo che indicizza sia i token testuali sia i valori delle colonne aggiuntive.

```sql
CREATE INDEX idx_doc_catsearch
ON documenti(testo)
INDEXTYPE IS CTXSYS.CTXCAT
PARAMETERS ('CTXCAT_INDEX_SET myindexset');
```

La query usa l'operatore `CATSEARCH` al posto del classico `CONTAINS`:

```sql
SELECT id, titolo
FROM documenti
WHERE CATSEARCH(testo, 'fattura AND scaduta', 'categoria = ''contabilita''') > 0;
```

Il predicato strutturale (`categoria = 'contabilita'`) viene risolto dentro l'indice, non come filtro post-scan.

## Quando si usa

CATSEARCH è indicato per archivi documentali con cardinalità medio-alta sulle colonne strutturate e query che combinano sistematicamente filtri su attributi e ricerca testuale: sistemi di ticketing, archivi email, repository di contratti. Non è adatto a scenari di ricerca full-text pura senza predicati strutturali, dove `CONTEXT` (con `CONTAINS`) offre funzionalità linguistiche più ricche. La sincronizzazione dell'indice richiede attenzione: come tutti gli indici Oracle Text, CATSEARCH non si aggiorna in tempo reale senza una policy di sync esplicita.
