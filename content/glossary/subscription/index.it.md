---
title: "Subscription"
description: "Oggetto PostgreSQL del subscriber che stabilisce la connessione al publisher e gestisce il ciclo di vita della replica logica: snapshot iniziale, streaming, riconnessione."
translationKey: "glossary_subscription"
aka: "PostgreSQL Logical Replication Subscription"
articles:
  - "/posts/postgresql/replica-logica-in-postgresql-scenari-d-uso-configurazione-e-monitoraggio"
---

**Subscription** è l'oggetto che, sul lato **subscriber** (il database destinazione), stabilisce la connessione al publisher PostgreSQL, specifica la publication a cui iscriversi e gestisce l'intero ciclo di vita della replica logica: snapshot iniziale dei dati, streaming delle modifiche incrementali, riconnessione automatica in caso di interruzione.

## Come si crea

Si dichiara con `CREATE SUBSCRIPTION`, indicando la connessione al publisher e la publication da consumare:

```sql
CREATE SUBSCRIPTION mia_sub
  CONNECTION 'host=pg-primary user=replica_user dbname=app'
  PUBLICATION mia_pub;
```

All'istante della creazione viene effettuato uno snapshot iniziale delle tabelle, poi parte lo streaming continuo via WAL.

## Stato e monitoraggio

La vista `pg_stat_subscription` espone lo stato di ogni subscription attiva: posizione corrente di applicazione, latenza, ultimo evento ricevuto. È il punto di ingresso per il troubleshooting di lag o di stalli.

## Limiti operativi

Una subscription **non può** essere paused/resumed nativamente prima della 14 — si disabilita con `ALTER SUBSCRIPTION ... DISABLE`. In caso di **conflitti** (riga già presente sul destinazione, violazione di constraint) lo streaming si ferma e va risolto manualmente prima di riprendere.
