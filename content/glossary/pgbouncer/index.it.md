---
title: "PgBouncer"
description: "Connection pooler leggero per PostgreSQL che riduce il costo delle connessioni mantenendo un pool ridotto di connessioni reali verso il database."
translationKey: "glossary_pgbouncer"
aka: "PgBouncer (PostgreSQL Connection Pooler)"
articles:
  - "/posts/postgresql/pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600"
---

PgBouncer è un connection pooler leggero per PostgreSQL, scritto in C con I/O asincrono. Si posiziona tra i client e il database, mantenendo un pool ridotto di connessioni reali verso PostgreSQL e riutilizzandole tra molti client concorrenti, abbattendo il costo di fork/autenticazione per ogni nuova connessione.

## Come funziona

PgBouncer intercetta le connessioni in arrivo e le mappa su un sottoinsieme di connessioni reali già aperte verso PostgreSQL. Supporta tre modalità di pooling:

- **Session pooling**: una connessione reale è assegnata al client per tutta la durata della sessione.
- **Transaction pooling**: la connessione reale è rilasciata al pool dopo ogni COMMIT o ROLLBACK. È la modalità più efficiente ma incompatibile con alcune funzionalità stateful (prepared statements lato server, `SET LOCAL`, advisory locks).
- **Statement pooling**: rilascio dopo ogni singola istruzione. Raramente usata in produzione.

La configurazione minima avviene tramite file `.ini`:

```ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
```

## Quando si usa

PgBouncer è indicato quando il numero di connessioni client supera la soglia sostenibile da PostgreSQL (tipicamente oltre 200-300 connessioni attive), oppure quando applicazioni stateless come worker o microservizi aprono e chiudono connessioni ad alta frequenza. Non sostituisce una progettazione corretta del connection management lato applicazione, ma ne attenua gli effetti su carichi elevati.

In transaction pooling, parametri come `server_reset_query` e la gestione dei prepared statements richiedono attenzione specifica per evitare comportamenti inattesi.
