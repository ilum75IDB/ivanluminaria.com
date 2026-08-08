---
title: "Indice CONTEXT"
description: "Indice Oracle Text per la ricerca full-text su testo non strutturato: costruisce una struttura invertita token→documento su colonne CLOB."
translationKey: "glossary_indice_context"
aka: "CONTEXT index (Oracle Text)"
articles:
  - "/posts/oracle/oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente"
---

L'indice CONTEXT è il tipo di indice principale di Oracle Text, progettato per la ricerca full-text su colonne che contengono testo non strutturato: documenti, articoli, pareri legali, note tecniche. A differenza di un B-tree classico, non indicizza valori discreti ma token linguistici, costruendo una struttura invertita che mappa ogni parola ai documenti in cui compare.

## Come funziona

Durante la creazione, Oracle Text tokenizza il contenuto della colonna (tipicamente `CLOB`), applica filtri linguistici (stemming, stopword, thesaurus opzionale) e popola una serie di tabelle interne — `$I`, `$K`, `$R`, `$N` — che formano l'indice invertito. Le query usano l'operatore `CONTAINS` al posto del `LIKE`:

```sql
SELECT doc_id, SCORE(1) AS rilevanza
FROM documenti
WHERE CONTAINS(testo, 'contratto AND (locazione OR affitto)', 1) > 0
ORDER BY rilevanza DESC;
```

L'indice evita la scansione sequenziale dell'intera colonna CLOB a ogni query, riducendo drasticamente i tempi su dataset di grandi dimensioni.

## Quando si usa

L'indice CONTEXT è adatto quando:

- la colonna contiene testo lungo e variabile (documenti, PDF convertiti, XML);
- le query richiedono operatori booleani, prossimità o ricerca per concetto;
- il volume di dati rende impraticabile qualsiasi approccio basato su `LIKE '%...%'`.

Un limite operativo rilevante: l'indice CONTEXT **non si aggiorna in tempo reale**. Le righe inserite o modificate dopo la creazione dell'indice diventano ricercabili solo dopo una sincronizzazione esplicita (`CTX_DDL.SYNC_INDEX`) o tramite un job schedulato. Per scenari con scritture frequenti va pianificata una strategia di sync coerente con la latenza accettabile.
