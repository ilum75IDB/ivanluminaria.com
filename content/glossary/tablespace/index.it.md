---
title: "Tablespace"
description: "Unità logica di storage in Oracle che raggruppa uno o più datafile fisici. Permette di organizzare, gestire e ottimizzare lo spazio su disco per tabelle, indici e partizioni."
translationKey: "glossary_tablespace"
articles:
  - "/posts/oracle/oracle-partitioning"
---

Un **Tablespace** è l'unità logica di organizzazione dello storage in Oracle Database. Ogni tablespace è composto da uno o più datafile fisici sul disco, e ogni oggetto del database (tabella, indice, partizione) risiede in un tablespace.

## Come funziona

Oracle separa la gestione logica (tablespace) da quella fisica (datafile). Un DBA può creare tablespace dedicati per scopi diversi: uno per i dati attivi, uno per gli indici, uno per l'archivio. Questo permette di distribuire il carico I/O su dischi diversi e di applicare politiche di gestione differenziate (es. read-only per i dati storici).

## A cosa serve

Nel contesto del partitioning, i tablespace permettono strategie di lifecycle management avanzate: spostare partizioni vecchie su tablespace di archivio economici, metterle in read-only per ridurre il carico di backup, e recuperare spazio attivo senza cancellare dati. Un `ALTER TABLE MOVE PARTITION ... TABLESPACE ts_archive` è un'operazione DDL che richiede meno di un secondo.

## Quando si usa

Ogni installazione Oracle usa tablespace. La progettazione dei tablespace diventa critica quando si gestiscono tabelle di centinaia di GB con partitioning, perché una buona distribuzione su tablespace separati abilita backup incrementali efficienti e gestione del ciclo di vita dei dati.
