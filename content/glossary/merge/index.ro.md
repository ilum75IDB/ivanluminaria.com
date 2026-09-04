---
title: "MERGE"
description: "Instrucțiune SQL care combină INSERT și UPDATE într-o singură operație atomică (upsert), eliminând dubla accesare a tabelei specifică pipeline-urilor ETL clasice."
translationKey: "glossary_merge"
aka: "UPSERT, MERGE INTO"
articles:
  - "/posts/data-warehouse/etl-oracle-da-4-ore-a-25-minuti-con-staging-tables-merge-e-parallel-dml"
---

`MERGE` este o instrucțiune SQL standard (ISO/IEC 9075) care unifică logica de INSERT și UPDATE într-o singură operație atomică. Motorul accesează tabela de destinație o singură dată, compară fiecare rând sursă cu corespondentul său din tabelă și decide în timp real dacă inserează, actualizează sau — acolo unde este suportat — șterge.

## Cum funcționează

Sintaxa de bază are trei clauze principale: `USING` (sursa de date), `ON` (condiția de join) și `WHEN MATCHED` / `WHEN NOT MATCHED` (acțiunile condiționale).

```sql
MERGE INTO comenzi_dw tgt
USING staging_comenzi src
  ON (tgt.comanda_id = src.comanda_id)
WHEN MATCHED THEN
  UPDATE SET tgt.valoare = src.valoare,
             tgt.stare   = src.stare
WHEN NOT MATCHED THEN
  INSERT (comanda_id, valoare, stare)
  VALUES (src.comanda_id, src.valoare, src.stare);
```

Întreaga operație este inclusă într-o singură tranzacție: fie totul reușește (COMMIT implicit sau explicit), fie nimic nu este scris (ROLLBACK automat în caz de eroare).

## Când se folosește

`MERGE` este soluția naturală pentru fluxurile ETL/ELT care încarcă date incrementale într-un data warehouse: staging table aduce rândurile noi sau modificate, iar `MERGE` le aplică în tabela de destinație fără un SELECT prealabil pentru a discrimina între INSERT și UPDATE.

Față de pattern-ul clasic `SELECT → IF EXISTS → INSERT/UPDATE`:

- **Elimină race condition-ul** dintre citire și scriere în medii concurente.
- **Reduce numărul de round-trip-uri** către baza de date.
- **Suportă paralelizarea** (ex. `PARALLEL DML` în Oracle) pe tabele partiționate.

Principalul dezavantaj este portabilitatea: sintaxa diferă între Oracle, SQL Server, PostgreSQL (care folosește `INSERT ... ON CONFLICT`) și MySQL (`INSERT ... ON DUPLICATE KEY UPDATE`), ceea ce face reutilizarea cross-vendor dificilă fără un strat de abstractizare.
