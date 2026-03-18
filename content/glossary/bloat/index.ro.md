---
title: "Bloat"
description: "Spațiu mort acumulat într-o tabelă sau index PostgreSQL din cauza dead tuple-urilor neșterse, care umflă dimensiunea pe disc și degradează performanțele interogărilor."
translationKey: "glossary_bloat"
aka: "Table Bloat / Index Bloat"
articles:
  - "/posts/postgresql/vacuum-autovacuum-postgresql"
---

**Bloat** este acumularea de spațiu mort în cadrul unei tabele sau index PostgreSQL, cauzată de dead tuples care nu au fost încă eliminate de VACUUM. O tabelă cu 50% bloat ocupă de două ori spațiul necesar și forțează scanările secvențiale să citească de două ori mai multe pagini.

## Cum funcționează

Bloat-ul se măsoară comparând dimensiunea efectivă a tabelei cu dimensiunea așteptată bazată pe rândurile vii. Extensia `pgstattuple` oferă câmpul `dead_tuple_percent`. Un bloat peste 20-30% este un semnal de alarmă; peste 50% este o urgență.

## La ce servește

Monitorizarea bloat-ului este esențială pentru a înțelege dacă autovacuum-ul ține pasul. Interogarea `pg_stat_user_tables` cu `n_dead_tup` și `last_autovacuum` este primul instrument de diagnostic. Dacă bloat-ul este scăpat de sub control, `pg_repack` reconstruiește tabela online fără lock-uri exclusive prelungite — spre deosebire de `VACUUM FULL`.

## Ce poate merge prost

VACUUM normal recuperează spațiul dead tuple-urilor dar nu compactează tabela — spațiul fragmentat rămâne. Dacă bloat-ul ajunge la 50-70%, VACUUM singur nu mai este suficient. Opțiunile sunt `VACUUM FULL` (lock exclusiv, blochează totul) sau `pg_repack` (online, dar necesită instalare). Adevărata soluție este să nu ajungi acolo, cu un autovacuum bine configurat.
