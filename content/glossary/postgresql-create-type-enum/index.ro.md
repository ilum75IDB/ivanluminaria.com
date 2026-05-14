---
title: "CREATE TYPE AS ENUM"
description: "Statement DDL PostgreSQL care creează un tip enumerativ ca obiect de primă clasă, refolosibil pe mai multe coloane și modificabil cu ALTER TYPE."
translationKey: "glossary_postgresql_create_type_enum"
aka: "Tipul ENUM PostgreSQL"
articles:
  - "/posts/postgresql/enum-postgresql-paga-o-pesa"
---

`CREATE TYPE ... AS ENUM` este statement-ul DDL al PostgreSQL care declară un tip enumerativ, adică un domeniu închis de valori textuale admise. Spre deosebire de MySQL, în PostgreSQL ENUM este un **tip de date de sine stătător**, nu o decorare a unei coloane `VARCHAR`.

## Cum este construit

Sintaxa de bază: `CREATE TYPE nume_tip AS ENUM ('valoare1','valoare2',...)`. Odată creat, tipul poate fi folosit ca tip al uneia sau mai multor coloane (`stare stare_abonament`), ca tip de parametru pentru funcții și proceduri, și în declarații de indecși parțiali. Intern PostgreSQL stochează fiecare valoare ca un OID de 4 octeți, menținând ordinea pozițională declarată la `CREATE TYPE`.

## La ce folosește

Pentru a impune, la nivel de schemă, apartenența unei valori la un set închis. Este mai strict decât un `CHECK` constraint pentru că definește un **tip** — așa că restricția călătorește cu coloana chiar și prin funcții, view-uri și parametri de procedură. Interogările cu `WHERE stare = 'ACTIV'` rămân lizibile și rapide, fără JOIN cu tabele lookup.

## Când se folosește

Este alegerea corectă când setul de valori este **stabil în timp** (zilele săptămânii, stări binare, polarități tehnice) și semantica trebuie controlată prin schemă. Nu este recomandat când vocabularul evoluează frecvent sau sunt necesare atribute suplimentare (etichete localizate, ordine de afișare, flag-uri), pentru că PostgreSQL nu oferă `ALTER TYPE DROP VALUE` nativ: eliminarea unei valori necesită recrearea tipului și migrarea coloanelor.
