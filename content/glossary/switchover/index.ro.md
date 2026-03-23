---
title: "Switchover"
description: "Operatiune planificata in Data Guard care inverseaza rolurile intre primary si standby fara pierdere de date, reversibila si controlata."
translationKey: "glossary_switchover"
articles:
  - "/posts/oracle/oracle-cloud-migration"
---

**Switchover-ul** este o operatiune planificata in Oracle Data Guard care inverseaza rolurile intre baza de date primary si standby. Primary-ul devine standby, standby-ul devine primary. Nicio data nu se pierde, nicio tranzactie nu esueaza — este o tranzitie curata si controlata.

## Switchover vs Failover

Distinctia este fundamentala:

| | Switchover | Failover |
|---|---|---|
| **Cand** | Planificat (mentenanta, migrare) | Urgenta (defectiune a primary-ului) |
| **Pierdere de date** | Zero | Posibila (depinde de mod) |
| **Reversibilitate** | Da, cu un alt switchover | Nu, standby-ul devine primary permanent |
| **Timp** | Minute (de obicei 1-3) | Secunde pana la minute |

## Cum se executa

Cu Data Guard Broker, switchover-ul este o singura comanda:

    DGMGRL> SWITCHOVER TO standby_db;

Broker-ul gestioneaza automat secventa: oprirea redo transport, aplicarea ultimelor redo pe standby, inversarea rolurilor, repornirea redo transport in directia opusa.

## Utilizare in migrari

Switchover-ul este strategia preferata pentru migrarile Oracle cross-site. Se configureaza Data Guard intre mediul sursa si cel de destinatie, se lasa sa se sincronizeze, iar la momentul cutover-ului se executa switchover-ul. Daca ceva nu merge bine pe noua infrastructura, un al doilea switchover readuce totul la punctul de plecare — o plasa de siguranta pe care Data Pump nu o poate oferi.
