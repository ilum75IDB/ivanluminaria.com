---
title: "Data Warehouse"
date: "2026-03-10T08:03:00+01:00"
description: "Architettura Data Warehouse nella pratica: modellazione dimensionale, gerarchie, ETL e strategie di caricamento. Quando i dati non servono solo a funzionare, ma a decidere."
image: "data-warehouse.cover.jpg"
layout: "list"
---

Ho visto data warehouse costruiti su granularità giornaliere perché "tanto al business basta così" — e diventare inutili il giorno dopo, quando il marketing ha chiesto l'analisi oraria delle conversioni. Ho visto dimensioni cliente senza storicizzazione, che sovrascrivevano il CAP ogni volta che uno si trasferiva — e report dell'anno prima che non tornavano più. Ho visto ETL che caricavano 200 milioni di righe in full ogni notte perché nessuno aveva mai avuto il coraggio di riprogettare il delta.

E ho visto l'esatto contrario: data mart piccoli, ben modellati, con il bus matrix disegnato bene — che rispondono a domande che nessuno aveva ancora pensato di fare, senza che si tocchi una riga di codice.

La differenza non è mai stata la tecnologia. È sempre stato **il modello**.

------------------------------------------------------------------------

Un data warehouse non è un database con le tabelle più grandi. È **un modo diverso di pensare ai dati** — orientato all'analisi, alla storia, alle decisioni.

Nei database transazionali conta il *momento presente*: l'ordine che stai inserendo, il saldo corrente, la riga che stai aggiornando. In un data warehouse conta il *percorso*: com'era quel cliente sei mesi fa, com'è cambiato il prodotto nel tempo, quale versione dell'anagrafica era valida quando è stato emesso quel contratto.

Quasi sempre, il DWH che non regge si riconosce da queste cose:

- **granularità sbagliata** in tabella dei fatti — troppo grossa e perdi dettaglio, troppo fine e rallenti tutto
- **dimensioni piatte** senza gestione SCD — storia persa, analisi "as-was" impossibili
- **gerarchie non bilanciate** che rompono le aggregazioni appena il business chiede un drill-down
- **bus matrix mai disegnato** — data mart che non dialogano, stesse entità modellate in modo diverso in ogni reparto
- **ETL progettati come copia** invece che come trasformazione — sporcizia del transazionale che arriva intatta in analisi

Sono problemi che in sviluppo non si vedono. Esplodono dopo sei mesi, quando il business chiede report che il modello non può supportare.

------------------------------------------------------------------------

## 📊 Cosa chiedo al business prima di mettere mano al modello

Prima ancora di disegnare una tabella dei fatti, ci sono cinque domande che pongo al business. Non sono opzionali — sono la differenza tra un data warehouse che dura dieci anni e uno che va riscritto dopo due.

| Domanda | Cosa sto cercando di capire | Perché è critica |
|---|---|---|
| **A che grana serve il dato?** | Giornaliera, oraria, per singola transazione | Scegliere la grana minima utile — sempre — poi aggregare si può, disaggregare no |
| **Quanto indietro nel tempo?** | Storia richiesta, profondità analitica | Definisce volumi, storage, strategie di partizionamento e archiviazione |
| **Cosa succede quando cambia un'anagrafica?** | Cliente che si trasferisce, prodotto che cambia categoria | Determina il tipo di SCD (1, 2, 3, 6) per ogni dimensione |
| **Quali gerarchie deve reggere?** | Drill-down, roll-up, percorsi alternativi | Evita dimensioni ragged, snowflake ingiustificati, join lenti su aggregazioni |
| **Qual è la latenza accettabile?** | Batch notturno, intraday, near real-time | Cambia tutto: ETL, modello, infrastruttura, costo |

Cinque domande. Venti minuti di riunione. Settimane di riscritture evitate.

------------------------------------------------------------------------

## 📚 Di cosa parlo qui

Storie vere di progettazione e ristrutturazione di data warehouse in produzione. Modellazione dimensionale (Kimball letto bene, non a slogan), slowly changing dimensions, bus matrix, gerarchie, strategie di caricamento incrementale e performance analitiche.

Niente ricette da manuale. Solo soluzioni applicate a sistemi veri — assicurazioni, finance, pubblica amministrazione, telco, postale — che servono decisioni aziendali reali.

------------------------------------------------------------------------

Un data warehouse non si costruisce per contenere dati.

Si costruisce per rispondere a domande — e quelle domande, inevitabilmente, cambiano.
