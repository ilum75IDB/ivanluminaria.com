---
title: "information_schema"
description: "Schema di sistema MySQL/MariaDB in sola lettura che espone metadati su database, tabelle, indici, utenti e stato del server. Base per ogni assessment e analisi strutturale."
translationKey: "glossary_information_schema"
aka: "Information Schema, INFORMATION_SCHEMA"
articles:
  - "/posts/mysql/mysql-pre-upgrade-assessment"
---

**information_schema** è lo schema virtuale standard SQL che MySQL e MariaDB espongono come interfaccia di introspezione: non contiene dati applicativi, ma metadati sullo stato del server (database presenti, tabelle, colonne, indici, utenti, privilegi, parametri di sessione).

## Come funziona

Le tabelle di `information_schema` sono viste sui cataloghi interni del database. Le più usate sono:

- `TABLES` — una riga per tabella, con dimensioni, tipo engine, numero di righe stimato
- `COLUMNS` — una riga per colonna, con tipo dato, nullability, collation
- `STATISTICS` — una riga per indice e per colonna inclusa, con cardinalità stimata
- `SCHEMATA` — una riga per database
- `PROCESSLIST` — sessioni attive (equivalente a `SHOW PROCESSLIST`)
- `INNODB_*` — metriche e stato dell'engine InnoDB

## A cosa serve

È il punto di partenza di qualsiasi assessment: sizing del database, identificazione delle tabelle più grandi, audit degli indici, analisi dei tipi di dato, controllo delle collation miste. Molti script di monitoraggio e tool BI leggono `information_schema` per costruire cruscotti di stato.

## Limitazioni da conoscere

I valori di `data_length`, `index_length` e `table_rows` sono **stime** aggiornate periodicamente da InnoDB e dipendono dall'ultima `ANALYZE TABLE`. Su tabelle molto volatili possono sottostimare del 10-15%. Per i dati critici (piano di migrazione, piano capacità) è buona prassi incrociare con la dimensione fisica dei file `.ibd` (`du -sh /var/lib/mysql/<schema>/*.ibd`).
