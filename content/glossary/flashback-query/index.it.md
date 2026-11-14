---
title: "Flashback Query"
description: "Funzionalità Oracle che permette di interrogare uno stato passato del database tramite timestamp o SCN, sfruttando i dati di undo."
translationKey: "glossary_flashback_query"
aka: "Oracle Flashback Query"
articles:
  - "/posts/oracle/oracle-flashback-recupero-dati-logici-senza-downtime-da-query-a-database"
---

Flashback Query è una funzionalità di Oracle Database che consente di eseguire una `SELECT` su uno stato passato dei dati, specificando un punto nel tempo tramite timestamp o System Change Number (SCN). Non richiede restore da backup né downtime: i dati storici vengono letti direttamente dai segmenti di undo.

## Come funziona

Oracle mantiene le versioni precedenti dei blocchi dati nei tablespace di undo per un periodo configurabile (`UNDO_RETENTION`). Flashback Query sfrutta questo meccanismo per ricostruire la vista dei dati com'era in un momento specifico.

```sql
-- Interrogazione tramite timestamp
SELECT *
FROM ordini AS OF TIMESTAMP (SYSTIMESTAMP - INTERVAL '2' HOUR)
WHERE stato = 'ANNULLATO';

-- Interrogazione tramite SCN
SELECT *
FROM ordini AS OF SCN 4521890;
```

La clausola `AS OF` è disponibile su qualsiasi `SELECT`, incluse query con JOIN e subquery.

## Quando si usa

Gli scenari tipici sono il recupero di righe cancellate o modificate per errore, l'analisi di dati prima di una transazione problematica e la verifica di cosa conteneva una tabella prima di un batch notturno. Il limite principale è la disponibilità dei dati di undo: se `UNDO_RETENTION` è basso o il tablespace di undo è sotto pressione, Oracle può sovrascrivere i blocchi storici prima del tempo configurato. Per finestre temporali più ampie o per interrogare l'intera cronologia delle modifiche riga per riga, si ricorre a Flashback Versions Query o Flashback Data Archive.
