---
title: "Data Mart"
description: "Submulțime a data warehouse-ului focalizată pe un singur proces de business sau arie funcțională. Adesea construit autonom de un departament."
translationKey: "glossary_data_mart"
aka: "Departmental Data Mart, Subject-Area Data Mart"
articles:
  - "/posts/data-warehouse/bus-matrix-terreno-comune"
---

**Data Mart** este o submulțime a unui data warehouse focalizată pe un singur proces de business, o arie funcțională (vânzări, marketing, finance) sau un departament. Conține de obicei una sau câteva fact tables și dimensiunile legate de ele.

## De ce există data marts

În realitatea organizațiilor, un DWH enterprise complet cere ani de proiect. Data marts se nasc ca un compromis pragmatic: se construiește întâi piesa de care un departament are nevoie acum (ex. un data mart de vânzări pentru marketing) și se integrează cu celelalte ulterior. Este abordarea bottom-up a lui Kimball.

## Riscul de divergență

Când mai multe data marts sunt construite autonom de fiecare departament — adesea cu tool-uri BI diferite, pe sisteme sursă diferite, pe calendare diferite — riscul este ca "client" să ajungă să însemne trei lucruri diferite în cele trei data marts. Totalurile nu cadrează, analizele cross-departament devin imposibile sau lente, iar CFO-ul se regăsește cu trei versiuni ale adevărului.

## Data mart conform vs independent

Diferența critică este dacă data mart-ul partajează sau nu dimensiuni conforme:

- **Data marts conforme** (Kimball): partajează dimensiuni conforme (client, produs, timp, geografie) și deci pot fi interogate împreună în mod coerent
- **Data marts independente**: construite fără guvernanță comună, diverg în timp și generează clasicele probleme de "trei versiuni ale adevărului"

Bus matrix este instrumentul de proiectare care previne al doilea scenariu.

## Când are sens

Un data mart are sens când:

- Perimetrul funcțional este bine definit (un proces, un departament)
- Dimensiunile conforme sunt deja disponibile sau vor fi construite în paralel
- Costul unui DWH enterprise complet nu este justificat
- Este nevoie de un time-to-value rapid pentru un caz de utilizare specific

Nu are sens în schimb ca "soluție permanentă izolată": fie este prima piesă a unei strategii integrate, fie devine datorie tehnică în câțiva ani.
