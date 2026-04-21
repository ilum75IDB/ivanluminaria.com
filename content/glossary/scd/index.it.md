---
title: "SCD"
description: "Slowly Changing Dimension — tecnica di data warehouse per tracciare le variazioni nel tempo dei dati nelle tabelle dimensionali."
translationKey: "glossary_scd"
aka: "Slowly Changing Dimension"
articles:
  - "/posts/data-warehouse/scd-tipo-2"
  - "/posts/data-warehouse/bus-matrix-terreno-comune"
---

**SCD** (Slowly Changing Dimension) indica un insieme di tecniche usate nel data warehouse per gestire i cambiamenti nei dati delle tabelle dimensionali nel corso del tempo.

## I tipi principali

- **Tipo 1**: sovrascrittura del valore precedente. Nessuna storia conservata
- **Tipo 2**: inserimento di una nuova riga con date di validità (data inizio, data fine). Conserva tutta la storia
- **Tipo 3**: aggiunta di una colonna per il valore precedente. Conserva solo l'ultimo cambiamento

## Perché serve

In un database transazionale, quando un cliente cambia indirizzo si aggiorna il record. In un data warehouse questo significherebbe perdere la storia: tutte le vendite precedenti risulterebbero associate al nuovo indirizzo.

La SCD Tipo 2 risolve questo problema mantenendo una riga per ogni versione del dato, con date di validità che permettono di ricostruire la situazione a qualsiasi punto nel tempo.

## Quando si usa

La scelta del tipo dipende dal requisito di business. Se serve solo il dato corrente, il Tipo 1 basta. Se il business ha bisogno di analisi storiche accurate — e nella maggior parte dei data warehouse reali è così — il Tipo 2 è la scelta standard.
