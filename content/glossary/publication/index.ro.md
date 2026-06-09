---
title: "Publication"
description: "Obiect PostgreSQL al replicării logice care definește setul de tabele (și rânduri, din 15) ale căror modificări sunt puse la dispoziția subscriber-ilor."
translationKey: "glossary_publication"
aka: "PostgreSQL Logical Replication Publication"
articles:
  - "/posts/postgresql/replica-logica-in-postgresql-scenari-d-uso-configurazione-e-monitoraggio"
---

**Publication** este un obiect al replicării logice PostgreSQL care definește un set de tabele ale căror modificări sunt puse la dispoziție pentru replicare. Trăiește pe **publisher** (baza de date sursă) și poate fi consumată de unul sau mai mulți subscriberi independenți, fiecare cu propria subscription.

## Cum se creează

Se declară cu `CREATE PUBLICATION` specificând tabelele de inclus. Din versiunea 15 se poate adăuga și o clauză `WHERE` pentru filtrarea rândurilor replicate:

```sql
CREATE PUBLICATION pub_mea
  FOR TABLE clienti, comenzi
  WHERE (status = 'active');
```

## Ce nu transportă

O publication transportă modificări **DML** (INSERT, UPDATE, DELETE, TRUNCATE) dar **nu DDL**: modificările de schemă (ALTER TABLE, CREATE INDEX) trebuie aplicate manual pe ambele părți ale replicării, sau cu unelte externe de orchestrare. Nici **sequence**-urile nu sunt replicate implicit.

## Când se folosește

Tipic în scenarii de migrare cross-versiune PostgreSQL, integrare CDC către un data warehouse, sau replicare selectivă a unor subseturi de tabele pe noduri de staging. O singură publication poate alimenta mai mulți subscriberi în paralel, fiecare cu propriul ritm de consum.
