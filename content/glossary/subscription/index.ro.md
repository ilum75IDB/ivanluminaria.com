---
title: "Subscription"
description: "Obiect PostgreSQL al subscriber-ului care stabilește conexiunea la publisher și gestionează ciclul de viață al replicării logice: snapshot inițial, streaming, reconectare."
translationKey: "glossary_subscription"
aka: "PostgreSQL Logical Replication Subscription"
articles:
  - "/posts/postgresql/replica-logica-in-postgresql-scenari-d-uso-configurazione-e-monitoraggio"
---

**Subscription** este obiectul care, pe partea **subscriber** (baza de date destinație), stabilește conexiunea la publisher-ul PostgreSQL, specifică publication-ul la care se abonează și gestionează întregul ciclu de viață al replicării logice: snapshot inițial al datelor, streaming al modificărilor incrementale, reconectare automată în caz de întrerupere.

## Cum se creează

Se declară cu `CREATE SUBSCRIPTION`, indicând conexiunea la publisher și publication-ul de consumat:

```sql
CREATE SUBSCRIPTION sub_mea
  CONNECTION 'host=pg-primary user=replica_user dbname=app'
  PUBLICATION pub_mea;
```

În momentul creării se efectuează un snapshot inițial al tabelelor, apoi pornește streaming-ul continuu prin WAL.

## Stare și monitorizare

View-ul `pg_stat_subscription` expune starea fiecărei subscription active: poziția curentă de aplicare, latența, ultimul eveniment primit. Este punctul de intrare pentru troubleshooting-ul lag-ului sau al blocajelor.

## Limite operaționale

O subscription **nu poate** fi pusă în pauză/reluată nativ înainte de versiunea 14 — se dezactivează cu `ALTER SUBSCRIPTION ... DISABLE`. În caz de **conflicte** (rând deja prezent pe destinație, încălcare de constraint) streaming-ul se oprește și trebuie rezolvat manual înainte de reluare.
