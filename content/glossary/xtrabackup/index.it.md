---
title: "xtrabackup"
description: "Strumento di backup fisico hot per MySQL/MariaDB sviluppato da Percona. Copia i file InnoDB a database in esecuzione, gestendo le transazioni attive tramite il redo log."
translationKey: "glossary_xtrabackup"
aka: "Percona XtraBackup"
articles:
  - "/posts/mysql/mysql-pre-upgrade-assessment"
---

**xtrabackup** è il principale strumento open source per il backup fisico hot di MySQL, MariaDB e Percona Server, sviluppato e mantenuto da Percona. A differenza di `mysqldump` e `mydumper` — che producono dump logici — copia direttamente i file di dati InnoDB sul filesystem mentre il database è in esecuzione, senza richiedere downtime.

## Come funziona

Il processo è in due fasi:

1. **Backup**: `xtrabackup` copia i file `.ibd` di InnoDB e contemporaneamente legge il redo log per registrare tutte le modifiche avvenute durante la copia. Il risultato è un set di file dati + un file di redo log che rappresentano uno stato *inconsistente* del database (i file sono stati copiati in momenti leggermente diversi) ma *ricostruibile*.
2. **Prepare**: prima del restore, `xtrabackup --prepare` esegue un crash recovery applicando il redo log ai file dati, portandoli a uno stato consistente.

## Quando è la scelta migliore

Su dataset superiori a ~100 GB il tempo di backup di xtrabackup è tipicamente 5-10 volte inferiore a `mysqldump` e 2-4 volte inferiore a `mydumper`, perché salta completamente la rigenerazione di `INSERT`. Il vantaggio è ancora più marcato in fase di restore, dove una copia binaria + crash recovery impiega pochi minuti rispetto alle ore di un restore logico.

È la scelta obbligata quando la finestra di manutenzione è stretta, per snapshot pre-upgrade e per migrazioni lift-and-shift verso nuovi storage.

## Vincoli da conoscere

- Le tabelle **MyISAM** vengono bloccate durante la loro copia (lock FLUSH TABLES WITH READ LOCK): su database residuali MyISAM questo può causare blocchi applicativi di minuti
- Il backup richiede accesso diretto al filesystem del server MySQL
- Il restore richiede il replay del redo log prima di poter avviare l'istanza (fase `--prepare`)
