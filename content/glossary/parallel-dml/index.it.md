---
title: "Parallel DML"
description: "Esecuzione parallela di INSERT, UPDATE, DELETE e MERGE in Oracle tramite processi multipli. Richiede abilitazione esplicita a livello di sessione."
translationKey: "glossary_parallel_dml"
aka: "Parallel DML (Oracle Parallel Execution)"
articles:
  - "/posts/data-warehouse/etl-oracle-da-4-ore-a-25-minuti-con-staging-tables-merge-e-parallel-dml"
---

Il Parallel DML è la funzionalità di Oracle che distribuisce le operazioni di scrittura — INSERT, UPDATE, DELETE e MERGE — su più processi slave coordinati da un processo query coordinator. A differenza del Parallel Query, che è attivo per default sulle tabelle configurate, il Parallel DML richiede un'abilitazione esplicita a livello di sessione prima che gli hint vengano rispettati.

## Come funziona

L'abilitazione avviene con un comando DDL sulla sessione corrente:

```sql
ALTER SESSION ENABLE PARALLEL DML;
```

Solo dopo questo comando gli hint `/*+ PARALLEL(tabella, grado) */` producono effetto sulle operazioni DML. Senza l'abilitazione, Oracle ignora silenziosamente gli hint senza restituire errori o warning, rendendo il problema difficile da diagnosticare.

```sql
INSERT /*+ PARALLEL(target_table, 8) */ INTO target_table
SELECT * FROM staging_table;
```

Ogni processo slave lavora su una partizione logica dei dati. Al termine, il COMMIT consolida tutte le scritture. Prima del COMMIT la tabella target non è accessibile ad altre sessioni DML.

## Quando si usa

Il Parallel DML è indicato nei carichi ETL su Data Warehouse, dove si processano decine o centinaia di milioni di righe in finestre temporali ristrette. Il beneficio è proporzionale alla larghezza di banda I/O disponibile e al grado di parallelismo configurato sulla tabella o specificato nell'hint.

Limiti da tenere presenti:

- Non applicabile su tabelle con trigger abilitati
- Incompatibile con alcune tipologie di vincoli di integrità referenziale
- Richiede che la sessione non abbia transazioni DML aperte prima dell'abilitazione
