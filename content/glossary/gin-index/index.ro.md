---
title: "GIN Index"
description: "Generalized Inverted Index — tip de index PostgreSQL optimizat pentru căutare full-text, pattern matching cu trigrame și interogări pe array-uri și JSONB."
translationKey: "glossary_gin-index"
aka: "Generalized Inverted Index"
articles:
  - "/posts/postgresql/like-optimization-postgresql"
---

Un **GIN Index** (Generalized Inverted Index) este un tip de index PostgreSQL proiectat pentru indexarea valorilor compuse: array-uri, documente JSONB, text cu trigrame și căutări full-text. Spre deosebire de B-Tree, un GIN creează un mapping inversat: de la fiecare element (cuvânt, trigramă, cheie JSON) la înregistrările care îl conțin.

## Cum funcționează

Pentru fiecare valoare distinctă din datele indexate, GIN menține o listă de pointeri către rândurile care conțin acea valoare. În cazul `pg_trgm`, textul este descompus în trigrame (secvențe de 3 caractere) și fiecare trigramă este indexată. O căutare `LIKE '%ABC%'` este tradusă într-o intersecție de trigrame, evitând scanarea secvențială.

## La ce folosește

GIN rezolvă problema căutărilor "conține" (`LIKE '%valoare%'`) pe coloane de text, care cu un B-Tree ar necesita o scanare secvențială a întregii tabele. Pe tabele cu milioane de rânduri, diferența este între secunde și milisecunde.

## Când se folosește

GIN este ideal pe tabele append-only sau cu churn scăzut (puține UPDATE/DELETE), deoarece costul de mentenanță al indexului este mai mare decât al unui B-Tree. Crearea în producție trebuie făcută cu `CREATE INDEX CONCURRENTLY` pentru a evita lock-urile pe scrieri.
