---
title: "Call Detail Record (CDR)"
description: "Înregistrare care documentează un singur apel telefonic: client, dată, durată, tip și cost. Datele operaționale primare în sistemele telco."
translationKey: "glossary_call_detail_record"
aka: "CDR, Call Data Record"
articles:
  - "/posts/data-warehouse/la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto"
---

Un Call Detail Record (CDR) este urma persistentă pe care un sistem de telefonie o generează la sfârșitul fiecărui apel. Conține informațiile minime necesare pentru facturarea serviciului și analiza traficului: cine a sunat, când, cât timp, prin ce tip de conexiune și la ce cost. În sistemele telco reprezintă datele operaționale de referință — echivalentul unui rând de tranzacție dintr-un sistem bancar.

## Structură tipică

Un CDR include cel puțin următoarele câmpuri:

| Câmp | Descriere |
|---|---|
| `caller_id` | Identificatorul clientului apelant |
| `callee_id` | Numărul sau identificatorul destinatarului |
| `start_time` | Timestamp-ul de început al apelului |
| `duration_sec` | Durata în secunde |
| `call_type` | Voce, SMS, date, roaming |
| `cost` | Costul calculat la sfârșitul apelului |

Structura variază între operatori și standarde (3GPP, IPDR), dar aceste câmpuri sunt aproape universale.

## Context operațional

CDR-urile se acumulează rapid: un operator de dimensiuni medii generează sute de GB pe lună. Acest lucru le face un caz de utilizare clasic pentru Data Warehouse-urile telco, unde sunt încărcate în batch sau prin streaming și apoi agregate pentru facturare, analiza traficului și detectarea fraudelor. Interogările analitice tipice — suma duratei per client, distribuția pe interval orar, comparație lună la lună — beneficiază de tehnici precum Materialized Views pentru a evita recalculele costisitoare pe tabele cu miliarde de rânduri.

## Considerații privind volumul

Un singur CDR ocupă câțiva bytes, dar cardinalitatea este foarte ridicată. Proiectarea schemei de stocare — partiționare pe dată, compresie columnară, indecși parțiali — este critică încă din faza de modelare, înainte de a defini tiparele de interogare.
