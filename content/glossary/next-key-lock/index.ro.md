---
title: "Next-key lock"
description: "Mecanism de blocare InnoDB care combină record lock și gap lock pentru a preveni phantom reads la scanările de index în REPEATABLE READ."
translationKey: "glossary_next_key_lock"
aka: "Next-key locking"
articles:
  - "/posts/mysql/mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb"
---

**Next-key lock** este strategia implicită de blocare a InnoDB în timpul scanărilor de index sub `REPEATABLE READ`. Combină un **record lock** pe înregistrarea curentă cu un **gap lock** pe intervalul deschis care o precedă, formând intervalul semi-deschis `(valoare_anterioară, valoare_curentă]`.

## Cum funcționează

Când o interogare achiziționează un next-key lock pe o înregistrare cu valoarea `42`, blochează atât înregistrarea `42`, cât și intervalul `(x, 42]`, unde `x` este valoarea imediat anterioară din index. Nicio altă tranzacție nu poate insera o valoare în acel interval până când lock-ul nu este eliberat.

```sql
-- Acest SELECT în REPEATABLE READ achiziționează next-key locks
-- pe fiecare înregistrare returnată și pe intervalele dintre ele
SELECT * FROM comenzi WHERE stare = 'deschis' FOR SHARE;
```

Pentru înregistrarea cu cea mai mare valoare din index, InnoDB extinde next-key lock-ul până la santinela internă `supremum`, acoperind toate valorile viitoare care ar putea fi inserate după maximul curent.

## Când se aplică

Next-key lock-urile sunt active implicit în `REPEATABLE READ` și garantează că recitirea aceleiași interogări în cadrul aceleiași tranzacții returnează întotdeauna aceleași rezultate, prevenind **phantom reads**. În `READ COMMITTED`, gap lock-urile sunt eliberate după evaluarea predicatului, reducând contența, dar expunând tranzacția la phantom reads.

Next-key lock-urile reprezintă cea mai frecventă cauză de deadlock în aplicațiile care execută operații concurente de INSERT și SELECT pe același index: două tranzacții pot deține gap lock-uri suprapuse și se pot bloca reciproc atunci când ambele încearcă un INSERT în același interval.
