---
title: "Next-key lock"
description: "Combinazione di record lock e gap lock in InnoDB: blocca il record corrente e l'intervallo precedente per prevenire i phantom read in REPEATABLE READ."
translationKey: "glossary_next_key_lock"
aka: "Next-key locking"
articles:
  - "/posts/mysql/mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb"
---

Il **next-key lock** è il meccanismo di locking predefinito di InnoDB durante le scansioni di indice in modalità `REPEATABLE READ`. Combina un **record lock** sul record corrente con un **gap lock** sull'intervallo aperto che lo precede, formando un intervallo semi-aperto `(valore_precedente, valore_corrente]`.

## Come funziona

Quando una query acquisisce un next-key lock su un record con valore `42`, blocca sia il record `42` sia l'intervallo `(x, 42]` dove `x` è il valore immediatamente precedente nell'indice. Nessuna altra transazione può inserire un valore in quell'intervallo finché il lock non viene rilasciato.

```sql
-- Questa SELECT in REPEATABLE READ acquisisce next-key lock
-- su tutti i record restituiti e sugli intervalli tra di essi
SELECT * FROM ordini WHERE stato = 'aperto' FOR SHARE;
```

Sul record con valore massimo dell'indice, InnoDB applica un next-key lock che si estende fino al valore sentinella `supremum`, coprendo tutti i valori futuri.

## Quando si usa

Il next-key lock è attivo per default in `REPEATABLE READ` e garantisce che una stessa query riletta nella stessa transazione restituisca sempre gli stessi risultati, prevenendo i **phantom read**. In `READ COMMITTED` i gap lock vengono rilasciati dopo la valutazione del predicato, riducendo la contesa ma esponendo la transazione ai phantom.

Il next-key lock è la causa più frequente di deadlock nelle applicazioni che eseguono INSERT e SELECT concorrenti sullo stesso indice: due transazioni possono acquisire gap lock sovrapposti e bloccarsi a vicenda quando tentano l'INSERT.
