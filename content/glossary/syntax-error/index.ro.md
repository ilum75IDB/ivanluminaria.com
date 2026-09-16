---
title: "?SYNTAX ERROR"
description: "Mesaj de eroare al Commodore 64 care semnalează o încălcare a regulilor sintactice BASIC, indicând linia detectată de interpretor."
translationKey: "glossary_syntax_error"
aka: "Syntax Error (Commodore BASIC)"
articles:
  - "/posts/project-management/il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire"
---

`?SYNTAX ERROR` este mesajul pe care interpretorul BASIC al Commodore 64 îl afișează atunci când o linie de cod încalcă regulile gramaticale ale limbajului. Semnul de întrebare de la început face parte din formatul standard de erori al sistemului Commodore (KERNAL + BASIC V2), nu este un element editorial.

## Cum funcționează

Interpretorul BASIC al C64 analizează codul linie cu linie, atât la execuție, cât și la introducerea instrucțiunilor în modul direct. Când întâlnește un token nerecunoscut — un cuvânt cheie scris greșit, o paranteză neînchisă, un operator plasat incorect — se oprește și afișează mesajul urmat de numărul liniei:

```
?SYNTAX ERROR IN 100
READY.
```

Numărul de linie indicat este cel în care interpretorul a *detectat* problema, nu neapărat cel în care aceasta a *apărut*. O expresie incompletă pe linia 90 se poate manifesta ca eroare pe linia 100, unde interpretorul încearcă să consume token-uri care nu mai sunt disponibile.

## Context operațional

La depanarea programelor BASIC pe C64, `?SYNTAX ERROR` este adesea un punct de plecare înșelător: linia raportată trebuie citită împreună cu liniile precedente, mai ales în prezența construcțiilor multi-token precum `IF...THEN`, `FOR...NEXT` sau lanțuri de comenzi separate prin `:`. Absența unui debugger simbolic face ca întregul proces să fie manual. Acest comportament — eroarea raportată în altă parte față de cauza sa reală — este un tipar care reapare în multe sisteme de parsare secvențială, de la compilatoare la motoare SQL, și amintește că numărul de linie raportat nu trebuie acceptat fără verificare.
