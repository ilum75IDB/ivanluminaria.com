---
title: "VACUUM"
description: "Comandă PostgreSQL care recuperează spațiul ocupat de dead tuples, făcându-l reutilizabil pentru inserări noi fără a-l returna sistemului de operare."
translationKey: "glossary_vacuum"
aka: "PostgreSQL VACUUM"
articles:
  - "/posts/postgresql/vacuum-autovacuum-postgresql"
---

**VACUUM** este comanda PostgreSQL care recuperează spațiul ocupat de dead tuples (rânduri moarte) și îl face disponibil pentru inserări noi. Nu returnează spațiu sistemului de operare, nu reorganizează tabela și nu compactează nimic — marchează paginile ca rescriptibile.

## Cum funcționează

`VACUUM tabela` scanează tabela, identifică dead tuple-urile care nu mai sunt vizibile niciunei tranzacții și marchează spațiul lor ca reutilizabil. Este o operațiune ușoară care nu blochează scrierile și poate rula în paralel cu interogările normale. `VACUUM FULL` în schimb rescrie fizic întreaga tabelă cu lock exclusiv — de folosit foarte rar și doar în urgențe.

## La ce servește

Fără VACUUM, tabelele cu trafic intens de UPDATE și DELETE acumulează dead tuples care ocupă spațiu pe disc și încetinesc scanările secvențiale. VACUUM este mecanismul esențial de curățare care echilibrează costul modelului MVCC al PostgreSQL.

## De ce contează

Autovacuum rulează VACUUM automat, dar cu valorile implicite ale PostgreSQL se poate activa prea rar pe tabelele cu trafic intens. Pe o tabelă cu 10 milioane de rânduri, valoarea implicită așteaptă 2 milioane de dead tuples înainte de a acționa — suficient pentru a degrada vizibil performanțele.
