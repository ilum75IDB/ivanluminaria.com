---
title: "RMAN"
description: "Recovery Manager — instrumentul Oracle pentru backup, restore si recovery al bazei de date, inclusiv crearea bazelor de date standby pentru Data Guard."
translationKey: "glossary_rman"
aka: "Recovery Manager"
articles:
  - "/posts/oracle/oracle-data-guard"
---

**RMAN** (Recovery Manager) este instrumentul nativ Oracle pentru backup, restore si recovery al bazei de date. Este o utilitate de linie de comanda care gestioneaza toate operatiunile de protectie a datelor in mod integrat cu baza de date.

## Ce face

- **Backup**: complet, incremental, doar archived log-uri
- **Restore**: recuperarea datafile-urilor, tablespace-urilor sau a intregii baze de date
- **Recovery**: aplicarea redo log-urilor pentru a aduce baza de date la un punct specific in timp
- **Duplicate**: crearea de copii ale bazei de date, inclusiv baze de date standby pentru Data Guard

## RMAN si Data Guard

Pentru crearea unei baze de date standby, RMAN permite `DUPLICATE ... FOR STANDBY FROM ACTIVE DATABASE` — o copie directa prin retea de la primar la standby, fara nevoia de backup-uri intermediare pe banda sau disc. Comanda transfera toate datafile-urile si controlfile-urile si le configureaza automat pentru replicare.

## De ce RMAN si nu copii manuale

RMAN cunoaste structura interna a bazei de date Oracle: stie ce blocuri s-au schimbat (pentru incrementale), ce fisiere sunt necesare, cum sa aplice redo-ul. O copie manuala a fisierelor (cu `cp` sau `rsync`) nu garanteaza consistenta si necesita ca baza de date sa fie inchisa. RMAN poate lucra cu baza de date deschisa, cu impact minim asupra performantei.
