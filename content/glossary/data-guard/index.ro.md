---
title: "Data Guard"
description: "Tehnologie Oracle pentru replicarea in timp real a unei baze de date pe un server standby, asigurand disponibilitate ridicata si disaster recovery."
translationKey: "glossary_data_guard"
aka: "Oracle Active Data Guard"
articles:
  - "/posts/oracle/oracle-data-guard"
---

**Data Guard** este tehnologia Oracle care mentine una sau mai multe copii sincronizate (standby) ale unei baze de date de productie (primar). Standby-ul primeste si aplica continuu redo log-urile generate de primar, ramanand aliniat in timp real sau aproape.

## Cum functioneaza

Primarul genereaza redo log-uri cu fiecare tranzactie. Aceste log-uri sunt transmise standby-ului prin retea, unde sunt aplicate in doua moduri posibile:

- **Physical standby**: aplica redo-ul la nivel de bloc (replica exacta, byte cu byte)
- **Logical standby**: reconstruieste instructiunile SQL din redo si le reexecuta

In caz de defectiune a primarului, standby-ul poate deveni noul primar prin **switchover** (planificat) sau **failover** (de urgenta).

## Active Data Guard

Varianta Active Data Guard permite deschiderea standby-ului in mod read-only in timp ce continua sa aplice redo-ul. Acest lucru permite folosirea sa pentru rapoarte, backup-uri si query-uri analitice, usurind sarcina primarului.

## Moduri de protectie

| Mod | Comportament | Pierdere de date |
|-----|-------------|-----------------|
| MaxPerformance | Replicare asincrona, fara impact asupra performantei primarului | Posibila (cateva secunde) |
| MaxAvailability | Replicare sincrona, degradeaza la MaxPerformance daca standby-ul nu e accesibil | Zero in conditii normale |
| MaxProtection | Replicare sincrona, primarul se opreste daca standby-ul nu confirma | Zero garantat |
