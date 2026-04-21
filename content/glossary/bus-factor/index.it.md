---
title: "Bus Factor"
description: "Numero di persone del team che, se venissero a mancare contemporaneamente, bloccherebbero il progetto. Misura la concentrazione di conoscenza critica in poche teste."
translationKey: "glossary_bus_factor"
aka: "Truck Factor, Lottery Factor"
articles:
  - "/posts/project-management/team-di-progetto-che-reggono"
---

**Bus Factor** (anche noto come Truck Factor o Lottery Factor) è una metrica empirica che risponde alla domanda: *"Quante persone del team devono venire a mancare contemporaneamente perché il progetto si fermi?"*. Il nome, un po' macabro, deriva dallo scenario ipotetico del collega investito da un autobus — ma vale ugualmente per ferie prolungate, malattie, dimissioni, trasferimenti.

## Come si calcola

Non esiste una formula matematica precisa, ma una stima ragionata che parte da alcune domande:

- Chi è l'unica persona che sa configurare il cluster di produzione?
- Chi è l'unica persona che conosce il dominio funzionale di una certa area?
- Chi ha scritto il pezzo di codice più critico senza documentarlo?
- Chi tiene i rapporti con uno stakeholder chiave del cliente?

Se la risposta a ciascuna domanda è "una persona sola", il bus factor è 1 su quella competenza. Il bus factor del team è il minimo tra tutti i bus factor delle singole competenze critiche.

## Valori tipici

- **Bus factor = 1**: rischio critico. Una sola persona detiene conoscenza che bloccherebbe il progetto. Frequente in team piccoli o in attività "da guru".
- **Bus factor = 2**: fragile. Coperto se una persona manca, ma se si fermano entrambe il progetto si arresta.
- **Bus factor ≥ 3**: resiliente. La conoscenza è distribuita abbastanza da assorbire assenze multiple.

Il limite pragmatico su cui ci si muove nei progetti reali è mantenere bus factor ≥ 3 sulle competenze davvero critiche, accettando valori inferiori su aree più periferiche.

## Come si alza il bus factor

Quattro strumenti, tutti a costo basso ma con richiesta di tempo di calendario:

- **Documentazione minima**: non enciclopedie, ma runbook operativi di 2-5 pagine sulle procedure critiche
- **Pair working**: due persone sulla stessa attività, alternate nel ruolo di "chi tocca la tastiera" e "chi osserva e interroga"
- **Rotazione**: chi ha sempre fatto X questo mese passa a Y, e viceversa. Anche solo per una settimana
- **Knowledge transfer ricorrente**: 30 minuti in agenda ogni settimana su un tema specifico, registrati

## Segnali che il bus factor è basso

- Quando una persona va in ferie, il team rallenta visibilmente
- Alcune attività vengono sistematicamente assegnate sempre alla stessa persona
- Una procedura critica non è mai stata documentata
- Il lead è l'unico che conosce il "perché" di certe scelte architetturali
