---
title: "Listing"
description: "Codul sursă complet al unui program, tipărit sau afișat linie cu linie. În calculatoarele home din anii '80 era publicat în reviste pentru a fi copiat manual."
translationKey: "glossary_listato"
aka: "listing de program, source listing"
articles:
  - "/posts/project-management/il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire"
---

Un **listing** este reprezentarea textuală completă a codului sursă al unui program, prezentată linie cu linie în ordinea în care interpretorul sau compilatorul o procesează. Termenul era curent în informatica anilor '70–'80, când tipărirea sau publicarea codului reprezenta singurul mecanism de distribuție în masă disponibil.

## Cum funcționează

Pe calculatoarele home pe 8 biți (Commodore 64, ZX Spectrum, MSX), listing-ul era de obicei un program BASIC numerotat pe linii:

```basic
10 PRINT "SALUT LUME"
20 GOTO 10
```

Reviste precum *Tehnium* sau publicații internaționale de profil tipăreau listing-uri de zeci de pagini. Cititorul le introducea manual de la tastatură, linie cu linie. Un singur caracter greșit putea face programul nefuncțional sau putea produce comportamente imprevizibile — fără copy-paste, fără diff și fără version control care să ajute la localizarea erorii.

## Context operațional

Listing-ul ca mecanism de distribuție a software-ului este relevant din punct de vedere istoric pentru a înțelege cultura de debugging a epocii. Erorile se căutau comparând vizual textul introdus cu cel tipărit, linie cu linie, cu atenție la detaliul sintactic. Această disciplină anticipează competențe considerate fundamentale astăzi: revizuirea scripturilor de migrare SQL, auditarea fișierelor de configurare sau urmărirea logicii în proceduri stocate.

În uzul tehnic modern, termenul supraviețuiește în funcțiile de export "Listing" din unele IDE-uri și informal pentru a descrie dump-uri complete de schemă (de exemplu, ieșirea comenzii `pg_dump` ca "listing" al unei scheme PostgreSQL).
