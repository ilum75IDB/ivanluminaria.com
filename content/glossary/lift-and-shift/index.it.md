---
title: "Lift-and-Shift"
description: "Strategia di migrazione cloud che trasferisce sistemi senza modificarne architettura o codice, rimandando le ottimizzazioni al post-migrazione."
translationKey: "glossary_lift_and_shift"
aka: "Rehost migration"
articles:
  - "/posts/oracle/latenza-wan-e-change-control-gxp-il-costo-reale-del-lift-and-shift"
---

Il lift-and-shift è un approccio di migrazione cloud che replica l'ambiente sorgente — server, database, applicazioni — sulla destinazione target senza alterare architettura, configurazione o codice. L'obiettivo primario è ridurre il perimetro di validazione e comprimere i tempi di go-live, accettando consapevolmente di portare in cloud un sistema non ottimizzato per quel contesto.

## Come funziona

Il sistema sorgente viene replicato 1:1 sulla piattaforma target: le VM sono convertite o ricreate con le stesse specifiche, i database sono migrati tramite backup/restore o strumenti di replication senza schema refactoring, e le dipendenze di rete vengono ricreate fedelmente. In ambienti regolamentati (GxP, SOX, PCI-DSS) questo approccio riduce il delta di validazione perché il comportamento applicativo rimane nominalmente invariato.

## Quando si usa

Il lift-and-shift è la scelta prevalente quando:

- i tempi di migrazione sono vincolati da scadenze contrattuali o di licenza
- il sistema è legacy e non dispone di competenze interne per un refactoring sicuro
- la validazione IQ/OQ/PQ deve essere contenuta per ragioni di budget o di calendario

Il limite principale è strutturale: i costi operativi cloud (compute, storage, networking) rimangono elevati perché il sistema non sfrutta elasticità, managed services o architetture cloud-native. La latenza WAN e i vincoli di change control in ambienti GxP possono amplificare questi costi in modo significativo, come analizzato nell'articolo collegato.
