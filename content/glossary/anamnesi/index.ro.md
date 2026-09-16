---
title: "Anamneză"
description: "Colectare sistematică a simptomelor, evenimentelor recente și configurației unui sistem, ca punct de plecare pentru diagnosticarea unei probleme tehnice."
translationKey: "glossary_anamnesi"
aka: "Colectarea istoricului sistemului"
articles:
  - "/posts/project-management/il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire"
---

În medicină, anamneza reprezintă colectarea structurată a istoricului clinic al pacientului înainte de formularea oricărui diagnostic. Aplicat sistemelor informatice, termenul descrie același proces îndreptat către mașini, baze de date și aplicații: colectarea sistematică a simptomelor observate, a modificărilor recente, a detaliilor de configurație și a contextului operațional, înainte de a formula orice ipoteză despre cauza rădăcină.

## Cum funcționează

O anamneză tehnică urmează o serie de întrebări precise și secvențiale:

- **Ce s-a schimbat recent?** Deploy-uri, actualizări de pachete, modificări ale parametrilor de configurație, ferestre de mentenanță.
- **Când a apărut simptomul pentru prima dată?** Timestamp-uri exacte, corelație cu evenimente programate (backup-uri, procese batch, vârfuri de încărcare).
- **Cine a avut acces și ce a făcut?** Log-uri de acces, istoricul comenzilor, tickete deschise în orele anterioare incidentului.
- **Care este configurația actuală?** Versiunea software-ului, resursele hardware, topologia rețelei, dependențele externe.

Abia după colectarea acestor informații are sens să se formuleze ipoteze de diagnostic. Omiterea acestui pas duce aproape întotdeauna la urmărirea unor cauze greșite.

## Când se folosește

Anamneza este primul pas ori de câte ori o problemă nu este imediat reproductibilă sau cauza sa nu este evidentă: încetiniri bruște, erori intermitente, comportamente anormale după o actualizare. Este deosebit de critică în mediile de producție, unde timpul de diagnosticare are un cost direct, și în sistemele legacy unde documentația este redusă, iar cunoștințele istorice sunt distribuite între mai multe persoane.

O anamneză bine realizată reduce riscul de a aplica remedieri care rezolvă simptomul fără a atinge cauza rădăcină.
