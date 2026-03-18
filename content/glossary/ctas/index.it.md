---
title: "CTAS"
description: "Create Table As Select — tecnica Oracle per creare una nuova tabella popolandola con i risultati di una query, usata per migrazioni e ristrutturazioni di tabelle di grandi dimensioni."
translationKey: "glossary_ctas"
aka: "Create Table As Select"
articles:
  - "/posts/oracle/oracle-partitioning"
---

**CTAS** (Create Table As Select) è un comando SQL Oracle che crea una nuova tabella e la popola in un'unica operazione con i risultati di una SELECT. È la tecnica standard per migrare dati da una struttura all'altra su tabelle di grandi dimensioni.

## Come funziona

Il comando combina DDL e DML: crea la tabella con la struttura derivata dalla SELECT e inserisce i dati in un unico passaggio. Con l'hint `PARALLEL` e la modalità `NOLOGGING`, la copia di centinaia di GB può completarsi in poche ore. Dopo la copia, si rinomina la tabella originale, si rinomina la nuova, e il downtime è limitato ai pochi secondi del rename.

## A cosa serve

CTAS è fondamentale quando serve ristrutturare una tabella senza poter usare `ALTER TABLE` direttamente — ad esempio per aggiungere il partitioning a una tabella esistente con miliardi di righe. Permette di lavorare sulla nuova struttura mentre il sistema è attivo sulla vecchia.

## Quando si usa

Si usa per migrazioni a tabelle partizionate, per riorganizzare dati frammentati, e per creare copie di tabelle con strutture diverse. In produzione, va sempre combinato con `NOLOGGING` (per ridurre i redo log) e seguito da un backup RMAN immediato.
