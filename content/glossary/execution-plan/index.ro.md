---
title: "Execution Plan (Plan de Executie)"
description: "Ce este un plan de executie si cum optimizatorul bazei de date decide strategia pentru executarea unei interogari."
translationKey: "glossary_execution_plan"
tags: ["glosar"]
---

Planul de executie este secventa de operatii pe care baza de date o alege pentru a rezolva o interogare SQL. Cand scrii un SELECT cu JOIN-uri, filtre WHERE si sortari, optimizatorul evalueaza zeci de strategii posibile — ce index sa foloseasca, ce tip de join, in ce ordine sa citeasca tabelele — si alege una pe baza statisticilor disponibile.

In PostgreSQL se vizualizeaza cu `EXPLAIN` (doar planul estimat) sau `EXPLAIN ANALYZE` (plan real cu timpii efectivi). Planul este reprezentat ca un arbore de noduri: fiecare nod este o operatie (scan, join, sort, aggregate) care primeste date de la nodurile copil si le transmite nodului parinte.

Citirea corecta a unui plan de executie este cea mai importanta competenta pentru optimizarea interogarilor. Nu este suficient sa te uiti la timpul total: trebuie sa compari randurile estimate cu cele reale nod cu nod, sa verifici bufferele de I/O si sa identifici unde optimizatorul a facut alegeri gresite.

## Articole corelate

- [EXPLAIN ANALYZE nu este suficient: cum sa citesti cu adevarat un plan de executie PostgreSQL](/ro/posts/postgresql/explain-analyze-postgresql/)
