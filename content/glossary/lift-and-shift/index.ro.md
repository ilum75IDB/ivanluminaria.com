---
title: "Lift-and-Shift"
description: "Strategie de migrare cloud care transferă sisteme fără a modifica arhitectura sau codul, amânând orice optimizare pentru faza post-migrare."
translationKey: "glossary_lift_and_shift"
aka: "Migrare rehost"
articles:
  - "/posts/oracle/latenza-wan-e-change-control-gxp-il-costo-reale-del-lift-and-shift"
---

Lift-and-shift este o abordare de migrare cloud care replică mediul sursă — servere, baze de date, aplicații — pe platforma țintă fără a modifica arhitectura, configurația sau codul. Obiectivul principal este reducerea perimetrului de validare și comprimarea timpului până la go-live, acceptând în mod deliberat că sistemul migrat nu va fi optimizat pentru noul său context.

## Cum funcționează

Sistemul sursă este reprodus 1:1 pe platforma țintă: VM-urile sunt convertite sau recreate cu aceleași specificații, bazele de date sunt migrate prin backup/restore sau instrumente de replicare fără refactorizarea schemei, iar dependențele de rețea sunt reconstruite fidel. În medii reglementate (GxP, SOX, PCI-DSS), această abordare limitează delta de validare deoarece comportamentul aplicației rămâne nominal nemodificat.

## Când se utilizează

Lift-and-shift este alegerea predominantă atunci când:

- termenele de migrare sunt constrânse de scadențe contractuale sau de licențiere
- sistemul este legacy și nu există expertiză internă pentru un refactoring sigur
- domeniul de validare IQ/OQ/PQ trebuie menținut restrâns din motive de buget sau calendar

Limitarea principală este structurală: costurile operaționale cloud (compute, stocare, rețea) rămân ridicate deoarece sistemul nu valorifică elasticitatea, managed services sau arhitecturile cloud-native. Latența WAN și constrângerile de change control în mediile GxP pot amplifica semnificativ aceste costuri, așa cum este analizat în articolul asociat.
