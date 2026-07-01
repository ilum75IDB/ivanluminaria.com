---
title: "join_buffer_size"
description: "Buffer MySQL alocat per thread pentru fiecare join fără index. Înmulțit cu conexiunile active, poate epuiza RAM-ul serverului."
translationKey: "glossary_join_buffer_size"
aka: "Join Buffer (MySQL)"
articles:
  - "/posts/mysql/articolo-mysql-saturazione-swap-su-innodb-cluster-3-nodi-analisi-e-fix-dei-param"
---

`join_buffer_size` este un parametru de sesiune MySQL care controlează dimensiunea buffer-ului folosit pentru a executa join-uri între tabele atunci când nu există un index adecvat. Spre deosebire de `innodb_buffer_pool_size`, care este o resursă partajată, acest buffer este alocat **pentru fiecare thread activ** care execută un astfel de join.

## Cum funcționează

Când MySQL nu poate folosi un index pentru a uni două tabele, recurge la un **Block Nested-Loop Join** (sau, în versiunile mai noi, la un Hash Join). În ambele cazuri, rândurile din tabela "externă" sunt încărcate în `join_buffer` și comparate cu tabela "internă".

```sql
-- Verificarea valorii curente la nivel de sesiune
SHOW VARIABLES LIKE 'join_buffer_size';

-- Modificare pentru sesiunea curentă
SET SESSION join_buffer_size = 4 * 1024 * 1024; -- 4 MB
```

Dacă buffer-ul nu este suficient de mare pentru a conține toate rândurile relevante, MySQL efectuează mai multe treceri peste tabela internă, crescând I/O-ul.

## Context operațional

Riscul principal nu este valoarea absolută a parametrului, ci **efectul său multiplicativ**: cu 500 de conexiuni concurente și un `join_buffer_size` de 8 MB, consumul potențial de memorie depășește 4 GB, indiferent de câte join-uri rulează efectiv în acel moment.

Recomandări practice:

- Menținerea valorii globale la un nivel scăzut (256 KB – 1 MB) și creșterea ei la nivel de sesiune doar pentru interogările specifice care beneficiază de aceasta.
- Înainte de a mări buffer-ul, verificați dacă absența indexului este intenționată sau o omisiune: un index corespunzător elimină problema la sursă.
- Monitorizați `Select_full_join` și `Select_range_check` în `SHOW GLOBAL STATUS` pentru a cuantifica frecvența join-urilor fără index.
