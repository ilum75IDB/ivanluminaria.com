---
title: "InnoDB Buffer Pool"
description: "Area di memoria principale di InnoDB che cacha pagine di dati e indici per ridurre le letture su disco. Configurabile via innodb_buffer_pool_size."
translationKey: "glossary_innodb_buffer_pool"
aka: "InnoDB Buffer Pool (MySQL)"
articles:
  - "/posts/mysql/innodb-buffer-pool-dimensionamento-hit-ratio-e-warm-up-dopo-restart"
---

L'InnoDB Buffer Pool è il componente di memoria centrale del motore InnoDB in MySQL. Funziona come una cache condivisa per pagine di dati e pagine di indice: ogni volta che una query legge o modifica una riga, InnoDB carica la pagina corrispondente nel buffer pool e la mantiene in memoria il più a lungo possibile. Più il buffer pool è grande rispetto al dataset attivo, meno I/O finisce su disco.

## Come funziona

InnoDB gestisce il buffer pool con un algoritmo LRU (Least Recently Used) modificato, diviso in una "young list" (pagine accedute di recente) e una "old list" (pagine candidate all'eviction). Quando una pagina non è in memoria, si verifica un **buffer pool miss** e InnoDB la legge dal disco. Il rapporto tra hit e miss si misura tramite il **buffer pool hit ratio**.

Il parametro principale è `innodb_buffer_pool_size`. Su server dedicati a MySQL si imposta tipicamente all'80% della RAM disponibile:

```sql
-- Verifica la dimensione attuale
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';

-- Modifica a runtime (MySQL 5.7.5+)
SET GLOBAL innodb_buffer_pool_size = 12884901888; -- 12 GB
```

## Contesto operativo

Il buffer pool si svuota a ogni riavvio del server. MySQL supporta il **warm-up automatico** tramite `innodb_buffer_pool_dump_at_shutdown` e `innodb_buffer_pool_load_at_startup`, che serializzano e ripristinano la lista delle pagine più usate. Senza warm-up, le prime ore dopo un restart mostrano hit ratio basso e latenze elevate.

Su sistemi con dataset superiore alla RAM disponibile, monitorare il hit ratio via `SHOW ENGINE INNODB STATUS` o le tabelle `information_schema.INNODB_BUFFER_POOL_STATS` è indispensabile per capire se un aumento di memoria è giustificato.
