---
title: "ASSERTION"
description: "Constrângere de integritate declarativă SQL care validează un predicat asupra întregii stări a bazei de date, acoperind simultan mai multe tabele."
translationKey: "glossary_assertion"
aka: "Constrângere declarativă multi-tabel"
articles:
  - "/posts/oracle/articolo-oracle-assertions-in-oracle-26ai"
---

Un ASSERTION este o constrângere de integritate declarativă introdusă de SQL-92, care exprimă un predicat boolean asupra întregii stări a bazei de date. Spre deosebire de `CHECK` — limitat la un singur rând sau, cel mult, la o singură tabelă — un ASSERTION poate acoperi mai multe tabele și agregări, și este violat atunci când predicatul evaluează la `FALSE` după orice operație DML sau DDL.

## Cum funcționează

ASSERTION-ul se definește cu `CREATE ASSERTION` și este asociat unui schema. Motorul îl evaluează la sfârșitul fiecărei tranzacții (sau, în funcție de implementare, după fiecare instrucțiune): dacă predicatul returnează `FALSE`, tranzacția este respinsă cu ROLLBACK automat.

```sql
CREATE ASSERTION max_comenzi_per_client
CHECK (
  NOT EXISTS (
    SELECT client_id
    FROM comenzi
    GROUP BY client_id
    HAVING COUNT(*) > 1000
  )
);
```

Predicatul poate referenția orice tabelă vizibilă în schema, folosind subinterogări, agregări și join-uri. Enforcement-ul este responsabilitatea motorului, nu a stratului aplicativ.

## Când se folosește

ASSERTION-urile acoperă reguli de business care nu pot fi exprimate cu `CHECK` sau `FOREIGN KEY`: limite agregate, invarianți cross-tabel, constrângeri temporale distribuite pe mai multe entități. Costul este real: fiecare tranzacție care atinge tabelele referențiate poate declanșa reevaluarea predicatului, cu impact asupra performanței în scenarii cu volum mare de scrieri.

SQL-92 le-a standardizat, dar timp de decenii niciun RDBMS enterprise mainstream nu le-a implementat nativ. Oracle 23ai/26ai reprezintă primul motor de producție la scară largă care a făcut acest pas.
