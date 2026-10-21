---
title: "REPEATABLE READ"
description: "Livello di isolamento predefinito di MySQL/InnoDB: garantisce uno snapshot coerente per tutta la durata della transazione tramite MVCC e next-key lock."
translationKey: "glossary_repeatable_read"
aka: "Repeatable Read Isolation Level"
articles:
  - "/posts/mysql/mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb"
---

REPEATABLE READ è il livello di isolamento predefinito di MySQL/InnoDB. Una transazione che opera a questo livello vede sempre lo stesso snapshot dei dati dal momento del primo SELECT, indipendentemente da quante modifiche altri client committano nel frattempo.

## Come funziona

InnoDB implementa REPEATABLE READ su due binari distinti:

- **Letture non bloccanti (consistent read):** gestite tramite MVCC. Ogni riga ha una catena di versioni; la transazione legge la versione valida al momento del proprio snapshot, ignorando le scritture successive.
- **Letture bloccanti e scritture:** usano i lock fisici. InnoDB applica **next-key lock** (record lock + gap lock) per impedire che righe fantasma compaiano tra un `SELECT ... FOR UPDATE` e il successivo nella stessa transazione.

```sql
-- La transazione vede sempre lo stesso snapshot
START TRANSACTION;
SELECT * FROM ordini WHERE stato = 'aperto';  -- snapshot fissato qui
-- ... altre operazioni ...
SELECT * FROM ordini WHERE stato = 'aperto';  -- stesso risultato
COMMIT;
```

## Quando si usa e limiti

REPEATABLE READ è adatto alla maggior parte dei carichi OLTP: bilanci, report intra-transazione, operazioni multi-step che devono lavorare su dati stabili. Il costo principale sono i next-key lock, che ampliano la superficie di lock rispetto a READ COMMITTED e aumentano il rischio di deadlock su INSERT concorrenti. Se l'applicazione non ha bisogno di protezione dalle phantom read, abbassare a READ COMMITTED riduce la contesa.
