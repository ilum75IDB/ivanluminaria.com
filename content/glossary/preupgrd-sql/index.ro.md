---
title: "preupgrd.sql"
description: "Script Oracle de pre-upgrade rulat pe instanța sursă: identifică obiecte invalide, parametri deprecați și probleme de compatibilitate înainte de cutover."
translationKey: "glossary_preupgrd_sql"
aka: "Oracle Pre-Upgrade Information Tool"
articles:
  - "/posts/oracle/oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback"
---

`preupgrd.sql` este scriptul de pre-upgrade livrat împreună cu Oracle 19c (și versiunile anterioare sub denumiri similare). Se rulează pe instanța **sursă**, înainte de orice procedură de migrare, și produce un raport text care fotografiază starea bazei de date față de cerințele versiunii țintă.

## Ce face

Scriptul interoghează dicționarul de date și vederile interne pentru a detecta:

- obiecte în stare `INVALID` care pot bloca faza de recompilare post-upgrade
- parametri de inițializare deprecați sau eliminați în versiunea țintă
- funcționalități obsolete încă active (ex.: nepotriviri `COMPATIBLE`, `DB_BLOCK_SIZE` în afara intervalului admis)
- probleme de timezone, character set și componente opționale care nu pot fi migrate automat

Rezultatul este scris în `$ORACLE_BASE/cfgtoollogs/db_unique_name/preupgrade/` ca fișiere text și, în versiunile recente, ca scripturi SQL corective gata de rulat.

```bash
sqlplus / as sysdba @$ORACLE_HOME/rdbms/admin/preupgrd.sql
```

## Când se folosește

`preupgrd.sql` trebuie rulat cu **săptămâni înainte** de cutover, nu în noaptea migrării. DBA-ul analizează raportul pentru a planifica remedierile: recompilarea obiectelor invalide, eliminarea parametrilor obsoleti, actualizarea componentelor opționale. În medii de producție critice — precum baze de date financiare de 8 TB — raportul devine input direct pentru planul de ROLLBACK și pentru estimarea ferestrei de mentenanță.

## Note operaționale

Oracle livrează versiuni actualizate ale scriptului cu fiecare PSU/RU. Înainte de rulare, trebuie verificat că se folosește copia din `ORACLE_HOME`-ul **versiunii țintă**, nu al celei sursă: acolo se află logica de validare actualizată.
