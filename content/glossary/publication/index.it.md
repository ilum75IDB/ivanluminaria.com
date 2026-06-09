---
title: "Publication"
description: "Oggetto PostgreSQL della replica logica che definisce l'insieme di tabelle (e righe, dalla 15) i cui cambiamenti vengono resi disponibili ai subscriber."
translationKey: "glossary_publication"
aka: "PostgreSQL Logical Replication Publication"
articles:
  - "/posts/postgresql/replica-logica-in-postgresql-scenari-d-uso-configurazione-e-monitoraggio"
---

**Publication** è un oggetto della replica logica PostgreSQL che definisce un insieme di tabelle i cui cambiamenti vengono resi disponibili per la replica. Risiede sul **publisher** (il database sorgente) e può essere consumata da uno o più subscriber indipendenti, ciascuno con la propria subscription.

## Come si crea

Si dichiara con `CREATE PUBLICATION` specificando le tabelle da includere. Dalla versione 15 è possibile aggiungere anche una clausola `WHERE` per filtrare le righe replicate:

```sql
CREATE PUBLICATION mia_pub
  FOR TABLE clienti, ordini
  WHERE (status = 'active');
```

## Cosa non contiene

Una publication trasporta cambiamenti **DML** (INSERT, UPDATE, DELETE, TRUNCATE) ma **non DDL**: le modifiche di schema (ALTER TABLE, CREATE INDEX) devono essere applicate manualmente su entrambi i lati della replica, o con strumenti di orchestrazione esterni. Anche le **sequence** non sono replicate per default.

## Quando si usa

Tipicamente in scenari di migrazione cross-versione di PostgreSQL, integrazione CDC verso un data warehouse, o replica selettiva di sotto-insiemi di tabelle su nodi di staging. Una stessa publication può alimentare più subscriber in parallelo, ognuno con il proprio ritmo di consumo.
