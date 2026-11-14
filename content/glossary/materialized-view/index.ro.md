---
title: "Materialized View (MV)"
description: "Vedere pre-calculată și stocată fizic pe disc: interogările citesc date deja agregate, fără recalcul. Suportată de Oracle, PostgreSQL, SQL Server."
translationKey: "glossary_materialized_view"
aka: "Vedere materializată"
articles:
  - "/posts/data-warehouse/la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto"
---

O Materialized View (MV) este o vedere al cărei rezultat este calculat o singură dată și stocat fizic pe disc, spre deosebire de o vedere obișnuită care re-execută interogarea la fiecare acces. Citirile ulterioare găsesc datele deja disponibile: niciun JOIN, nicio agregare de recalculat la runtime.

## Cum funcționează

MV este creată cu o interogare de definiție; motorul execută acea interogare și persistă rezultatul ca și cum ar fi un tabel. Actualizarea se face printr-un **refresh**: complet (`COMPLETE`) sau incremental (`FAST`/`INCREMENTAL`), în funcție de RDBMS și de structura interogării.

```sql
-- PostgreSQL
CREATE MATERIALIZED VIEW mv_revenue_daily AS
SELECT
    date_trunc('day', event_ts) AS day,
    customer_id,
    SUM(amount)                 AS total_revenue
FROM fact_events
GROUP BY 1, 2;

-- Refresh manual
REFRESH MATERIALIZED VIEW mv_revenue_daily;
```

În Oracle, refresh-ul poate fi programat și suportă modul `FAST` prin materialized view logs. În SQL Server, construcția echivalentă este o **Indexed View**.

## Când se folosește

MV-urile sunt instrumentul potrivit atunci când:

- interogarea de bază este costisitoare (agregări pe miliarde de rânduri, JOIN-uri multi-tabel) și datele se modifică rar sau după un program previzibil;
- se dorește separarea încărcării OLTP de cea analitică fără a duplica întregul pipeline;
- un Data Warehouse sau Data Mart necesită straturi pre-agregate pentru dashboard-uri și rapoarte.

Principalul trade-off este **latența datelor**: între un refresh și următorul, MV poate conține date învechite. În contextele unde prospețimea datelor este critică (near-real-time), trebuie evaluat dacă refresh-urile frecvente nu anulează avantajul de performanță.
