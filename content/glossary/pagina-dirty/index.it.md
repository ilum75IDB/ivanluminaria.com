---
title: "Pagina dirty"
description: "Pagina del buffer pool modificata in memoria ma non ancora scritta su disco. Un numero elevato segnala che il flush InnoDB non tiene il passo con le scritture."
translationKey: "glossary_pagina_dirty"
aka: "Dirty page, pagina sporca"
articles:
  - "/posts/mysql/innodb-buffer-pool-dimensionamento-hit-ratio-e-warm-up-dopo-restart"
---

Nel buffer pool di InnoDB, una **pagina dirty** è una pagina da 16 KB che è stata modificata in memoria — da un INSERT, UPDATE o DELETE — ma il cui contenuto aggiornato non è ancora stato scritto nel file dati su disco. La versione su disco è quindi obsoleta rispetto a quella in RAM.

## Come funziona

Ogni volta che una transazione modifica una riga, InnoDB aggiorna la pagina corrispondente nel buffer pool e la marca come dirty. In parallelo, il thread di flush in background (`page_cleaner`) scrive periodicamente le pagine dirty sui file `.ibd`, seguendo due politiche principali:

- **Fuzzy checkpoint**: flush continuo e incrementale per mantenere la percentuale di pagine dirty sotto `innodb_max_dirty_pages_pct` (default 90%).
- **Flush adattivo**: accelera il flush quando il ritmo di scrittura nel redo log si avvicina alla capacità massima, per evitare che InnoDB debba bloccare le scritture utente per fare spazio.

```sql
-- Monitorare le pagine dirty in tempo reale
SELECT VARIABLE_NAME, VARIABLE_VALUE
FROM performance_schema.global_status
WHERE VARIABLE_NAME IN (
    'Innodb_buffer_pool_pages_dirty',
    'Innodb_buffer_pool_pages_total'
);
```

## Contesto operativo

Un numero di pagine dirty stabile e contenuto è normale. Il segnale di allarme è una **crescita sostenuta e monotona**: significa che il flush non riesce a smaltire le scritture in arrivo. Le cause più frequenti sono un buffer pool sovradimensionato rispetto alla velocità del disco, un `innodb_io_capacity` troppo basso, o un carico di scrittura improvvisamente elevato.

In caso di crash, InnoDB usa il redo log per ripristinare le pagine dirty non ancora flushate: più pagine dirty ci sono, più lungo sarà il crash recovery al riavvio.
