---
title: "Bus Matrix"
description: "Matrice bidimensionale di Ralph Kimball con i processi di business sulle righe e le dimensioni conformi sulle colonne. Strumento di allineamento organizzativo prima della progettazione fisica del DWH."
translationKey: "glossary_bus_matrix"
aka: "Kimball Bus Matrix, Data Warehouse Bus Architecture"
articles:
  - "/posts/data-warehouse/bus-matrix-terreno-comune"
---

**Bus Matrix** è uno strumento di progettazione introdotto da Ralph Kimball per allineare in modo esplicito i processi di business di un'organizzazione con le dimensioni analitiche condivise che serviranno a descriverli nel data warehouse.

## Come è fatta

Una matrice bidimensionale:

- Sulle **righe**: i processi di business (vendite, resi, campagne, fatturazione, movimenti di magazzino, emissione polizze, incassi, ecc.)
- Sulle **colonne**: le dimensioni candidate a diventare conformi (cliente, prodotto, tempo, geografia, canale, dipendente, ecc.)
- Nelle **celle**: una X se quel processo usa quella dimensione

Una lettura verticale della matrice indica quante fact table toccano una certa dimensione: più X ci sono, più quella dimensione è critica per la conformità.

## A cosa serve

Il bus matrix non genera codice, non crea tabelle e non ottimizza query. Serve a una cosa sola: obbligare le parti coinvolte (IT, business, finance, marketing) a guardare lo stesso foglio e concordare esplicitamente cosa intendono per "cliente", "prodotto", "data". È un esercizio di allineamento organizzativo che precede la progettazione fisica.

## Quando farlo

All'inizio del progetto, prima di qualunque CREATE TABLE. Kimball lo raccomanda come primo passo del ciclo di vita del DWH. Farlo dopo, quando i data mart sono già stati costruiti in autonomia dai reparti, costa ordini di grandezza in più: servono workshop di governance, processi di matching a posteriori, tabelle di mappatura (xref) e tempo per rinegoziare le definizioni esistenti.

## Relazione con le dimensioni conformi

Il bus matrix è lo strumento di diagnosi, le dimensioni conformi sono la soluzione. Dove due processi condividono una dimensione nella matrice, quella dimensione *deve* essere conforme — stessa chiave, stessa struttura, stessa semantica — altrimenti le analisi cross-processo restituiranno numeri incoerenti.
