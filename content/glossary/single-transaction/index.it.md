---
title: "--single-transaction"
description: "Flag di mysqldump che apre una transazione REPEATABLE READ per esportare dati InnoDB in modo consistente, senza acquisire lock sulle tabelle."
translationKey: "glossary_single_transaction"
aka: null
articles:
  - "/posts/mysql/articolo-mysql-patching-mysql-8-0-dal-backup-alla-verifica-passo-per-passo"
---

`--single-transaction` è un'opzione di `mysqldump` che avvia una transazione `REPEATABLE READ` prima di iniziare l'esportazione. Grazie all'isolamento garantito da InnoDB, il dump legge uno snapshot coerente dei dati senza bloccare le scritture in corso.

## Come funziona

All'avvio del dump, MySQL emette implicitamente `START TRANSACTION WITH CONSISTENT SNAPSHOT`. Tutte le letture successive avvengono all'interno della stessa transazione, vedendo i dati com'erano al momento dell'apertura. Le operazioni DML concorrenti (INSERT, UPDATE, DELETE) continuano senza interruzioni perché InnoDB le isola tramite MVCC.

```bash
mysqldump --single-transaction --routines --events \
  -u root -p my_database > backup.sql
```

Il file risultante contiene un dump logicamente consistente, equivalente a uno snapshot puntuale nel tempo.

## Quando si usa e limiti

`--single-transaction` è la scelta standard per database InnoDB in produzione: evita i lock a livello di tabella che bloccherebbero le applicazioni. Non è applicabile alle tabelle **MyISAM** o **MEMORY**, che non supportano le transazioni: per quelle si ricade su `--lock-tables`, che acquisisce un lock condiviso per tutta la durata del dump.

Se lo schema contiene un mix di engine, i due flag sono mutuamente esclusivi: `--single-transaction` disabilita automaticamente `--lock-tables`. Le tabelle non-transazionali presenti nel dump potrebbero quindi risultare inconsistenti rispetto alle tabelle InnoDB.

## Note operative

Per dump di grandi dimensioni, la transazione aperta può accumulare undo log significativi in InnoDB. Monitorare `innodb_history_list_length` durante operazioni di backup prolungate è una buona pratica per evitare pressione sul tablespace di undo.
