---
title: "Flashback Database"
description: "Funcționalitate Oracle care readuce întreaga bază de date la un moment anterior folosind flashback logs, mai rapidă decât un restore RMAN complet pentru erori logice extinse."
translationKey: "glossary_flashback_database"
aka: "Oracle Flashback Database Recovery"
articles:
  - "/posts/oracle/oracle-flashback-recupero-dati-logici-senza-downtime-da-query-a-database"
---

Flashback Database este o funcționalitate Oracle care permite readucerea întregii baze de date la o stare anterioară fără a restaura datafile-urile din backup. Spre deosebire de un restore RMAN complet, se bazează pe log-uri dedicate scrise continuu în fundal, ceea ce face recuperarea semnificativ mai rapidă atunci când o eroare logică s-a propagat deja pe mulți obiecți.

## Cum funcționează

Oracle înregistrează continuu imaginile anterioare ale blocurilor modificate în **flashback logs**, stocate în Fast Recovery Area (FRA). Când se inițiază un Flashback Database, motorul citește aceste log-uri înapoi până la punctul în timp (sau SCN) dorit și aplică imaginile salvate peste blocurile curente.

Operațiunea necesită ca baza de date să fie în modul `MOUNT`:

```sql
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
FLASHBACK DATABASE TO TIMESTAMP (SYSTIMESTAMP - INTERVAL '2' HOUR);
ALTER DATABASE OPEN RESETLOGS;
```

`OPEN RESETLOGS` este obligatoriu: resetează secvența redo log-urilor și face ca punctul de flashback să nu mai fie accesibil în sens înainte.

## Când se utilizează

Flashback Database este instrumentul potrivit când o eroare logică — un `DELETE` masiv fără `WHERE`, o migrare eșuată, un proces batch care a corupt date în zeci de tabele — a depășit deja fereastra în care Flashback Table sau Flashback Query ar fi suficiente.

Constrângeri de reținut:

- `DB_FLASHBACK_RETENTION_TARGET` trebuie configurat, iar FRA trebuie să aibă spațiu suficient pentru flashback logs pe perioada dorită.
- Datafile-urile adăugate după punctul de flashback nu sunt recuperate automat și trebuie gestionate separat.
- După `RESETLOGS`, bazele de date standby dintr-o configurație Data Guard trebuie resincronizate.
