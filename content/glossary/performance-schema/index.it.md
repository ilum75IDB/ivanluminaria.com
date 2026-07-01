---
title: "performance_schema"
description: "Schema di sistema MySQL che raccoglie metriche di esecuzione in tempo reale: query digest, wait events e memoria per thread. Base per la diagnostica delle performance."
translationKey: "glossary_performance_schema"
aka: "P_S (abbreviazione comune)"
articles:
  - "/posts/mysql/articolo-mysql-saturazione-swap-su-innodb-cluster-3-nodi-analisi-e-fix-dei-param"
---

`performance_schema` è un database di sistema presente in MySQL dalla versione 5.5, progettato per esporre metriche di esecuzione interne del server senza richiedere strumenti esterni. I dati sono raccolti in memoria tramite strutture a basso overhead e aggiornati in tempo reale.

## Come funziona

Il motore di strumentazione intercetta eventi interni (query, lock, I/O, allocazioni di memoria) e li aggrega in tabelle consultabili via SQL standard. Le principali aree coperte sono:

- **Statement digest**: statistiche aggregate per query normalizzata (`events_statements_summary_by_digest`)
- **Wait events**: attese su mutex, I/O, lock (`events_waits_summary_global_by_event_name`)
- **Memory**: allocazioni per thread e per componente (`memory_summary_by_thread_by_event_name`)

```sql
-- Top 10 query per latenza media
SELECT
    digest_text,
    count_star,
    ROUND(avg_timer_wait / 1e9, 2) AS avg_ms
FROM performance_schema.events_statements_summary_by_digest
ORDER BY avg_timer_wait DESC
LIMIT 10;
```

L'abilitazione granulare degli strumenti avviene tramite le tabelle `setup_instruments` e `setup_consumers`: è possibile attivare solo le categorie necessarie per ridurre l'impatto sul workload.

## Quando si usa

`performance_schema` è il punto di partenza per qualsiasi analisi di performance su MySQL senza accesso a APM esterni. Scenari tipici:

- Identificare query lente in assenza di slow query log abilitato
- Diagnosticare contese su InnoDB buffer pool o lock di riga
- Monitorare l'utilizzo di memoria per thread in ambienti con molte connessioni concorrenti (rilevante in configurazioni InnoDB Cluster)

**Limiti da tenere presenti**: i dati sono volatili (si azzerano al restart), le tabelle non sono persistenti su disco, e l'overhead — pur basso — è misurabile su workload ad altissima frequenza di statement brevi.
