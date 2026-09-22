---
title: "LRU list"
description: "Struttura a due zone di InnoDB che gestisce l'eviction delle pagine dal buffer pool, proteggendo i dati caldi dai full scan occasionali."
translationKey: "glossary_lru_list"
aka: "LRU list (young list + old list)"
articles:
  - "/posts/mysql/innodb-buffer-pool-dimensionamento-hit-ratio-e-warm-up-dopo-restart"
---

La LRU list è la struttura dati con cui InnoDB decide quali pagine mantenere nel buffer pool e quali scartare quando la memoria è piena. A differenza di un LRU classico a lista singola, InnoDB adotta una variante a due zone che separa le pagine "calde" da quelle appena lette, riducendo il rischio che un'operazione di scansione massiva espella dati frequentemente acceduti.

## Come funziona

La lista è divisa in due sottozone contigue:

- **Young list** (testa, ~5/8 della lista): contiene le pagine accedute di recente più volte. Sono le pagine "calde" che InnoDB cerca di tenere in cache il più a lungo possibile.
- **Old list** (coda, ~3/8 della lista): punto di ingresso per ogni pagina caricata per la prima volta dal disco. Una pagina rimane nell'old list per almeno `innodb_old_blocks_time` millisecondi (default 1000 ms) prima di poter essere promossa nella young list.

Quando il buffer pool è saturo, InnoDB rimuove le pagine dalla coda dell'old list (le più "fredde"). La promozione dalla old alla young list avviene solo se la pagina viene acceduta di nuovo dopo il periodo di attesa configurato.

## Contesto operativo

Il meccanismo a due zone protegge la young list durante i full scan: le pagine lette sequenzialmente entrano nell'old list ma, se non vengono riaccedute entro il timeout, vengono evitte senza mai scalzare i dati caldi. Questo è particolarmente rilevante in scenari con:

- report notturni o ETL che eseguono `SELECT` su tabelle grandi
- `mysqldump` o backup logici che leggono l'intera tabella
- query analitiche occasionali su istanze OLTP

I parametri chiave da monitorare e regolare sono `innodb_old_blocks_pct` (percentuale riservata all'old list, default 37) e `innodb_old_blocks_time`. Un valore troppo basso di `innodb_old_blocks_time` rende la protezione inefficace; un valore troppo alto può rallentare la promozione di pagine genuinamente calde.
