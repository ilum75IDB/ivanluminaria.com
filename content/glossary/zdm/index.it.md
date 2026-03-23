---
title: "ZDM"
description: "Zero Downtime Migration — strumento Oracle per automatizzare le migrazioni verso OCI combinando Data Guard e Data Pump sotto un layer di orchestrazione."
translationKey: "glossary_zdm"
aka: "Zero Downtime Migration"
articles:
  - "/posts/oracle/oracle-cloud-migration"
---

**ZDM** (Zero Downtime Migration) è lo strumento che Oracle fornisce per automatizzare le migrazioni di database Oracle verso OCI (Oracle Cloud Infrastructure) o verso database on-premises di versione superiore. Il nome è un po' ottimistico — il downtime non è zero, ma è ridotto al minimo.

## Come funziona

ZDM è essenzialmente un orchestratore che combina tecnologie Oracle esistenti sotto un unico flusso automatizzato. Supporta due modalità:

- **Migrazione fisica** (basata su Data Guard): crea uno standby del database sorgente sulla destinazione, lo sincronizza tramite redo transport, e poi esegue uno switchover. Downtime dell'ordine di minuti.
- **Migrazione logica** (basata su Data Pump): esegue export e import logico con sincronizzazione incrementale tramite GoldenGate o Data Pump. Più flessibile ma più lenta.

## Quando usarlo

ZDM è indicato per migrazioni standard dove l'infrastruttura sorgente e quella di destinazione sono configurate in modo convenzionale. Il vantaggio è l'automazione: riduce la possibilità di errore umano nei passaggi ripetitivi.

## Quando non usarlo

Per configurazioni complesse — RAC con DB link cross-engine, dipendenze esterne non standard, procedure PL/SQL con chiamate HTTP — il layer di automazione di ZDM può diventare un ostacolo. In questi casi, configurare Data Guard manualmente dà più controllo sui dettagli e sulla sequenza delle operazioni.

## Requisiti

ZDM richiede un host dedicato (il "ZDM service host") con accesso SSH sia al database sorgente che alla destinazione. Il sorgente deve essere Oracle 11.2.0.4 o superiore, la destinazione può essere su OCI o on-premises.
