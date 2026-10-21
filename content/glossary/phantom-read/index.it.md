---
title: "Phantom Read"
description: "Anomalia di concorrenza in cui una transazione legge un range due volte e ottiene risultati diversi per via di INSERT o DELETE concorrenti."
translationKey: "glossary_phantom_read"
aka: "Lettura fantasma"
articles:
  - "/posts/mysql/mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb"
---

Un **Phantom Read** si verifica quando una transazione esegue la stessa query su un range di righe in due momenti distinti e ottiene set di risultati diversi, perché un'altra transazione ha inserito o eliminato righe nell'intervallo nel frattempo. Il termine "fantasma" descrive bene il fenomeno: righe che appaiono o scompaiono senza che la transazione corrente le abbia mai toccate.

## Come funziona

La sequenza classica coinvolge due transazioni concorrenti:

```sql
-- Transazione A
BEGIN;
SELECT * FROM ordini WHERE importo > 1000;
-- restituisce 5 righe

-- Transazione B (nel frattempo)
INSERT INTO ordini (importo) VALUES (1500);
COMMIT;

-- Transazione A, stessa query
SELECT * FROM ordini WHERE importo > 1000;
-- ora restituisce 6 righe → phantom read
COMMIT;
```

La transazione A non ha modificato nulla, ma il risultato cambia. Questo è distinto dal **Non-Repeatable Read**, che riguarda la modifica di righe già lette, non l'aggiunta o rimozione di righe nel range.

## Isolation level e prevenzione

Il livello `READ COMMITTED` ammette i phantom read: ogni SELECT vede uno snapshot aggiornato al momento dell'esecuzione. Il livello `REPEATABLE READ` — default in InnoDB — li previene tramite **gap lock** e **next-key lock**, che bloccano gli intervalli di indice impedendo INSERT concorrenti nel range letto. Il livello `SERIALIZABLE` offre la garanzia più forte, convertendo le SELECT implicite in letture bloccanti.

Scegliere `READ COMMITTED` in scenari ad alta concorrenza riduce il rischio di deadlock da gap lock, ma espone l'applicazione ai phantom read: un trade-off da valutare in base alla logica di business.
