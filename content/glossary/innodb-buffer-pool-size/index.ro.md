---
title: "innodb_buffer_pool_size"
description: "Parametru global MySQL care definește dimensiunea buffer pool-ului InnoDB pentru cache de date și indecși — cel mai important parametru de memorie al serverului."
translationKey: "glossary_innodb_buffer_pool_size"
aka: "InnoDB Buffer Pool"
articles:
  - "/posts/mysql/articolo-mysql-saturazione-swap-su-innodb-cluster-3-nodi-analisi-e-fix-dei-param"
---

`innodb_buffer_pool_size` este parametrul global MySQL care controlează câtă RAM este rezervată pentru Buffer Pool-ul InnoDB — structura din memorie care păstrează în cache paginile de date și indecși pentru a reduce accesele la disc. Este parametrul cu cel mai mare impact asupra performanței unui server MySQL dedicat.

## Cum funcționează

InnoDB gestionează Buffer Pool-ul ca un set de pagini de 16 KB (implicit). Când o interogare accesează un rând, InnoDB încarcă pagina corespunzătoare în Buffer Pool; citirile ulterioare pe aceeași pagină sunt servite din RAM fără a accesa discul. Paginile modificate (dirty pages) sunt scrise pe disc asincron de thread-uri de flushing care rulează în fundal.

Valoarea se configurează în `my.cnf` sau `my.ini`:

```ini
[mysqld]
innodb_buffer_pool_size = 12G
```

Pe servere cu RAM ≥ 1 GB, MySQL permite și reconfigurarea dinamică la runtime:

```sql
SET GLOBAL innodb_buffer_pool_size = 12884901888;
```

## Dimensionare și context operațional

Pe servere dedicate MySQL, regula empirică consacrată este **70-80% din RAM-ul disponibil**. Lăsarea a mai puțin de 20% liber pune presiune pe sistemul de operare și, în cazurile cele mai grave, declanșează utilizarea swap-ului — cu o degradare drastică a performanței.

Într-un cluster InnoDB cu 3 noduri, fiecare nod menține propriul Buffer Pool independent. Supradimensionarea pe mașini unde RAM-ul este partajat cu alte procese (agenți de monitorizare, servere binlog etc.) este o cauză frecventă de saturare a swap-ului.

Monitorizarea **Buffer Pool hit rate** este primul indicator de urmărit:

```sql
SELECT
  (1 - (Innodb_buffer_pool_reads / Innodb_buffer_pool_read_requests)) * 100
    AS hit_rate_pct
FROM information_schema.GLOBAL_STATUS
WHERE Variable_name IN ('Innodb_buffer_pool_reads','Innodb_buffer_pool_read_requests');
```

Un hit rate sub 95% pe sarcini OLTP indică un Buffer Pool subdimensionat.
