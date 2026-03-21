---
title: "shared_buffers"
description: "Zona de memorie partajată a PostgreSQL care servește drept cache pentru blocurile de date, cel mai important parametru pentru tuning-ul memoriei."
translationKey: "glossary_shared-buffers"
aka: "Shared Buffer Cache"
articles:
  - "/posts/postgresql/pg-stat-statements"
---

**shared_buffers** este parametrul care controlează dimensiunea zonei de memorie partajată pe care PostgreSQL o folosește ca cache pentru blocurile de date citite de pe disc. De fiecare dată când PostgreSQL citește o pagină de date (8 KB), o păstrează în shared_buffers pentru citirile ulterioare.

## Cum funcționează

PostgreSQL alocă memoria pentru shared_buffers la pornirea serviciului. Toate procesele backend partajează această zonă de memorie. Când un proces are nevoie de un bloc de date, caută mai întâi în shared_buffers. Dacă îl găsește (cache hit), citirea este imediată. Dacă nu (cache miss), trebuie să citească de pe disc — o operație cu ordine de mărime mai lentă.

## Cât să aloci

Valoarea implicită este 128 MB — inadecvată pentru orice bază de date de producție. Regula empirică este să configurezi shared_buffers la 25% din RAM-ul disponibil. Pe un server cu 64 GB de RAM, 16 GB este un bun punct de pornire. Valori peste 40% din RAM rareori aduc beneficii deoarece PostgreSQL se bazează și pe cache-ul sistemului de operare.

## Cum să-l monitorizezi

View-ul `pg_stat_bgwriter` arată raportul dintre `buffers_alloc` (blocuri nou alocate) și totalul blocurilor servite. Un cache hit ratio sub 95% sugerează că shared_buffers ar putea fi subdimensionat.
