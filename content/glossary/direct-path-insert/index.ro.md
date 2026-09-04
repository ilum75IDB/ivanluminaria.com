---
aka: Direct-path insert (hint APPEND Oracle)
articles:
- /posts/oracle/articolo-oracle-assertions-in-oracle-26ai
- /posts/data-warehouse/etl-oracle-da-4-ore-a-25-minuti-con-staging-tables-merge-e-parallel-dml
description: Mod de încărcare date Oracle care ocolește buffer cache-ul și scrie direct
  în datafile-uri folosind hint-ul /*+ APPEND */.
title: Direct-path insert
translationKey: glossary_direct_path_insert
---

Direct-path insert este un mod de scriere Oracle care ocolește buffer cache-ul și plasează datele direct în datafile-uri, deasupra high-water mark-ului segmentului. Se activează prin hint-ul `/*+ APPEND */` pe o instrucțiune `INSERT` și este utilizat în mod obișnuit în operațiuni de încărcare în masă pentru a reduce overhead-ul de I/O și volumul de redo generat.

## Cum funcționează

În timpul unui Direct-path insert, Oracle nu caută blocuri libere în segmentul existent: alocă spațiu nou dincolo de high-water mark și scrie direct pe disc, ocolind complet buffer pool-ul. Generarea de redo este minimă (sau zero în modul `NOLOGGING`), ceea ce face operațiunea semnificativ mai rapidă decât un conventional insert pe volume mari de date.

```sql
INSERT /*+ APPEND */ INTO target_table
SELECT * FROM source_table;
COMMIT;
```

Până la COMMIT, tabela este blocată la scriere pentru celelalte sesiuni: niciun alt proces nu poate insera rânduri în aceeași tabelă pe durata tranzacției.

## Când se folosește și limitări

Direct-path insert este potrivit pentru pipeline-uri ETL, încărcări în masă și popularea tabelelor de staging. Vine cu câteva restricții operaționale importante:

- **Constrângeri de integritate**: constrângerile `CHECK` și `NOT NULL` sunt evaluate, dar cheile externe pot necesita dezactivare sau amânare pentru a păstra performanța.
- **Trigger-e**: trigger-ele `BEFORE/AFTER INSERT ROW` nu sunt executate în modul direct-path.
- **Assertions (Oracle 23ai+)**: comportamentul cu Assertions trebuie verificat caz cu caz, deoarece mecanismul de validare diferă față de conventional insert.

În mediile cu Assertions active, testarea explicită este necesară înainte de adoptarea Direct-path insert în producție.
