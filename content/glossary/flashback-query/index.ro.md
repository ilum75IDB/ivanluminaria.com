---
title: "Flashback Query"
description: "Funcționalitate Oracle care permite interogarea unei stări trecute a bazei de date prin timestamp sau SCN, citind direct din segmentele de undo."
translationKey: "glossary_flashback_query"
aka: "Oracle Flashback Query"
articles:
  - "/posts/oracle/oracle-flashback-recupero-dati-logici-senza-downtime-da-query-a-database"
---

Flashback Query este o funcționalitate Oracle Database care permite executarea unui `SELECT` pe o stare trecută a datelor, specificând un moment în timp printr-un timestamp sau un System Change Number (SCN). Nu necesită restaurare din backup și nici downtime: datele istorice sunt citite direct din segmentele de undo.

## Cum funcționează

Oracle păstrează versiunile anterioare ale blocurilor de date în tablespace-urile de undo pentru o perioadă configurabilă (`UNDO_RETENTION`). Flashback Query folosește acest mecanism pentru a reconstrui imaginea datelor așa cum existau la un moment dat.

```sql
-- Interogare prin timestamp
SELECT *
FROM comenzi AS OF TIMESTAMP (SYSTIMESTAMP - INTERVAL '2' HOUR)
WHERE stare = 'ANULAT';

-- Interogare prin SCN
SELECT *
FROM comenzi AS OF SCN 4521890;
```

Clauza `AS OF` este disponibilă în orice `SELECT`, inclusiv în interogări cu JOIN-uri și subinterogări.

## Când se folosește

Scenariile tipice includ recuperarea rândurilor șterse sau modificate din greșeală, analiza datelor înainte de o tranzacție problematică și verificarea conținutului unei tabele înainte de un proces batch nocturn. Principala limitare este disponibilitatea datelor de undo: dacă `UNDO_RETENTION` este prea mic sau tablespace-ul de undo este sub presiune, Oracle poate suprascrie blocurile istorice înainte de expirarea ferestrei configurate. Pentru intervale de timp mai mari sau pentru interogarea istoricului complet al modificărilor rând cu rând, se utilizează Flashback Versions Query sau Flashback Data Archive.
