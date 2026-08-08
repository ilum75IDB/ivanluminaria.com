---
title: "View invalidă"
description: "O view MySQL al cărei corp SQL referențiază obiecte inexistente sau inaccesibile: tabele redenumite, coloane șterse, permisiuni revocate."
translationKey: "glossary_view_invalida"
aka: "View stricată, Broken view"
articles:
  - "/posts/mysql/articolo-mysql-patching-mysql-8-0-dal-backup-alla-verifica-passo-per-passo"
---

O **view invalidă** este o vedere al cărei corp SQL referențiază obiecte care nu mai există sau nu mai sunt accesibile: tabele redenumite, coloane șterse, permisiuni revocate. MySQL nu invalidează automat view-urile atunci când tabelul de bază este modificat, astfel că eroarea rămâne silențioasă până la prima execuție a view-ului sau în timpul unui `mysqldump`.

## Cum funcționează

MySQL stochează textul SQL al view-ului în `information_schema.VIEWS` la momentul creării, fără a urmări dependențele la runtime. Dacă un tabel referențiat este redenumit sau o coloană este eliminată prin `ALTER TABLE ... DROP COLUMN`, view-ul continuă să existe în catalog fără niciun semnal de eroare.

```sql
-- Verificare rapidă a stării view-urilor din baza de date curentă
SELECT table_name, is_updatable
FROM information_schema.VIEWS
WHERE table_schema = DATABASE();

-- Accesarea view-ului expune starea invalidă
SELECT * FROM nume_view;
-- ERROR 1356 (HY000): View 'db.nume_view' references invalid table(s) or column(s)
```

## Context operațional

Problema apare de obicei în trei scenarii: în timpul unui ciclu de **patching** sau al unei migrări de schemă, după un `RENAME TABLE` executat fără actualizarea view-urilor dependente, sau în timpul unui dump cu `mysqldump --routines` care încearcă să exporte definiția view-ului. În ultimul caz, dump-ul poate fi finalizat, dar restaurarea eșuează sau generează avertismente greu de urmărit. Înainte de orice operațiune de mentenanță, verificarea sistematică prin `CHECK TABLE nume_view` sau prin interogarea `information_schema` este practica standard.
