---
title: "pg_stat_user_indexes"
description: "Vista di sistema PostgreSQL che traccia quante volte ogni indice è stato usato dal planner — strumento principe per identificare indici inutili in produzione."
translationKey: "glossary_pg_stat_user_indexes"
aka: ""
articles:
  - "/posts/postgresql/postgresql-indici-quando-fanno-male"
---

`pg_stat_user_indexes` è una vista di sistema PostgreSQL che espone le statistiche d'uso di tutti gli indici delle tabelle utente (esclusi quelli di sistema). Per ogni indice tiene il conteggio di quante volte il planner lo ha effettivamente scelto.

## Come funziona

La colonna chiave è `idx_scan`: parte da zero al boot del database (o all'ultimo `pg_stat_reset()`) e si incrementa di uno ogni volta che il planner sceglie quell'indice per eseguire una query. Le altre colonne utili includono:

- `idx_tup_read` — quanti puntatori a riga sono stati letti dall'indice
- `idx_tup_fetch` — quante righe sono state poi effettivamente lette dalla tabella tramite l'indice
- `relname` — nome della tabella su cui sta l'indice
- `indexrelname` — nome dell'indice

## A cosa serve

È lo strumento principe per identificare **indici inutili in produzione**. Se un indice ha `idx_scan = 0` dopo settimane o mesi di attività, il planner non l'ha mai considerato utile per nessuna query. È candidato alla rimozione (dopo aver verificato che non sia un indice usato solo per vincoli di unicità o foreign key).

## Quando si usa

Si consulta come prima diagnostica quando si vuole capire quanto valgono davvero gli indici di una tabella, soprattutto quando ce ne sono molti. Esempio tipico:

```sql
SELECT relname, indexrelname, idx_scan,
       pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
WHERE relname = 'tabella'
ORDER BY idx_scan ASC;
```

Da abbinare a `pg_stat_reset()` se serve azzerare le statistiche dopo un cambio significativo del workload.
