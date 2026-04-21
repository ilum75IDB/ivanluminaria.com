---
title: "information_schema"
description: "Schema de sistem MySQL/MariaDB read-only care expune metadate despre baze de date, tabele, indecși, utilizatori și starea serverului. Baza oricărui assessment și analiză structurală."
translationKey: "glossary_information_schema"
aka: "Information Schema, INFORMATION_SCHEMA"
articles:
  - "/posts/mysql/mysql-pre-upgrade-assessment"
---

**information_schema** este schema virtuală standard SQL pe care MySQL și MariaDB o expun ca interfață de introspecție: nu conține date aplicative, ci metadate despre starea serverului (baze de date prezente, tabele, coloane, indecși, utilizatori, privilegii, parametri de sesiune).

## Cum funcționează

Tabelele din `information_schema` sunt viste peste cataloagele interne ale bazei de date. Cele mai folosite sunt:

- `TABLES` — un rând per tabelă, cu dimensiune, tip engine, număr de rânduri estimat
- `COLUMNS` — un rând per coloană, cu tip de date, nullability, collation
- `STATISTICS` — un rând per index și per coloană inclusă, cu cardinalitate estimată
- `SCHEMATA` — un rând per bază de date
- `PROCESSLIST` — sesiuni active (echivalent cu `SHOW PROCESSLIST`)
- `INNODB_*` — metrici și stare pentru engine-ul InnoDB

## La ce servește

Este punctul de plecare al oricărui assessment: sizing-ul bazei de date, identificarea celor mai mari tabele, audit al indecșilor, analiza tipurilor de date, controlul collation-urilor mixte. Multe script-uri de monitorizare și instrumente BI citesc `information_schema` pentru a construi dashboard-uri de stare.

## Limitări de cunoscut

Valorile `data_length`, `index_length` și `table_rows` sunt **estimări** actualizate periodic de InnoDB și dependente de ultima `ANALYZE TABLE`. Pe tabele foarte volatile pot subestima cu 10-15%. Pentru date critice (plan de migrare, plan de capacitate) este bună practică să verificăm cu dimensiunea fizică a fișierelor `.ibd` (`du -sh /var/lib/mysql/<schema>/*.ibd`).
