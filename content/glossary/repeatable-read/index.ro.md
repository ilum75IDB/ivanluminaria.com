---
title: "REPEATABLE READ"
description: "Nivelul de izolare implicit al MySQL/InnoDB: garantează un snapshot consistent pe toată durata tranzacției prin MVCC și next-key locks."
translationKey: "glossary_repeatable_read"
aka: "Nivel de izolare Repeatable Read"
articles:
  - "/posts/mysql/mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb"
---

REPEATABLE READ este nivelul de izolare implicit al MySQL/InnoDB. O tranzacție care rulează la acest nivel vede întotdeauna același snapshot al datelor din momentul primului SELECT, indiferent de câte modificări au fost COMMITate de alți clienți între timp.

## Cum funcționează

InnoDB implementează REPEATABLE READ pe două mecanisme distincte:

- **Citiri neblocante (consistent read):** gestionate prin MVCC. Fiecare rând menține un lanț de versiuni; tranzacția citește versiunea validă la momentul snapshot-ului, ignorând scrierile ulterioare.
- **Citiri blocante și scrieri:** folosesc lock-uri fizice. InnoDB aplică **next-key locks** (record lock + gap lock) pentru a împiedica apariția rândurilor fantomă între un `SELECT ... FOR UPDATE` și următorul din aceeași tranzacție.

```sql
-- Tranzacția vede întotdeauna același snapshot
START TRANSACTION;
SELECT * FROM comenzi WHERE stare = 'deschis';  -- snapshot fixat aici
-- ... alte operații ...
SELECT * FROM comenzi WHERE stare = 'deschis';  -- același rezultat
COMMIT;
```

## Când se folosește și limitări

REPEATABLE READ este potrivit pentru majoritatea sarcinilor OLTP: verificări de sold, rapoarte intra-tranzacție, operații multi-pas care necesită date stabile. Costul principal îl reprezintă next-key locks, care extind suprafața de blocare față de READ COMMITTED și cresc riscul de deadlock-uri la INSERT-uri concurente. Dacă aplicația nu are nevoie de protecție împotriva phantom reads, coborârea la READ COMMITTED reduce contența.
