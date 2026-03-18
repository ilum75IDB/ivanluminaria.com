---
title: "NOLOGGING"
description: "Mod Oracle care suprimă generarea de redo log în timpul operațiunilor masive (CTAS, INSERT APPEND, ALTER TABLE MOVE), accelerând operațiunile dar necesitând un backup imediat."
translationKey: "glossary_nologging"
articles:
  - "/posts/oracle/oracle-partitioning"
---

**NOLOGGING** este un mod Oracle care dezactivează generarea de redo log în timpul operațiunilor de încărcare masivă. Operațiunile se completează mult mai rapid, dar datele nu sunt recuperabile prin redo în caz de crash înainte de un backup.

## Cum funcționează

Când un segment (tabelă, index, partiție) este în mod NOLOGGING, operațiunile masive precum CTAS, `INSERT /*+ APPEND */` și `ALTER TABLE MOVE` nu scriu redo log pentru blocurile de date. Pe o copie de 380 GB, acest lucru elimină generarea aceleiași cantități de redo, prevenind saturarea zonei de archivelog și reducând timpii de la zile la ore.

## La ce folosește

NOLOGGING este esențial pentru operațiunile de migrare pe tabele de dimensiuni mari. Fără NOLOGGING, un CTAS de 380 GB ar genera 380 GB de redo log, punând sistemul în mod archivelog timp de zile. Cu NOLOGGING, aceeași operație se completează în câteva ore cu impact minim asupra sistemului.

## Când se folosește

Se activează înainte de operațiunea masivă și se dezactivează imediat după (`ALTER TABLE ... LOGGING`). Este obligatoriu să se execute un backup RMAN imediat după, deoarece segmentele NOLOGGING nu sunt recuperabile cu un restore din redo. Niciodată nu se lasă NOLOGGING activ permanent pe tabele de producție.
