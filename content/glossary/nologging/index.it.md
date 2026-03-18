---
title: "NOLOGGING"
description: "Modalità Oracle che sopprime la generazione di redo log durante operazioni bulk (CTAS, INSERT APPEND, ALTER TABLE MOVE), velocizzando le operazioni ma richiedendo un backup immediato."
translationKey: "glossary_nologging"
articles:
  - "/posts/oracle/oracle-partitioning"
---

**NOLOGGING** è una modalità Oracle che disabilita la generazione di redo log durante operazioni di caricamento massivo. Le operazioni completano molto più velocemente, ma i dati non sono recuperabili tramite redo in caso di crash prima di un backup.

## Come funziona

Quando un segmento (tabella, indice, partizione) è in modalità NOLOGGING, le operazioni bulk come CTAS, `INSERT /*+ APPEND */` e `ALTER TABLE MOVE` non scrivono redo log per i blocchi dati. Su una copia di 380 GB, questo elimina la generazione di altrettanti GB di redo, evitando di saturare l'area di archivelog e riducendo i tempi da giorni a ore.

## A cosa serve

NOLOGGING è essenziale per le operazioni di migrazione su tabelle di grandi dimensioni. Senza NOLOGGING, un CTAS di 380 GB genererebbe 380 GB di redo log, mandando il sistema in archivelog per giorni. Con NOLOGGING, la stessa operazione completa in poche ore con impatto minimo sul sistema.

## Quando si usa

Si attiva prima dell'operazione bulk e si disattiva subito dopo (`ALTER TABLE ... LOGGING`). È obbligatorio eseguire un backup RMAN immediatamente dopo, perché i segmenti NOLOGGING non sono recuperabili con un restore dai redo. Mai lasciare NOLOGGING attivo permanentemente su tabelle di produzione.
