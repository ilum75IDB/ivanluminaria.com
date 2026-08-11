---
title: "Parallel Replication"
description: "Modalità di replica MySQL che applica gli eventi con più worker thread in parallelo, riducendo il lag dello slave tramite LOGICAL_CLOCK."
translationKey: "glossary_parallel_replication"
aka: "Multi-threaded Replication (MTR)"
articles:
  - "/posts/mysql/replica-mysql-quando-lo-slave-resta-indietro-e-nessuno-se-ne-accorge"
---

La Parallel Replication è la modalità con cui MySQL applica gli eventi del binlog sullo slave usando più worker thread contemporaneamente, invece del tradizionale singolo SQL thread. L'obiettivo è ridurre il replication lag quando il master genera transazioni a una velocità superiore a quella con cui lo slave riesce ad applicarle in sequenza.

## Come funziona

MySQL offre due policy configurabili tramite `slave_parallel_type`:

- **`DATABASE`**: parallelizza le transazioni che modificano database diversi. Efficace solo se il carico è distribuito su più schemi.
- **`LOGICAL_CLOCK`**: usa i commit timestamp registrati nel binlog per identificare transazioni che erano in esecuzione contemporaneamente sul master e che quindi possono essere applicate in parallelo sullo slave senza violare la consistenza.

La modalità `LOGICAL_CLOCK` è quella raccomandata nella maggior parte dei casi. Il numero di worker si controlla con `slave_parallel_workers`.

```sql
-- Configurazione tipica sullo slave
SET GLOBAL slave_parallel_type = 'LOGICAL_CLOCK';
SET GLOBAL slave_parallel_workers = 8;
```

## Quando si usa

La Parallel Replication diventa rilevante quando lo slave accumula lag nonostante l'hardware non sia saturo: il collo di bottiglia è la serializzazione degli eventi, non le risorse. È particolarmente efficace su workload OLTP con molte transazioni brevi e concorrenti sul master.

Ha però dei limiti: se il master esegue transazioni prevalentemente seriali o su una singola tabella, il guadagno è marginale. Inoltre, aumentare `slave_parallel_workers` oltre un certo soglia introduce overhead di coordinamento che può peggiorare le prestazioni invece di migliorarle. Il valore ottimale va trovato empiricamente in base al profilo del carico.
