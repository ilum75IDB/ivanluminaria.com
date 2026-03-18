---
title: "pg_trgm"
description: "Extensie PostgreSQL care oferă funcții și operatori pentru căutare de similaritate bazată pe trigrame, activând indexuri GIN pentru LIKE cu wildcarduri."
translationKey: "glossary_pg-trgm"
articles:
  - "/posts/postgresql/like-optimization-postgresql"
---

**pg_trgm** este o extensie PostgreSQL care implementează căutarea bazată pe trigrame — secvențe de trei caractere consecutive extrase din text. Activează utilizarea indexurilor GIN și GiST pentru a accelera căutări `LIKE '%valoare%'` și `ILIKE`, care altfel ar necesita scanări secvențiale.

## Cum funcționează

Extensia descompune fiecare șir în trigrame: de exemplu, "hello" devine {"  h", " he", "hel", "ell", "llo", "lo "}. Un index GIN cu operator class `gin_trgm_ops` indexează aceste trigrame. Când se execută un `LIKE '%ell%'`, PostgreSQL caută trigramele corespunzătoare în index în loc să scaneze întreaga tabelă.

## La ce folosește

pg_trgm rezolvă una dintre cele mai comune probleme din PostgreSQL: căutarea "conține" pe coloane de text mari. Fără pg_trgm, un `LIKE '%valoare%'` pe o tabelă cu milioane de rânduri necesită o scanare completă. Cu pg_trgm și un index GIN, aceeași căutare folosește indexul și răspunde în milisecunde.

## Când se folosește

Se activează cu `CREATE EXTENSION IF NOT EXISTS pg_trgm` și se creează indexul cu `USING gin (coloana gin_trgm_ops)`. Este ideal pe tabele cu churn scăzut (puține UPDATE/DELETE). Crearea indexului trebuie făcută cu `CONCURRENTLY` în producție pentru a evita lock-urile.
