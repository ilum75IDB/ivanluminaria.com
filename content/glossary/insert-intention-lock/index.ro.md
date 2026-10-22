---
title: "Insert Intention Lock"
description: "Lock de intenție achiziționat de INSERT înainte de a scrie într-un gap. Compatibil cu alte insert intention lock-uri, blocat de gap lock-urile existente."
translationKey: "glossary_insert_intention_lock"
aka: "Insert Intention Gap Lock"
articles:
  - "/posts/mysql/mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb"
---

Un **Insert Intention Lock** este un tip special de gap lock pe care InnoDB îl achiziționează ori de câte ori o tranzacție execută o `INSERT` într-un gap dintre două valori de index. Mai multe insert intention lock-uri pe același gap sunt mutual compatibile — inserții concurente în același interval pot avansa în paralel — dar orice gap lock sau next-key lock existent pe acel gap le va bloca.

## Cum funcționează

Înainte de a scrie înregistrarea nouă, InnoDB plasează un insert intention lock pe gap-ul țintă. Dacă o altă tranzacție deține deja un gap lock pe același interval (de exemplu, printr-un `SELECT ... FOR UPDATE` cu predicat de interval), `INSERT`-ul așteaptă până când acel lock este eliberat.

```sql
-- Tranzacția A: achiziționează un gap lock pe intervalul (10, 20)
SELECT * FROM comenzi WHERE id BETWEEN 10 AND 20 FOR UPDATE;

-- Tranzacția B: încearcă să insereze în același interval, așteaptă gap lock-ul lui A
INSERT INTO comenzi (id, stare) VALUES (15, 'nou');
```

Compatibilitatea dintre insert intention lock-uri este intenționată: permite inserții cu concurență ridicată în același gap fără serializare inutilă, atât timp cât rândurile inserate nu colizionează pe aceeași cheie.

## Deadlock-uri din INSERT-uri concurente

Cel mai frecvent tipar de deadlock cu insert intention lock-uri apare când două tranzacții achiziționează fiecare câte un gap lock — de obicei printr-un `SELECT ... FOR UPDATE` care nu returnează rânduri — și apoi ambele încearcă să insereze în același gap. Fiecare așteaptă ca cealaltă să elibereze gap lock-ul propriu, formând un ciclu pe care InnoDB îl detectează și îl rezolvă prin ROLLBACK-ul uneia dintre tranzacții.

```sql
-- Secvența tipică de deadlock
-- T1: SELECT ... FOR UPDATE pe gap → gap lock achiziționat
-- T2: SELECT ... FOR UPDATE pe același gap → gap lock achiziționat
-- T1: INSERT în gap → așteaptă gap lock-ul lui T2
-- T2: INSERT în gap → așteaptă gap lock-ul lui T1 → DEADLOCK
```

Pentru a diagnostica acest scenariu, analizează ieșirea comenzii `SHOW ENGINE INNODB STATUS`: modurile de lock relevante apar ca `LOCK_MODE: X,GAP` și `LOCK_MODE: X,INSERT_INTENTION`.
