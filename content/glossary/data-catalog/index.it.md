---
title: "Data Catalog"
description: "Inventario centralizzato dei dati aziendali con metadati, lineage e ricerca integrata: rende la governance accessibile agli utenti business."
translationKey: "glossary_data_catalog"
aka: "Enterprise Data Catalog"
articles:
  - "/posts/data-warehouse/data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati"
---

Un Data Catalog è l'inventario organizzato di tutti gli asset di dati disponibili in un'organizzazione: tabelle, view, dataset, report, API, file. Ogni asset è corredato di metadati tecnici e business, lineage, classificazioni di qualità e un glossario condiviso. L'obiettivo è rendere i dati trovabili e comprensibili senza dover aprire un ticket al team tecnico per ogni domanda.

## Come funziona

Il catalog raccoglie metadati da sorgenti eterogenee tramite connettori (database relazionali, data lake, strumenti BI, pipeline ETL). Per ogni asset espone:

- **metadati tecnici**: schema, tipo di dato, cardinalità, frequenza di aggiornamento
- **metadati business**: owner, descrizione in linguaggio naturale, tag di dominio
- **lineage**: grafo che mostra da dove arriva un dato e dove viene consumato
- **data quality score**: metriche aggregate calcolate dai processi di validazione upstream

Gli utenti cercano asset tramite full-text search o navigazione per dominio/tag. I data steward arricchiscono le voci con annotazioni e approvazioni.

## Quando si usa

Il Data Catalog diventa necessario quando il numero di sorgenti supera la capacità di documentazione manuale — tipicamente oltre 20-30 dataset attivi — oppure quando la compliance richiede tracciabilità end-to-end (GDPR, HIPAA, SOX). È anche il punto di ingresso naturale per i data contract: il catalog espone le specifiche di un dataset, il contratto ne formalizza le garanzie di qualità e SLA.

Senza catalog, la governance rimane un documento Word aggiornato raramente; con il catalog, diventa un sistema vivo interrogabile da chiunque abbia accesso.
