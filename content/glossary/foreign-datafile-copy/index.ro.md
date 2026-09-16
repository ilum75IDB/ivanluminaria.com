---
title: "Foreign datafile copy"
description: "Datafile pe care RMAN îl materializează pe baza de date de destinație pornind de la un backset transportabil, înainte ca tablespace-urile să fie conectate prin plug-in."
translationKey: "glossary_foreign_datafile_copy"
aka: "Foreign Datafile Copy (RMAN cross-platform transportable backup)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

Un *foreign datafile copy* este datafile-ul pe care RMAN îl materializează pe baza de date de destinație pornind de la un backupset produs cu clauza `FOR TRANSPORT`, înainte ca tablespace-urile corespunzătoare să fie conectate prin plug-in în PDB-ul target. Este obiectul intermediar al mecanismului de transportable backup — ceea ce face posibilă aplicarea backup-urilor incrementale RMAN pe datafile-uri care pe target încă nu aparțin niciunui tablespace înregistrat.

## Cum funcționează

Fluxul tipic este în două faze. Mai întâi se generează backupset-ul transportabil pe sursă, de obicei cu baza de date deschisă folosind `ALLOW INCONSISTENT`:

```bash
# Pe sursă
rman target /
BACKUP INCREMENTAL LEVEL 0
  FOR TRANSPORT ALLOW INCONSISTENT
  TABLESPACE DATA_01, DATA_02
  FORMAT '/backup/rman/xtts_l0_%U';
```

Pe target, backupset-ul se restaurează ca *foreign datafile copy* — încă nu este un tablespace, ci un fișier deja poziționat în filesystem-ul CDB-ului target:

```bash
# Pe target
RESTORE FOREIGN TABLESPACE DATA_01, DATA_02 TO NEW
  FROM BACKUPSET '/backup/rman/xtts_l0_1_1';
```

Fiecare incremental ulterior se aplică pe foreign datafile copy cu `RECOVER FOREIGN DATAFILECOPY`, enumerând explicit căile fizice ale fișierelor target:

```bash
RECOVER FOREIGN DATAFILECOPY '/u02/oradata/pdb1/data_01.dbf',
                             '/u02/oradata/pdb1/data_02.dbf'
  FROM BACKUPSET '/backup/rman/xtts_l1_2_1';
```

**Limită operațională importantă**: fiecare `RECOVER FOREIGN DATAFILECOPY` acceptă un singur backupset odată. Un script care încearcă să pună în coadă mai multe backupset-uri într-o singură comandă eșuează.

## Când se utilizează

În migrări prin Transportable Tablespaces (TTS) cross-version combinate cu backup incremental — pattern folosit pentru a muta volume de ordinul terabyte-lor când fereastra de downtime este prea strâmtă pentru un Data Pump complet. Foreign datafile copy este "landing zone"-ul care permite aplicarea lanțului de incrementale pe target în timp ce source database rămâne în scriere, reducând downtime-ul final doar la ultimul apply de delta plus plug-in-ul metadatelor.
