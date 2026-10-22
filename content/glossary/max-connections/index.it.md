---
title: "max_connections"
description: "Parametro PostgreSQL che definisce il numero massimo di connessioni simultanee accettabili. Ogni connessione ha un costo reale in memoria e scheduling."
translationKey: "glossary_max_connections"
aka: "max_connections (PostgreSQL connection limit)"
articles:
  - "/posts/postgresql/pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600"
---

`max_connections` è il parametro di `postgresql.conf` che stabilisce quante connessioni client PostgreSQL può accettare contemporaneamente. Non si tratta di un limite arbitrario: ogni connessione attiva un processo backend dedicato, con un costo fisso in memoria condivisa e overhead di scheduling del sistema operativo.

## Come funziona

PostgreSQL usa un modello process-per-connection: per ogni client che si connette viene forkato un processo separato. Il valore di `max_connections` definisce il tetto massimo di questi processi. Superato il limite, il server rifiuta nuove connessioni con un errore esplicito.

```sql
-- Verifica il valore corrente
SHOW max_connections;

-- Connessioni attive in questo momento
SELECT count(*) FROM pg_stat_activity;
```

La modifica richiede riavvio del server perché il parametro determina l'allocazione iniziale della shared memory (in particolare per le lock table e i buffer di processo).

## Contesto operativo

Un valore elevato di `max_connections` non è gratuito: ogni slot occupa circa 5-10 MB di shared memory anche se la connessione è idle. Con 500 connessioni si parla di gigabyte riservati prima ancora che arrivi una query.

Il pattern raccomandato è mantenere `max_connections` basso (tipicamente 100-200 per istanze OLTP) e delegare il multiplexing a un connection pooler come PgBouncer in modalità transaction pooling. In questo modo migliaia di client applicativi condividono un numero contenuto di connessioni reali verso PostgreSQL.

## Note

Modificare `max_connections` verso l'alto richiede anche di rivedere `work_mem` e `shared_buffers`: la memoria disponibile per istanza si divide tra tutti i processi backend attivi. Alzare il limite senza considerare il footprint complessivo porta a memory pressure o, nei casi peggiori, a OOM del sistema operativo.
