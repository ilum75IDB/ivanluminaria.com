---
title: "ALTER TYPE ADD VALUE"
description: "Comandă PostgreSQL care adaugă o valoare la un ENUM existent. Operație de metadata, tranzacțională, fără rebuild al tabelului care folosește tipul."
translationKey: "glossary_postgresql_alter_type_add_value"
aka: "Extinderea ENUM PostgreSQL"
articles:
  - "/posts/postgresql/enum-postgresql-paga-o-pesa"
---

`ALTER TYPE ... ADD VALUE` este comanda PostgreSQL care adaugă o valoare nouă la un tip enumerativ deja existent. Este una dintre modificările DDL cele mai frecvente pe un ENUM, și este una **dintre diferențele principale** față de MySQL: în PostgreSQL nu necesită un rebuild al tabelului care folosește tipul.

## Cum funcționează

Sintaxă: `ALTER TYPE nume_tip ADD VALUE 'valoare_noua' [BEFORE|AFTER 'alta_valoare']`. Fără clauza pozițională, noua valoare merge la coada listei. Cu `BEFORE` sau `AFTER`, este inserată în poziția specificată, influențând ordinea folosită de `ORDER BY` pe acea coloană. Disponibilă din PostgreSQL 9.1; poziționarea `BEFORE`/`AFTER` a venit cu 9.6.

## La ce folosește

La extinderea vocabularului unui ENUM fără a fi nevoie să recreezi tipul. Este o operație de **doar metadata**: PostgreSQL actualizează catalogul `pg_enum` fără să atingă tabelele care folosesc tipul, chiar dacă conțin miliarde de rânduri. Se execută în milisecunde, în interiorul unei tranzacții, cu posibilitate de rollback dacă ceva merge greșit la deploy.

## Când se folosește

Este modificarea naturală în ciclul de viață al unui ENUM PostgreSQL: produs nou, canal nou, politică de business nouă → o valoare nouă de adăugat la set. Spre deosebire de `ADD VALUE`, în PostgreSQL **nu există un `DROP VALUE` nativ**: eliminarea unei valori necesită recrearea tipului de la zero și migrarea coloanelor care îl folosesc. Această asimetrie este principala limitare operațională a tipului ENUM în PostgreSQL.
