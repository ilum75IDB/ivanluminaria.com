---
title: "Refresh (MV)"
description: "Actualizarea unei Materialized View: COMPLETE (recalcul total) sau FAST (incremental prin MV log). Alegere arhitecturală cu impact direct asupra performanței și prospeții datelor."
translationKey: "glossary_refresh"
aka: "Materialized View Refresh"
articles:
  - "/posts/data-warehouse/la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto"
---

Refresh-ul este operațiunea care resincronizează datele unei Materialized View cu tabelele de bază din care derivă. Fără el, MV rămâne un snapshot static: rapid de interogat, dar din ce în ce mai desincronizat față de datele sursă reale.

## Moduri de refresh

Există două modalități principale:

- **COMPLETE**: recalculează întreaga MV de la zero. Simplu de gestionat, costisitor pe volume mari.
- **FAST**: aplică doar modificările înregistrate într-un MV log (structură de change tracking creată pe tabela de bază). Necesită existența log-ului și impune restricții asupra query-ului definit în MV.

```sql
-- Refresh complet (Oracle)
EXEC DBMS_MVIEW.REFRESH('MV_REVENUE_DAILY', method => 'C');

-- Refresh incremental — necesită MV log pe tabela de bază
EXEC DBMS_MVIEW.REFRESH('MV_REVENUE_DAILY', method => 'F');
```

Pe PostgreSQL, refresh-ul este întotdeauna COMPLETE (`REFRESH MATERIALIZED VIEW`), cu opțiunea `CONCURRENTLY` pentru a evita blocarea citirilor în timpul operațiunii.

## Când se alege fiecare modalitate

FAST refresh reduce timpul de actualizare, dar adaugă complexitate operațională: MV log-ul consumă spațiu, trebuie întreținut și nu este compatibil cu orice query — agregările complexe, `DISTINCT` sau subcererile corelate îl exclud frecvent. COMPLETE este întotdeauna aplicabil, dar nu scalează bine pe tabele cu milioane de rânduri.

Frecvența contează la fel de mult ca modalitatea: un refresh la cerere, unul programat orar sau unul automat ON COMMIT au implicații radical diferite asupra throughput-ului tranzacțiilor de bază și a latenței datelor.
