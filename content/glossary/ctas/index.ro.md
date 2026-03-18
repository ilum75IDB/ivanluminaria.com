---
title: "CTAS"
description: "Create Table As Select — tehnică Oracle pentru crearea unei tabele noi populate cu rezultatele unei interogări, folosită pentru migrări și restructurări ale tabelelor mari."
translationKey: "glossary_ctas"
aka: "Create Table As Select"
articles:
  - "/posts/oracle/oracle-partitioning"
---

**CTAS** (Create Table As Select) este o comandă SQL Oracle care creează o tabelă nouă și o populează într-o singură operație cu rezultatele unui SELECT. Este tehnica standard pentru migrarea datelor de la o structură la alta pe tabele de dimensiuni mari.

## Cum funcționează

Comanda combină DDL și DML: creează tabela cu structura derivată din SELECT și inserează datele într-un singur pas. Cu hint-ul `PARALLEL` și modul `NOLOGGING`, copierea a sute de GB se poate completa în câteva ore. După copiere, tabela originală se redenumește, cea nouă îi ia locul, iar downtime-ul se limitează la cele câteva secunde ale redenumirii.

## La ce folosește

CTAS este esențial când trebuie restructurată o tabelă fără a putea folosi `ALTER TABLE` direct — de exemplu, adăugarea partitioning-ului la o tabelă existentă cu miliarde de rânduri. Permite lucrul pe noua structură în timp ce sistemul este activ pe cea veche.

## Când se folosește

Se folosește pentru migrări la tabele partiționale, reorganizarea datelor fragmentate și crearea de copii ale tabelelor cu structuri diferite. În producție, trebuie combinat întotdeauna cu `NOLOGGING` (pentru reducerea redo log-urilor) și urmat de un backup RMAN imediat.
