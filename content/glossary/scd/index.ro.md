---
title: "SCD"
description: "Slowly Changing Dimension — tehnica de data warehouse pentru urmarirea modificarilor in timp in tabelele dimensionale."
translationKey: "glossary_scd"
aka: "Slowly Changing Dimension"
articles:
  - "/posts/data-warehouse/scd-tipo-2"
---

**SCD** (Slowly Changing Dimension) se refera la un set de tehnici folosite in data warehouse pentru gestionarea modificarilor in datele tabelelor dimensionale de-a lungul timpului.

## Tipurile principale

- **Tipul 1**: suprascrierea valorii anterioare. Nicio istorie conservata
- **Tipul 2**: inserarea unui rand nou cu date de valabilitate (data inceput, data sfarsit). Conserva toata istoria
- **Tipul 3**: adaugarea unei coloane pentru valoarea anterioara. Conserva doar ultima modificare

## De ce conteaza

Intr-o baza de date tranzactionala, cand un client isi schimba adresa se actualizeaza inregistrarea. Intr-un data warehouse acest lucru ar insemna pierderea istoriei: toate vanzarile anterioare ar aparea asociate noii adrese.

SCD Tipul 2 rezolva aceasta problema mentinand un rand pentru fiecare versiune a datelor, cu date de valabilitate care permit reconstructia situatiei in orice moment in timp.

## Cand se foloseste

Alegerea tipului depinde de cerinta de business. Daca conteaza doar valoarea curenta, Tipul 1 este suficient. Daca business-ul are nevoie de analize istorice precise — si in majoritatea data warehouse-urilor reale asa este — Tipul 2 este alegerea standard.
