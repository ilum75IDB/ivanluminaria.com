---
title: "Indice CTXXPATH"
description: "Indice Oracle Text per documenti XML o JSON in CLOB/BLOB: preserva la gerarchia dei path e consente query su nodi specifici."
translationKey: "glossary_indice_ctxxpath"
aka: "CTXXPATH index (Oracle Text)"
articles:
  - "/posts/oracle/oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente"
---

L'indice CTXXPATH è un tipo specializzato di Oracle Text progettato per documenti XML o JSON archiviati in colonne `CLOB` o `BLOB`. A differenza degli indici full-text generici, CTXXPATH mantiene la struttura gerarchica del documento durante l'indicizzazione, rendendo possibile limitare le ricerche a path o nodi specifici anziché cercare sull'intero contenuto testuale.

## Come funziona

La creazione avviene con `CREATE INDEX ... INDEXTYPE IS CTXSYS.CTXXPATH`. Oracle Text analizza il documento, costruisce una mappa dei path XML/JSON e indicizza sia il contenuto testuale sia la posizione strutturale di ogni nodo.

```sql
CREATE INDEX idx_doc_xml
ON documenti(contenuto_xml)
INDEXTYPE IS CTXSYS.CTXXPATH;
```

Le query sfruttano poi la funzione `existsNode` o l'operatore `CONTAINS` con la sintassi path-aware per circoscrivere la ricerca:

```sql
SELECT id
FROM documenti
WHERE existsNode(contenuto_xml, '/fattura/cliente[nome="Rossi"]') = 1;
```

## Quando si usa

CTXXPATH è la scelta corretta quando i documenti hanno una struttura XML o JSON significativa e le query devono distinguere tra nodi con lo stesso valore testuale ma posizioni diverse nel documento. Scenari tipici: archivi di fatture elettroniche, cataloghi prodotto in XML, payload JSON eterogenei.

Il limite principale è la dipendenza dal formato: il documento deve essere XML o JSON ben formato. Per testo non strutturato conviene `CTXSYS.CONTEXT`; per ricerche puramente strutturali (senza full-text) bastano gli indici relazionali standard su colonne estratte con `XMLTable` o `JSON_TABLE`.
