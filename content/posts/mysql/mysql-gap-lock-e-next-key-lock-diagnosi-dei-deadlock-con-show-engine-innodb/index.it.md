---
categories:
- mysql
date: '2026-11-03'
description: 'Gap lock e next-key lock di InnoDB spiegati sul caso reale: deadlock
  su INSERT concorrenti, diagnosi con SHOW ENGINE INNODB STATUS e quando READ COMMITTED
  risolve tutto.'
draft: false
image: mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb.cover.jpg
seoTitle: 'MySQL gap lock e next-key lock: diagnosi e fix dei deadlock'
tags:
- innodb
- locking
- deadlock
- isolation-level
- concurrency
title: 'MySQL gap lock e next-key lock: diagnosi dei deadlock con SHOW ENGINE INNODB
  STATUS'
translationKey: mysql_gap_lock_e_next_key_lock_diagnosi_dei_deadlock_con_show_engine_innodb
webo_generated_at: 2026-10-21
webo_status: scheduled
---

## La riunione del martedì mattina

Era un martedì mattina, e la riunione era iniziata male. Da una parte il team di sviluppo, dall'altra il DBA del cliente — un operatore postale e logistico nazionale con circa millecinquecento istanze MySQL sparse su altrettanti nodi. Il sistema di tracking dei pacchi generava deadlock sporadici sulle INSERT, circa tre o quattro al giorno in condizioni di carico normale, molti di più nei picchi di smistamento.

Gli sviluppatori avevano portato i log applicativi: "il database blocca le nostre INSERT senza motivo". Il DBA aveva portato i grafici di utilizzo: "le query sono scritte male, fanno range scan su tabelle enormi". Entrambi avevano ragione su qualcosa. Entrambi avevano torto sulla causa.

Il problema era nei gap lock di InnoDB — un meccanismo che la maggior parte dei team conosce di nome ma non capisce davvero finché non ci sbatte contro in produzione.

## Record lock, gap lock, next-key lock: tre cose diverse

Prima di entrare nel caso specifico, vale la pena chiarire la terminologia perché InnoDB usa tre tipi di lock distinti e spesso vengono confusi.

Un **record lock** blocca una singola riga dell'indice. Se fai `SELECT ... FOR UPDATE WHERE id = 42`, InnoDB mette un record lock sulla riga con `id = 42`. Intuitivo.

Un **gap lock** blocca un *intervallo* tra due valori dell'indice — il "buco" tra due record esistenti — senza bloccare i record stessi. Se nell'indice hai i valori 10, 20, 30, un gap lock sull'intervallo (10, 20) impedisce a qualunque altra transazione di inserire un valore in quell'intervallo. Il punto chiave: il gap lock non blocca i record esistenti, blocca lo spazio tra di loro.

Un **next-key lock** è la combinazione dei due: record lock sul record corrente più gap lock sull'intervallo che lo precede. È il tipo di lock predefinito che InnoDB usa per le scansioni di indice in `REPEATABLE READ`. Se fai una range scan che tocca i valori 10, 20, 30, InnoDB mette next-key lock su (-∞, 10], (10, 20], (20, 30], (30, +∞). Stai bloccando non solo i record che hai letto, ma tutti i "buchi" tra di loro.

Perché InnoDB fa questo? Per prevenire i **phantom read** — la situazione in cui una transazione legge un range due volte e ottiene risultati diversi perché un'altra transazione ha inserito righe nel mezzo. In `REPEATABLE READ`, lo standard SQL richiede che questo non accada, e InnoDB lo garantisce bloccando i gap.

```sql
-- Esempio: questa query in REPEATABLE READ
-- acquisisce next-key lock sull'intervallo scansionato
SELECT * FROM shipment_log
WHERE status = 'PENDING' AND created_at > '2024-01-15 08:00:00'
FOR UPDATE;
```

Il problema nasce quando due transazioni fanno range scan su intervalli sovrapposti e poi entrambe provano a fare INSERT nello stesso gap. Classico deadlock.

## Perché REPEATABLE READ è il contesto in cui tutto esplode

MySQL usa `REPEATABLE READ` come isolation level predefinito [1]. È una scelta storica legata alla replica basata su statement — in `READ COMMITTED`, certi pattern di replica binlog potevano produrre inconsistenze sullo slave. Con la replica row-based (default da MySQL 5.7.7) quella preoccupazione è in gran parte superata, ma il default è rimasto.

In `REPEATABLE READ`, InnoDB deve garantire che una transazione veda sempre lo stesso snapshot dei dati per tutta la sua durata. Per le letture normali (senza `FOR UPDATE`) usa il MVCC — legge una versione storica dei dati e non acquisisce lock. Ma per le letture con lock (`SELECT ... FOR UPDATE`, `SELECT ... LOCK IN SHARE MODE`) e per le operazioni di scrittura, deve usare i next-key lock per prevenire i phantom.

Il pattern che genera deadlock nel caso del tracking pacchi era questo:

1. Transazione A: cerca i pacchi in stato `PENDING` in un certo intervallo di tempo → acquisisce next-key lock su un range dell'indice
2. Transazione B: fa la stessa cosa su un range sovrapposto → acquisisce next-key lock su un range che si sovrappone parzialmente
3. Transazione A: prova a inserire un nuovo record di log → il record cade nel gap bloccato da B → attende
4. Transazione B: prova a inserire un nuovo record di log → il record cade nel gap bloccato da A → attende
5. InnoDB rileva il ciclo e uccide una delle due transazioni

Il codice applicativo non aveva nulla di sbagliato in senso assoluto. Il problema era l'interazione tra il pattern di accesso (range scan + INSERT nello stesso gap) e l'isolation level predefinito.

## Diagnosi: SHOW ENGINE INNODB STATUS

Quando si sospetta un deadlock in MySQL, il primo strumento è `SHOW ENGINE INNODB STATUS` [2]. La sezione che interessa è `LATEST DETECTED DEADLOCK`, che mostra l'ultimo deadlock rilevato da InnoDB con tutti i dettagli: le transazioni coinvolte, i lock che tenevano, i lock che aspettavano, e quale transazione è stata scelta come vittima.

```sql
SHOW ENGINE INNODB STATUS\G
```

L'output è verboso e va letto con attenzione. Un esempio semplificato di quello che si trova nella sezione deadlock:

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

Le frasi chiave da cercare: `lock_mode X locks gap before rec` (gap lock acquisito) e `insert intention waiting` (INSERT in attesa di entrare in un gap bloccato). Quando vedi entrambe in un deadlock, stai guardando esattamente il pattern gap lock / INSERT intention lock.

Un altro strumento utile, disponibile da MySQL 5.6, è la tabella `performance_schema.data_locks` (o `information_schema.INNODB_LOCKS` nelle versioni precedenti):

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

## Il caso ricostruito passo per passo

La tabella coinvolta aveva una struttura simile a questa:

```sql
CREATE TABLE shipment_log (
    id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    shipment_id BIGINT UNSIGNED NOT NULL,
    status      VARCHAR(20) NOT NULL,
    created_at  DATETIME NOT NULL,
    INDEX idx_status_created (status, created_at)
);
```

Il codice applicativo, semplificato, faceva questo in una singola transazione:

```sql
-- Step 1: cerca i record recenti in stato PENDING
SELECT id, shipment_id FROM shipment_log
WHERE status = 'PENDING'
  AND created_at > NOW() - INTERVAL 5 MINUTE
FOR UPDATE;

-- Step 2: aggiorna lo stato dei record trovati
UPDATE shipment_log SET status = 'PROCESSING'
WHERE id IN (...);

-- Step 3: inserisce un record di audit
INSERT INTO shipment_log (shipment_id, status, created_at)
VALUES (?, 'PROCESSING', NOW());
```

Il `FOR UPDATE` al passo 1 era intenzionale — il team voleva evitare che due worker paralleli processassero lo stesso pacco. Ragionevole. Il problema è che quella `SELECT ... FOR UPDATE` con la condizione su `created_at > NOW() - INTERVAL 5 MINUTE` acquisiva next-key lock su tutto il range dell'indice `idx_status_created` per i valori di `created_at` negli ultimi cinque minuti. E l'INSERT al passo 3 inseriva un record con `created_at = NOW()` — esattamente nel gap bloccato dall'altra transazione concorrente.

Due worker che partivano a distanza di pochi millisecondi si incastravano sistematicamente.

## READ COMMITTED: quando è la risposta giusta

La soluzione più diretta, nel caso specifico, era abbassare l'isolation level a `READ COMMITTED` per quelle transazioni [3]:

```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

In `READ COMMITTED`, InnoDB non usa gap lock per le letture. Usa solo record lock sulle righe effettivamente trovate. Il motivo è che in `READ COMMITTED` i phantom read sono ammessi — ogni statement vede i dati committed al momento della sua esecuzione, non al momento di inizio transazione. Senza la necessità di prevenire i phantom, non servono i gap lock, e il pattern deadlock scompare.

La domanda legittima è: è sicuro? Dipende dal contesto, e vale la pena essere espliciti sui trade-off.

`READ COMMITTED` è sicuro quando:
- La logica applicativa non dipende dalla stabilità del range tra due letture nella stessa transazione (cioè non ti importa se un'altra transazione inserisce righe nel mezzo)
- Stai usando replica row-based (default da MySQL 5.7.7) — con la replica statement-based, `READ COMMITTED` può produrre inconsistenze sullo slave in certi scenari di UPDATE/DELETE con subquery [4]
- I phantom read non sono un problema per la semantica dell'applicazione

Nel caso del tracking pacchi, la risposta a tutte e tre le domande era sì. Il worker non aveva bisogno di un range stabile — aveva bisogno di processare i pacchi disponibili in quel momento, non di garantire che nessun altro pacco fosse comparso nel mezzo. La replica era row-based. I phantom read erano irrilevanti per la correttezza del sistema.

Il cambio è stato fatto a livello di sessione nel connection pool, non a livello globale — una scelta conservativa che permetteva di lasciare `REPEATABLE READ` come default per il resto del sistema.

## Pattern per ridurre i deadlock senza cambiare isolation level

`READ COMMITTED` non è sempre la risposta. Quando non si può o non si vuole cambiare isolation level, ci sono altri pattern che riducono la probabilità di deadlock.

**Ordine di accesso consistente.** La maggior parte dei deadlock classici (non da gap lock) nasce da transazioni che accedono alle stesse risorse in ordine diverso. Se la transazione A blocca prima la tabella X poi la Y, e la transazione B fa il contrario, il deadlock è quasi garantito. Standardizzare l'ordine di accesso alle risorse elimina questa classe di problemi.

**Batch size ridotto.** Range scan su intervalli grandi acquisiscono gap lock su intervalli grandi. Ridurre la finestra temporale della query (da 5 minuti a 30 secondi, per esempio) riduce l'ampiezza dei gap lock e la probabilità di sovrapposizione.

```sql
-- Invece di:
WHERE status = 'PENDING' AND created_at > NOW() - INTERVAL 5 MINUTE

-- Considera:
WHERE status = 'PENDING' AND created_at > NOW() - INTERVAL 30 SECOND
  AND created_at <= NOW() - INTERVAL 5 SECOND  -- evita la finestra più recente
```

**Retry logic applicativa.** I deadlock in InnoDB sono eventi normali, non anomalie. InnoDB sceglie sempre una vittima e fa rollback di una delle transazioni — l'applicazione deve essere pronta a riprovare. Un pattern robusto prevede un retry con backoff esponenziale e un numero massimo di tentativi:

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
                # ER_LOCK_DEADLOCK — riprova con backoff
                wait = (2 ** attempt) + random.uniform(0, 0.5)
                time.sleep(wait)
                continue
            raise
```

**Indici selettivi sulla colonna di lock.** Se il `FOR UPDATE` è necessario, un indice più selettivo riduce il numero di righe (e gap) coinvolti nella scansione. Nel caso specifico, aggiungere `shipment_id` all'indice e filtrare per worker specifico avrebbe ridotto drasticamente l'ampiezza del range bloccato.

## Quello che rimane dopo la riunione

Il cambio a `READ COMMITTED` a livello di sessione ha eliminato i deadlock nel giro di un'ora dal deploy. Non era magia — era la conseguenza diretta di capire cosa stava succedendo sotto il cofano.

La cosa più utile emersa da quella settimana di analisi non era la soluzione in sé, ma il metodo: leggere `SHOW ENGINE INNODB STATUS` con attenzione, capire la differenza tra record lock e gap lock, e non dare per scontato che il default di MySQL sia sempre quello giusto per il proprio caso d'uso. `REPEATABLE READ` è una scelta conservativa e corretta in molti contesti. In altri, come quello dei worker concorrenti con range scan + INSERT, è la causa diretta dei problemi.

Il DBA del cliente ha aggiunto il monitoraggio dei deadlock al proprio sistema di alerting — una query periodica su `information_schema.INNODB_METRICS` che traccia il contatore `lock_deadlocks`. Gli sviluppatori hanno aggiunto la retry logic. Entrambe le cose erano necessarie, e nessuna delle due da sola sarebbe bastata.

## Fonti ufficiali

1. MySQL Documentation — [InnoDB Transaction Isolation Levels](https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-isolation-levels.html)
2. MySQL Documentation — [SHOW ENGINE INNODB STATUS](https://dev.mysql.com/doc/refman/8.0/en/innodb-standard-monitor.html)
3. MySQL Documentation — [InnoDB Locking: Gap Locks](https://dev.mysql.com/doc/refman/8.0/en/innodb-locking.html#innodb-gap-locks)
4. MySQL Documentation — [Binary Logging Formats and READ COMMITTED](https://dev.mysql.com/doc/refman/8.0/en/binary-log-formats.html)

## Glossario
- **[Gap lock](/it/glossary/gap-lock/)** (InnoDB) — lock che blocca un intervallo tra due valori di un indice, senza bloccare i record stessi. Impedisce INSERT nell'intervallo bloccato. Attivo in `REPEATABLE READ`, assente in `READ COMMITTED`.

- **[Next-key lock](/it/glossary/gap-lock/)** (InnoDB) — combinazione di record lock sul record corrente e gap lock sull'intervallo che lo precede. Tipo di lock predefinito per le scansioni di indice in `REPEATABLE READ`; previene i phantom read.

- **[Insert intention lock](/it/glossary/next-key-lock/)** (InnoDB) — lock di intenzione acquisito da una INSERT prima di inserire un record in un gap. Compatibile con altri insert intention lock sullo stesso gap, ma bloccato dai gap lock esistenti. Causa diretta dei deadlock da INSERT concorrenti.

- **[REPEATABLE READ](/it/glossary/gap-lock/)** — isolation level predefinito di MySQL/InnoDB. Garantisce che una transazione veda sempre lo stesso snapshot dei dati per tutta la sua durata; implementato tramite MVCC per le letture e next-key lock per le operazioni con lock.

- **[Phantom read](/it/glossary/next-key-lock/)** — anomalia di concorrenza in cui una transazione legge un range due volte e ottiene risultati diversi perché un'altra transazione ha inserito o eliminato righe nel mezzo. Prevenuto da `REPEATABLE READ` tramite gap lock; ammesso in `READ COMMITTED`.
