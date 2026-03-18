---
title: "Dead Tuple"
description: "Rând obsolet într-o tabelă PostgreSQL, marcat ca nevizibil după un UPDATE sau DELETE dar încă neșters fizic de pe disc."
translationKey: "glossary_dead-tuple"
aka: "Tuplu mort"
articles:
  - "/posts/postgresql/vacuum-autovacuum-postgresql"
---

Un **Dead Tuple** este un rând într-o tabelă PostgreSQL care a fost actualizat (UPDATE) sau șters (DELETE) dar nu a fost încă eliminat fizic. Rămâne în paginile de date, ocupând spațiu pe disc și încetinind scanările.

## Cum funcționează

Când PostgreSQL execută un UPDATE, nu suprascrie rândul original: creează o versiune nouă și o marchează pe cea veche ca "moartă." Rândul vechi rămâne fizic în pagina de date până când VACUUM îl curăță. Dead tuple-urile sunt prețul modelului MVCC — necesare pentru a garanta izolarea tranzacțională.

## La ce servește

Dead tuple-urile sunt un indicator cheie al sănătății unei tabele. Vizualizarea `pg_stat_user_tables` arată `n_dead_tup` și `last_autovacuum` — dacă dead tuple-urile cresc mai repede decât poate curăța autovacuum-ul, tabela are o problemă. Un dead_tuple_percent peste 20-30% este un semnal de alarmă.

## Ce poate merge prost

Pe o tabelă cu 500.000 de update-uri pe zi și valorile implicite ale autovacuum-ului (scale_factor 0.2), VACUUM se activează la fiecare 4 zile. Între timp dead tuple-urile se acumulează, tabelele se umflă iar interogările încetinesc progresiv — tiparul "luni bine, vineri dezastru".
