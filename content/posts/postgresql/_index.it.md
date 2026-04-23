---
title: "PostgreSQL"
layout: "list"
description: "PostgreSQL: architettura, performance e progettazione su uno dei database open source più avanzati e longevi della storia."
image: "postgresql.cover.jpg"
---

Ho visto PostgreSQL in produzione con `shared_buffers` a 128MB su macchine con 256GB di RAM — "perché abbiamo seguito il default". Ho visto `autovacuum` disabilitato perché "rallentava il sistema", e tre mesi dopo una tabella da 500 milioni di righe con l'80% di bloat e query che non finivano più. Ho visto repliche streaming rotte silenziosamente da settimane, e ce ne siamo accorti solo quando il master si è fermato e il failover non è partito.

E ho visto l'esatto contrario: cluster Postgres che reggono migliaia di connessioni concorrenti, gestiscono terabyte di dati e sopravvivono a upgrade major senza un minuto di downtime percepito.

La differenza non è nel codice. È in **chi ha avuto il coraggio di toccare i default invece di subirli.**

------------------------------------------------------------------------

PostgreSQL non è solo un database open source. È il risultato di quasi quarant'anni di evoluzione accademica e industriale.

Nato nel 1986 all'Università di Berkeley come evoluzione di Ingres, il progetto POSTGRES introduceva concetti che all'epoca erano avanguardia: **estendibilità, tipi di dato personalizzati, regole e un modello relazionale avanzato**. Nel 1996 arriva il supporto SQL e il nome cambia in PostgreSQL. Il mondo però ha continuato a chiamarlo semplicemente "Postgres". E va bene così.

Dopo vent'anni che ci lavoro sopra, una cosa l'ho capita: PostgreSQL **premia chi lo capisce e punisce chi lo lascia a default**. È un motore progettato per essere tunato, non per essere installato e dimenticato. Le assunzioni dello sviluppo vengono smontate dalla realtà della produzione:

- **VACUUM e autovacuum** non sono optional — sono come lavarsi i denti
- **`shared_buffers`** al default di 128MB è ragionevole solo su un portatile
- **`work_mem`** impostato male moltiplicato per le connessioni attive ti fa OOM nel momento peggiore
- **Le repliche** hanno bisogno di monitoring attivo — lo streaming si interrompe in silenzio
- **Le estensioni** possono cambiare il comportamento del catalog e bloccare gli upgrade

------------------------------------------------------------------------

## 🔧 I parametri che non lascio mai a default

Quando metto in produzione un cluster Postgres, ci sono cinque parametri che non lascio mai al valore di uscita. Non perché il default sia sbagliato in assoluto, ma perché è pensato per girare ovunque — e "ovunque" non è mai la tua macchina di produzione.

| Parametro | Cosa regola | Come lo tocco |
|---|---|---|
| **`shared_buffers`** | Cache condivisa di Postgres | Tipicamente 25% della RAM — non di più, il filesystem cache fa il resto |
| **`effective_cache_size`** | Cosa il planner crede ci sia in cache | 50-75% della RAM — non alloca nulla, influenza le scelte dell'ottimizzatore |
| **`work_mem`** | Memoria per sort e hash per operazione | Basso (4-16MB) se ci sono molte connessioni, alto solo per workload analitici dedicati |
| **`autovacuum_*`** | Pulizia automatica di dead tuples | Mai disabilitato. Eventualmente tunato (`naptime`, `cost_limit`) per essere più aggressivo su tabelle calde |
| **`wal_level` + `max_wal_senders`** | Dettaglio dei WAL, slot per repliche | `replica` o `logical` a seconda del caso, sender dimensionati sulle repliche reali + margine |

Cinque parametri. Venti minuti di analisi. Mesi di problemi di performance evitati.

------------------------------------------------------------------------

## 📚 Di cosa parlo qui

Storie vere e scelte tecniche su PostgreSQL in produzione. Architettura, VACUUM e bloat, tuning dei parametri, replica streaming e logica, strategie di upgrade, backup con pg_basebackup e WAL archiving, estensioni che servono davvero (e quelle che si potevano evitare).

Niente ricette preconfezionate. Solo quello che ho visto funzionare su ambienti veri — postale, banche, pubblica amministrazione, telco — dove Postgres regge migliaia di istanze in parallelo e non può permettersi approssimazioni.

------------------------------------------------------------------------

Usare PostgreSQL non significa scegliere un database open source.

Significa scegliere un motore progettato per essere esteso, analizzato e compreso — e accettare che i default non ti porteranno lontano.
