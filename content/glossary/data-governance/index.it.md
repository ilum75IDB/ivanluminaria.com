---
title: "Data Governance"
description: "Framework operativo continuo di processi, politiche e standard che garantiscono qualità, integrità, sicurezza e conformità normativa dei dati aziendali."
translationKey: "glossary_data_governance"
aka: "Governo del dato"
articles:
  - "/posts/data-warehouse/data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati"
---

La Data Governance è l'insieme strutturato di processi, politiche, standard e metriche che regolano come un'organizzazione gestisce i propri dati. Non si tratta di un progetto con una data di fine, ma di un framework operativo continuo che attraversa persone, tecnologie e processi.

## Come funziona

Un programma di Data Governance definisce chi è responsabile di ogni dato (data ownership), come viene classificato, quali regole ne governano la qualità e chi può accedervi. Gli strumenti operativi includono data catalog, data lineage, policy di retention e controlli di qualità automatizzati integrati nelle pipeline ETL/ELT.

Nel contesto di un Data Warehouse, la governance si applica a ogni layer: dalla staging zone fino ai mart esposti agli utenti finali. Un check di qualità tipico può bloccare il caricamento di record con valori nulli su colonne critiche o segnalare derive statistiche nei KPI.

## Contesto operativo

La Data Governance diventa non negoziabile quando entrano in gioco normative come GDPR, HIPAA o PCI-DSS: la tracciabilità del dato — chi lo ha creato, modificato, consumato — deve essere dimostrabile in sede di audit. Altrettanto rilevante è la gestione del data quality debt: senza governance, i problemi di qualità si accumulano silenziosamente fino a compromettere decisioni di business critiche.

Il principale trade-off è tra rigore e velocità: processi di governance troppo pesanti rallentano i team di sviluppo. La soluzione pratica è calibrare i controlli sul rischio effettivo del dato, non applicare lo stesso livello di scrutinio a ogni tabella.
