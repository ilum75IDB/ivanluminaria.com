---
title: "BASIC"
description: "BASIC è un linguaggio di programmazione interpretato degli anni '80, progettato per home computer con righe numerate e sintassi leggibile anche da non specialisti."
translationKey: "glossary_basic"
aka: "Beginner's All-purpose Symbolic Instruction Code"
articles:
  - "/posts/project-management/il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire"
---

BASIC (Beginner's All-purpose Symbolic Instruction Code) è un linguaggio di programmazione nato nel 1964 al Dartmouth College e diventato il linguaggio dominante degli home computer degli anni '80. Su macchine come il Commodore 64, lo ZX Spectrum o l'Apple II, BASIC era spesso l'unico ambiente di sviluppo disponibile all'avvio.

## Come funziona

I programmi BASIC sono sequenze di righe numerate, eseguite in ordine crescente dall'interprete. Il numero di riga serve anche come destinazione per i salti condizionali (`GOTO`) e le chiamate a subroutine (`GOSUB`).

```basic
10 PRINT "Inserisci un numero: "
20 INPUT N
30 IF N > 10 THEN GOTO 60
40 PRINT "Numero piccolo"
50 GOTO 70
60 PRINT "Numero grande"
70 END
```

L'interprete legge ed esegue ogni riga al momento dell'esecuzione, senza una fase di compilazione separata. Questo rende il ciclo modifica-esegui immediato, ma penalizza le prestazioni rispetto ai linguaggi compilati.

## Contesto operativo

BASIC era pensato per utenti non specialisti: studenti, appassionati, professionisti che volevano automatizzare calcoli senza formarsi come programmatori. La semplicità della sintassi aveva un costo preciso — la mancanza di strutture dati complesse, la gestione manuale della memoria tramite `PEEK` e `POKE`, e la dipendenza dal `GOTO` che rendeva difficile la manutenzione di programmi oltre le poche centinaia di righe.

Nei contesti aziendali degli anni '80, BASIC veniva usato per gestionali elementari, fogli di calcolo rudimentali e automazione di report su minicomputer. Oggi sopravvive in ambienti embedded e in dialetti moderni come FreeBASIC o QB64, ma il suo ruolo storico più rilevante è aver avvicinato una generazione intera al concetto di programmazione come strumento di lavoro quotidiano.
