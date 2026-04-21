---
title: "mysqldump"
description: "Utility di backup logico inclusa in ogni installazione MySQL, produce un file SQL sequenziale per ricreare schema e dati."
translationKey: "glossary_mysqldump"
aka: "MySQL dump"
articles:
  - "/posts/mysql/mysqldump-mysqlpump-mydumper"
  - "/posts/mysql/mysql-pre-upgrade-assessment"
---

**mysqldump** è l'utility di backup logico inclusa di serie in ogni installazione di MySQL e MariaDB. Produce un file SQL contenente tutte le istruzioni (CREATE TABLE, INSERT) necessarie per ricostruire completamente schema e dati di un database.

## Come funziona

mysqldump si connette al server MySQL e legge le tabelle una alla volta, generando le istruzioni SQL corrispondenti in output. L'operazione è rigorosamente single-threaded: una tabella dopo l'altra, una riga dopo l'altra. Il file prodotto può essere compresso esternamente (gzip, zstd) ma lo strumento stesso non offre compressione nativa.

Con l'opzione `--single-transaction`, il dump avviene all'interno di una transazione con isolation level REPEATABLE READ, che garantisce una snapshot consistente su tabelle InnoDB senza acquisire lock sulle scritture.

## A cosa serve

mysqldump è lo strumento standard per:

- Backup logico di database di piccole e medie dimensioni
- Migrazioni tra versioni diverse di MySQL
- Export di singole tabelle o database per trasferimento tra ambienti
- Creazione di dump leggibili e ispezionabili manualmente

## Quando diventa un problema

Su database oltre i 10-15 GB, il dump single-threaded diventa un collo di bottiglia. Un database da 60 GB può richiedere 3-4 ore di dump e altrettante di restore. La mancanza di parallelismo è il limite strutturale: non c'è modo di velocizzare il processo se non passando a strumenti come mydumper.
