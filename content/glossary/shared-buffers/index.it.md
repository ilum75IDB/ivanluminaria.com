---
title: "shared_buffers"
description: "Area di memoria condivisa di PostgreSQL che funge da cache per i blocchi dati, il parametro più importante per il tuning della memoria."
translationKey: "glossary_shared-buffers"
aka: "Shared Buffer Cache"
articles:
  - "/posts/postgresql/pg-stat-statements"
---

**shared_buffers** è il parametro che controlla la dimensione dell'area di memoria condivisa usata da PostgreSQL come cache per i blocchi dati letti dal disco. Ogni volta che PostgreSQL legge una pagina dati (8 KB), la conserva in shared_buffers per le letture successive.

## Come funziona

PostgreSQL alloca la memoria per shared_buffers all'avvio del servizio. Tutti i processi backend condividono questa area di memoria. Quando un processo ha bisogno di un blocco dati, cerca prima in shared_buffers. Se lo trova (cache hit), la lettura è immediata. Se non lo trova (cache miss), deve leggere dal disco — un'operazione ordini di grandezza più lenta.

## Quanto allocare

Il valore di default è 128 MB — inadeguato per qualsiasi database di produzione. La regola empirica è impostare shared_buffers al 25% della RAM disponibile. Su un server con 64 GB di RAM, 16 GB è un buon punto di partenza. Valori oltre il 40% della RAM raramente portano benefici perché PostgreSQL si appoggia anche alla cache del sistema operativo.

## Come monitorarlo

La vista `pg_stat_bgwriter` mostra il rapporto tra `buffers_alloc` (nuovi blocchi allocati) e il totale dei blocchi serviti. Un cache hit ratio sotto il 95% suggerisce che shared_buffers potrebbe essere sottodimensionato.
