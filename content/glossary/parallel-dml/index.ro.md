---
title: "Parallel DML"
description: "Funcționalitate Oracle care distribuie operațiunile INSERT, UPDATE, DELETE și MERGE pe mai multe procese slave. Necesită activare explicită la nivel de sesiune."
translationKey: "glossary_parallel_dml"
aka: "Parallel DML (Oracle Parallel Execution)"
articles:
  - "/posts/data-warehouse/etl-oracle-da-4-ore-a-25-minuti-con-staging-tables-merge-e-parallel-dml"
---

Parallel DML este mecanismul Oracle care distribuie operațiunile de scriere — INSERT, UPDATE, DELETE și MERGE — pe mai multe procese slave coordonate de un singur query coordinator. Spre deosebire de Parallel Query, care se activează automat pe tabelele cu un grad de paralelism configurat, Parallel DML necesită o activare explicită la nivel de sesiune înainte ca hint-urile să fie luate în considerare.

## Cum funcționează

Activarea se realizează printr-un comandă DDL pe sesiunea curentă:

```sql
ALTER SESSION ENABLE PARALLEL DML;
```

Doar după această comandă hint-urile `/*+ PARALLEL(tabel, grad) */` produc efect asupra operațiunilor DML. Fără activarea la nivel de sesiune, Oracle ignoră silențios hint-urile — fără erori, fără avertismente — ceea ce face problema dificil de diagnosticat în analiza de performanță.

```sql
INSERT /*+ PARALLEL(target_table, 8) */ INTO target_table
SELECT * FROM staging_table;
```

Fiecare proces slave lucrează pe o partiție logică a datelor. COMMIT-ul final consolidează toate scrierile în mod atomic. Până la acel moment, tabela destinație nu este accesibilă altor sesiuni DML.

## Când se folosește

Parallel DML este soluția potrivită pentru încărcările ETL în medii de Data Warehouse, unde zeci sau sute de milioane de rânduri trebuie procesate în ferestre de timp reduse. Câștigul de performanță scalează cu lățimea de bandă I/O disponibilă și cu gradul de paralelism configurat pe tabelă sau specificat în hint.

Restricții de reținut:

- Nu se aplică tabelelor cu trigger-e activate
- Incompatibil cu anumite tipuri de constrângeri de integritate referențială
- Sesiunea nu trebuie să aibă tranzacții DML deschise înainte de activare
