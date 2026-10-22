---
title: "Insert Intention Lock"
description: "Lock di intenzione acquisito da INSERT prima di inserire in un gap. Compatibile con altri insert intention lock, bloccato dai gap lock esistenti."
translationKey: "glossary_insert_intention_lock"
aka: "Insert Intention Gap Lock"
articles:
  - "/posts/mysql/mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb"
---

L'**Insert Intention Lock** è un tipo speciale di gap lock acquisito da InnoDB ogni volta che una transazione esegue una `INSERT` all'interno di un gap tra due valori di indice. Non blocca altri insert intention lock sullo stesso gap — due INSERT concorrenti sullo stesso intervallo possono procedere in parallelo — ma viene bloccato da qualsiasi gap lock o next-key lock già presente su quel gap.

## Come funziona

Quando una transazione esegue una `INSERT`, InnoDB acquisisce un insert intention lock sul gap target prima di scrivere il record. Se un'altra transazione detiene un gap lock sullo stesso intervallo (ad esempio per via di una `SELECT ... FOR UPDATE` o di una ricerca con `WHERE` su un range), la INSERT si mette in attesa.

```sql
-- Transazione A: acquisisce un gap lock sull'intervallo (10, 20)
SELECT * FROM ordini WHERE id BETWEEN 10 AND 20 FOR UPDATE;

-- Transazione B: tenta di inserire nell'intervallo, attende il gap lock di A
INSERT INTO ordini (id, stato) VALUES (15, 'nuovo');
```

La compatibilità tra insert intention lock è intenzionale: permette a più INSERT di operare sullo stesso gap senza serializzarsi, a patto che non collidano sulla stessa riga.

## Deadlock da INSERT concorrenti

Il pattern di deadlock più comune con gli insert intention lock si verifica quando due transazioni acquisiscono ciascuna un gap lock (ad esempio tramite una `SELECT ... FOR UPDATE` che non trova righe) e poi tentano entrambe di inserire nello stesso gap. Ognuna attende che l'altra rilasci il proprio gap lock, generando un deadlock rilevato da InnoDB e risolto con il rollback di una delle due transazioni.

```sql
-- Schema tipico del deadlock
-- T1: SELECT ... FOR UPDATE su gap → gap lock acquisito
-- T2: SELECT ... FOR UPDATE su stesso gap → gap lock acquisito
-- T1: INSERT nel gap → attende gap lock di T2
-- T2: INSERT nel gap → attende gap lock di T1 → DEADLOCK
```

Diagnosticare questo scenario richiede l'analisi dell'output di `SHOW ENGINE INNODB STATUS`, dove il lock type appare come `LOCK_MODE: X,GAP` e `LOCK_MODE: X,INSERT_INTENTION`.
