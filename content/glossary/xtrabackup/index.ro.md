---
title: "xtrabackup"
description: "Instrument de backup fizic hot pentru MySQL/MariaDB dezvoltat de Percona. Copiază fișierele InnoDB cu baza de date în execuție, gestionând tranzacțiile active prin redo log."
translationKey: "glossary_xtrabackup"
aka: "Percona XtraBackup"
articles:
  - "/posts/mysql/mysql-pre-upgrade-assessment"
---

**xtrabackup** este principalul instrument open source pentru backup fizic hot al MySQL, MariaDB și Percona Server, dezvoltat și întreținut de Percona. Spre deosebire de `mysqldump` și `mydumper` — care produc dump-uri logice — copiază direct fișierele de date InnoDB pe sistemul de fișiere în timp ce baza de date rulează, fără a necesita downtime.

## Cum funcționează

Procesul are două faze:

1. **Backup**: `xtrabackup` copiază fișierele `.ibd` ale InnoDB și simultan citește redo log-ul pentru a înregistra toate modificările survenite în timpul copiei. Rezultatul este un set de fișiere de date + un fișier redo log care reprezintă o stare *inconsistentă* a bazei de date (fișierele au fost copiate în momente ușor diferite) dar *reconstructibilă*.
2. **Prepare**: înainte de restore, `xtrabackup --prepare` execută un crash recovery aplicând redo log-ul la fișierele de date, aducându-le la o stare consistentă.

## Când este alegerea cea mai bună

Pe dataset-uri mai mari de ~100 GB timpul de backup al xtrabackup este tipic de 5-10 ori mai rapid decât `mysqldump` și de 2-4 ori mai rapid decât `mydumper`, pentru că sare complet regenerarea `INSERT`-urilor. Avantajul este și mai pronunțat în faza de restore, unde o copie binară + crash recovery durează minute în comparație cu orele unui restore logic.

Este alegerea obligatorie când fereastra de mentenanță este strâmtă, pentru snapshot-uri pre-upgrade și pentru migrări lift-and-shift către storage-uri noi.

## Restricții de cunoscut

- Tabelele **MyISAM** sunt blocate în timpul copiei lor (FLUSH TABLES WITH READ LOCK): pe baze de date cu MyISAM rezidual acest lucru poate cauza blocări aplicative de minute
- Backup-ul necesită acces direct la sistemul de fișiere al serverului MySQL
- Restore-ul necesită aplicarea redo log-ului înainte ca instanța să poată porni (faza `--prepare`)
