---
title: "REM"
description: "Instrucțiune BASIC care introduce un comentariu în codul sursă: linia este ignorată de interpret și servește exclusiv la documentarea programului."
translationKey: "glossary_rem"
aka: "REMark"
articles:
  - "/posts/project-management/il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire"
---

`REM` este o instrucțiune a limbajului BASIC — prescurtare de la **REMark** — care marchează o linie drept comentariu în codul sursă. Interpretorul sare complet peste acea linie: nu produce niciun rezultat, nu execută calcule și nu modifică variabile. Scopul său unic este să transmită intenții celui care citește listingul.

## Cum funcționează

Când interpretorul BASIC întâlnește `REM`, avansează la următoarea linie numerotată și continuă execuția de acolo. În majoritatea dialectelor (Commodore BASIC, GW-BASIC, QBasic), numărul de linie precede instrucțiunea:

```basic
10 REM Program de calcul TVA
20 LET COTA = 0.19
30 REM Introduceti pretul net
40 INPUT PRET
50 LET TVA = PRET * COTA
60 PRINT "TVA: "; TVA
```

Unele dialecte acceptă și apostroful (`'`) ca sinonim pentru `REM`, cu un comportament identic la execuție.

## Când contează

`REM` era adesea singurul mecanism disponibil pentru a lăsa o explicație lizibilă în interiorul unui program, într-o epocă fără IDE-uri, unelte de diff sau sisteme de versionare. Un listing fără instrucțiuni `REM` putea deveni de neînțeles chiar și pentru autorul său, la câteva săptămâni după ce îl scrisese.

Astăzi `REM` este în primul rând o referință istorică și culturală: marchează punctul de plecare al documentării inline a codului, practică ce a evoluat în limbajele moderne spre docstring-uri, adnotări și formate de comentariu structurate.
