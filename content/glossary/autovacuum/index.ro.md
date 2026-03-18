---
title: "Autovacuum"
description: "Daemon PostgreSQL care rulează automat VACUUM și ANALYZE pe tabele când numărul de dead tuples depășește un prag configurabil."
translationKey: "glossary_autovacuum"
aka: "Autovacuum Daemon"
articles:
  - "/posts/postgresql/vacuum-autovacuum-postgresql"
---

**Autovacuum** este un daemon PostgreSQL care rulează automat VACUUM și ANALYZE pe tabele când numărul de dead tuples depășește un prag calculat ca: `threshold + scale_factor × n_live_tup`. Cu valorile implicite (threshold=50, scale_factor=0.2), pe o tabelă cu 10 milioane de rânduri se activează după 2 milioane de dead tuples.

## Cum funcționează

Daemon-ul verifică periodic `pg_stat_user_tables` și lansează un worker pentru fiecare tabelă care depășește pragul. Numărul maxim de workeri simultani este controlat de `autovacuum_max_workers` (implicit 3). Parametrul `autovacuum_vacuum_cost_delay` controlează cât se autofrânează vacuum-ul pentru a nu supraîncărca I/O-ul.

## La ce servește

Este custodele tăcut care împiedică tabelele să se umfle din cauza acumulării de dead tuples. Nu trebuie dezactivat niciodată — este cel mai rău lucru pe care îl poți face unui PostgreSQL în producție. Trebuie configurat per-tabelă: tabelele cu trafic intens necesită scale_factor-uri mici (0.01-0.05) și cost_delay redus.

## Ce poate merge prost

Cu valorile implicite, autovacuum-ul este prea conservator pentru tabelele cu trafic intens. 3 workeri pentru zeci de tabele active nu sunt suficienți. Un scale_factor de 20% pe tabele mari generează milioane de dead tuples înainte de intervenție. Tuning-ul per-tabelă cu `ALTER TABLE ... SET (autovacuum_vacuum_scale_factor = 0.01)` este esențial.
