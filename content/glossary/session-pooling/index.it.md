---
title: "Session pooling"
description: "Modalità di pooling in cui una connessione backend resta assegnata al client per tutta la sessione: più compatibile ma meno efficiente del transaction pooling."
translationKey: "glossary_session_pooling"
aka: "Session-level pooling"
articles:
  - "/posts/postgresql/pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600"
---

Nel session pooling una connessione backend viene riservata a un client dal momento in cui si connette fino a quando si disconnette. È la modalità più vicina al comportamento di una connessione diretta e garantisce la massima compatibilità con funzionalità che dipendono dallo stato di sessione: variabili `SET`, cursori, tabelle temporanee, prepared statements.

## Come funziona

Il pool manager (ad esempio PgBouncer) assegna una connessione backend al client all'atto del login e la mantiene riservata per tutta la durata della sessione. Nessun altro client può usarla nel frattempo, anche se il client è idle.

In PgBouncer si configura così:

```ini
[pgbouncer]
pool_mode = session
```

Il numero massimo di connessioni simultanee al database rimane quindi uguale al numero di client attivi, il che limita il guadagno rispetto alle connessioni dirette.

## Quando si usa

Il session pooling è la scelta corretta quando l'applicazione usa funzionalità che richiedono stato persistente di sessione: ORM che emettono `SET search_path`, driver che usano prepared statements con nome, o codice legacy che si aspetta che le variabili di sessione sopravvivano tra una query e l'altra.

È meno efficiente del transaction pooling perché il backend rimane occupato anche durante i periodi di inattività del client. In scenari ad alto numero di connessioni concorrenti, il vantaggio rispetto alle connessioni dirette è principalmente la riduzione dell'overhead di autenticazione e di fork dei processi backend, non una vera multiplexazione.
