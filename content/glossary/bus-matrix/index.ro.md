---
title: "Bus Matrix"
description: "Matrice bidimensională a lui Ralph Kimball cu procesele de business pe rânduri și dimensiunile conforme pe coloane. Instrument de aliniere organizațională înainte de proiectarea fizică a DWH-ului."
translationKey: "glossary_bus_matrix"
aka: "Kimball Bus Matrix, Data Warehouse Bus Architecture"
articles:
  - "/posts/data-warehouse/bus-matrix-terreno-comune"
---

**Bus Matrix** este un instrument de proiectare introdus de Ralph Kimball pentru a alinia explicit procesele de business ale unei organizații cu dimensiunile analitice partajate care le vor descrie în data warehouse.

## Cum arată

O matrice bidimensională:

- Pe **rânduri**: procesele de business (vânzări, retururi, campanii, facturare, mișcări de stoc, emitere polițe, încasări, etc.)
- Pe **coloane**: dimensiunile candidate să devină conforme (client, produs, timp, geografie, canal, angajat, etc.)
- În **celule**: un X dacă acel proces folosește acea dimensiune

Citirea pe verticală a matricei arată câte fact tables ating o anumită dimensiune: cu cât sunt mai multe X-uri, cu atât conformitatea este mai critică pentru acea dimensiune.

## La ce servește

Bus matrix nu generează cod, nu creează tabele și nu optimizează interogări. Servește la un singur lucru: să oblige părțile implicate (IT, business, finance, marketing) să privească aceeași foaie și să convină explicit ce înțeleg prin "client", "produs", "dată". Este un exercițiu de aliniere organizațională care precede proiectarea fizică.

## Când se face

La începutul proiectului, înainte de orice CREATE TABLE. Kimball îl recomandă ca prim pas din ciclul de viață al DWH-ului. Făcându-l după, când data marts-urile au fost deja construite autonom de departamente, costă ordine de mărime mai mult: sunt necesare ateliere de guvernanță, procese de matching retroactive, tabele de mapare (xref) și timp pentru a renegocia definițiile existente.

## Relația cu dimensiunile conforme

Bus matrix este instrumentul de diagnostic, dimensiunile conforme sunt soluția. Acolo unde două procese partajează o dimensiune în matrice, acea dimensiune *trebuie* să fie conformă — aceeași cheie, aceeași structură, aceeași semantică — altfel analizele cross-proces vor returna numere incoerente.
