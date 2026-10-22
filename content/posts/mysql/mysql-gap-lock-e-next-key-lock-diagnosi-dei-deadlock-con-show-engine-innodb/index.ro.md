---
categories:
- mysql
date: '2026-11-03'
description: 'Gap lock și next-key lock InnoDB explicate pe un caz real: deadlock
  pe INSERT concurente, diagnosticare cu SHOW ENGINE INNODB STATUS și când READ COMMITTED
  rezolvă totul.'
draft: false
image: mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb.cover.jpg
seoTitle: 'MySQL gap lock și next-key lock: deadlock InnoDB diagnosticat'
tags:
- innodb
- locking
- deadlock
- isolation-level
- concurrency
title: 'Gap lock și next-key lock în MySQL: diagnosticare și rezolvare deadlock-urilor'
translationKey: mysql_gap_lock_e_next_key_lock_diagnosi_dei_deadlock_con_show_engine_innodb
webo_generated_at: 2026-10-21
webo_status: scheduled
---

## Ședința de marți dimineață

Era marți dimineață, și ședința începuse prost. Pe de o parte echipa de dezvoltare, pe de alta DBA-ul clientului — un operator poștal și logistic național cu aproximativ o mie cinci sute de instanțe MySQL răspândite pe tot atâtea noduri. Sistemul de tracking al coletelor genera deadlock-uri sporadice pe INSERT-uri, vreo trei-patru pe zi în condiții normale de încărcare, mult mai multe în vârfurile de sortare.

Dezvoltatorii aduseseră log-urile aplicative: „baza de date blochează INSERT-urile noastre fără motiv". DBA-ul adusese graficele de utilizare: „query-urile sunt scrise prost, fac range scan pe tabele uriașe". Amândoi aveau dreptate în câte ceva. Amândoi greșeau în privința cauzei.

Problema era în gap lock-urile InnoDB — un mecanism pe care majoritatea echipelor îl cunoaște din auzite, dar nu îl înțelege cu adevărat până nu se lovește de el în producție.

## Record lock, gap lock, next-key lock: trei lucruri diferite

Înainte de a intra în cazul concret, merită clarificată terminologia, pentru că InnoDB folosește trei tipuri distincte de lock-uri care sunt adesea confundate.

Un **record lock** blochează o singură linie din index. Dacă faci `SELECT ... FOR UPDATE WHERE id = 42`, InnoDB pune un record lock pe linia cu `id = 42`. Intuitiv.

Un **gap lock** blochează un *interval* între două valori ale indexului — „golul" dintre două înregistrări existente — fără să blocheze înregistrările în sine. Dacă în index ai valorile 10, 20, 30, un gap lock pe intervalul (10, 20) împiedică orice altă tranzacție să insereze o valoare în acel interval. Punctul esențial: gap lock-ul nu blochează înregistrările existente, blochează spațiul dintre ele.

Un **next-key lock** este combinația celor două: record lock pe înregistrarea curentă plus gap lock pe intervalul care o precede. Este tipul de lock implicit pe care InnoDB îl folosește pentru scanările de index în `REPEATABLE READ`. Dacă faci un range scan care atinge valorile 10, 20, 30, InnoDB pune next-key lock-uri pe (-∞, 10], (10, 20], (20, 30], (30, +∞). Blochezi nu doar înregistrările citite, ci toate „golurile" dintre ele.

De ce face InnoDB asta? Pentru a preveni **phantom read** — situația în care o tranzacție citește un range de două ori și obține rezultate diferite pentru că o altă tranzacție a inserat linii la mijloc. În `REPEATABLE READ`, standardul SQL impune ca acest lucru să nu se întâmple, iar InnoDB garantează asta blocând gap-urile.

```sql
-- Exemplu: această query în REPEATABLE READ
-- achiziționează next-key lock pe intervalul scanat
SELECT * FROM shipment_log
WHERE status = 'PENDING' AND created_at > '2024-01-15 08:00:00'
FOR UPDATE;
```

Problema apare când două tranzacții fac range scan pe intervale suprapuse și apoi ambele încearcă să facă INSERT în același gap. Deadlock clasic.

## De ce REPEATABLE READ este contextul în care totul explodează

MySQL folosește `REPEATABLE READ` ca nivel de izolare implicit [1]. Este o alegere istorică legată de replicarea bazată pe statement — în `READ COMMITTED`, anumite pattern-uri de replicare binlog puteau produce inconsistențe pe slave. Cu replicarea row-based (implicit din MySQL 5.7.7) acea preocupare este în mare parte depășită, dar valoarea implicită a rămas.

În `REPEATABLE READ`, InnoDB trebuie să garanteze că o tranzacție vede întotdeauna același snapshot al datelor pe toată durata ei. Pentru citirile normale (fără `FOR UPDATE`) folosește MVCC — citește o versiune istorică a datelor și nu achiziționează lock-uri. Dar pentru citirile cu lock (`SELECT ... FOR UPDATE`, `SELECT ... LOCK IN SHARE MODE`) și pentru operațiunile de scriere, trebuie să folosească next-key lock-uri pentru a preveni phantom-urile.

Pattern-ul care genera deadlock-uri în cazul tracking-ului de colete era acesta:

1. Tranzacția A: caută coletele în starea `PENDING` într-un anumit interval de timp → achiziționează next-key lock pe un range al indexului
2. Tranzacția B: face același lucru pe un range parțial suprapus → achiziționează next-key lock pe un range care se suprapune parțial
3. Tranzacția A: încearcă să insereze o nouă înregistrare de log → înregistrarea cade în gap-ul blocat de B → așteaptă
4. Tranzacția B: încearcă să insereze o nouă înregistrare de log → înregistrarea cade în gap-ul blocat de A → așteaptă
5. InnoDB detectează ciclul și termină una dintre cele două tranzacții

Codul aplicativ nu avea nimic greșit în sens absolut. Problema era interacțiunea dintre pattern-ul de acces (range scan + INSERT în același gap) și nivelul de izolare implicit.

## Diagnosticare: SHOW ENGINE INNODB STATUS

Când se suspectează un deadlock în MySQL, primul instrument este `SHOW ENGINE INNODB STATUS` [2]. Secțiunea de interes este `LATEST DETECTED DEADLOCK`, care arată ultimul deadlock detectat de InnoDB cu toate detaliile: tranzacțiile implicate, lock-urile pe care le dețineau, lock-urile pe care le așteptau și care tranzacție a fost aleasă ca victimă.

```sql
SHOW ENGINE INNODB STATUS\G
```

Output-ul este voluminos și trebuie citit cu atenție. Un exemplu simplificat din ce se găsește în secțiunea deadlock:

```text
------------------------
LATEST DETECTED DEADLOCK
------------------------
2024-01-16 09:23:41 0x7f8b4c001700
*** (1) TRANSACTION:
TRANSACTION 421938, ACTIVE 0 sec inserting
mysql tables in use 1, locked 1
LOCK WAIT 4 lock struct(s), heap size 1136, 2 row lock(s)
MySQL thread id 1842, OS thread handle 140234..., query id 98234 ...
INSERT INTO shipment_log (shipment_id, status, created_at)
VALUES (10045, 'PROCESSING', NOW())

*** (1) HOLDS THE LOCK(S):
RECORD LOCKS space id 312 page no 4 n bits 72 index idx_status_created
of table `tracking`.`shipment_log` trx id 421938 lock_mode X locks gap before rec

*** (1) WAITING FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS space id 312 page no 4 n bits 72 index idx_status_created
of table `tracking`.`shipment_log` trx id 421938 lock_mode X locks gap before rec insert intention waiting

*** (2) TRANSACTION:
TRANSACTION 421939, ACTIVE 0 sec inserting
...
*** (2) HOLDS THE LOCK(S):
RECORD LOCKS ... lock_mode X locks gap before rec

*** (2) WAITING FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS ... lock_mode X locks gap before rec insert intention waiting

*** WE ROLL BACK TRANSACTION (2)
```

Frazele cheie de căutat: `lock_mode X locks gap before rec` (gap lock achiziționat) și `insert intention waiting` (INSERT în așteptare să intre într-un gap blocat). Când le vezi pe amândouă într-un deadlock, te uiți exact la pattern-ul gap lock / INSERT intention lock.

Un alt instrument util, disponibil din MySQL 5.6, este tabela `performance_schema.data_locks` (sau `information_schema.INNODB_LOCKS` în versiunile anterioare):

```sql
-- MySQL 8.0+
SELECT
    r.trx_id AS waiting_trx,
    r.trx_mysql_thread_id AS waiting_thread,
    r.trx_query AS waiting_query,
    b.trx_id AS blocking_trx,
    b.trx_mysql_thread_id AS blocking_thread,
    b.trx_query AS blocking_query
FROM information_schema.INNODB_TRX b
JOIN information_schema.INNODB_TRX r
    ON r.trx_id != b.trx_id
JOIN performance_schema.data_locks dl
    ON dl.ENGINE_TRANSACTION_ID = r.trx_id
    AND dl.LOCK_STATUS = 'WAITING'
WHERE b.trx_id = dl.BLOCKING_ENGINE_TRANSACTION_ID;
```

## Cazul reconstituit pas cu pas

Tabela implicată avea o structură similară cu aceasta:

```sql
CREATE TABLE shipment_log (
    id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    shipment_id BIGINT UNSIGNED NOT NULL,
    status      VARCHAR(20) NOT NULL,
    created_at  DATETIME NOT NULL,
    INDEX idx_status_created (status, created_at)
);
```

Codul aplicativ, simplificat, făcea asta într-o singură tranzacție:

```sql
-- Pasul 1: caută înregistrările recente în starea PENDING
SELECT id, shipment_id FROM shipment_log
WHERE status = 'PENDING'
  AND created_at > NOW() - INTERVAL 5 MINUTE
FOR UPDATE;

-- Pasul 2: actualizează starea înregistrărilor găsite
UPDATE shipment_log SET status = 'PROCESSING'
WHERE id IN (...);

-- Pasul 3: inserează o înregistrare de audit
INSERT INTO shipment_log (shipment_id, status, created_at)
VALUES (?, 'PROCESSING', NOW());
```

`FOR UPDATE` de la pasul 1 era intenționat — echipa voia să evite ca doi workeri paraleli să proceseze același colet. Rezonabil. Problema este că acel `SELECT ... FOR UPDATE` cu condiția pe `created_at > NOW() - INTERVAL 5 MINUTE` achiziționa next-key lock-uri pe tot range-ul indexului `idx_status_created` pentru valorile `created_at` din ultimele cinci minute. Iar INSERT-ul de la pasul 3 insera o înregistrare cu `created_at = NOW()` — exact în gap-ul blocat de cealaltă tranzacție concurentă.

Doi workeri care porneau la câteva milisecunde distanță se blocau sistematic unul pe celălalt.

## READ COMMITTED: când este răspunsul corect

Soluția cea mai directă, în cazul specific, era coborârea nivelului de izolare la `READ COMMITTED` pentru acele tranzacții [3]:

```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

În `READ COMMITTED`, InnoDB nu folosește gap lock-uri pentru citiri. Folosește doar record lock-uri pe liniile efectiv găsite. Motivul este că în `READ COMMITTED` phantom read-urile sunt permise — fiecare statement vede datele committed la momentul execuției sale, nu la momentul începerii tranzacției. Fără necesitatea de a preveni phantom-urile, gap lock-urile nu mai sunt necesare, iar pattern-ul de deadlock dispare.

Întrebarea legitimă este: este sigur? Depinde de context, și merită să fim expliciți cu privire la compromisuri.

`READ COMMITTED` este sigur când:
- Logica aplicativă nu depinde de stabilitatea range-ului între două citiri în aceeași tranzacție (adică nu contează dacă o altă tranzacție inserează linii la mijloc)
- Folosești replicare row-based (implicit din MySQL 5.7.7) — cu replicarea statement-based, `READ COMMITTED` poate produce inconsistențe pe slave în anumite scenarii de UPDATE/DELETE cu subquery [4]
- Phantom read-urile nu sunt o problemă pentru semantica aplicației

În cazul tracking-ului de colete, răspunsul la toate trei întrebările era da. Worker-ul nu avea nevoie de un range stabil — trebuia să proceseze coletele disponibile în acel moment, nu să garanteze că niciun alt colet nu apăruse între timp. Replicarea era row-based. Phantom read-urile erau irelevante pentru corectitudinea sistemului.

Modificarea a fost făcută la nivel de sesiune în connection pool, nu la nivel global — o alegere conservatoare care permitea menținerea `REPEATABLE READ` ca implicit pentru restul sistemului.

## Pattern-uri pentru reducerea deadlock-urilor fără a schimba nivelul de izolare

`READ COMMITTED` nu este întotdeauna răspunsul. Când nu se poate sau nu se dorește schimbarea nivelului de izolare, există alte pattern-uri care reduc probabilitatea deadlock-urilor.

**Ordine de acces consistentă.** Majoritatea deadlock-urilor clasice (nu din gap lock) apare din tranzacții care accesează aceleași resurse în ordine diferită. Dacă tranzacția A blochează mai întâi tabela X apoi Y, iar tranzacția B face invers, deadlock-ul este aproape garantat. Standardizarea ordinii de acces la resurse elimină această clasă de probleme.

**Batch size redus.** Range scan-urile pe intervale mari achiziționează gap lock-uri pe intervale mari. Reducerea ferestrei temporale a query-ului (de la 5 minute la 30 de secunde, de exemplu) reduce amplitudinea gap lock-urilor și probabilitatea de suprapunere.

```sql
-- În loc de:
WHERE status = 'PENDING' AND created_at > NOW() - INTERVAL 5 MINUTE

-- Consideră:
WHERE status = 'PENDING' AND created_at > NOW() - INTERVAL 30 SECOND
  AND created_at <= NOW() - INTERVAL 5 SECOND  -- evită fereastra cea mai recentă
```

**Retry logic aplicativă.** Deadlock-urile în InnoDB sunt evenimente normale, nu anomalii. InnoDB alege întotdeauna o victimă și face rollback pe una dintre tranzacții — aplicația trebuie să fie pregătită să reîncerce. Un pattern robust prevede un retry cu backoff exponențial și un număr maxim de încercări:

```python
import time
import random
import mysql.connector

def execute_with_retry(conn, fn, max_retries=3):
    for attempt in range(max_retries):
        try:
            return fn(conn)
        except mysql.connector.errors.DatabaseError as e:
            if e.errno == 1213 and attempt < max_retries - 1:
                # ER_LOCK_DEADLOCK — reîncearcă cu backoff
                wait = (2 ** attempt) + random.uniform(0, 0.5)
                time.sleep(wait)
                continue
            raise
```

**Indici selectivi pe coloana de lock.** Dacă `FOR UPDATE` este necesar, un index mai selectiv reduce numărul de linii (și gap-uri) implicate în scanare. În cazul specific, adăugarea `shipment_id` la index și filtrarea pe worker specific ar fi redus drastic amplitudinea range-ului blocat.

## Ce rămâne după ședință

Trecerea la `READ COMMITTED` la nivel de sesiune a eliminat deadlock-urile în aproximativ o oră de la deploy. Nu era magie — era consecința directă a înțelegerii a ceea ce se întâmpla sub capotă.

Lucrul cel mai util ieșit din acea săptămână de analiză nu era soluția în sine, ci metoda: citirea atentă a `SHOW ENGINE INNODB STATUS`, înțelegerea diferenței dintre record lock și gap lock, și neluarea de bun că implicit-ul MySQL este întotdeauna cel potrivit pentru propriul caz de utilizare. `REPEATABLE READ` este o alegere conservatoare și corectă în multe contexte. În altele, cum ar fi cel al workerilor concurenți cu range scan + INSERT, este cauza directă a problemelor.

DBA-ul clientului a adăugat monitorizarea deadlock-urilor în propriul sistem de alerting — o query periodică pe `information_schema.INNODB_METRICS` care urmărește contorul `lock_deadlocks`. Dezvoltatorii au adăugat retry logic. Ambele erau necesare, și niciuna dintre ele singură nu ar fi fost suficientă.

## Surse oficiale

1. MySQL Documentation — [InnoDB Transaction Isolation Levels](https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-isolation-levels.html)
2. MySQL Documentation — [SHOW ENGINE INNODB STATUS](https://dev.mysql.com/doc/refman/8.0/en/innodb-standard-monitor.html)
3. MySQL Documentation — [InnoDB Locking: Gap Locks](https://dev.mysql.com/doc/refman/8.0/en/innodb-locking.html#innodb-gap-locks)
4. MySQL Documentation — [Binary Logging Formats and READ COMMITTED](https://dev.mysql.com/doc/refman/8.0/en/binary-log-formats.html)

## Glosar
- **[Gap lock](/ro/glossary/gap-lock/)** (InnoDB) — lock care blochează un interval între două valori ale unui index, fără să blocheze înregistrările în sine. Împiedică INSERT-urile în intervalul blocat. Activ în `REPEATABLE READ`, absent în `READ COMMITTED`.

- **[Next-key lock](/ro/glossary/gap-lock/)** (InnoDB) — combinație de record lock pe înregistrarea curentă și gap lock pe intervalul care o precede. Tipul de lock implicit pentru scanările de index în `REPEATABLE READ`; previne phantom read-urile.

- **[Insert intention lock](/ro/glossary/next-key-lock/)** (InnoDB) — lock de intenție achiziționat de un INSERT înainte de a insera o înregistrare într-un gap. Compatibil cu alte insert intention lock-uri pe același gap, dar blocat de gap lock-urile existente. Cauza directă a deadlock-urilor din INSERT-uri concurente.

- **[REPEATABLE READ](/ro/glossary/gap-lock/)** — nivelul de izolare implicit al MySQL/InnoDB. Garantează că o tranzacție vede întotdeauna același snapshot al datelor pe toată durata ei; implementat prin MVCC pentru citiri și next-key lock-uri pentru operațiunile cu lock.

- **[Phantom read](/ro/glossary/next-key-lock/)** — anomalie de concurență în care o tranzacție citește un range de două ori și obține rezultate diferite deoarece o altă tranzacție a inserat sau șters linii la mijloc. Prevenit de `REPEATABLE READ` prin gap lock-uri; permis în `READ COMMITTED`.
