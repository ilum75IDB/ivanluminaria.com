---
title: "mysqlpump"
description: "Evoluzione di mysqldump introdotta in MySQL 5.7 con parallelismo a livello di tabella, deprecata da Oracle in MySQL 8.0.34."
translationKey: "glossary_mysqlpump"
aka: "MySQL pump"
articles:
  - "/posts/mysql/mysqldump-mysqlpump-mydumper"
---

**mysqlpump** è l'utility di backup logico introdotta da Oracle in MySQL 5.7 come evoluzione di mysqldump. La differenza principale è il supporto per il parallelismo a livello di tabella e la compressione nativa dell'output (zlib, lz4, zstd).

## Come funziona

mysqlpump può dumpare più tabelle contemporaneamente usando thread paralleli, configurabili con `--default-parallelism`. La compressione viene applicata direttamente durante il dump, senza bisogno di pipe esterne verso gzip. Supporta anche il dump selettivo di utenti e account MySQL.

Il parallelismo però opera solo a livello di tabella intera: se una singola tabella è molto più grande delle altre, un thread si trascina da solo mentre gli altri hanno già finito.

## Il problema della consistenza

Con il parallelismo attivo, mysqlpump non garantisce consistenza tra tabelle diverse — tabelle esportate da thread differenti possono riflettere momenti diversi nel tempo. Questo è un limite critico per backup di produzione su database relazionali con foreign key.

## Stato attuale

Oracle ha dichiarato mysqlpump deprecato in MySQL 8.0.34 e lo ha rimosso completamente in MySQL 8.4. Per chi cerca parallelismo nel backup logico, mydumper è l'alternativa consigliata.
