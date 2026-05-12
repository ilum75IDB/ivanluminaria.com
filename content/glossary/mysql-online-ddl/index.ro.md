---
title: "Online DDL"
description: "Mecanism MySQL/InnoDB care permite executarea operațiunilor ALTER TABLE fără a bloca scrierile concurente, cu limite precise în funcție de operațiune."
translationKey: "glossary_mysql_online_ddl"
aka: "MySQL Online DDL"
articles:
  - "/posts/mysql/enum-mysql-semplifica-o-complica"
---

**Online DDL** este mecanismul MySQL și al motorului de stocare InnoDB care permite executarea multor operațiuni `ALTER TABLE` fără a bloca scrierile concurente pe tabelă. A fost introdus în MySQL 5.6 și extins progresiv în versiunile ulterioare.

## Cum funcționează

MySQL evaluează automat operațiunea solicitată și alege între trei algoritmi: `INSTANT` (modifică doar metadatele, fracțiune de secundă), `INPLACE` (modifică tabela fără a o copia, suportă DML în paralel), `COPY` (rebuild complet, blochează scrierile). Algoritmul folosit depinde de tipul de ALTER și de versiunea MySQL.

## La ce servește

Reducerea drastică a downtime-ului în timpul mentenanțelor de schemă pe baze de date în producție. Operațiuni ca adăugarea unei coloane la final, adăugarea unui index, modificarea unui default au devenit practic instantanee. Operațiuni mai grele (schimbarea tipului unei coloane, reconstrucția unui index primar) cer încă rebuild, dar adesea cu concurența păstrată.

## Când să fii atent

Online DDL nu este gratis: chiar și `INPLACE` generează încărcare semnificativă pe I/O și replication lag. Pe tabele cu sute de milioane de rânduri, chiar și operațiunile "online" pot produce ore de lag pe replici. În plus, anumite operațiuni (ex. modificarea unei coloane ENUM prin inserarea valorilor la mijloc) cad încă pe `ALGORITHM=COPY` și blochează scrierile. Merită întotdeauna să specifici explicit `ALGORITHM=INPLACE, LOCK=NONE` pentru a fi sigur de comportament, și să testezi prima dată pe o replică.
