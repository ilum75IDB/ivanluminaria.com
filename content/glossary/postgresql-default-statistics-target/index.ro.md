---
title: "default_statistics_target"
description: "Parametrul PostgreSQL care controleaza granularitatea statisticilor colectate de ANALYZE (dimensiunea MCV si a histogramei)."
translationKey: "glossary_postgresql_default_statistics_target"
aka: "default_statistics_target (PostgreSQL)"
articles:
  - "/posts/postgresql/explain-analyze-postgresql"
---

**default_statistics_target** este parametrul PostgreSQL care controleaza **granularitatea statisticilor** pe care `ANALYZE` le construieste pentru fiecare coloana. Valoarea implicita este 100.

## Cum functioneaza

ANALYZE construieste pentru fiecare coloana doua structuri statistice folosite de optimizator:

- **Most common values (MCV)**: lista valorilor celor mai frecvente, cu frecventele respective
- **Histograma**: distributia valorilor ramase, impartita in bucket-uri de populatie egala

`default_statistics_target` determina cate elemente pot avea aceste structuri. Cu valoarea `100`: pana la 100 de valori in lista MCV si pana la 100 de bucket-uri in histograma.

**Numarul de randuri esantionate este o chestiune separata si depinde de target**: este aproximativ `300 × default_statistics_target`. Cu default-ul de 100, ANALYZE citeste ~30.000 de randuri per coloana; cu un target de 500, ~150.000. Asadar cresterea target-ului mareste atat granularitatea statisticilor **cat si** costul ANALYZE.

## Cand trebuie crescut

Pentru tabele mici sau cu distributie uniforma, 100 de esantioane sunt suficiente. Pentru tabele mari cu distributie asimetrica (skewed) — unde putine valori domina majoritatea randurilor — 100 de esantioane pot da o reprezentare distorsionata, ducand optimizatorul la estimari de cardinalitate gresite.

Se poate creste target-ul la nivel de coloana individuala:

    ALTER TABLE orders ALTER COLUMN status SET STATISTICS 500;
    ANALYZE orders;

Valori intre 500 si 1000 imbunatatesc semnificativ calitatea estimarilor pe coloane cu distributie neuniforma.

## Limite practice

Peste 1000 beneficiul este marginal si `ANALYZE`-ul insusi devine mai lent, pentru ca trebuie sa esantioneze mai multe randuri si sa construiasca structuri mai mari. Este o reglare fina: trebuie aplicata doar coloanelor care cauzeaza efectiv estimari gresite, nu tuturor coloanelor din toate tabelele.
