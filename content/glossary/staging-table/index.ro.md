---
title: "Staging Table"
description: "Tabel temporar folosit ca zonă de aterizare pentru date brute într-un proces ETL, separând ingestia de transformare și încărcarea finală."
translationKey: "glossary_staging_table"
aka: "Zonă de staging, landing table"
articles:
  - "/posts/data-warehouse/etl-oracle-da-4-ore-a-25-minuti-con-staging-tables-merge-e-parallel-dml"
---

O staging table este un tabel intermediar care primește datele brute din sursă înainte ca acestea să fie transformate și încărcate în destinația finală. Separă clar cele trei faze ale unui proces ETL, făcând fiecare fază independentă, monitorizabilă și reanalizabilă după un eșec.

## Cum funcționează

Datele sunt mai întâi copiate în bloc în staging table — de obicei fără constrângeri de integritate referențială active, pentru a maximiza debitul INSERT-urilor — și abia ulterior se aplică verificările de calitate, transformările și MERGE-ul către tabelele de destinație.

```sql
-- 1. Încărcare brută în staging table (fără constrângeri active)
INSERT /*+ APPEND */ INTO stg_orders
SELECT * FROM ext_orders_source;

-- 2. Transformare și MERGE în tabelul de destinație
MERGE INTO orders tgt
USING stg_orders src
  ON (tgt.order_id = src.order_id)
WHEN MATCHED THEN UPDATE SET tgt.status = src.status
WHEN NOT MATCHED THEN INSERT (order_id, status) VALUES (src.order_id, src.status);
```

Procesarea în bulk pe staging table în loc de rând cu rând reduce drastic numărul de COMMIT-uri și presiunea asupra redo log-ului.

## Când se folosește

Staging table-urile sunt soluția potrivită ori de câte ori volumul de date face impracticabilă transformarea în zbor în timpul ingestiei. Sunt deosebit de utile când:

- procesul ETL trebuie să fie reanalizabil (este suficient să se reia de la ultimul TRUNCATE/INSERT pe staging);
- sistemul sursă nu tolerează interogări lente sau tranzacții de lungă durată;
- se dorește aplicarea Parallel DML în faza de MERGE fără a bloca sursa.

Principalul trade-off este spațiul suplimentar pe disc și latența introdusă de dubla scriere, acceptabilă în aproape toate contextele batch.
