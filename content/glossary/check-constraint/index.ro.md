---
title: "CHECK constraint"
description: "Constrângere SQL standard care limitează valorile admise într-o coloană printr-o expresie booleană."
translationKey: "glossary_check_constraint"
aka: "CHECK constraint"
articles:
  - "/posts/mysql/enum-mysql-semplifica-o-complica"
---

**CHECK constraint** este o constrângere SQL standard care limitează valorile admise într-o coloană sau tabelă printr-o expresie booleană. Când un `INSERT` sau `UPDATE` ar produce o valoare care încalcă expresia, baza de date respinge operațiunea.

## Cum funcționează

Se declară la nivel de coloană sau de tabelă în `CREATE TABLE` sau se adaugă ulterior cu `ALTER TABLE ADD CONSTRAINT`. Expresia poate fi orice condiție booleană validă: `status IN ('NEW','ACTIVE','CLOSED')`, `pret > 0`, `data_sfarsit >= data_inceput`. Constrângerea este evaluată la fiecare scriere pe coloană.

## La ce servește

Garantarea integrității datelor direct în schemă, fără a fi nevoie de validare la nivel aplicativ. Este utilă în special pentru:

- Limitarea unui câmp la un set de valori (alternativă la ENUM)
- Constrângeri inter-coloană (ex. coerență date, sume care trebuie să corespundă)
- Validare de format de bază (ex. email-uri, coduri fiscale)

## Când se folosește în MySQL

Atenție la versiune: înainte de **MySQL 8.0.16** constrângerile CHECK erau parsate și ignorate în tăcere. Doar de la 8.0.16 sunt aplicate cu adevărat. Este ceva care a surprins mulți dezvoltatori migrați de la PostgreSQL sau Oracle, unde CHECK funcționează dintotdeauna.

Față de ENUM, CHECK este mai flexibilă (redenumirea unei valori este doar un `ALTER CONSTRAINT`) dar mai verboasă. Merge pentru seturi de 5-15 valori care se ating din când în când, fără nevoia de atribute suplimentare.
