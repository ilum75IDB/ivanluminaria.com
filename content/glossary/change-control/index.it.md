---
title: "Change Control"
description: "Processo formale GxP per gestire modifiche a hardware, software e procedure: risk assessment, test protocol, documentazione e firme autorizzative."
translationKey: "glossary_change_control"
aka: "Change Management Process"
articles:
  - "/posts/oracle/latenza-wan-e-change-control-gxp-il-costo-reale-del-lift-and-shift"
---

Il change control è il processo formale obbligatorio nei sistemi validati GxP (Good Practice) che governa qualsiasi modifica a infrastruttura, software o procedure operative. Non è una burocrazia opzionale: nei contesti farmaceutici, medicali e biotech regolamentati, un'implementazione senza change control approvato equivale a una deviazione documentabile con conseguenze regolatorie dirette.

## Come funziona

Il ciclo tipico prevede quattro fasi sequenziali:

1. **Richiesta di modifica** — descrizione tecnica della modifica proposta, motivazione e sistemi impattati.
2. **Valutazione del rischio** — analisi dell'impatto su validazione esistente (IQ/OQ/PQ), integrità dei dati e continuità operativa.
3. **Protocollo di test** — definizione dei test da eseguire prima del go-live, con criteri di accettazione espliciti.
4. **Approvazione e implementazione** — firme autorizzative dei ruoli designati (QA, IT, business owner) e documentazione post-implementazione.

Ogni fase produce artefatti tracciabili che devono rimanere nel sistema di gestione documentale per audit interni e ispezioni regolatorie.

## Contesto operativo

Il change control diventa un collo di bottiglia critico nei progetti di migrazione cloud (lift-and-shift) perché ogni componente migrato — database, middleware, sistema operativo — può richiedere un change request separato. In ambienti Oracle su sistemi GxP, anche un aggiornamento di patch minore può innescare un ciclo completo di re-validazione se impatta funzionalità già qualificate. Il tempo medio di approvazione in organizzazioni mid-size varia da 2 a 8 settimane per change a medio rischio, un fattore che i piani di migrazione spesso sottostimano sistematicamente.
