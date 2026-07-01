---
title: "innodb_buffer_pool_size"
description: "Parametro MySQL che definisce la dimensione della cache principale di InnoDB per dati e indici: il più impattante sulla memoria del server."
translationKey: "glossary_innodb_buffer_pool_size"
aka: "InnoDB Buffer Pool"
articles:
  - "/posts/mysql/articolo-mysql-saturazione-swap-su-innodb-cluster-3-nodi-analisi-e-fix-dei-param"
---

`innodb_buffer_pool_size` è il parametro globale di MySQL che controlla quanta RAM viene riservata al Buffer Pool di InnoDB — la struttura in memoria che mantiene pagine di dati e indici per ridurre gli accessi a disco. È il singolo parametro con il maggiore impatto sulle prestazioni di un server MySQL dedicato.

## Come funziona

InnoDB gestisce il Buffer Pool come un insieme di pagine da 16 KB (default). Quando una query accede a una riga, InnoDB carica la pagina corrispondente nel Buffer Pool; le letture successive sulla stessa pagina avvengono in RAM senza toccare il disco. Le pagine modificate (dirty pages) vengono scritte su disco in background dal flushing thread.

Il valore si imposta in `my.cnf` o `my.ini`:

```ini
[mysqld]
innodb_buffer_pool_size = 12G
```

Su server con RAM ≥ 1 GB, MySQL consente anche la configurazione dinamica a runtime:

```sql
SET GLOBAL innodb_buffer_pool_size = 12884901888;
```

## Dimensionamento e contesto operativo

Su server dedicati a MySQL, la regola empirica consolidata è **70-80% della RAM disponibile**. Lasciare meno del 20% libero espone il sistema operativo a pressione di memoria e, nei casi peggiori, all'uso dello swap — con degrado drastico delle prestazioni.

In un cluster InnoDB a 3 nodi, ogni nodo mantiene il proprio Buffer Pool indipendente: un dimensionamento eccessivo su macchine con RAM condivisa tra più processi (agente di monitoraggio, binlog server, ecc.) è una causa frequente di saturazione dello swap.

Monitorare il **Buffer Pool hit rate** è il primo indicatore da tenere sotto controllo:

```sql
SELECT
  (1 - (Innodb_buffer_pool_reads / Innodb_buffer_pool_read_requests)) * 100
    AS hit_rate_pct
FROM information_schema.GLOBAL_STATUS
WHERE Variable_name IN ('Innodb_buffer_pool_reads','Innodb_buffer_pool_read_requests');
```

Un hit rate sotto il 95% su carichi OLTP è segnale che il Buffer Pool è sottodimensionato.
