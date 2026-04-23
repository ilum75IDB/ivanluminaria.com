---
title: "MySQL"
layout: "list"
description: "MySQL și MariaDB: securitate, performanță și arhitectură pe una dintre cele mai utilizate baze de date din lume."
image: "mysql.cover.jpg"
---

Am văzut servere MySQL cu 64GB de RAM și `innodb_buffer_pool_size` lăsat la 128MB — "pentru că e default-ul și nu am atins nimic". Am văzut tabele MyISAM încă în producție în 2026 pentru că "nu avem timp să le convertim", cu lock-uri la nivel de tabelă care blocau aplicații întregi în timpul backup-urilor. Am văzut replici master-slave cu 47.000 de secunde întârziere și nimeni care să observe, pentru că nimeni nu se uita la `Seconds_Behind_Master`.

Și am văzut exact opusul: parcuri MySQL cu sute de instanțe gestionate cu disciplină, unde fiecare decizie — storage engine, charset, binlog format, topologie — este luată conștient și nu din inerție.

Diferența nu a fost niciodată motorul. A fost întotdeauna **seriozitatea cu care cineva a ales opțiunile**.

------------------------------------------------------------------------

MySQL este baza de date care nu mai are nevoie de prezentare. Este motorul care a alimentat creșterea web-ului timp de peste douăzeci de ani.

Născut în 1995 în Suedia, în 2008 a fost achiziționat de Sun Microsystems — iar când Oracle a finalizat achiziția Sun în 2010, MySQL a ajuns în portofoliul celui mai mare furnizor de baze de date comerciale din lume. **Eram angajat Oracle în acea perioadă** și îmi amintesc bine atmosfera: pe de o parte curiozitatea de a vedea cum va gestiona Oracle un produs open source atât de popular, pe de altă parte teama că MySQL va fi marginalizat în favoarea bazei de date proprietare.

Acea teamă l-a determinat pe Michael "Monty" Widenius — creatorul original al MySQL — să facă fork-ul în 2009, dând naștere **MariaDB**. Un proiect care împărtășește rădăcinile cu MySQL dar a luat propriile direcții pe motoare de stocare, optimizator și funcționalități avansate.

Istoria a demonstrat că ambele proiecte au supraviețuit și au evoluat. Dar în cotidianul celor care gestionează producții reale, MySQL rămâne cel care *pare* simplu și în schimb ascunde alegeri critice:

- **storage engines amestecate** din obișnuință veche — MyISAM, InnoDB și uneori Archive conviețuiesc fără motiv
- **charset greșit** (latin1 în loc de utf8mb4) care corupe în tăcere datele multilingve
- **binlog în format STATEMENT** care cauzează inconsistențe în replicare pentru interogări nedeterministe
- **`sql_mode`** permisiv pentru "retrocompatibilitate" — interogări care returnează rezultate diferite la fiecare execuție
- **replicare fără monitoring activ** — iar când master-ul cade, slave-ul e cu trei zile în urmă

------------------------------------------------------------------------

## 🔧 Alegerile care fac diferența în producție

Sunt cinci decizii care — luate bine — fac MySQL să funcționeze zece ani, și — luate prost — te obligă să rescrii jumătate din aplicație. Sunt decizii banal de enumerat, extrem de incomod de schimbat după.

| Alegere | Ce decide | Cum o setez |
|---|---|---|
| **Storage engine** | Granularitatea lock-ului, tranzacționalitate, crash recovery | InnoDB întotdeauna, cu excepția cazurilor marginale și motivate — MyISAM este moștenire, nu alegere |
| **`innodb_buffer_pool_size`** | Memorie pentru cache de date și indecși InnoDB | 70-80% din RAM pe server dedicat, restul e risipă pentru motor |
| **Charset și collation** | Codificarea caracterelor și sortarea | `utf8mb4` + `utf8mb4_0900_ai_ci` — fără `utf8` (care în MySQL este incomplet) |
| **`binlog_format`** | Formatul log-urilor binare pentru replicare și PITR | `ROW` aproape întotdeauna — `STATEMENT` provoacă probleme în replicare cu interogări nedeterministe |
| **`sql_mode`** | Ce erori tolerează MySQL și ce nu | Strict mode activ, `ONLY_FULL_GROUP_BY` inclus — un MySQL permisiv este un MySQL care te minte |

Cinci alegeri. Treizeci de minute de discuție. Ani de operativitate fără incidente mari.

------------------------------------------------------------------------

## 📚 Despre ce vorbesc aici

Povești reale și decizii operaționale pe MySQL și MariaDB în producție. Securitate, gestionarea utilizatorilor și privilegiilor, tuning InnoDB, replicare master-slave și InnoDB Cluster, strategii de upgrade și migrare, backup-uri consistente cu `mysqldump` și unelte fizice, diferențe reale între MySQL și MariaDB care apar doar sub sarcină.

Fără rețete generice. Doar ce am văzut funcționând pe medii reale — postal, telco, finance, administrație publică — unde MySQL susține parcuri de instanțe în paralel și nu își poate permite alegeri făcute "din inerție".

------------------------------------------------------------------------

A folosi MySQL nu înseamnă doar a rula interogări.

Înseamnă a înțelege cum gestionează motorul conexiuni, privilegii și resurse sub sarcină reală — și a recunoaște că simplitatea aparentă este, adesea, cea mai costisitoare capcană.
