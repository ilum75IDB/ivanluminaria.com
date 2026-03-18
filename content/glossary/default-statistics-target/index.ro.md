---
title: "default_statistics_target"
description: "Parametrul PostgreSQL care controleaza cate esantioane colecteaza optimizatorul pentru a estima distributia datelor intr-o coloana."
translationKey: "glossary_default_statistics_target"
tags: ["glosar"]
---

`default_statistics_target` este parametrul PostgreSQL care defineste numarul de esantioane colectate de comanda ANALYZE pentru a construi statisticile fiecarei coloane. Valoarea implicita este 100, ceea ce inseamna ca PostgreSQL esantioneaza 100 de valori pentru a construi histograme si liste de valori frecvente.

Pentru tabele mici sau cu distributie uniforma, 100 de esantioane sunt suficiente. Pentru tabele mari cu distributie asimetrica (skewed) — unde putine valori domina majoritatea randurilor — 100 de esantioane pot da o reprezentare distorsionata, ducand optimizatorul la estimari de cardinalitate gresite.

Se poate creste target-ul la nivel de coloana individuala cu `ALTER TABLE ... ALTER COLUMN ... SET STATISTICS N`. Valori intre 500 si 1000 imbunatatesc semnificativ calitatea estimarilor pe coloane cu distributie neuniforma. Peste 1000 beneficiul este marginal si ANALYZE-ul insusi devine mai lent. Este o reglare fina care face diferenta in interogarile cu join-uri complexe pe tabele cu milioane de randuri.

## Articole corelate

- [EXPLAIN ANALYZE nu este suficient: cum sa citesti cu adevarat un plan de executie PostgreSQL](/ro/posts/postgresql/explain-analyze-postgresql/)
