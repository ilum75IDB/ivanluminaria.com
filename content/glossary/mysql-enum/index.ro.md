---
title: "ENUM (MySQL)"
description: "Tip de date MySQL care admite un set predefinit de valori șir, stocat intern ca index numeric de 1-2 octeți."
translationKey: "glossary_mysql_enum"
aka: "MySQL ENUM type"
articles:
  - "/posts/mysql/enum-mysql-semplifica-o-complica"
---

**ENUM (MySQL)** este un tip de date care admite doar un set predefinit de valori șir, declarat în momentul creării coloanei. Este una dintre feature-urile caracteristice MySQL — puține alte DBMS-uri mainstream au un tip enumerat nativ.

## Cum funcționează

Când declari `status ENUM('NEW','ACTIVE','CLOSED')`, MySQL atribuie fiecărei valori un index numeric: 'NEW'=1, 'ACTIVE'=2, 'CLOSED'=3. Pe disc se stochează indexul întreg, nu șirul. Conversia are loc la citire. Sub 256 de valori declarate ENUM ocupă 1 octet pe rând; între 256 și 65535, ocupă 2 octeți.

## La ce servește

ENUM oferă trei avantaje concrete: stocare compactă (1-2 octeți în loc de N caractere ale unui VARCHAR), constrângere "doar aceste valori" declarată la nivel de schemă fără un CHECK separat, citire lizibilă în query-uri (`WHERE status = 'ACTIVE'`) fără JOIN împotriva unei tabele de lookup.

## Când se folosește

Este alegerea potrivită atunci când domeniul valorilor este cu adevărat închis și stabil în timp: zilele săptămânii, statusuri binare sau ternare fixe, polaritate, tipuri reglementate prin lege. Este perfect și în interiorul unei lookup table mici (5-50 rânduri), unde limitele sale devin irelevante.

## Limite de știut

- **Case-insensitive**: `'ACTIVE'` și `'active'` sunt aceeași valoare (comportament diferit față de PostgreSQL)
- **Ordonare după poziția de declarare**, nu alfabetică — un `ORDER BY` poate produce rezultate surprinzătoare
- **Modificarea ENUM-ului** (adăugarea unei valori la mijloc, redenumire, reordonare) cere un rebuild al tabelei, costisitor pe tabele mari
