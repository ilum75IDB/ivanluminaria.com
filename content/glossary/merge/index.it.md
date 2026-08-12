---
title: "MERGE"
description: "Istruzione SQL che combina INSERT e UPDATE in un'unica operazione atomica (upsert), eliminando il doppio accesso alla tabella tipico degli ETL legacy."
translationKey: "glossary_merge"
aka: "UPSERT, MERGE INTO"
articles:
  - "/posts/data-warehouse/etl-oracle-da-4-ore-a-25-minuti-con-staging-tables-merge-e-parallel-dml"
---

`MERGE` è un'istruzione SQL standard (ISO/IEC 9075) che unisce la logica di INSERT e UPDATE in un'unica operazione atomica. Il motore accede alla tabella di destinazione una sola volta, confronta ogni riga sorgente con la riga target corrispondente e decide in tempo reale se inserire, aggiornare o — dove supportato — eliminare.

## Come funziona

La sintassi base prevede tre clausole principali: `USING` (sorgente dati), `ON` (condizione di join), `WHEN MATCHED` / `WHEN NOT MATCHED` (azioni condizionali).

```sql
MERGE INTO ordini_dw tgt
USING staging_ordini src
  ON (tgt.ordine_id = src.ordine_id)
WHEN MATCHED THEN
  UPDATE SET tgt.importo = src.importo,
             tgt.stato   = src.stato
WHEN NOT MATCHED THEN
  INSERT (ordine_id, importo, stato)
  VALUES (src.ordine_id, src.importo, src.stato);
```

L'intera operazione è racchiusa in una singola transazione: o tutto va a buon fine (COMMIT implicito o esplicito), o nulla viene scritto (ROLLBACK automatico in caso di errore).

## Quando si usa

`MERGE` è lo strumento naturale per i flussi ETL/ELT che caricano dati incrementali in un data warehouse: la staging table porta le righe nuove o modificate, e `MERGE` le applica alla tabella di destinazione senza richiedere un SELECT preventivo per discriminare INSERT da UPDATE.

Rispetto al pattern legacy `SELECT → IF EXISTS → INSERT/UPDATE`:

- **Elimina la race condition** tra lettura e scrittura in ambienti concorrenti.
- **Riduce il numero di round-trip** verso il database.
- **Si presta alla parallelizzazione** (es. `PARALLEL DML` in Oracle) su tabelle partizionate.

Il limite principale è la portabilità: la sintassi varia tra Oracle, SQL Server, PostgreSQL (che usa `INSERT ... ON CONFLICT`) e MySQL (`INSERT ... ON DUPLICATE KEY UPDATE`), rendendo il codice difficilmente riutilizzabile cross-vendor senza un layer di astrazione.
