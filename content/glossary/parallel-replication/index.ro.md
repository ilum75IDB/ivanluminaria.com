---
title: "Parallel Replication"
description: "Mod de replicare MySQL care aplică evenimentele din binlog cu mai mulți worker threads, reducând lag-ul replicii prin gruparea LOGICAL_CLOCK."
translationKey: "glossary_parallel_replication"
aka: "Multi-threaded Replication (MTR)"
articles:
  - "/posts/mysql/mysql-slave-lag-diagnosi-e-fix-con-parallel-replication"
---

Parallel Replication este modul în care MySQL aplică evenimentele din binlog pe replică folosind mai mulți worker threads simultan, înlocuind tradiționalul SQL thread unic. Scopul este reducerea replication lag-ului atunci când primarul generează tranzacții mai rapid decât replica le poate aplica secvențial.

## Cum funcționează

MySQL expune două politici configurabile prin `slave_parallel_type`:

- **`DATABASE`**: paralelizează tranzacțiile care modifică baze de date diferite. Este eficient doar dacă încărcarea este distribuită pe mai multe scheme.
- **`LOGICAL_CLOCK`**: folosește commit timestamp-urile înregistrate în binlog pentru a identifica tranzacțiile care rulau concurent pe primar și care pot fi aplicate în paralel pe replică fără a compromite consistența.

`LOGICAL_CLOCK` este modul recomandat în majoritatea scenariilor. Numărul de workers se controlează prin `slave_parallel_workers`.

```sql
-- Configurare tipică pe replică
SET GLOBAL slave_parallel_type = 'LOGICAL_CLOCK';
SET GLOBAL slave_parallel_workers = 8;
```

## Când se folosește

Parallel Replication devine relevantă când replica acumulează lag chiar dacă hardware-ul nu este saturat — blocajul este serializarea evenimentelor, nu resursele. Este deosebit de eficientă pe workload-uri OLTP cu multe tranzacții scurte și concurente pe primar.

Există și limitări: dacă primarul rulează tranzacții preponderent seriale sau concentrate pe o singură tabelă, câștigul este marginal. Creșterea `slave_parallel_workers` peste un anumit prag introduce overhead de coordonare care poate degrada performanța în loc să o îmbunătățească. Valoarea optimă trebuie determinată empiric în funcție de profilul real al încărcării.
