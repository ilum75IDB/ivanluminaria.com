---
title: "ANALYZE"
description: "Comanda PostgreSQL care actualizeaza statisticile tabelelor folosite de optimizator pentru a alege planul de executie."
translationKey: "glossary_analyze"
tags: ["glosar"]
---

`ANALYZE` este comanda PostgreSQL care colecteaza statistici despre distributia datelor in tabele si le stocheaza in catalogul `pg_statistic` (citibil prin vizualizarea `pg_stats`). Optimizatorul foloseste aceste statistici pentru a estima cardinalitatea — cate randuri va returna fiecare operatie — si a alege cel mai eficient plan de executie.

Statisticile colectate includ: valorile cele mai frecvente (most common values), histograme de distributie, numarul de valori distincte si procentul de NULL pentru fiecare coloana. Fara statistici actualizate, optimizatorul este fortat sa ghiceasca, iar estimarile gresite duc la planuri de executie dezastruoase — cum ar fi alegerea unui nested loop pe milioane de randuri crezand ca sunt sute.

PostgreSQL executa ANALYZE automat prin autovacuum, dar pragul implicit (50 de randuri + 10% din randurile vii) poate fi prea mare pentru tabelele care cresc rapid. Dupa importuri masive sau schimbari semnificative in distributia datelor, un ANALYZE manual este prima actiune de diagnostic de efectuat.

## Articole corelate

- [EXPLAIN ANALYZE nu este suficient: cum sa citesti cu adevarat un plan de executie PostgreSQL](/ro/posts/postgresql/explain-analyze-postgresql/)
