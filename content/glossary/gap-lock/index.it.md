---
title: "Gap Lock"
description: "Il Gap Lock di InnoDB blocca un intervallo tra valori di indice impedendo INSERT nell'intervallo. Attivo in REPEATABLE READ, assente in READ COMMITTED."
translationKey: "glossary_gap_lock"
aka: "Gap Lock (InnoDB)"
articles:
  - "/posts/mysql/mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb"
---

Il Gap Lock è un meccanismo di locking di InnoDB che protegge un **intervallo** tra due valori di un indice, senza bloccare i record che delimitano quell'intervallo. Il suo scopo principale è impedire che altre transazioni inseriscano righe nell'intervallo bloccato, garantendo la consistenza della lettura.

## Come funziona

Quando una transazione legge un range con `SELECT ... FOR UPDATE` o `SELECT ... LOCK IN SHARE MODE`, InnoDB può acquisire un Gap Lock sull'intervallo tra i valori dell'indice coinvolti. Nessun record fisico viene bloccato: il lock esiste solo sullo "spazio" tra i valori.

```sql
-- Transazione A: legge righe con id tra 10 e 20
SELECT * FROM ordini WHERE id BETWEEN 10 AND 20 FOR UPDATE;

-- Transazione B: tenta di inserire id = 15 → bloccata dal Gap Lock
INSERT INTO ordini (id, stato) VALUES (15, 'nuovo');
```

Due Gap Lock sullo stesso intervallo sono **compatibili tra loro**: il conflitto avviene solo con i tentativi di INSERT nell'intervallo protetto.

## Contesto operativo

Il Gap Lock è attivo esclusivamente con il livello di isolamento `REPEATABLE READ` (default di InnoDB). Passando a `READ COMMITTED`, InnoDB rilascia i Gap Lock dopo ogni statement, riducendo la contesa ma esponendo la transazione a letture non ripetibili e a phantom read.

Nei sistemi ad alta concorrenza con molti INSERT, i Gap Lock sono una causa frequente di deadlock: due transazioni possono acquisire Gap Lock sovrapposti e poi bloccarsi a vicenda nel tentativo di inserire. Diagnosticare questi scenari richiede l'analisi dell'output di `SHOW ENGINE INNODB STATUS`.
