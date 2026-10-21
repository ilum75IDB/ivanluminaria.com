---
title: "SQL*Net roundtrips to/from client"
description: "Statistică de sesiune Oracle care numără schimburile de rețea între client și baza de date. Valori ridicate indică o aplicație chatty penalizată de latența WAN."
translationKey: "glossary_sql_net_roundtrips_to_from_client"
aka: "SQL*Net message roundtrips"
articles:
  - "/posts/oracle/latenza-wan-e-change-control-gxp-il-costo-reale-del-lift-and-shift"
---

`SQL*Net roundtrips to/from client` este o statistică de sesiune Oracle care numără de câte ori clientul și baza de date schimbă un mesaj de rețea complet în timpul unei sesiuni. Nu măsoară octeții transferați, ci numărul de cicluri cerere/răspuns pe canalul SQL*Net. Fiecare FETCH, fiecare apel de procedură la distanță și fiecare răspuns al serverului incrementează contorul.

## Cum funcționează

Oracle expune valoarea prin `V$SESSTAT` (sau `V$MYSTAT` pentru sesiunea curentă), unită cu `V$STATNAME`:

```sql
SELECT s.value AS roundtrips
FROM   v$mystat s
JOIN   v$statname n ON n.statistic# = s.statistic#
WHERE  n.name = 'SQL*Net roundtrips to/from client';
```

Fiecare ciclu cerere/răspuns între stratul aplicației și listener-ul Oracle contează ca un roundtrip. Cu un `arraysize` mic sau cu recuperare rând cu rând, roundtrip-urile cresc liniar cu numărul de rânduri returnate. Creșterea `arraysize` — sau utilizarea `BULK COLLECT` pe partea PL/SQL — reduce roundtrip-urile prin împachetarea mai multor rânduri în fiecare mesaj.

## Context operațional

Statistica devine critică atunci când baza de date este accesată printr-un WAN sau VPN cloud, unde fiecare roundtrip adaugă zeci de milisecunde. O aplicație care efectuează 10 000 de roundtrip-uri pe un LAN de 0,1 ms acumulează aproximativ 1 secundă de latență; pe un WAN de 30 ms, aceeași sarcină de lucru acumulează aproximativ 5 minute. Acesta este profilul tipic al unui lift-and-shift neoptimizat: interogările sunt identice, dar timpul de răspuns perceput se prăbușește.

Raportul dintre `SQL*Net roundtrips` și numărul de rânduri procesate (sau operații COMMIT) este indicatorul cheie. O aplicație bine proiectată menține acest raport scăzut prin batch fetching, connection pooling și eliminarea apelurilor remote inutile.
