---
title: "Conformed Dimension"
description: "Dimensione condivisa tra più data mart con la stessa struttura, semantica e chiave. Permette analisi cross-processo coerenti e sommabili."
translationKey: "glossary_conformed_dimension"
aka: "Dimensione Conforme, Shared Dimension"
articles:
  - "/posts/data-warehouse/bus-matrix-terreno-comune"
---

**Conformed Dimension** (dimensione conforme) è una dimensione usata in più di una fact table o di un data mart con la stessa struttura, la stessa semantica e la stessa chiave. È il pilastro della bus architecture di Kimball.

## Cosa significa "conformare"

Conformare una dimensione significa concordare tre elementi:

- **Chiave naturale univoca**: quale identificativo rappresenta l'entità (codice fiscale, codice cliente, codice prodotto, partita IVA)
- **Attributi condivisi**: quali colonne sono comuni a tutti i data mart che usano la dimensione (paese, regione, categoria, ecc.)
- **Grana**: il livello di dettaglio della dimensione (una riga per cliente, non per segmento)

Gli attributi specifici di un singolo reparto possono restare in tabelle dimensionali locali, ma non devono entrare nella parte conforme della dimensione.

## A cosa serve

Senza dimensioni conformi, le misure provenienti da fact table diverse non si possono confrontare in modo affidabile. Con dimensioni conformi, una query che incrocia vendite e campagne marketing sullo stesso cliente restituisce un risultato coerente perché "cliente" significa la stessa cosa nei due processi.

## Implementazione fisica

Una dimensione conforme non deve necessariamente essere una singola tabella fisica condivisa. Può essere:

- **Replicata** in più schemi (soluzione pragmatica quando i data mart sono su database diversi)
- **Centralizzata** in uno schema dedicato (es. `dim_conformed`) con viste o sinonimi nei data mart
- **Virtualizzata** tramite strumenti di data virtualization

L'importante è che le tre proprietà — struttura, semantica, chiave — siano identiche in ogni copia.

## Quando serve la governance

Mantenere la conformità nel tempo richiede un comitato di governance con rappresentanti dei reparti che usano la dimensione. Ogni modifica (nuovo attributo, nuova regola di deduplica, nuovo canale di acquisizione) va concordata e propagata in modo coordinato, altrimenti le dimensioni conformi divergono e tutto il castello crolla.
