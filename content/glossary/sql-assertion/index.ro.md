---
title: "ASSERTION"
description: "Construct SQL standard pentru exprimarea constrângerilor cross-tabel validate la nivel tranzacțional de motorul bazei de date. Anunțat în Oracle 26ai."
translationKey: "glossary_sql_assertion"
aka: "SQL ASSERTION (cross-table constraint)"
articles:
  - "/posts/oracle/enum-oracle-workaround-fino-a-23ai"
  - "/posts/oracle/enum-oracle-19c-26ai-domini"
---

**`ASSERTION`** este un construct prevăzut de standardul SQL — încă din anii '90 — pentru exprimarea constrângerilor care **traversează mai multe tabele**, validate direct de motorul bazei de date la nivel tranzacțional. Pe hârtie este o soluție elegantă pentru probleme care astăzi se rezolvă cu trigger sau cu check aplicative. În practică, până în 2026, niciun DBMS mainstream nu a implementat-o cu adevărat. Oracle a anunțat-o pentru 26ai.

## Cum funcționează (pe hârtie)

`CREATE ASSERTION nume CHECK (<condiție>)` definește o condiție pe care baza de date o garantează întotdeauna adevărată. Spre deosebire de un `CHECK` de tabel (care evaluează un singur rând în momentul INSERT/UPDATE), o `ASSERTION` poate face referință la **mai multe tabele**, poate face agregări, poate număra rânduri. Exemplu: "cel puțin un rând în `stari_x` trebuie să aibă `activ='Y'`", sau "suma sumelor în `linie_comanda` nu poate depăși `total`-ul în `comanda`".

## De ce a întârziat atât

Implementarea `ASSERTION` în mod eficient este dificilă. La fiecare modificare a tabelelor implicate motorul trebuie să revalideze aserțiunea — iar a face asta fără a serializa toate tranzacțiile necesită mecanisme sofisticate de incremental checking sau de lock cross-tabel. Niciun vendor nu a găsit vreodată formula câștigătoare. Oracle 26ai va fi prima încercare serioasă pe un DBMS comercial important.

## Ce se schimbă pentru cine modelează enumerări

Pentru taxonomiile gestionate cu lookup table, `ASSERTION` deschid un scenariu nou: constrângeri care astăzi trăiesc ca trigger aplicative (ex. "taxonomia nu poate rămâne fără stări active") vor deveni exprimabile în DDL, validate la nivel tranzacțional, gestionate de motor. Este material care se dezvoltă când implementarea 26ai va fi disponibilă în test.
