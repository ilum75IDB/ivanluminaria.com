---
title: "Transaction Pooling"
description: "Modalità di connection pooling in cui il backend viene assegnato al client solo per la durata di una transazione, massimizzando il riuso delle connessioni reali."
translationKey: "glossary_transaction_pooling"
aka: "Transaction-level pooling"
articles:
  - "/posts/postgresql/pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600"
---

Il Transaction Pooling è la modalità di pooling più aggressiva disponibile in strumenti come PgBouncer: una connessione al backend PostgreSQL viene assegnata a un client solo per il tempo strettamente necessario a completare una transazione. Non appena arriva il COMMIT o il ROLLBACK, il backend torna immediatamente nel pool, pronto per un altro client.

## Come funziona

Dal punto di vista del client, la connessione sembra persistente. Internamente, il pooler intercetta i boundary di transazione e riassegna il backend fisico ad ogni ciclo. Con 1000 client connessi e transazioni brevi, possono bastare 20-50 connessioni reali verso PostgreSQL.

Il parametro chiave in PgBouncer è `pool_mode = transaction` nella sezione `[pgbouncer]` o per singolo database:

```ini
[databases]
mydb = host=127.0.0.1 port=5432 pool_mode=transaction
```

## Quando si usa e limiti

È la scelta standard per applicazioni web ad alto numero di connessioni concorrenti (es. backend con connection pool applicativo + PgBouncer davanti a PostgreSQL). Riduce drasticamente il numero di processi backend attivi, abbassando il consumo di memoria e i context switch.

I limiti sono reali: funzionalità che dipendono dallo stato di sessione — prepared statements lato server, `SET` di variabili di sessione, advisory locks, cursori `WITH HOLD` — non funzionano correttamente in Transaction Pooling perché la sessione backend cambia tra una transazione e l'altra. In questi casi occorre usare Session Pooling oppure disabilitare le funzionalità incompatibili lato applicazione.
