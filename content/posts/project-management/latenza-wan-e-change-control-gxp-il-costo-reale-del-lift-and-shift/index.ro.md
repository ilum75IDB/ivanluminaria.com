---
categories:
- project-management
date: '2026-11-10'
description: Migrezi baza de date în cloud și optimizezi după pare rezonabil. Într-un
  sistem GxP, orice modificare post go-live deschide un ciclu de revalidare. Iată
  de ce.
draft: false
image: latenza-wan-e-change-control-gxp-il-costo-reale-del-lift-and-shift.cover.jpg
seoTitle: 'Lift-and-shift și sisteme validate: costul real al fazei a doua'
tags:
- cloud-migration
- database
- gxp-compliance
- change-control
- oracle
- lift-and-shift
title: 'Lift-and-shift acum, optimizăm după: cât costă «după» într-un sistem validat'
translationKey: latenza_wan_e_change_control_gxp_il_costo_reale_del_lift_and_shift
webo_generated_at: 2026-10-21
webo_status: scheduled
---

*De ce în migrarea cloud faza cea mai ieftină pentru a regândi baza de date este cea dinainte de mutare — și ce se întâmplă când, după go-live, orice modificare trebuie să treacă prin change control GxP.*

---

## Cazul de business era corect

Documentul aprobat de comitetul de investiții era bine construit. O companie farmaceutică de dimensiuni medii, trei unități de producție, un data center propriu cu contractul de hosting pe cale să expire și un parc de servere ajuns la sfârșitul suportului. În centru, o bază de date Oracle de aproximativ 6 TB pe care rulează sistemul de management al calității, LIMS-ul laboratoarelor de control și raportarea eliberării loturilor. Planul era clar: mutarea totul pe infrastructură cloud în nouă luni, *lift-and-shift*, aceeași versiune, aceeași arhitectură aplicativă, nicio rescriere. Optimizarea și modernizarea într-o a doua fază, deja prevăzută în buget pentru anul următor.

Alegerea avea o logică solidă, iar cei care au luat-o nu au greșit calculele pe care le aveau în față. Contractul data center-ului impunea termenul. Rescrierea aplicativă ar fi necesitat o nouă validare completă a sistemelor, cu termene incompatibile cu scadența. *«Mai întâi ieșim din data center, apoi optimizăm în liniște»* era, la acea masă, fraza cea mai rezonabilă posibilă.

Go-live-ul a venit la timp. Sistemul funcționa. După șase săptămâni, directorul de Calitate a întrebat de ce raportul de eliberare a loturilor, care înainte rula în trei minute, acum dura unsprezece.

## Unsprezece minute, și de unde vin

Răspunsul nu era în baza de date. Serverele aplicative ale LIMS-ului rămăseseră într-una din unități — conectate la instrumente de laborator care nu puteau fi mutate — în timp ce baza de date mersese în cloud. O alegere sensibilă pe hârtie: aplicația rămânea aproape de instrumente, baza de date mergea acolo unde costa mai puțin să fie gestionată.

Raportul de eliberare, scris cu cincisprezece ani în urmă pentru o LAN, nu executa o singură interogare: executa sute de mii, câte una pentru fiecare rând de rezultat analitic, într-un ciclu aplicativ. În AWR semnătura este inconfundabilă: statistica *SQL\*Net roundtrips to/from client* extrem de ridicată față de *user calls* utile, iar timpul dominat de evenimentul *SQL\*Net message from client* — baza de date stând să aștepte clientul.

Calculele, odată puse în ordine, sunt simple:

- aproximativ **180.000 round-trip-uri** per execuție a raportului;
- în LAN, latență de aproximativ **0,3 ms** per round-trip → 54 de secunde de rețea din trei minute totale;
- între unitate și region-ul cloud, aproximativ **3 ms** → 540 de secunde doar de rețea, nouă minute;
- restul muncii (aproximativ două minute) identic înainte și după.

Trei minute devin unsprezece fără ca o singură interogare să se fi înrăutățit. Baza de date, în cloud, era chiar mai rapidă. *(Numere reprezentative pentru contexte similare — DE VERIFICAT înainte de publicare: latența efectivă unitate-region și numărul de round-trip-uri trebuie calibrate pe un caz documentabil.)*

Între timp factura lunară ajunsese cu 35% peste cazul de business. Instanțele fuseseră dimensionate pe vârful istoric on-premises, cu marjă, pentru că nimeni nu voia să riște performanța într-un sistem validat; storage-ul fusese ales pe tier-ul care garanta IOPS-urile vechiului array; backup-urile fuseseră replicate cu aceeași politică de retenție ca înainte, acum plătită pe gigabyte. *(Procentaj DE VERIFICAT.)*

## De ce «după» costă mai mult decât «înainte»

Până aici este o poveste pe care oricine a făcut o migrare cloud o recunoaște: o aplicație *chatty*, o latență care înainte era invizibilă, un dimensionament prudent. Partea specifică sectorului farmaceutic apare când se deschide faza a doua.

Baza de date și LIMS-ul sunt **sisteme computerizate validate**: susțin decizii GxP și intră sub incidența EU GMP Annex 11 și, pentru produsele destinate pieței americane, sub 21 CFR Part 11. Orice modificare a unui sistem validat trece prin change control, evaluarea riscului, teste documentate, aprobarea Calității. Rescrierea ciclului raportului într-o interogare set-based, mutarea calculului pe partea bazei de date, revizuirea dimensionării instanțelor: fiecare dintre aceste modificări, pe un sistem în producție, deschide un ciclu de revalidare.

Înainte de migrare, aceleași modificări ar fi călătorit **în interiorul** validării migrării în sine — care trebuia făcută oricum. Pachetul de teste, protocolul, semnăturile: totul era deja prevăzut și plătit. După go-live, fiecare intervenție devine un proiect de sine stătător, cu protocolul său, semnăturile sale, fereastra de oprire convenită cu producția.

Acesta este punctul pe care cazul de business nu îl putea vedea. **Faza a doua era în buget ca muncă tehnică. În realitate este muncă de validare**, iar costul ei este proporțional cu numărul de intervenții, nu cu dificultatea lor tehnică. În cazul specific, estimarea fazei a doua a trecut de la patru la unsprezece luni calendaristice când Calitatea a aliniat change-urile necesare. *(DE VERIFICAT.)*

Nimeni, în această poveste, nu a lucrat prost. Echipa de infrastructură a migrat exact ceea ce i se ceruse, la timp. Echipa aplicativă a menținut codul neschimbat pentru a nu invalida validarea. Calitatea și-a făcut treaba. Punctul slab era în fraza însăși: *«optimizăm după»* presupune că după are același cost ca înainte.

## Mutarea și cutiile închise

Cine s-a mutat cel puțin o dată cunoaște fenomenul. Mutarea are o dată, și data comandă. În ultimele două săptămâni cutiile se umplu fără să alegi: *«duc totul, apoi aranjez în liniște în casa nouă»*. În casa nouă, cutiile nedeschise ajung la subsol. Sunt acolo și după cinci ani, iar acum subsolul se plătește pe metru pătrat.

Momentul în care alegerea costă mai puțin este **înainte** de a închide cutia — când o ai deja în mână. După, a o deschide înseamnă să cobori la subsol, să muți celelalte, să găsești timp. În cloud subsolul se plătește în fiecare lună; într-un sistem validat, pentru a deschide o cutie este nevoie și de semnătura altcuiva.

## Patru întrebări de pus înainte de a scrie «faza a doua» în plan

Niciuna dintre aceste întrebări nu servește la a renunța la lift-and-shift, care rămâne adesea alegerea corectă când există un termen real. Servesc la a decide **ce** să aduci așa cum este și ce merită regândit cât timp costul de a-l regândi este încă cel al migrării.

**1. Ce componente rămân în afara cloud-ului, și cât de mult vorbesc cu baza de date?**
O aplicație care rămâne în unitate și o bază de date care merge în region transformă fiecare round-trip în latență WAN. Numărarea round-trip-urilor pentru tranzacțiile critice — din AWR, înainte de migrare — costă o după-amiază. Înmulțindu-le cu latența măsurată între cele două site-uri se obține timpul pe care sistemul îl va pierde, înainte să îl piardă.

**2. Dimensionarea a fost calculată pe sarcina măsurată sau pe teama de sarcină?**
Pe hardware-ul vechi se cumpăra o dată pentru cinci ani, iar marja era gratuită după achiziție. În cloud marja se plătește în fiecare oră. Dimensionarea pe sarcina măsurată, cu un plan explicit de creștere, este o decizie diferită față de dimensionarea *«ca înainte, cu puțină siguranță în plus»*.

**3. Ce intervenții din faza a doua ating un sistem validat, și cât costă să le validezi după față de în timpul migrării?**
Este întrebarea care mută discuția din planul tehnic în cel economic. Dacă răspunsul este *«le-am valida oricum în timpul migrării»*, faza a doua costă o fracțiune din ce va costa pe un sistem în producție.

**4. Cine semnează faza a doua, și cu ce buget deja aprobat?**
O fază a doua fără proprietar și fără buget deliberat este, în fapt, un subsol. A numi cine răspunde de ea și cu ce resurse — înainte de go-live — este singurul mod de a evita ca ea să devină o intenție.

## Ce lasă în afară acest articol

Două teme merită un articol separat și rămân intenționat în afara acestuia: **licențierea Oracle în cloud** (regulile de numărare a vCPU-urilor pe hyperscaleri schimbă destul de mult calculele cazului de business) și **rezidența datelor** pentru datele de calitate și de farmacovigilență. Cine le-a abordat într-o migrare GxP are probabil o bucată din această poveste care lipsește aici.

## O întrebare de dus cu tine

Data viitoare când un plan de migrare conține fraza *«optimizare într-o fază ulterioară»*, merită să te întrebi:

*«Câte round-trip-uri face tranzacția noastră cea mai critică — și cât va costa să o schimbăm după, față de a o schimba acum?»*

Pentru cei care au traversat deja o migrare cu aplicații rămase on-premises și baza de date în cloud: care a fost primul semnal că «după» va costa mai mult decât era prevăzut?

## Glosar
- **[Lift-and-shift](/ro/glossary/lift-and-shift/)** — strategie de migrare cloud care mută sistemul existent fără modificări arhitecturale sau de cod, pentru a respecta un termen sau a limita riscul de validare.
- **[Round-trip](/ro/glossary/awr/)** (SQL\*Net) — ciclu complet cerere-răspuns între client și server de baze de date; în aplicații *chatty*, numărul lor determină latența totală percepută.
- **[GxP](/ro/glossary/lift-and-shift/)** — termen colectiv pentru reglementările farmaceutice (Good Manufacturing Practice, Good Laboratory Practice etc.) care impun trasabilitate și validare documentată a sistemelor computerizate.
- **[Change control](/ro/glossary/awr/)** (sisteme validate) — proces formal de evaluare, aprobare și documentare a oricărei modificări aduse unui sistem computerizat validat, obligatoriu înainte de implementare în producție.
- **[AWR](/ro/glossary/sql-net-roundtrips-to-from-client/)** (Oracle) — Automatic Workload Repository: instantanee periodice ale metricilor de workload, baza rapoartelor AWR și a ADDM; instrument esențial pentru diagnosticarea problemelor de performanță.
