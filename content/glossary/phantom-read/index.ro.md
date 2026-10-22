---
title: "Phantom Read"
description: "Anomalie de concurență în care o tranzacție citește un interval de două ori și obține rezultate diferite deoarece altă tranzacție a inserat sau șters rânduri între timp."
translationKey: "glossary_phantom_read"
aka: "Citire fantomă"
articles:
  - "/posts/mysql/mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb"
---

Un **Phantom Read** apare atunci când o tranzacție execută aceeași interogare pe un interval de rânduri în două momente diferite și primește seturi de rezultate distincte, deoarece o altă tranzacție a inserat sau șters rânduri în acel interval între timp. Termenul „fantomă" descrie bine fenomenul: rânduri care apar sau dispar fără ca tranzacția curentă să le fi atins.

## Cum funcționează

Secvența clasică implică două tranzacții concurente:

```sql
-- Tranzacția A
BEGIN;
SELECT * FROM comenzi WHERE valoare > 1000;
-- returnează 5 rânduri

-- Tranzacția B (între timp)
INSERT INTO comenzi (valoare) VALUES (1500);
COMMIT;

-- Tranzacția A, aceeași interogare
SELECT * FROM comenzi WHERE valoare > 1000;
-- acum returnează 6 rânduri → phantom read
COMMIT;
```

Tranzacția A nu a modificat nimic, dar rezultatul diferă. Aceasta este o situație distinctă față de **Non-Repeatable Read**, care privește modificarea rândurilor deja citite, nu apariția sau dispariția de rânduri în intervalul scanat.

## Niveluri de izolare și prevenire

`READ COMMITTED` permite phantom reads: fiecare SELECT vede un snapshot actualizat la momentul propriei execuții. `REPEATABLE READ` — nivelul implicit în InnoDB — le previne prin **gap locks** și **next-key locks**, care blochează intervalele de index și împiedică INSERT-urile concurente în intervalul citit. `SERIALIZABLE` oferă garanția cea mai puternică, transformând SELECT-urile implicite în citiri blocante.

Alegerea `READ COMMITTED` în scenarii cu concurență ridicată reduce riscul de deadlock-uri cauzate de gap lock, dar expune aplicația la phantom reads — un compromis care trebuie evaluat în funcție de logica de business.
