---
title: "OLAP"
description: "Online Analytical Processing — elaborazione orientata all'analisi multidimensionale dei dati, tipica dei data warehouse."
translationKey: "glossary_olap"
aka: "Online Analytical Processing"
articles:
  - "/posts/data-warehouse/ragged-hierarchies"
---

**OLAP** (Online Analytical Processing) indica un approccio all'elaborazione dei dati orientato all'analisi multidimensionale: aggregazioni, drill-down, confronti temporali, slice-and-dice su grandi volumi di dati storici.

## OLAP vs OLTP

| Caratteristica | OLAP | OLTP |
|----------------|------|------|
| Scopo | Analisi e reporting | Transazioni operative |
| Modello dati | Star schema, denormalizzato | 3NF, normalizzato |
| Query tipica | Aggregazioni su milioni di righe | Lettura/scrittura di poche righe |
| Utenti | Analisti, management | Applicazioni, operatori |
| Aggiornamento | Batch (ETL periodico) | Real-time |

## Operazioni OLAP

Le operazioni fondamentali dell'analisi OLAP sono:

- **Drill-down**: dal livello aggregato al dettaglio
- **Drill-up** (roll-up): dal dettaglio all'aggregato
- **Slice**: selezionare una "fetta" dei dati fissando una dimensione (es. solo anno 2025)
- **Dice**: selezionare un sottocubo specificando più dimensioni
- **Pivot**: ruotare le dimensioni di analisi (righe ↔ colonne)

## Implementazioni

- **ROLAP** (Relational OLAP): i dati restano in tabelle relazionali, le aggregazioni sono calcolate con query SQL. È l'approccio usato nei data warehouse con star schema
- **MOLAP** (Multidimensional OLAP): i dati sono pre-aggregati in strutture multidimensionali (cubi). Più veloce nelle query ma richiede più spazio e tempi di build
- **HOLAP** (Hybrid): combinazione dei due approcci
