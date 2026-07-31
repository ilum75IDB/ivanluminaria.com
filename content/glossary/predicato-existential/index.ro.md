---
title: "Predicat Existențial"
description: "Expresie logică SQL care verifică existența cel puțin a unui rând ce satisface o condiție, baza pattern-urilor EXISTS și NOT EXISTS."
translationKey: "glossary_predicato_existential"
aka: "Existential predicate, predicat de existență"
articles:
  - "/posts/oracle/articolo-oracle-assertions-in-oracle-26ai"
---

Un **predicat existențial** este o expresie logică ce returnează `TRUE` dacă există cel puțin un rând care satisface o condiție dată. În SQL stă la baza operatorilor `EXISTS` și `NOT EXISTS`, utilizați de obicei în subinterogări corelate pentru a verifica prezența sau absența datelor corelate fără a le recupera explicit.

## Cum funcționează

Motorul evaluează subinterogarea corelată rând cu rând față de interogarea externă. De îndată ce găsește primul rând care îndeplinește condiția, returnează `TRUE` și oprește parcurgerea (evaluare în scurtcircuit). Acest comportament îl face adesea mai eficient decât un `JOIN` sau un `IN` pe seturi mari de date.

```sql
-- Verifică că există cel puțin o comandă activă pentru fiecare client
SELECT c.id, c.nume
FROM clienti c
WHERE EXISTS (
    SELECT 1
    FROM comenzi o
    WHERE o.client_id = c.id
      AND o.stare = 'ACTIV'
);
```

`SELECT 1` din subinterogare este o convenție: valoarea proiectată este irelevantă — contează doar existența rândului.

## Când se folosește

Predicatul existențial este pattern-ul natural pentru implementarea **Assertions de tip „cel puțin unul"**: constrângeri sau verificări care impun prezența garantată a cel puțin unui înregistrări corelate. În Oracle 23ai, unde Assertions declarative nu sunt încă expuse ca obiecte DDL native, `EXISTS` în triggere sau check constraints reprezintă substitutul operațional standard.

`NOT EXISTS` acoperă cazul complementar — niciun rând nu trebuie să satisfacă condiția — util pentru constrângeri de excludere sau pentru detectarea golurilor în serii temporale.

Un aspect de reținut: pe subinterogări necorelate sau pe coloane fără index, costul poate degrada la o parcurgere completă. Analiza planului de execuție (`EXPLAIN PLAN`) înainte de a duce în producție interogări cu `EXISTS` pe tabele de dimensiuni mari este întotdeauna recomandată.
