---
title: "InnoDB Buffer Pool"
description: "Zona principală de memorie a InnoDB care stochează în cache pagini de date și indecși pentru a reduce citirile de pe disc. Se configurează prin innodb_buffer_pool_size."
translationKey: "glossary_innodb_buffer_pool"
aka: "InnoDB Buffer Pool (MySQL)"
articles:
  - "/posts/mysql/innodb-buffer-pool-dimensionamento-hit-ratio-e-warm-up-dopo-restart"
---

InnoDB Buffer Pool este componenta centrală de memorie a motorului de stocare InnoDB din MySQL. Funcționează ca un cache partajat pentru paginile de date și paginile de indecși: ori de câte ori o interogare citește sau modifică un rând, InnoDB încarcă pagina corespunzătoare în buffer pool și o menține în memorie cât mai mult posibil. Cu cât buffer pool-ul este mai mare față de dataset-ul activ, cu atât mai puțin I/O ajunge pe disc.

## Cum funcționează

InnoDB gestionează buffer pool-ul printr-un algoritm LRU (Least Recently Used) modificat, împărțit într-o "young list" (pagini accesate recent) și o "old list" (candidate la eviction). Când o pagină nu se află în memorie, apare un **buffer pool miss** și InnoDB o citește de pe disc. Raportul dintre accesări reușite și ratate reprezintă **buffer pool hit ratio**.

Parametrul principal este `innodb_buffer_pool_size`. Pe servere dedicate MySQL, acesta se setează de obicei la 80% din RAM-ul disponibil:

```sql
-- Verificarea dimensiunii curente
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';

-- Modificare la runtime (MySQL 5.7.5+)
SET GLOBAL innodb_buffer_pool_size = 12884901888; -- 12 GB
```

## Context operațional

Buffer pool-ul se golește la fiecare repornire a serverului. MySQL suportă **warm-up automat** prin `innodb_buffer_pool_dump_at_shutdown` și `innodb_buffer_pool_load_at_startup`, care serializează și restaurează lista paginilor cel mai frecvent utilizate. Fără warm-up, primele ore după un restart prezintă un hit ratio scăzut și latențe ridicate.

Pe sisteme unde dataset-ul depășește RAM-ul disponibil, monitorizarea hit ratio-ului prin `SHOW ENGINE INNODB STATUS` sau tabelul `information_schema.INNODB_BUFFER_POOL_STATS` este esențială pentru a determina dacă o creștere a memoriei este justificată.
