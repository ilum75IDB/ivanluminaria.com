---
title: "Tablespace"
description: "Unitate logică de stocare în Oracle care grupează unul sau mai multe fișiere de date fizice. Permite organizarea, gestionarea și optimizarea spațiului pe disc pentru tabele, indexuri și partiții."
translationKey: "glossary_tablespace"
articles:
  - "/posts/oracle/oracle-partitioning"
---

Un **Tablespace** este unitatea logică de organizare a stocării în Oracle Database. Fiecare tablespace este compus din unul sau mai multe fișiere de date (datafile) fizice pe disc, iar fiecare obiect al bazei de date (tabelă, index, partiție) rezidă într-un tablespace.

## Cum funcționează

Oracle separă gestionarea logică (tablespace) de cea fizică (datafile). Un DBA poate crea tablespace-uri dedicate pentru scopuri diferite: unul pentru datele active, unul pentru indexuri, unul pentru arhivă. Aceasta permite distribuirea sarcinii de I/O pe discuri diferite și aplicarea de politici de gestionare diferențiate (ex. read-only pentru datele istorice).

## La ce folosește

În contextul partitioning-ului, tablespace-urile permit strategii avansate de gestionare a ciclului de viață: mutarea partițiilor vechi pe tablespace-uri de arhivă economice, punerea lor în read-only pentru reducerea sarcinii de backup și recuperarea spațiului activ fără ștergerea datelor. Un `ALTER TABLE MOVE PARTITION ... TABLESPACE ts_archive` este o operație DDL care durează mai puțin de o secundă.

## Când se folosește

Fiecare instalare Oracle folosește tablespace-uri. Designul tablespace-urilor devine critic când se gestionează tabele de sute de GB cu partitioning, deoarece o bună distribuție pe tablespace-uri separate activează backup-uri incrementale eficiente și gestionarea ciclului de viață al datelor.
