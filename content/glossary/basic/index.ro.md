---
title: "BASIC"
description: "BASIC este un limbaj de programare interpretat din anii '80, conceput pentru calculatoare personale cu linii numerotate și sintaxă lizibilă pentru utilizatori fără pregătire specializată."
translationKey: "glossary_basic"
aka: "Beginner's All-purpose Symbolic Instruction Code"
articles:
  - "/posts/project-management/il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire"
---

BASIC (Beginner's All-purpose Symbolic Instruction Code) este un limbaj de programare creat în 1964 la Dartmouth College, devenit limbajul dominant pe calculatoarele personale din anii '80. Pe mașini precum Commodore 64, ZX Spectrum sau Apple II, BASIC era adesea singurul mediu de dezvoltare disponibil la pornirea sistemului.

## Cum funcționează

Programele BASIC sunt secvențe de linii numerotate, executate în ordine crescătoare de către interpretor. Numărul de linie servește și ca destinație pentru salturile condiționale (`GOTO`) și apelurile de subrutine (`GOSUB`).

```basic
10 PRINT "Introdu un număr: "
20 INPUT N
30 IF N > 10 THEN GOTO 60
40 PRINT "Număr mic"
50 GOTO 70
60 PRINT "Număr mare"
70 END
```

Interpretorul citește și execută fiecare linie la momentul rulării, fără o etapă separată de compilare. Aceasta face ca ciclul editare-execuție să fie imediat, dar performanța este inferioară față de limbajele compilate.

## Context operațional

BASIC a fost conceput pentru utilizatori fără pregătire specializată: studenți, pasionați și profesioniști care doreau să automatizeze calcule fără o formare formală în programare. Simplitatea sintaxei avea un cost precis — lipsa structurilor de date complexe, gestionarea manuală a memoriei prin `PEEK` și `POKE`, și dependența de `GOTO` care îngreuna întreținerea programelor de peste câteva sute de linii.

În mediile de afaceri ale anilor '80, BASIC era folosit pentru software de gestiune elementar, foi de calcul rudimentare și automatizarea rapoartelor pe minicalculatoare. Astăzi supraviețuiește în medii embedded și în dialecte moderne precum FreeBASIC sau QB64, dar rolul său istoric cel mai semnificativ a fost acela de a apropia o întreagă generație de conceptul de programare ca instrument de lucru zilnic.
