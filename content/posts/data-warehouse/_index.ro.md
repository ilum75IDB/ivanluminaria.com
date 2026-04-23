---
title: "Data Warehouse"
date: "2026-03-10T08:03:00+01:00"
description: "Arhitectură Data Warehouse în practică: modelare dimensională, ierarhii, ETL și strategii de încărcare. Când datele nu trebuie doar să funcționeze, ci să ajute la decizii."
image: "data-warehouse.cover.jpg"
layout: "list"
---

Am văzut data warehouse-uri construite pe granularitate zilnică pentru că "business-ului îi e bine așa" — și devenind inutile a doua zi, când marketingul a cerut analiza orară a conversiilor. Am văzut dimensiuni client fără istoricizare, care suprascriau codul poștal de fiecare dată când cineva se muta — și rapoarte de acum un an care nu mai ieșeau la fel. Am văzut ETL-uri care încărcau 200 de milioane de rânduri în full în fiecare noapte pentru că nimeni nu avusese niciodată curajul să reproiecteze delta-ul.

Și am văzut exact opusul: data marts mici, bine modelate, cu bus matrix-ul desenat corect — care răspund la întrebări pe care nimeni nu se gândise încă să le pună, fără să se atingă o singură linie de cod.

Diferența nu a fost niciodată tehnologia. A fost întotdeauna **modelul**.

------------------------------------------------------------------------

Un data warehouse nu este o bază de date cu tabele mai mari. Este **un mod diferit de a gândi datele** — orientat spre analiză, istorie, decizii.

În bazele de date tranzacționale contează *momentul prezent*: comanda pe care o inserezi, soldul curent, rândul pe care îl actualizezi. Într-un data warehouse contează *traseul*: cum era acel client acum șase luni, cum s-a schimbat produsul în timp, care versiune a nomenclatorului era validă când a fost emis acel contract.

Aproape întotdeauna, DWH-ul care nu rezistă se recunoaște după aceste lucruri:

- **granularitate greșită** în tabela de fapte — prea grosieră și pierzi detaliul, prea fină și încetinești tot
- **dimensiuni plate** fără gestiune SCD — istorie pierdută, analize "as-was" imposibile
- **ierarhii neechilibrate** care rup agregările imediat ce business-ul cere un drill-down
- **bus matrix niciodată desenat** — data marts care nu vorbesc între ele, aceleași entități modelate diferit în fiecare departament
- **ETL-uri proiectate ca o copie** în loc de ca o transformare — mizeria din tranzacțional ajungând intactă în analitic

Sunt probleme pe care în dezvoltare nu le vezi. Explodează după șase luni, când business-ul cere rapoarte pe care modelul nu le poate susține.

------------------------------------------------------------------------

## 📊 Ce întreb business-ul înainte să ating modelul

Înainte chiar să desenez o tabelă de fapte, sunt cinci întrebări pe care le pun business-ului. Nu sunt opționale — sunt diferența între un data warehouse care durează zece ani și unul care trebuie rescris după doi.

| Întrebare | Ce încerc să înțeleg | De ce e critică |
|---|---|---|
| **La ce granularitate ai nevoie de date?** | Zilnică, orară, tranzacție individuală | Alege întotdeauna granularitatea minimă utilă — se poate agrega după, dezagrega nu |
| **Cât de departe în timp?** | Istoria necesară, profunzime analitică | Definește volume, stocare, strategii de partiționare și arhivare |
| **Ce se întâmplă când se schimbă un nomenclator?** | Client care se mută, produs care schimbă categoria | Determină tipul de SCD (1, 2, 3, 6) pentru fiecare dimensiune |
| **Ce ierarhii trebuie să susțină?** | Drill-down, roll-up, căi alternative | Evită dimensiuni ragged, snowflake nejustificate, join-uri lente pe agregări |
| **Care e latența acceptabilă?** | Batch nocturn, intraday, near real-time | Schimbă tot: ETL, model, infrastructură, cost |

Cinci întrebări. Douăzeci de minute de ședință. Săptămâni de rescrieri evitate.

------------------------------------------------------------------------

## 📚 Despre ce vorbesc aici

Povești reale de proiectare și restructurare de data warehouse-uri în producție. Modelare dimensională (Kimball citit cu cap, nu pe sloganuri), slowly changing dimensions, bus matrix, ierarhii, strategii de încărcare incrementală și performanță analitică.

Fără rețete de manual. Doar soluții aplicate pe sisteme reale — asigurări, finance, administrație publică, telco, postal — care servesc decizii de afaceri reale.

------------------------------------------------------------------------

Un data warehouse nu se construiește pentru a conține date.

Se construiește pentru a răspunde la întrebări — și acele întrebări, inevitabil, se schimbă.
