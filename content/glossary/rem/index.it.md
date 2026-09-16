---
title: "REM"
description: "Istruzione BASIC che introduce un commento nel codice: la riga viene ignorata dall'interprete e serve a documentare il programma."
translationKey: "glossary_rem"
aka: "REMark"
articles:
  - "/posts/project-management/il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire"
---

`REM` è un'istruzione del linguaggio BASIC — abbreviazione di **REMark** — che introduce un commento nel codice sorgente. La riga che inizia con `REM` viene completamente ignorata dall'interprete: non produce output, non esegue calcoli, non modifica variabili. Esiste esclusivamente per chi legge il listato.

## Come funziona

L'interprete BASIC, quando incontra `REM`, salta l'intera riga e passa alla successiva. In molti dialetti (Commodore BASIC, GW-BASIC, QBasic) il numero di riga precede l'istruzione:

```basic
10 REM Programma di calcolo IVA
20 LET ALIQUOTA = 0.22
30 REM Inserire il prezzo netto
40 INPUT PREZZO
50 LET IVA = PREZZO * ALIQUOTA
60 PRINT "IVA: "; IVA
```

In alcuni dialetti è ammessa anche la forma abbreviata con l'apostrofo (`'`), che si comporta in modo identico a `REM`.

## Quando si usa

`REM` era lo strumento principale — spesso l'unico — per lasciare traccia delle intenzioni del programmatore in un'epoca in cui non esistevano IDE, diff tool o sistemi di versionamento. Un listato senza `REM` poteva diventare illeggibile anche per chi lo aveva scritto poche settimane prima.

Oggi `REM` è rilevante soprattutto come riferimento storico e culturale: rappresenta il punto di partenza della pratica di documentare il codice inline, pratica che nei linguaggi moderni si è evoluta in docstring, annotation e commenti strutturati.
