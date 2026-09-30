---
title: "Piano di esecuzione"
description: "Sequenza di operazioni scelta dall'ottimizzatore SQL per eseguire una query: scansioni, join, ordinamenti. Statistiche obsolete lo degradano silenziosamente."
translationKey: "glossary_piano_di_esecuzione"
aka: "Query execution plan, Query plan"
articles:
  - "/posts/project-management/il-preventivo-dell-upgrade-e-la-domanda-che-non-e-istintiva"
---

Il piano di esecuzione è la ricetta che il motore del database segue per rispondere a una query SQL. L'ottimizzatore valuta più strategie possibili — quali indici usare, in che ordine unire le tabelle, se ordinare prima o dopo il join — e sceglie quella con il costo stimato più basso. Il risultato è un albero di operatori che il motore esegue in sequenza.

## Come funziona

L'ottimizzatore si basa su **statistiche** (distribuzione dei valori, cardinalità delle tabelle, selettività degli indici) per stimare il costo di ogni piano candidato. Su PostgreSQL il punto di partenza è `EXPLAIN` o `EXPLAIN ANALYZE`:

```sql
EXPLAIN ANALYZE
SELECT o.id, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'pending';
```

L'output mostra ogni nodo (Seq Scan, Index Scan, Hash Join, Sort…), il costo stimato e — con `ANALYZE` — il tempo reale e le righe effettivamente elaborate. La differenza tra righe stimate e righe reali è il primo segnale di statistiche obsolete.

## Quando diventa un problema

Un piano degradato si manifesta tipicamente dopo:

- **caricamenti massivi** che alterano la distribuzione dei dati senza un `ANALYZE` successivo;
- **upgrade di versione** del database, dove l'ottimizzatore cambia euristica;
- **crescita organica** delle tabelle oltre le soglie per cui il piano era stato calibrato.

Il sintomo classico è una query che funzionava in millisecondi e improvvisamente impiega decine di secondi, senza alcuna modifica al codice applicativo. Aggiungere hardware non risolve: un Full Table Scan su 500 milioni di righe resta costoso indipendentemente dalla RAM disponibile. Il correttivo è aggiornare le statistiche (`ANALYZE`, `UPDATE STATISTICS`, `DBMS_STATS`) e verificare che l'ottimizzatore scelga il piano atteso.
