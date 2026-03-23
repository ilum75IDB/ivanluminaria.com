---
title: "Cutover"
description: "Momentul critic intr-o migrare in care sistemul de productie este mutat definitiv de pe infrastructura veche pe cea noua."
translationKey: "glossary_cutover"
articles:
  - "/posts/oracle/oracle-cloud-migration"
---

**Cutover-ul** este momentul in care un sistem de productie este mutat de pe infrastructura veche pe cea noua. Este faza cea mai vizibila a unei migrari — cea pe care toata lumea si-o aminteste, in bine sau in rau.

## Anatomia unui cutover

Un cutover bine planificat urmeaza un runbook detaliat cu pasi numerotati, timpi estimati, criterii de succes si proceduri de rollback pentru fiecare pas. Componentele tipice:

1. **Oprirea aplicatiei** — inchiderea conexiunilor si verificarea ca nicio sesiune nu este activa
2. **Sincronizarea finala** — intr-o migrare Data Guard, verificarea ca transport lag si apply lag sunt la zero
3. **Switchover/migrare** — operatiunea tehnica care transfera serviciul
4. **Validare** — teste de conectivitate, query-uri de verificare, teste functionale
5. **Deschidere graduala** — readmiterea progresiva a utilizatorilor

## Downtime si ferestre

Downtime-ul unui cutover este timpul intre deconectarea ultimului utilizator si reconectarea primului. Cu Data Guard switchover, downtime-ul poate fi de ordinul minutelor. Cu Data Pump, poate fi de ore sau zile.

Fereastra de cutover se planifica in momentele de utilizare minima: nopti, weekenduri, sarbatori. Dar "utilizare minima" nu inseamna "utilizare zero" — in companiile de productie cu schimburi 24/7, nu exista un moment in care baza de date nu este necesara nimanui.

## Rollback

Orice cutover trebuie sa aiba un plan de rollback. Cu Data Guard, rollback-ul este un al doilea switchover — relativ simplu. Cu Data Pump, rollback-ul inseamna repornirea bazei de date originale si acceptarea pierderii tranzactiilor aparute dupa inceputul migrarii. Calitatea planului de rollback este invers proportionala cu probabilitatea de a-l folosi — dar vai de cei care nu il au.
