---
title: "performance_schema"
description: "Schema de sistem MySQL care colectează metrici de execuție în timp real: digest-uri de interogări, wait events și memorie per thread. Baza diagnosticării performanței."
translationKey: "glossary_performance_schema"
aka: "P_S (abreviere uzuală)"
articles:
  - "/posts/mysql/articolo-mysql-saturazione-swap-su-innodb-cluster-3-nodi-analisi-e-fix-dei-param"
---

`performance_schema` este o bază de date de sistem disponibilă în MySQL începând cu versiunea 5.5, concepută pentru a expune metrici interne de execuție ale serverului fără a necesita instrumente externe. Datele sunt colectate în memorie prin structuri de instrumentare cu overhead redus și actualizate în timp real.

## Cum funcționează

Motorul de instrumentare interceptează evenimente interne (interogări, locks, I/O, alocări de memorie) și le agregează în tabele interogabile prin SQL standard. Principalele zone acoperite sunt:

- **Statement digests**: statistici agregate per interogare normalizată (`events_statements_summary_by_digest`)
- **Wait events**: așteptări pe mutex-uri, I/O, locks (`events_waits_summary_global_by_event_name`)
- **Memorie**: alocări per thread și per componentă (`memory_summary_by_thread_by_event_name`)

```sql
-- Top 10 interogări după latența medie
SELECT
    digest_text,
    count_star,
    ROUND(avg_timer_wait / 1e9, 2) AS avg_ms
FROM performance_schema.events_statements_summary_by_digest
ORDER BY avg_timer_wait DESC
LIMIT 10;
```

Activarea granulară a instrumentelor se controlează prin tabelele `setup_instruments` și `setup_consumers`: pot fi activate doar categoriile necesare pentru a minimiza impactul asupra workload-ului.

## Când se folosește

`performance_schema` este punctul de plecare pentru orice analiză de performanță pe MySQL atunci când nu sunt disponibile instrumente APM externe. Scenarii tipice:

- Identificarea interogărilor lente când slow query log-ul nu este activat
- Diagnosticarea contențiunii pe InnoDB buffer pool sau pe lock-uri la nivel de rând
- Monitorizarea utilizării memoriei per thread în medii cu multe conexiuni concurente (relevant în configurații InnoDB Cluster)

**Limitări de reținut**: datele sunt volatile (se resetează la repornirea serverului), tabelele nu sunt persistate pe disc, iar overhead-ul — deși redus — este măsurabil pe workload-uri cu frecvență foarte ridicată de statement-uri scurte.
