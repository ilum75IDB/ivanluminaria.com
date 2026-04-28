---
title: "pg_stat_user_indexes"
description: "View de sistem PostgreSQL care urmărește de câte ori a fost folosit fiecare index de către planner — instrumentul principal pentru identificarea indexurilor inutile în producție."
translationKey: "glossary_pg_stat_user_indexes"
aka: ""
articles:
  - "/posts/postgresql/postgresql-indici-quando-fanno-male"
---

`pg_stat_user_indexes` este un view de sistem PostgreSQL care expune statisticile de utilizare ale tuturor indexurilor pe tabelele utilizator (excluzând cele de sistem). Pentru fiecare index ține un contor cu de câte ori a fost ales efectiv de planner.

## Cum funcționează

Coloana cheie este `idx_scan`: pleacă de la zero la pornirea bazei de date (sau la ultimul `pg_stat_reset()`) și crește cu unu de fiecare dată când planner-ul alege acel index pentru a executa o interogare. Alte coloane utile includ:

- `idx_tup_read` — câți pointeri la rând au fost citiți din index
- `idx_tup_fetch` — câte rânduri au fost efectiv citite din tabel prin index
- `relname` — numele tabelului căruia îi aparține indexul
- `indexrelname` — numele indexului

## La ce servește

Este instrumentul principal pentru identificarea **indexurilor inutile în producție**. Dacă un index are `idx_scan = 0` după săptămâni sau luni de activitate, planner-ul nu l-a considerat util pentru nicio interogare. E candidat la eliminare (după ce verifici că nu e un index folosit doar pentru constrângeri de unicitate sau foreign key).

## Când se folosește

Se consultă ca primă diagnoză când vrei să înțelegi cât valorează cu adevărat indexurile unui tabel, mai ales când sunt multe. Exemplu tipic:

```sql
SELECT relname, indexrelname, idx_scan,
       pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
WHERE relname = 'tabel'
ORDER BY idx_scan ASC;
```

A se combina cu `pg_stat_reset()` dacă e nevoie să resetezi statisticile după o schimbare semnificativă a workload-ului.
