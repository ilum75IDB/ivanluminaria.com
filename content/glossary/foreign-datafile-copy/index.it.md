---
title: "Foreign datafile copy"
description: "Datafile che RMAN materializza sul database di destinazione a partire da un backset trasportabile, prima che le tablespace vengano agganciate via plug-in."
translationKey: "glossary_foreign_datafile_copy"
aka: "Foreign Datafile Copy (RMAN cross-platform transportable backup)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

Un *foreign datafile copy* è il datafile che RMAN materializza sul database di destinazione a partire da un backupset prodotto con la clausola `FOR TRANSPORT`, prima che le tablespace corrispondenti vengano agganciate via plug-in nella PDB target. È l'oggetto intermedio del meccanismo di transportable backup, quello che rende possibile applicare backup incrementali RMAN a datafile che sul target non appartengono ancora a nessuna tablespace registrata.

## Come funziona

Il flusso tipico è in due fasi. Prima si genera il backupset trasportabile sul sorgente, tipicamente a database aperto con `ALLOW INCONSISTENT`:

```bash
# Sul sorgente
rman target /
BACKUP INCREMENTAL LEVEL 0
  FOR TRANSPORT ALLOW INCONSISTENT
  TABLESPACE DATA_01, DATA_02
  FORMAT '/backup/rman/xtts_l0_%U';
```

Sul target, il backupset viene restaurato come *foreign datafile copy* — non ancora una tablespace, ma un file già posizionato nel filesystem del CDB target:

```bash
# Sul target
RESTORE FOREIGN TABLESPACE DATA_01, DATA_02 TO NEW
  FROM BACKUPSET '/backup/rman/xtts_l0_1_1';
```

Ogni incrementale successivo si applica al foreign datafile copy con `RECOVER FOREIGN DATAFILECOPY`, elencando esplicitamente i path fisici dei file target:

```bash
RECOVER FOREIGN DATAFILECOPY '/u02/oradata/pdb1/data_01.dbf',
                             '/u02/oradata/pdb1/data_02.dbf'
  FROM BACKUPSET '/backup/rman/xtts_l1_2_1';
```

**Limite operativo importante**: ogni `RECOVER FOREIGN DATAFILECOPY` accetta un solo backupset alla volta. Uno script che tenta di accodare più backupset in un unico comando fallisce.

## Quando si usa

Nella migrazione via Transportable Tablespaces (TTS) cross-version con backup incrementale — pattern usato per spostare volumi da terabyte quando la finestra di downtime è troppo stretta per un Data Pump completo. Il foreign datafile copy è la "landing zone" che permette di applicare la catena di incrementali sul target mentre il source database resta in scrittura, riducendo il downtime finale alla sola applicazione dell'ultimo delta più il plug-in dei metadati.
