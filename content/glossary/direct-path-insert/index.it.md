---
aka: Direct-path insert (Oracle APPEND hint)
articles:
- /posts/oracle/articolo-oracle-assertions-in-oracle-26ai
- /posts/data-warehouse/etl-oracle-da-4-ore-a-25-minuti-con-staging-tables-merge-e-parallel-dml
description: Modalità di caricamento dati Oracle che bypassa il buffer cache e scrive
  direttamente nei datafile tramite il hint /*+ APPEND */.
title: Direct-path insert
translationKey: glossary_direct_path_insert
---

Il Direct-path insert è una modalità di scrittura Oracle che bypassa il buffer cache e inserisce i dati direttamente nei datafile, al di sopra dell'high-water mark del segmento. Si attiva tramite il hint `/*+ APPEND */` su un'istruzione `INSERT` e viene usato tipicamente in operazioni di caricamento massivo per ridurre l'overhead di I/O e il volume di redo generato.

## Come funziona

Durante un Direct-path insert Oracle non cerca blocchi liberi nel segmento esistente: alloca nuova spazio oltre l'high-water mark e scrive direttamente su disco, saltando il buffer pool. Il redo generato è minimo (o nullo in modalità `NOLOGGING`), il che rende l'operazione molto più veloce rispetto a un conventional insert su grandi volumi.

```sql
INSERT /*+ APPEND */ INTO target_table
SELECT * FROM source_table;
COMMIT;
```

Fino al COMMIT la tabella è bloccata in scrittura per altre sessioni: nessun altro processo può inserire righe nella stessa tabella durante la transazione.

## Quando si usa e limiti

Il Direct-path insert è indicato per ETL, bulk load e popolamento di tabelle di staging. Presenta però alcune restrizioni operative rilevanti:

- **Vincoli di integrità**: i vincoli `CHECK` e `NOT NULL` vengono valutati, ma i vincoli di foreign key possono essere disabilitati o differiti per mantenere le prestazioni.
- **Trigger**: i trigger `BEFORE/AFTER INSERT ROW` non vengono eseguiti in modalità direct-path.
- **Assertions (Oracle 23ai+)**: il comportamento con le Assertions va verificato caso per caso, poiché il meccanismo di validazione differisce dal conventional insert.

In ambienti con Assertions attive, è necessario testare esplicitamente il comportamento prima di adottare il Direct-path insert in produzione.
