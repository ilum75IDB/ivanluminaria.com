---
title: "Listato"
description: "Testo completo del codice sorgente stampato riga per riga. Nei home computer degli anni '80 veniva pubblicato su riviste per essere ricopiato manualmente."
translationKey: "glossary_listato"
aka: "listato di programma, source listing"
articles:
  - "/posts/project-management/il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire"
---

Un **listato** è la rappresentazione testuale completa del codice sorgente di un programma, presentata riga per riga nell'ordine in cui l'interprete o il compilatore la elabora. Il termine era corrente nell'informatica degli anni '70 e '80, quando stampare o pubblicare il codice era l'unico modo per distribuirlo su larga scala.

## Come funziona

Nei home computer dell'era 8-bit (Commodore 64, ZX Spectrum, MSX), il listato coincideva spesso con il programma BASIC numerato per righe:

```basic
10 PRINT "CIAO MONDO"
20 GOTO 10
```

Riviste come *Commodore Computer Club* o *MC Microcomputer* pubblicavano listati anche di decine di pagine. Il lettore li ricopiava manualmente sulla tastiera, riga per riga, e il programma prendeva vita solo dopo l'immissione completa e corretta. Un singolo carattere sbagliato poteva rendere il programma non funzionante o produrre comportamenti imprevedibili.

## Contesto operativo

Il listato come strumento di distribuzione del software è storicamente rilevante per capire la cultura del debugging dell'epoca: senza diff, senza version control, senza copia-incolla, l'errore si cercava a occhio confrontando il proprio testo con quello stampato. Questa pratica ha plasmato un approccio alla lettura del codice — riga per riga, con attenzione al dettaglio sintattico — che anticipa competenze oggi considerate fondamentali per chiunque lavori con SQL, script di migrazione o configuration file complessi.

Nel gergo tecnico moderno il termine sopravvive in contesti di stampa o esportazione del codice sorgente (`LISTING` in alcuni ambienti IDE, `pg_dump` come "listato" dello schema in ambito PostgreSQL).
