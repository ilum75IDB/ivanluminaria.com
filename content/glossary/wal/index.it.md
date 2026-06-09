---
title: "WAL"
description: "Write-Ahead Log — registro sequenziale di tutte le modifiche al database PostgreSQL, scritto prima dei file dati. Base di durability, crash recovery, replica fisica e logica."
translationKey: "glossary_wal"
aka: "Write-Ahead Log"
articles:
  - "/posts/postgresql/replica-logica-in-postgresql-scenari-d-uso-configurazione-e-monitoraggio"
---

Il **WAL** (Write-Ahead Log) è il registro sequenziale di tutte le modifiche apportate al database PostgreSQL: ogni INSERT, UPDATE, DELETE, DDL viene scritto qui **prima** che le modifiche vengano applicate ai file dati veri e propri. È il fondamento di durability, crash recovery, replica fisica e replica logica.

## Perché è "Write-Ahead"

La regola è: la transazione è considerata committed solo quando il record WAL corrispondente è stato `fsync`-ato su disco. Anche se il server crasha subito dopo, il file dati può essere ricostruito riproducendo i record WAL dall'ultimo checkpoint. Questa garanzia permette a PostgreSQL di tollerare crash improvvisi senza corruzione del database.

## Struttura su disco

I record WAL sono raggruppati in **segmenti** da 16 MB di default (configurabile via `wal_segment_size`) nella directory `pg_wal/`. Ogni segmento ha un nome esadecimale a 24 caratteri (es. `000000010000000000000042`) che codifica timeline + offset LSN — il **Log Sequence Number**, l'identificatore monotonico di posizione nel WAL.

## Replica logica e WAL

La replica logica di PostgreSQL **decodifica** i record WAL (originariamente in formato fisico) in cambi logici riga per riga (INSERT/UPDATE/DELETE con valori di colonna) tramite il plugin `pgoutput`. È questo passaggio di "logical decoding" che permette ai subscriber di applicare le modifiche su tabelle anche con layout fisico diverso (es. PostgreSQL 13 → 15 con tablespace cambiato). Senza WAL non c'è replica.
