---
title: "MVCC"
description: "Multi-Version Concurrency Control — modelul de concurență al PostgreSQL care menține mai multe versiuni ale rândurilor pentru a garanta izolarea tranzacțională fără lock-uri exclusive pe citiri."
translationKey: "glossary_mvcc"
aka: "Multi-Version Concurrency Control"
articles:
  - "/posts/postgresql/vacuum-autovacuum-postgresql"
---

**MVCC** (Multi-Version Concurrency Control) este modelul de concurență folosit de PostgreSQL pentru a gestiona accesul simultan la date. Fiecare UPDATE creează o nouă versiune a rândului și o marchează pe cea veche ca "moartă"; fiecare DELETE marchează rândul ca nevizibil. Citirile nu blochează scrierile și invers.

## Cum funcționează

Fiecare tranzacție vede un snapshot consistent al bazei de date din momentul începerii sale. Rândurile modificate de alte tranzacții neconfirmate sunt invizibile. Aceasta elimină nevoia de lock-uri exclusive pe citiri, permițând concurență ridicată — dar generează "gunoi" sub formă de dead tuples care trebuie curățate de VACUUM.

## La ce servește

MVCC este compromisul arhitectural al PostgreSQL: concurență ridicată fără lock-uri, la prețul de a gestiona curățarea versiunilor obsolete. Este un preț rezonabil — cu condiția ca autovacuum-ul să fie configurat corect pentru a ține pasul cu ritmul de modificare al tabelelor.

## De ce contează

Dacă VACUUM nu poate ține pasul cu rata de generare a dead tuple-urilor, tabelele se umflă (bloat), scanările secvențiale încetinesc iar indexurile devin ineficiente. Tiparul clasic: luni baza de date merge bine, vineri e un dezastru.
