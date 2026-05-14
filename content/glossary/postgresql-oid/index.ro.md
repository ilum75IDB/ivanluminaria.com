---
title: "OID (Object Identifier)"
description: "Identificator numeric intern folosit de PostgreSQL pentru a se referi la obiecte de sistem (tabele, tipuri, funcții). Întreg fără semn de 4 octeți."
translationKey: "glossary_postgresql_oid"
aka: "PostgreSQL OID, Object Identifier"
articles:
  - "/posts/postgresql/enum-postgresql-paga-o-pesa"
---

**OID** (Object Identifier) este un identificator numeric intern pe care PostgreSQL îl folosește pentru a se referi la obiecte de sistem: tabele, tipuri de date, funcții, scheme, roluri. Este un întreg fără semn de 4 octeți gestionat de PostgreSQL însuși, distinct de cheile primare ale tabelelor utilizator.

## Cum funcționează

Fiecare obiect din catalogul de sistem (de ex. `pg_class` pentru tabele, `pg_type` pentru tipuri, `pg_enum` pentru valori ENUM) are o coloană `oid` care funcționează ca identificator unic. OID-urile sunt atribuite automat de motor și folosite ca chei în JOIN-urile între cataloagele de sistem. PostgreSQL expune mai multe funcții de conversie (`oid::regclass`, `oid::regtype`, etc.) pentru a obține numele lizibil al unui obiect din OID-ul său.

## La ce folosește

Pentru a identifica fiecare obiect al bazei de date în mod unic și stabil prin dump-restore. Pentru tipurile ENUM, fiecare valoare declarată în `CREATE TYPE ... AS ENUM` primește un OID, care este salvat în rândurile tabelului care folosește tipul. Asta permite stocarea valorii în doar 4 octeți menținând în același timp legătura cu numele lizibil și ordinea pozițională.

## Când se folosește

Rareori direct în aplicații — OID-ul este un detaliu de implementare pe care majoritatea interogărilor nu îl văd. Devine relevant când se analizează cataloagele de sistem (`information_schema`, `pg_catalog`), când se scriu instrumente de introspection sau monitoring, și când se debuggează comportamentul tipurilor complexe precum ENUM-urile sau domain-urile.
