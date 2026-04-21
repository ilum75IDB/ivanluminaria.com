---
title: "Pre-upgrade Assessment"
description: "Măsurare structurată a dimensiunii, creșterii, timpilor de backup și timpilor de restore ai unei baze de date înainte de un upgrade. Servește la dimensionarea ferestrei de mentenanță și la definirea unui rollback realist."
translationKey: "glossary_pre_upgrade_assessment"
aka: "Upgrade Readiness Check, Database Sizing & Timing Assessment"
articles:
  - "/posts/mysql/mysql-pre-upgrade-assessment"
---

**Pre-upgrade Assessment** este un document tehnic, dar mai ales un instrument de guvernare a riscului. Traduce întrebarea operațională "reușim să finalizăm upgrade-ul în fereastra de mentenanță?" în cifre măsurate, nu estimate aproximativ.

## Cele patru cifre fundamentale

Un assessment complet răspunde la patru întrebări concrete:

1. **Dimensiuni actuale**: cât cântărește astăzi fiecare bază de date, per schemă, per tabelă, pe disc real vs. estimare `information_schema`
2. **Rata de creștere**: cât cresc datele în timp, măsurată prin snapshot-uri istoricizate și/sau volumul binary log-ului
3. **Timpi de backup**: cât durează un backup complet, măsurat pe fiecare instrument care ar putea fi folosit (`mysqldump`, `mydumper`, `xtrabackup`, `pg_dump`, `expdp`…)
4. **Timpi de restore**: cât durează să reconstruiești baza de date de la zero — cifra cea mai importantă și cea mai des uitată

## De ce timpii de restore contează mai mult decât cei de backup

Backup-urile rulează în fundal, adesea în afara ferestrei de mentenanță. Restore-urile, în schimb, sunt în fereastră, în planul de rollback, în SLA-ul de restaurare a serviciului. Un dataset care se salvează în 30 minute poate cere 4 ore de restore logic: dacă planul de rollback nu ține cont, fereastra nu este suficientă.

## Când se face

- Înainte de un **upgrade major** (MySQL 5.7→8.0, Oracle 12c→19c, PostgreSQL 14→16)
- Înainte de o **migrare de infrastructură** (storage nou, hypervisor nou, cloud migration)
- Înainte de un **re-platforming** de la on-premises la cloud
- Ca **audit periodic** anual pe bazele de date din producție, pentru a verifica că timpii măsurați sunt încă valabili după creșterea datelor

## Ce să livrezi PM-ului

Un singur tabel, nu treizeci de slide-uri. Coloane: server, dimensiune actuală, creștere estimată, timp de backup, timp de restore (instrument principal), timp de restore worst-case (mysqldump sau echivalent). PM-ul trebuie să îl poată atașa la planul de cutover fără modificări.
