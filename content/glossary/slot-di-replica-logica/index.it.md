---
title: "Slot di replica logica"
description: "Struttura PostgreSQL persistente sul publisher che traccia la posizione di consumo dei WAL per ogni subscriber. Protegge dalla perdita di dati in caso di disconnessione."
translationKey: "glossary_slot_di_replica_logica"
aka: "Logical Replication Slot"
articles:
  - "/posts/postgresql/replica-logica-in-postgresql-scenari-d-uso-configurazione-e-monitoraggio"
---

Lo **slot di replica logica** è una struttura persistente sul publisher PostgreSQL che memorizza la posizione di consumo dei WAL per ogni subscriber. Garantisce che nessuna modifica venga persa anche se il subscriber si disconnette temporaneamente: i segmenti WAL vengono trattenuti finché non sono stati consumati e confermati.

## Perché esiste

Senza uno slot, PostgreSQL recicla i segmenti WAL appena diventano superflui per il crash recovery — tipicamente in pochi minuti su sistemi attivi. Un subscriber disconnesso per un'ora si troverebbe con un buco irrecuperabile e l'unica via d'uscita sarebbe re-inizializzare la subscription da snapshot. Lo slot risolve questo problema mantenendo i WAL disponibili.

## Il rischio dello slot orfano

Uno slot smesso di consumare (subscriber crashato, dropped senza prima rimuovere lo slot, migrazione interrotta) **continua a trattenere WAL all'infinito**, riempiendo il disco del publisher. È la causa numero uno di outage da replica logica in produzione.

## Monitoraggio essenziale

La vista `pg_replication_slots` espone `active` (è in uso?), `restart_lsn` (da dove ripartirebbe), e calcolando il delta tra `pg_current_wal_lsn()` e `restart_lsn` si ottiene il volume di WAL trattenuto. Su sistemi critici è doveroso un allarme quando il delta supera una soglia (es. 10 GB) o quando uno slot resta `active = false` per troppo tempo. Dal PostgreSQL 13 esiste anche `max_slot_wal_keep_size` come cap di sicurezza.
