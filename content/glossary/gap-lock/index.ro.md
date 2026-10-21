---
title: "Gap Lock"
description: "Gap Lock-ul InnoDB blochează un interval între valorile unui index pentru a preveni INSERT în acel interval. Activ în REPEATABLE READ, absent în READ COMMITTED."
translationKey: "glossary_gap_lock"
aka: "Gap Lock (InnoDB)"
articles:
  - "/posts/mysql/mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb"
---

Un Gap Lock este un mecanism de blocare InnoDB care protejează un **interval** între două valori ale unui index, fără a bloca înregistrările care delimitează acel interval. Scopul său principal este de a împiedica alte tranzacții să insereze rânduri în intervalul protejat, garantând consistența citirii.

## Cum funcționează

Când o tranzacție citește un interval folosind `SELECT ... FOR UPDATE` sau `SELECT ... LOCK IN SHARE MODE`, InnoDB poate achiziționa un Gap Lock asupra intervalului dintre valorile de index implicate. Niciun înregistrare fizică nu este blocată: lock-ul există doar în „spațiul" dintre valori.

```sql
-- Tranzacția A: citește rânduri cu id între 10 și 20
SELECT * FROM comenzi WHERE id BETWEEN 10 AND 20 FOR UPDATE;

-- Tranzacția B: încearcă să insereze id = 15 → blocată de Gap Lock
INSERT INTO comenzi (id, stare) VALUES (15, 'nou');
```

Două Gap Lock-uri pe același interval sunt **compatibile între ele**: conflictul apare doar cu tentativele de INSERT în intervalul protejat.

## Context operațional

Gap Lock-ul este activ exclusiv la nivelul de izolare `REPEATABLE READ` (implicit în InnoDB). Trecând la `READ COMMITTED`, InnoDB eliberează Gap Lock-urile după fiecare instrucțiune, reducând contența, dar expunând tranzacția la citiri nerepetabile și phantom reads.

În sistemele cu concurență ridicată și multe operațiuni INSERT, Gap Lock-urile sunt o cauză frecventă de deadlock-uri: două tranzacții pot deține Gap Lock-uri suprapuse și se pot bloca reciproc în momentul inserției. Diagnosticarea acestor scenarii necesită analiza ieșirii comenzii `SHOW ENGINE INNODB STATUS`.
