---
title: "mydumper"
description: "Tool open source di backup logico per MySQL/MariaDB con parallelismo reale a livello di chunk, con restore parallelo tramite myloader."
translationKey: "glossary_mydumper"
aka: "myloader"
articles:
  - "/posts/mysql/mysqldump-mysqlpump-mydumper"
---

**mydumper** è un tool open source di backup logico per MySQL e MariaDB che implementa il parallelismo reale: non solo tra tabelle diverse, ma anche all'interno della stessa tabella, dividendola in chunk basati sulla primary key.

## Come funziona

mydumper si connette al server MySQL, acquisisce una snapshot consistente con `FLUSH TABLES WITH READ LOCK` (o `--trx-consistency-only` per evitare lock globali su InnoDB), poi distribuisce il lavoro tra thread multipli. Ogni tabella grande viene spezzata in chunk — per default basati sui range della primary key — e ogni chunk viene esportato da un thread separato.

L'output non è un singolo file SQL ma una directory con un file per ogni tabella (o per ogni chunk), più i file di metadati, schema e stored procedure.

## Il restore con myloader

Il compagno di mydumper è `myloader`, che carica i file in parallelo disabilitando i check delle foreign key e ricostruendo gli indici alla fine. Questo approccio rende il restore significativamente più veloce rispetto al caricamento sequenziale di un singolo file SQL.

## Quando si usa

mydumper è la scelta raccomandata per database di produzione sopra i 10 GB dove la velocità di dump e restore è critica. Su un database da 60 GB con 8 thread, un dump che con mysqldump richiede 3-4 ore si completa in 20-25 minuti.
