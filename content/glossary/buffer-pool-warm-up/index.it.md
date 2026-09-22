---
title: "Buffer pool warm-up"
description: "Processo di ricaricamento delle pagine calde nel buffer pool InnoDB dopo un restart, per ridurre il cold start da ore a minuti."
translationKey: "glossary_buffer_pool_warm_up"
aka: "Buffer pool preloading"
articles:
  - "/posts/mysql/innodb-buffer-pool-dimensionamento-hit-ratio-e-warm-up-dopo-restart"
---

Quando MySQL si riavvia, il buffer pool è vuoto: ogni query deve leggere da disco finché le pagine più usate non tornano in memoria. Il buffer pool warm-up è il processo che accelera questo rientro a regime, ripristinando le pagine calde prima che il traffico produzione le richieda.

## Come funziona

InnoDB può salvare gli identificatori delle pagine presenti in memoria al momento dello shutdown e ricaricarli all'avvio successivo. Due variabili di sistema controllano il comportamento:

```sql
-- Abilita dump automatico allo shutdown
SET GLOBAL innodb_buffer_pool_dump_at_shutdown = ON;

-- Abilita load automatico all'avvio (va impostato in my.cnf)
-- innodb_buffer_pool_load_at_startup = ON
```

Il file prodotto (`ib_buffer_pool`) contiene coppie `(tablespace_id, page_id)`, non i dati effettivi: è leggero e il ripristino avviene in background senza bloccare le connessioni in ingresso. La variabile `innodb_buffer_pool_dump_pct` (default 25) limita la percentuale di pagine serializzate, bilanciando completezza e tempo di dump.

## Quando si usa

Il warm-up è rilevante in tre scenari principali:

- **Restart pianificati** (patching OS, upgrade MySQL): senza warm-up, il hit ratio può restare sotto il 50% per ore su istanze con buffer pool da decine di GB.
- **Failover su replica**: la replica promossa a primary parte con buffer pool freddo; abilitare dump/load anche sulle repliche riduce il degrado post-failover.
- **Ambienti cloud con istanze spot/preemptible**: il ciclo stop-start frequente rende il warm-up automatico quasi obbligatorio.

Il progresso del load è monitorabile in tempo reale:

```sql
SHOW STATUS LIKE 'Innodb_buffer_pool_load_status';
```
