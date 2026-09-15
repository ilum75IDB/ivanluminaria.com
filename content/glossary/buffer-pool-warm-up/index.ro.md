---
title: "Buffer pool warm-up"
description: "Proces de reîncărcare a paginilor fierbinți în buffer pool-ul InnoDB după un restart, pentru a reduce cold start-ul de la ore la minute."
translationKey: "glossary_buffer_pool_warm_up"
aka: "Buffer pool preloading"
articles:
  - "/posts/mysql/innodb-buffer-pool-dimensionamento-hit-ratio-e-warm-up-dopo-restart"
---

Când MySQL repornește, buffer pool-ul este gol: fiecare interogare trebuie să citească de pe disc până când paginile cele mai utilizate revin în memorie. Buffer pool warm-up este procesul care accelerează această revenire la regim normal, restaurând paginile fierbinți înainte ca traficul de producție să le solicite.

## Cum funcționează

InnoDB poate salva identificatorii paginilor rezidente în memorie la momentul shutdown-ului și să îi reîncarce la următoarea pornire. Două variabile de sistem controlează comportamentul:

```sql
-- Activează dump-ul automat la oprire
SET GLOBAL innodb_buffer_pool_dump_at_shutdown = ON;

-- Activează încărcarea automată la pornire (se setează în my.cnf)
-- innodb_buffer_pool_load_at_startup = ON
```

Fișierul generat (`ib_buffer_pool`) conține perechi `(tablespace_id, page_id)`, nu datele efective: este ușor ca dimensiune, iar restaurarea rulează în fundal fără a bloca conexiunile primite. Variabila `innodb_buffer_pool_dump_pct` (implicit 25) limitează procentul de pagini serializate, echilibrând completitudinea cu timpul de dump.

## Când se folosește

Warm-up-ul este relevant în trei scenarii principale:

- **Reporniri planificate** (patch-uri OS, upgrade-uri MySQL): fără warm-up, hit ratio-ul poate rămâne sub 50% ore întregi pe instanțe cu buffer pool-uri de zeci de GB.
- **Failover pe replică**: o replică promovată la primary pornește cu buffer pool-ul rece; activarea dump/load și pe replici reduce degradarea post-failover.
- **Medii cloud cu instanțe spot/preemptible**: ciclurile frecvente de oprire-pornire fac warm-up-ul automat aproape obligatoriu.

Progresul încărcării poate fi monitorizat în timp real:

```sql
SHOW STATUS LIKE 'Innodb_buffer_pool_load_status';
```
