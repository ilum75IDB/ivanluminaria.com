---
title: "Pagină dirty"
description: "Pagină din buffer pool modificată în memorie, dar nescrisă încă pe disc. Un număr mare și în creștere indică că flush-ul InnoDB nu ține pasul cu scrierile."
translationKey: "glossary_pagina_dirty"
aka: "Dirty page, pagină murdară"
articles:
  - "/posts/mysql/innodb-buffer-pool-dimensionamento-hit-ratio-e-warm-up-dopo-restart"
---

În buffer pool-ul InnoDB, o **pagină dirty** este o pagină de 16 KB care a fost modificată în memorie — printr-un INSERT, UPDATE sau DELETE — dar al cărei conținut actualizat nu a fost încă scris în fișierul de date de pe disc. Versiunea de pe disc este, prin urmare, depășită față de cea din RAM.

## Cum funcționează

De fiecare dată când o tranzacție modifică un rând, InnoDB actualizează pagina corespunzătoare din buffer pool și o marchează ca dirty. Un thread de flush în fundal (`page_cleaner`) scrie periodic paginile dirty în fișierele `.ibd`, urmând două strategii principale:

- **Fuzzy checkpoint**: flush continuu și incremental pentru a menține procentul de pagini dirty sub `innodb_max_dirty_pages_pct` (implicit 90%).
- **Flush adaptiv**: accelerează flush-ul atunci când rata de scriere în redo log se apropie de capacitatea maximă, prevenind situația în care InnoDB ar trebui să blocheze scrierile utilizatorilor pentru a elibera spațiu.

```sql
-- Monitorizarea paginilor dirty în timp real
SELECT VARIABLE_NAME, VARIABLE_VALUE
FROM performance_schema.global_status
WHERE VARIABLE_NAME IN (
    'Innodb_buffer_pool_pages_dirty',
    'Innodb_buffer_pool_pages_total'
);
```

## Context operațional

Un număr stabil și redus de pagini dirty este normal. Semnalul de alarmă este o **creștere susținută și monotonă**: înseamnă că thread-ul de flush nu reușește să proceseze scrierile primite suficient de rapid. Cauzele cele mai frecvente sunt un buffer pool supradimensionat față de debitul discului, o valoare prea mică pentru `innodb_io_capacity`, sau un vârf brusc de scrieri.

În cazul unui crash, InnoDB folosește redo log-ul pentru a recupera paginile dirty care nu au fost scrise pe disc. Cu cât există mai multe pagini dirty la momentul crash-ului, cu atât crash recovery-ul va dura mai mult la repornire.
