---
title: "AIOps"
description: "AIOps applica AI e machine learning all'IT operations per rilevare anomalie e correlazioni nei log e nelle metriche, senza ricostruire automaticamente la catena causale."
translationKey: "glossary_aiops"
aka: "Artificial Intelligence for IT Operations"
articles:
  - "/posts/oracle/ai-mostra-sintomo-board-chiede-causa"
---

AIOps (Artificial Intelligence for IT Operations) è l'applicazione di algoritmi di machine learning e analisi statistica ai dati operativi di un sistema IT: metriche di performance, log applicativi, eventi di infrastruttura. L'obiettivo è ridurre il rumore degli alert e portare in superficie pattern anomali che un operatore umano faticherebbe a individuare manualmente su volumi elevati.

## Come funziona

Una piattaforma AIOps ingerisce stream continui di dati (metriche di CPU, query time, error rate, log strutturati) e applica modelli di anomaly detection — tipicamente basati su clustering, serie temporali o reti neurali — per identificare deviazioni dalla baseline. Quando due anomalie si sovrappongono temporalmente, il sistema le correla e le presenta come un unico evento aggregato.

Il risultato è un alert arricchito: invece di ricevere cinquanta notifiche separate, il team riceve un singolo incident con i segnali correlati e una finestra temporale comune.

## Limiti operativi

La correlazione temporale non equivale a causalità. AIOps può segnalare che un picco di latenza su Oracle coincide con un aumento di I/O su storage, ma non determina automaticamente quale dei due sia la causa e quale l'effetto — né individua la root cause a monte (es. una query non ottimizzata, un lock contention, un batch notturno fuori controllo).

In un incident complesso, la ricostruzione della catena causale richiede ancora l'intervento di un DBA o di un ingegnere con contesto applicativo. AIOps riduce il tempo di triage, non lo elimina.
