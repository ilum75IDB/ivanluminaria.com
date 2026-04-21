---
title: "Pre-upgrade Assessment"
description: "Misurazione strutturata di dimensioni, crescita, tempi di backup e tempi di restore di un database prima di un upgrade. Serve a dimensionare la finestra di manutenzione e definire un rollback realistico."
translationKey: "glossary_pre_upgrade_assessment"
aka: "Upgrade Readiness Check, Database Sizing & Timing Assessment"
articles:
  - "/posts/mysql/mysql-pre-upgrade-assessment"
---

**Pre-upgrade Assessment** è un documento tecnico, ma soprattutto uno strumento di governance del rischio. Traduce la domanda operativa "ce la facciamo a fare l'upgrade nella finestra di manutenzione?" in numeri misurati, non stimati a occhio.

## Le quattro cifre fondamentali

Un assessment completo risponde a quattro domande concrete:

1. **Dimensioni attuali**: quanto pesa oggi ciascun database, per schema, per tabella, su disco reale vs stima `information_schema`
2. **Tasso di crescita**: quanto crescono i dati nel tempo, misurato via snapshot storicizzati e/o volume del binary log
3. **Tempi di backup**: quanto dura un backup completo, misurato su ogni strumento che potrebbe essere usato (`mysqldump`, `mydumper`, `xtrabackup`, `pg_dump`, `expdp`…)
4. **Tempi di restore**: quanto ci vuole a rimettere su il database da zero — la cifra più importante e più spesso dimenticata

## Perché i tempi di restore contano più dei tempi di backup

I backup sono lanciati in background, spesso fuori dalla finestra di manutenzione. I restore invece sono dentro la finestra, dentro il piano di rollback, dentro l'SLA di ripristino servizio. Un dataset che si salva in 30 minuti può richiedere 4 ore di restore logico: se il rollback plan non lo tiene in conto, la finestra non basta.

## Quando farlo

- Prima di un **upgrade major** (MySQL 5.7→8.0, Oracle 12c→19c, PostgreSQL 14→16)
- Prima di una **migrazione infrastrutturale** (nuovo storage, nuovo hypervisor, cloud migration)
- Prima di una **re-platforming** da on-premises a cloud
- Come **audit periodico** annuale sui database in produzione, per verificare che i tempi misurati siano ancora validi dopo la crescita dei dati

## Cosa consegnare al PM

Una singola tabella, non trenta slide. Colonne: server, dimensione attuale, crescita stimata, backup time, restore time (strumento primario), restore time worst-case (mysqldump o equivalente). Il PM deve poterla allegare al piano di cutover senza adattarla.
