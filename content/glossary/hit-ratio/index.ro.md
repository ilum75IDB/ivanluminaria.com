---
title: "Hit ratio"
description: "Procentajul citirilor InnoDB servite din Buffer Pool față de total. Valori sub 990/1000 indică presiune excesivă pe disc."
translationKey: "glossary_hit_ratio"
aka: "Buffer Pool hit ratio"
articles:
  - "/posts/mysql/innodb-buffer-pool-dimensionamento-hit-ratio-e-warm-up-dopo-restart"
---

Hit ratio-ul măsoară câte citiri de pagini InnoDB sunt rezolvate direct din Buffer Pool, fără acces la disc. Este indicatorul principal al eficienței memoriei alocate InnoDB: o valoare ridicată înseamnă că working set-ul activ încape în RAM; o valoare scăzută înseamnă I/O fizic frecvent și latențe mai mari.

## Cum se citește

MySQL raportează hit ratio-ul în ieșirea comenzii `SHOW ENGINE INNODB STATUS`, în secțiunea `BUFFER POOL AND MEMORY`:

```
Buffer pool hit rate X / 1000
```

O valoare de `997 / 1000` înseamnă că 997 din 1000 de citiri au fost servite din memorie. Pragul operațional acceptat în general este **990/1000**: scăderea sub acest nivel semnalează că Buffer Pool-ul este subdimensionat față de working set-ul activ.

## Context operațional

Hit ratio-ul este deosebit de instabil după un restart MySQL: Buffer Pool-ul este rece, iar primele interogări generează page fault-uri în cascadă, coborând valoarea chiar și sub 900/1000. InnoDB oferă dump și reload automat al Buffer Pool-ului (`innodb_buffer_pool_dump_at_shutdown` / `innodb_buffer_pool_load_at_startup`) tocmai pentru a accelera warm-up-ul.

Un hit ratio cronic scăzut nu se rezolvă întotdeauna doar prin creșterea `innodb_buffer_pool_size`. Interogările ineficiente care execută full scan pe tabele mari poluează Buffer Pool-ul cu pagini folosite o singură dată, eliminând datele calde indiferent de cantitatea de memorie disponibilă.
