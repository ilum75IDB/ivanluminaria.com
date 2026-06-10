---
title: "SCN"
description: "System Change Number: numărul secvențial monoton crescător pe care Oracle îl folosește pentru a marca fiecare COMMIT și a garanta consistența și recovery point-in-time."
translationKey: "glossary_scn"
aka: "System Change Number"
articles:
  - "/posts/oracle/quali-sono-i-files-critici-di-un-db-oracle"
---

SCN (System Change Number) este contorul intern prin care Oracle ordonează fiecare modificare produsă în baza de date. Crește strict monoton: fiecare COMMIT primește un SCN mai mare decât cel anterior, permițând reconstruirea cu precizie a stării bazei de date în orice moment din trecut.

## Cum funcționează

Ori de câte ori o tranzacție execută un COMMIT, Oracle alocă un SCN unic și îl înregistrează în redo log, în control file și în headerele datafile-urilor. Această valoare reprezintă punctul de referință pentru toate operațiunile de consistență și recovery.

```sql
-- Citirea SCN-ului curent al bazei de date
SELECT CURRENT_SCN FROM V$DATABASE;

-- SCN înregistrat în headerul unui datafile
SELECT NAME, CHECKPOINT_CHANGE# FROM V$DATAFILE;
```

În timpul unui instance recovery, Oracle compară SCN-ul stocat în control file cu cel din headerele fiecărui datafile pentru a determina ce blocuri necesită redo și care sunt deja consistente.

## Context operațional

SCN este central în trei scenarii principale:

- **Point-in-time recovery (PITR)**: se specifică un SCN țintă, iar Oracle reaaplică redo-ul până la acel punct exact.
- **Flashback**: Flashback Query și Flashback Database folosesc SCN-ul pentru a naviga prin istoricul datelor.
- **Data Guard și replicare**: standby-ul aplică archived redo până la SCN-ul transmis de primary, garantând sincronizarea.

SCN are un maxim teoretic (legat de arhitectura pe 48 de biți în versiunile recente), dar în condiții normale nu reprezintă o constrângere operațională. Situațiile anormale de SCN headroom redus pot fi monitorizate prin `V$DATABASE_INCARNATION` și notele MOS aferente.
