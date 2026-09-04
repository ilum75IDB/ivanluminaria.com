---
title: "Staging Table"
description: "Tabella temporanea che funge da area di atterraggio per i dati grezzi in un processo ETL, separando l'ingestione dalla trasformazione e dal caricamento finale."
translationKey: "glossary_staging_table"
aka: "Staging area, landing table"
articles:
  - "/posts/data-warehouse/etl-oracle-da-4-ore-a-25-minuti-con-staging-tables-merge-e-parallel-dml"
---

Una staging table è una tabella intermedia che riceve i dati grezzi dalla sorgente prima che vengano trasformati e caricati nella destinazione finale. Separa nettamente le tre fasi di un processo ETL, rendendo ogni fase indipendente, monitorabile e riprendibile in caso di errore.

## Come funziona

I dati vengono prima copiati in blocco nella staging table — spesso senza vincoli di integrità referenziale per massimizzare la velocità di INSERT — e solo in un secondo momento vengono applicati i controlli di qualità, le trasformazioni e il MERGE verso le tabelle di destinazione.

```sql
-- 1. Caricamento grezzo nella staging table (nessun vincolo attivo)
INSERT /*+ APPEND */ INTO stg_orders
SELECT * FROM ext_orders_source;

-- 2. Trasformazione e MERGE nella tabella di destinazione
MERGE INTO orders tgt
USING stg_orders src
  ON (tgt.order_id = src.order_id)
WHEN MATCHED THEN UPDATE SET tgt.status = src.status
WHEN NOT MATCHED THEN INSERT (order_id, status) VALUES (src.order_id, src.status);
```

Lavorare in bulk sulla staging table invece che riga per riga riduce drasticamente il numero di COMMIT e il carico sul redo log.

## Quando si usa

Le staging table sono indicate ogni volta che il volume di dati rende impraticabile la trasformazione in-flight durante l'ingestione. Sono particolarmente utili quando:

- il processo ETL deve essere riprendibile (basta ripartire dall'ultimo TRUNCATE/INSERT sulla staging);
- la sorgente è un sistema esterno che non tollera query lente o transazioni lunghe;
- si vuole applicare Parallel DML sulla fase di MERGE senza bloccare la sorgente.

Il trade-off principale è lo spazio disco aggiuntivo e la latenza introdotta dalla doppia scrittura, accettabile in quasi tutti i contesti batch.
