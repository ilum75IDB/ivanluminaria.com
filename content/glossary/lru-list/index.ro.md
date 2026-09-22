---
title: "LRU list"
description: "Structura cu două zone a InnoDB care gestionează evicția paginilor din buffer pool, protejând datele fierbinți de full scan-urile ocazionale."
translationKey: "glossary_lru_list"
aka: "LRU list (young list + old list)"
articles:
  - "/posts/mysql/innodb-buffer-pool-dimensionamento-hit-ratio-e-warm-up-dopo-restart"
---

LRU list este structura de date prin care InnoDB decide ce pagini să păstreze în buffer pool și pe care să le elimine atunci când memoria este plină. Spre deosebire de un LRU clasic cu listă unică, InnoDB folosește o variantă cu două zone care separă paginile „fierbinți" de cele încărcate recent, reducând riscul ca o operațiune de scanare masivă să expulzeze date accesate frecvent.

## Cum funcționează

Lista este împărțită în două subzone contigue:

- **Young list** (capul listei, ~5/8 din listă): conține paginile accesate de mai multe ori recent. Acestea sunt paginile „fierbinți" pe care InnoDB încearcă să le mențină în cache cât mai mult timp posibil.
- **Old list** (coada listei, ~3/8 din listă): punctul de intrare pentru fiecare pagină încărcată pentru prima dată de pe disc. O pagină rămâne în old list cel puțin `innodb_old_blocks_time` milisecunde (implicit 1000 ms) înainte de a putea fi promovată în young list.

Când buffer pool-ul este plin, InnoDB elimină paginile de la coada old list (cele mai „reci"). Promovarea din old în young are loc doar dacă pagina este accesată din nou după expirarea perioadei de așteptare configurate.

## Context operațional

Mecanismul cu două zone protejează young list în timpul full scan-urilor: paginile citite secvențial intră în old list, dar dacă nu sunt reaccesate în intervalul de timeout, sunt eliminate fără a înlocui vreodată datele fierbinți. Acest lucru este relevant în special în scenarii precum:

- rapoarte nocturne sau joburi ETL care execută `SELECT` pe tabele mari
- `mysqldump` sau backup-uri logice care citesc tabele întregi
- interogări analitice ocazionale pe instanțe OLTP

Parametrii cheie de monitorizat și ajustat sunt `innodb_old_blocks_pct` (procentul rezervat pentru old list, implicit 37) și `innodb_old_blocks_time`. O valoare prea mică pentru `innodb_old_blocks_time` face protecția ineficientă; una prea mare poate întârzia promovarea paginilor cu adevărat fierbinți.
