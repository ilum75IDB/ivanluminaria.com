---
title: "Oracle de la On-Premises la Cloud: Strategie, Planificare și Cutover"
description: "Un Oracle 19c Enterprise cu RAC, Data Guard și 2 TB de date. Trei luni pentru a muta totul în OCI fără a pierde nici măcar o tranzacție. De la analiza licențelor până la cutover-ul peste noapte, povestea unei migrații reale."
date: "2026-04-28T10:00:00+01:00"
draft: false
translationKey: "oracle_cloud_migration"
tags: ["migration", "cloud", "oci", "data-guard", "architecture", "licensing"]
categories: ["oracle"]
image: "oracle-cloud-migration.cover.jpg"
---

Săptămâna trecută, un coleg mi-a scris: „Trebuie să mut Oracle în cloud — cât durează?” I-am răspuns cu o întrebare: „Știi exact câte funcționalități Enterprise Edition folosești cu adevărat?” Liniște.

Se repetă de fiecare dată același scenariu. Cineva din management decide că a venit momentul pentru cloud — pentru că expiră contractul de hosting, pentru că CFO-ul a citit un raport Gartner, pentru că noul CTO vrea modernizare. Și prima idee care apare este: lift-and-shift. Luăm ce avem și mutăm. Trei luni, buget aprobat, să-i dăm drumul.

Problema este că Oracle nu e o aplicație pe care o pui într-un container și o muți. Este un ecosistem: licențe, dependențe, configurații de kernel, conexiuni de rețea prin firewall-uri și VPN-uri. Dacă îl muți fără să-l înțelegi, ajungi în cloud cu aceleași probleme — și, de obicei, cu unele noi.

## Clientul și contextul

Proiectul era pentru o companie de producție din nordul Italiei — una dintre acelea care merg bine financiar, dar cu un departament IT foarte mic. Patru oameni pentru tot: ERP, sisteme interne, tot.

Oracle 19c Enterprise Edition rula pe un RAC cu două noduri, cu Data Guard replicând într-un site secundar la 20 km distanță. Aproximativ 2 TB de date, cam 200 de utilizatori simultan la orele de vârf și un batch nocturn care alimenta data warehouse-ul.

Providerul de hosting anunțase că nu mai prelungește contractul decât cu +40%. Managementul a decis: mergem în cloud. Trei luni pentru livrare, deadline fix.

Când am ajuns, planul era deja făcut: lift-and-shift pe AWS. Integratorul propusese EC2, EBS și gata. În Excel totul arăta impecabil. Două rânduri: cost actual vs cost viitor. Costul viitor mai mic. Toată lumea mulțumită.

## De ce am spus nu la AWS

Primul lucru pe care l-am cerut a fost raportul de licențe. Oracle 19c Enterprise Edition cu RAC, Data Guard, Partitioning și Advanced Compression.

Aici începe distracția.

Oracle are reguli de licențiere în cloud care nu sunt deloc intuitive. Pe AWS, fiecare vCPU contează ca jumătate de procesor. Două noduri RAC cu câte 8 vCPU = 8 licențe de procesor. Cu Enterprise Edition + opțiuni, costul explodează.

Și Oracle, când face audit — pentru că face — nu se uită la contractul AWS. Se uită la ce rulează efectiv.

Pe OCI lucrurile sunt diferite:
- raport 1:1 pentru OCPU
- program BYOL (Bring Your Own License)

Clientul deja plătise licențele. Pe OCI le refolosea gratuit. Pe AWS trebuia să le cumpere din nou sau să riște audit.

Am făcut un tabel cu trei scenarii:
- AWS cu licențe noi
- AWS cu risc de audit
- OCI cu BYOL

Decizia s-a schimbat în 30 de minute.

## Evaluarea: două săptămâni care au salvat luni

Înainte să atingem ceva, am cerut două săptămâni pentru assessment complet.

Nu e opțional.

Am învățat asta pe pielea mea într-un proiect unde am descoperit în mijlocul migrației că baza de date folosea Advanced Queuing cu IP hardcodat. Două zile de downtime pentru ceva ce puteam descoperi în 5 minute.

Am analizat patru lucruri.

**Funcționalități folosite.**  
RAC și Data Guard — clar.  
Partitioning — doar 3 tabele.  
Advanced Compression — inutil pentru producție.

**Dependențe externe.**  
DB link-uri către MySQL, API-uri interne — toate trebuiau să continue să funcționeze.

**Rețea și latență.**  
12 ms către OCI Frankfurt. OK pentru query-uri.  
Catastrofă pentru batch-uri cu milioane de rânduri.

Soluția: staging local.

**Sizing.**  
CPU max 35%, RAM max 48 GB.  
Configurație OCI: 2 noduri + standby.

## Strategia: Data Guard, fără compromisuri

Data Pump → exclus  
ZDM → prea abstract pentru acest setup  

Data Guard → control total

Downtime estimat: < 1 oră  
Downtime real: 42 minute

### Configurarea Data Guard

VPN 500 Mbps  
Redo peak: 180 MB/min → lag ~45 sec → acceptabil

Sincronizare inițială: 14 ore  
Lag mediu: 3 secunde

## Cutover: fără improvizații

Runbook: 47 pași (și da, fiecare contează)

Totul a mers conform planului.

Downtime total: 42 minute.

## După migrare: realitatea

Aici începe partea interesantă.

**Timezone**  
UTC vs Europe/Rome → date „din viitor”

**TLS**  
Wallet invalid → ORA-29024

**Scheduler**  
Job-uri decalate → fix manual

Nimic critic. Dar toate enervante.

## Costuri reale

OCI: ~63k/an  
On-prem: ~120k/an

Dar:
- networking mai scump
- consultanță (da, inclusiv eu)

## Ce am învățat (din nou)

Licențierea Oracle în cloud = teren minat.

Assessment-ul nu e negociabil.

Data Guard este cea mai curată soluție.

Și… timezone-ul. Pune-l primul pe listă.

------------------------------------------------------------------------

## Glossary

**[OCI](/ro/glossary/oci/)** — Oracle Cloud Infrastructure, platforma cloud a Oracle. Pentru bazele de date Oracle oferă avantaje semnificative de licențiere prin programul BYOL și raportul 1:1 pentru OCPU.

**[BYOL](/ro/glossary/byol/)** — Bring Your Own License, program care permite reutilizarea licențelor Oracle existente on-premises în cloud OCI fără costuri suplimentare de licențiere.

**[RAC](/ro/glossary/rac/)** — Real Application Clusters, tehnologie Oracle care permite mai multor instanțe să acceseze simultan aceeași bază de date, oferind disponibilitate ridicată și scalabilitate orizontală.

**[Data Guard](/ro/glossary/data-guard/)** — tehnologie Oracle pentru replicarea în timp real a unei baze de date către unul sau mai multe servere standby, asigurând disponibilitate ridicată și recuperare în caz de dezastru.

**[ZDM](/ro/glossary/zdm/)** — Zero Downtime Migration, tool Oracle pentru migrarea bazelor de date către OCI, care combină Data Guard și Data Pump într-un strat de orchestrare automatizată.

**[Switchover](/ro/glossary/switchover/)** — operațiune planificată în Data Guard care inversează rolurile între primary și standby fără pierdere de date. Spre deosebire de failover, este controlată și reversibilă.

**[AWR](/ro/glossary/awr/)** — Automatic Workload Repository, instrument integrat în Oracle Database pentru colectarea și analiza statisticilor de performanță.

**[Transport Lag](/ro/glossary/transport-lag/)** — întârzierea în transmiterea redo log-urilor de la baza de date primary către standby în configurațiile Data Guard. Indicator esențial pentru sănătatea replicării.

**[SCAN Listener](/ro/glossary/scan-listener/)** — Single Client Access Name, componentă Oracle RAC care oferă un punct unic de acces către cluster, distribuind automat conexiunile între noduri.

**[Cutover](/ro/glossary/cutover/)** — momentul critic într-o migrare în care sistemul de producție este mutat definitiv de pe infrastructura veche pe cea nouă.
