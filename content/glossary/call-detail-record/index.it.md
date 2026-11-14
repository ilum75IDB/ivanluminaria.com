---
title: "Call Detail Record (CDR)"
description: "Record che documenta una singola chiamata telefonica con dati di cliente, durata, tipo e costo. Dato operativo primario nei sistemi telco."
translationKey: "glossary_call_detail_record"
aka: "CDR, Call Data Record"
articles:
  - "/posts/data-warehouse/la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto"
---

Un Call Detail Record (CDR) è la traccia persistente che un sistema di telefonia genera al termine di ogni chiamata. Contiene le informazioni minime necessarie per fatturare il servizio e analizzare il traffico: chi ha chiamato, quando, per quanto tempo, con quale tipo di connessione e a quale costo. Nei sistemi telco è il dato operativo di riferimento, analogo a una riga di transazione in un sistema bancario.

## Struttura tipica

Un CDR include almeno questi campi:

| Campo | Descrizione |
|---|---|
| `caller_id` | Identificativo del cliente chiamante |
| `callee_id` | Numero o identificativo del destinatario |
| `start_time` | Timestamp di inizio chiamata |
| `duration_sec` | Durata in secondi |
| `call_type` | Voce, SMS, dati, roaming |
| `cost` | Costo calcolato a fine chiamata |

La struttura varia tra operatori e standard (3GPP, IPDR), ma questi campi sono pressoché universali.

## Contesto operativo

I CDR si accumulano a velocità elevata: un operatore di medie dimensioni produce centinaia di GB mensili. Questo li rende un caso d'uso classico per i Data Warehouse telco, dove vengono caricati in batch o via streaming e poi aggregati per fatturazione, analisi del traffico e rilevamento frodi. Le query analitiche tipiche — somma di durata per cliente, distribuzione per fascia oraria, confronto mese su mese — beneficiano di tecniche come le Materialized View per evitare ricalcoli costosi su tabelle da miliardi di righe.

## Note sul volume

Un singolo CDR pesa pochi byte, ma la cardinalità è altissima. Progettare lo schema di storage (partitioning per data, compressione columnar, indici parziali) è critico già in fase di modellazione, prima ancora di ragionare sulle query.
