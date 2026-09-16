---
title: "?SYNTAX ERROR"
description: "Messaggio di errore del Commodore 64 che segnala una violazione sintattica del BASIC, indicando la riga rilevata dall'interprete."
translationKey: "glossary_syntax_error"
aka: "Syntax Error (Commodore BASIC)"
articles:
  - "/posts/project-management/il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire"
---

`?SYNTAX ERROR` è il messaggio con cui l'interprete BASIC del Commodore 64 comunica che una riga di codice viola le regole grammaticali del linguaggio. Il punto interrogativo iniziale è parte integrante del formato di errore del sistema operativo Commodore (KERNAL + BASIC V2), non un'aggiunta editoriale.

## Come funziona

L'interprete BASIC del C64 analizza il codice riga per riga al momento dell'esecuzione (o dell'inserimento in modalità diretta). Quando incontra un token non riconoscibile — una parola chiave mal scritta, una parentesi non bilanciata, un operatore fuori posto — si ferma e stampa il messaggio seguito dal numero di riga incriminata:

```
?SYNTAX ERROR IN 100
READY.
```

Il numero di riga indicato è quello in cui l'interprete ha *rilevato* il problema, non necessariamente quello in cui il problema ha *origine*. Un'espressione incompleta nella riga 90 può manifestarsi come errore alla riga 100, dove l'interprete tenta di consumare token che non trova.

## Contesto operativo

Nel debug di programmi BASIC su C64, `?SYNTAX ERROR` è spesso un punto di partenza fuorviante: la riga segnalata va letta insieme alle righe precedenti, specialmente in presenza di istruzioni multi-token come `IF...THEN`, `FOR...NEXT` o concatenazioni di comandi separati da `:`. L'assenza di un debugger simbolico rende il processo interamente manuale. Questo comportamento — l'errore segnalato altrove rispetto alla causa — è un pattern che ritorna in molti sistemi di parsing sequenziale, dai compilatori ai motori SQL, e insegna a non fidarsi ciecamente del numero di riga riportato.
