---
categories:
- oracle
date: '2026-10-27'
description: 'Cum planifici upgrade-ul de la Oracle 11g R2 la 19c pe OCI pentru un
  DB financiar de 8 TB: strategie XTTS, cutover în 4 ore și rollback demonstrabil.'
draft: false
image: oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback.cover.jpg
seoTitle: 'Upgrade Oracle 11g la 19c pe OCI: 8 TB cu XTTS și rollback'
tags:
- oracle
- database-migration
- upgrade
- oci
- disaster-recovery
- financial-systems
title: 'Oracle 11g R2 → 19c pe OCI: 8 TB în finanțe, un plan de upgrade cu faze și
  rollback'
translationKey: oracle_11g_r2_19c_su_oci_8_tb_in_finanza_un_piano_di_upgrade_con_fasi_e_rollback
webo_generated_at: 2026-10-10
webo_status: scheduled
---

*Cum dezmembrezi paralizia decizională pe o instanță Oracle 11g EOL încă în producție, alegi strategia de upgrade potrivită pentru 8 TB cloud-to-cloud și aduci cutover-ul în patru ore cu rollback pregătit la fiecare pas.*

---

## O instanță pe care nimeni nu voia s-o atingă

Există un pattern pe care cei care lucrează de ani buni cu sisteme financiare îl cunosc bine. O instanță Oracle 11g Release 2 — în cazul specific **11.2.0.4**, ultima minor a întregii familii 11g, lansată în 2013 — este încă pornită în producție în 2026. Deasupra ei rulează un sistem de middle-office pentru controlul limitelor de expunere intraday, construit în anii 2010 pe PL/SQL complex, cu 420+ pachete și proceduri, 1.400 de obiecte aplicative și o logică de postare contabilă stratificată pe mai multe release-uri de business. Baza de date cântărește **8 TB** și crește cu câteva sute de GB pe an. Rulează pe o instanță OCI VM.Standard dedicată, migrată în cloud cu patru ani în urmă printr-un lift-and-shift curat.

Oracle a declarat Premier Support pentru 11g **încheiat în ianuarie 2015**, Extended Support **încheiat în decembrie 2020**. De aproape șase ani instanța nu primește patch-uri de securitate, niciun fix de bug major, nicio CPU trimestrială. În auditurile interne din ultimii trei ani instanța este clasificată sistematic drept «risc ridicat», dar nu s-a produs niciodată un incident suficient de grav pentru a forța decizia. Între timp cadrul de conformitate s-a schimbat: DORA a intrat în vigoare, Banca d'Italia și-a rafinat așteptările privind suportabilitatea infrastructurilor critice, auditorii externi au început să ceară planuri de remediere cu date concrete.

**De ce era instanța blocată la 11g?** Nu din lipsă de competență tehnică — echipa internă știa cum se face un upgrade. Era blocată din cauza **paraliziei decizionale**. Aplicația de deasupra era critică (oprirea ei însemna că traderii nu-și vedeau limitele de expunere în timp real), fereastra de downtime acceptabilă pentru business era de maximum patru ore într-o noapte de sâmbătă, niciunul dintre vendor-ii aplicativi implicați nu mai era disponibil pentru suport, și nimeni din echipa internă nu voia **să semneze** o procedură de upgrade care atingea inima postării contabile. Era un caz clasic de *«atâta timp cât merge, nu se atinge»* — de înțeles, legitim, insustenabil.

## Când decizia nu mai poate fi amânată

La un moment dat balanța riscurilor s-a inversat. Riscul unei vulnerabilități nepatchabile a devenit mai mare decât riscul cutover-ului. Comitetul de risc a cerut un plan cu **date certe** și **rollback demonstrabil**. Planul a fost propus în șase săptămâni de studiu, discutat în două ședințe cu business-ul, aprobat cu angajamentul formal de **a lăsa vechea instanță în read-only timp de două săptămâni după cutover**, în cazul în care ar fi nevoie să se revină.

Ținta a fost aleasă **19c (19.24)** — nu 21c, nu 23ai. Două motive. Primul: 19c este **Terminal Release** a branch-ului 12.2, ceea ce înseamnă în jargon Oracle că este release-ul destinat Long-Term Support (Premier Support până în 2027, Market-Driven Support până în 2032). Este versiunea cea mai stabilă și mai bine documentată din prezent, cu un ecosistem de patch set matur. Al doilea: 19c este **minimul compatible target** pentru un upgrade direct din 11.2.0.4 (direct upgrade este suportat: niciun hop intermediar necesar prin 12c). A sări direct la 21c sau 23ai ar fi necesitat un hop multi-release mai lung și un risc de stabilitate post-migrare mai mare, cu câștig funcțional redus pentru o aplicație legacy.

## Opțiunile tehnice pe masă

Pentru o bază de date Oracle de 8 TB care servește drept storage unui aplicativ mission-critical cu o fereastră de cutover de patru ore, strategiile realiste sunt cinci. Merită să le articulăm împreună, pentru că alegerea este un trade-off între timp de pregătire, downtime efectiv, complexitate de rollback și costul de licensing al instrumentelor auxiliare.

| Strategie | Downtime | Pregătire | Rollback | Note |
|---|---|---|---|---|
| **DBUA in-place** (direct 11.2.0.4 → 19c) | 6-12 ore pe 8 TB | Zile | Dificil (restore backup) | Suportat, dar prea mult downtime pentru acest caz |
| **Data Pump expdp/impdp** full | 10-20 ore pe 8 TB | Zile | Ușor (vechea instanță intactă) | Lent, dar curat. Prea mult downtime |
| **Transportable Tablespaces (TTS) + Data Pump metadata** | 4-6 ore pe 8 TB | 1 săptămână | Ușor | Copiere inițială lungă, cutover acceptabil |
| **Cross-Platform Transportable Tablespaces cu Incremental Backups (XTTS)** | **2-4 ore pe 8 TB** | **2 săptămâni în paralel** | **Ușor (RO pe sursă)** | **Ales** — minimizează cutover-ul cu prețul unei pregătiri lungi |
| **Oracle Zero Downtime Migration (ZDM)** | 10-30 minute | 3-4 săptămâni + licensing | Automatizat | Opțiune premium, eliminată din cauza costului tool + complexității de setup |

Alegerea a căzut pe **XTTS cu incremental backups**. Permite împărțirea upgrade-ului în două faze distincte: una **lungă, dar invizibilă pentru business** (pregătire de două săptămâni de copiere și sincronizare) și una **scurtă și vizibilă** (cutover de patru ore în noaptea de sâmbătă). Metoda este documentată de Oracle în MOS Note 2471245.1 și este cea mai folosită în producție pentru baze de date de dimensiuni mari cross-version și cross-platform. Rollback-ul rămâne simplu pentru că sursa nu este atinsă — rămâne în producție până în momentul cutover-ului și poate fi reactivată în treizeci de minute chiar și după.

## Planul, în șase faze

### Faza 0 — Assessment (2 săptămâni înainte de cutover)

Execuția **`preupgrd.sql`** (tool-ul de pre-upgrade distribuit cu 19c, de executat pe sursa 11.2.0.4 după ce a fost copiat din download-ul de 19c) + **`autoupgrade.jar`** în modul analyze. Output-ul este un raport care listează:

- Obiecte invalide de remediat înainte de upgrade
- Parametri `init.ora` deprecați (clasici în 11g: `background_dump_dest`, `user_dump_dest`, `plsql_v2_compatibility`)
- Feature-uri deprecate folosite de aplicativ (cel mai comun: tipurile `LONG` și `RAW`, de verificat dacă aplicația are dependențe)
- Statistici obsolete pe tabele mari
- Parole cu hashing slab (11g accepta implicit `DES`, 19c necesită `SHA-2`)

În cazul de față raportul a semnalat 23 de obiecte invalide (aproape toate procedurale, rezolvabile printr-o recompilare), 7 parametri deprecați în `spfile` și **nicio utilizare de LONG/RAW** în codul aplicativ (verificat via `dba_tab_columns`). Două săptămâni au fost suficiente pentru a remedia totul fără grabă.

### Faza 1 — Construirea mediului 19c țintă pe OCI

În paralel cu Faza 0, provisionarea unei **noi instanțe OCI** cu 19c (19.24 RU trimestrial curent), aceeași shape ca sursa, dar cu **storage NVMe local** pentru performanță de import, nu network block volume. Instalare curată, configurare rețea, listener, service name identice cu sursa (pentru a minimiza schimbarea aplicativă la cutover). **Tablespace-urile USER sunt create goale** cu aceeași topologie ca sursa — aceleași nume, aceleași dimensiuni inițiale, aceeași extindere. Tablespace-urile de sistem (`SYSTEM`, `SYSAUX`, `UNDO`, `TEMP`) sunt cele native 19c, nu cele transportate.

### Faza 2 — Initial RMAN backup level 0 + rollforward inițial (zilele 1-7 de pregătire)

Backup incremental **level 0** al tuturor tablespace-urilor USER ale sursei, în format *backupset*, prin RMAN cu paralelism ridicat (`CONFIGURE DEVICE TYPE DISK PARALLELISM 8`). Transfer pe țintă via **Object Storage OCI** (bucket partajat între cele două instanțe — latență mică, niciun hop internet). Rollforward inițial pe ținta 19c prin **convert** cross-version (`RMAN> CONVERT DATAFILE ... TO PLATFORM 'Linux x86 64-bit'` dacă cross-platform, sau simplu restore dacă aceeași platformă).

Durată: ~5-6 zile pentru 8 TB cu acea shape de storage. Operațiunea este complet **în background**, fără niciun impact asupra sursei productive.

### Faza 3 — Incremental backup level 1 ciclice (zilele 7-14 de pregătire)

Din acel moment, RMAN **incremental level 1 la fiecare 4 ore** pe sursă (`BACKUP INCREMENTAL LEVEL 1 FOR RECOVER OF COPY WITH TAG 'xtts_incr' ...`). Transfer continuu pe țintă, rollforward aplicat pe țintă. **Lag-ul** dintre sursă și țintă rămâne sub 6 ore pe toată săptămâna anterioară cutover-ului. Monitorizare cu scripturi dedicate care urmăresc SCN-ul celor două instanțe.

### Faza 4 — Pre-cutover testing (weekendul înainte de go-live)

Într-un mediu de staging — copie completă a aplicației și a bazei de date — simulare completă a procedurii de cutover. Validarea aplicativului cu endpoint 19c, smoke test al tuturor batch-urilor nocturne, testarea tuturor serviciilor online care apelează stored procedure complexe. Corectarea a patru diferențe de comportament apărute (niciuna gravă: un `ORA-29913` pe o external table cu un path absolut hardcodat, două query-uri cu hint-uri deprecate, un job `DBMS_SCHEDULER` cu un parametru care și-a schimbat formatul).

### Faza 5 — Cutover nocturn (noaptea de sâmbătă, 4 ore)

| Oră | Acțiune |
|---|---|
| **T−00:30** | Comunicare către echipa de business: freeze iminent |
| **T+00:00** | `SHUTDOWN IMMEDIATE` al aplicativului (oprire scrieri pe sursă) |
| **T+00:10** | Ultimul RMAN incremental level 1 pe sursă |
| **T+00:40** | Apply al ultimului incremental pe ținta 19c |
| **T+01:00** | Sursa 11g pusă în `READ ONLY` pe toate tablespace-urile USER |
| **T+01:10** | Export metadata via **Data Pump** (`expdp TRANSPORT_TABLESPACES=...`) — toate tablespace-urile USER + users + grants + public synonyms + sequences + views + packages + triggers + jobs |
| **T+01:40** | Transport fizic al datafile-urilor USER de la sursă la țintă (metadata deja aplicat) + import metadata pe 19c (`impdp TRANSPORT_DATAFILES=... TRANSPORT_TABLESPACES=... REMAP_SCHEMA=...` dacă e necesar) |
| **T+02:30** | `ALTER TABLESPACE ... READ WRITE` pe țintă + `UTL_RECOMP.RECOMP_PARALLEL` pentru recompilarea obiectelor invalide |
| **T+03:00** | Smoke test al tuturor serviciilor aplicative împotriva noului endpoint 19c |
| **T+03:30** | Switch-ul service name DNS aplicativ (TTL coborât preventiv la 60 de secunde) pe noul endpoint |
| **T+04:00** | **GO-LIVE** |

### Faza 6 — Planul de rollback (cele două săptămâni după go-live)

Două plase de siguranță, în ordine crescătoare de invazivitate:

**Plasa 1 — Switch DNS înapoi**: vechea 11g rămâne pornită în read-only timp de 14 zile. În cazul unor probleme grave irezolvabile în primele ore, este suficient să **repui `READ WRITE` pe tablespace-urile sursă** (operațiune de câteva secunde) și să **switchezi înapoi service name-ul DNS**. Aplicativul revine să vorbească cu 11g în mai puțin de 30 de minute, pierzând cel mult datele scrise pe 19c după cutover (cuantificabile și recuperabile via Data Pump din 19c în 11g, dacă e necesar). Costul acestei plase: menținerea instanței 11g pornite încă două săptămâni.

**Plasa 2 — Snapshot OCI**: snapshot la nivel de bloc al instanței 19c înainte de cutover + snapshot al instanței 11g cu ultimul stat RW. În cazul unei catastrofe în timpul cutover-ului însuși (ex. corupere a metadata în timpul import-ului), restore din snapshot-uri în 1-2 ore. Plasă de siguranță rar necesară, dar care oferă liniște comitetului de risc la aprobarea planului.

## Primele zile după go-live

Prima luni dimineață este momentul critic. Deschiderea pieței aduce primul val de încărcare reală pe o instanță 19c care până atunci văzuse doar testul de sâmbătă noapte. Monitorizarea atentă din primele 48 de ore se concentrează pe trei aspecte:

- **Planuri de execuție schimbate**: 19c introduce un cost-based optimizer semnificativ diferit față de 11g — Automatic SQL Plan Management, Statistics Advisor mai agresiv, algoritmi noi de join. În cazul de față, din 420+ pachete aplicative, 11 query-uri critice și-au schimbat planul cu regresie de performanță. Rezolvate în 48 de ore cu hint-uri țintite (`USE_NL`, `INDEX`) sau baseline-uri `SPM` capturate din planul anterior executat în staging.
- **Statistici**: colectare completă post-upgrade cu **noul optimizer 19c**, nu reutilizarea valorilor din 11g, care ar fi obsolete pe structuri de memorie diferite. Operațiune costisitoare (ore), dar necesară.
- **AWR comparison**: snapshot-uri AWR pentru 48 de ore pre-cutover pe 11g și pentru 48 de ore post-cutover pe 19c, comparate cu `DBMS_WORKLOAD_REPOSITORY.AWR_DIFF_REPORT_HTML`. Nicio degradare sistemică, îmbunătățire netă pe unele query-uri batch (19c are un adaptive join pe care 11g nu îl avea).

După 14 zile, cu zero rollback-uri necesare și metrici stabile, vechea 11g a fost **oprită și arhivată** (snapshot păstrat 90 de zile pentru audit, apoi retention normal). Comitetul de risc a închis punctul de pe agenda sa pentru prima dată în cinci ani.

## Ce rămâne pe masă, dacă ești în aceeași situație

Un upgrade de la 11g la 19c nu este o operațiune tehnic complicată — este o operațiune **politic** complicată. Tehnica este cunoscută, documentată, repetată în mii de implementări. Ceea ce blochează cu adevărat instanțele EOL în producție este combinația dintre: aplicativ critic fără vendor de suport activ, fereastră de downtime strânsă, absența unei proceduri de rollback demonstrabile care să-i permită celui care semnează să doarmă noaptea după cutover.

Trei întrebări merită puse, dacă evaluezi un upgrade similar:

**1. Care este downtime-ul aplicativ maxim apărabil în fața business-ului, și ce strategie tehnică se încadrează în acea fereastră?** Dacă răspunsul este *«maximum patru ore într-o noapte de sâmbătă»*, XTTS cu incremental este aproape obligatoriu pentru baze de date de peste 2-3 TB. Dacă răspunsul este *«maximum zece minute»*, ZDM este singura opțiune realistă — și trebuie bugetat tool-ul.

**2. Care este planul de rollback, măsurat în minute?** Un plan de rollback care necesită *«restore complet din backup»* nu este un plan de rollback, este o speranță. Un plan serios înseamnă *«switch service name DNS înapoi în 30 de minute cu vechea instanță pornită în read-only»*. Diferența, în fața comitetului de risc, este totul.

**3. Cine semnează procedura de cutover, și ce îi trebuie acelei persoane pentru a semna?** În cazurile reale pe care le-am văzut, blocajul nu este niciodată tehnic — este căutarea acelei semnături. Când planul include rollback măsurabil, snapshot pre-cutover, pre-test complet pe staging, semnătura vine. Fără acele elemente, planul rămâne în sertar ani de zile.

O instanță 11g în producție în 2026 nu este o eroare — este un simptom. Planul de upgrade nu este doar tehnică: este momentul în care repornești o decizie care stătuse blocată ani de zile.

---

*Ivan Luminaria este Technical Leader pentru baze de date mission-critical. Lucrează cu CIO, CTO și IT Director din bănci mid-tier, asigurări, telco, utilități și mari instituții publice italiene, cu o metodă de lectură cross-layer construită în aproape treizeci de ani de sisteme reale.*

## Glosar
- **[XTTS](/ro/glossary/xtts/)** (Oracle) — Cross-Platform Transportable Tablespaces: metodă de migrare care combină backup-uri RMAN incrementale cu transportul fizic al datafile-urilor, minimizând downtime-ul pentru baze de date de mari dimensiuni.
- **[cutover](/ro/glossary/cutover/)** — momentul de comutare definitivă de la sistemul vechi la cel nou; în contextul upgrade-urilor de baze de date, fereastra de timp în care producția este oprită și traficul este redirecționat.
- **[EOL](/ro/glossary/xtts/)** (End of Life) — starea unui produs software pentru care vendor-ul a încetat orice formă de suport, inclusiv patch-uri de securitate și fix-uri de bug.
- **[SPM](/ro/glossary/preupgrd-sql/)** (SQL Plan Management) — funcționalitate Oracle care permite capturarea, verificarea și stabilizarea planurilor de execuție SQL, prevenind regresiile de performanță după upgrade-uri sau modificări de statistici.
- **[AWR](/ro/glossary/cutover/)** (Automatic Workload Repository) — repository Oracle care stochează snapshot-uri periodice ale metricilor de workload, baza rapoartelor de performanță și a comparațiilor pre/post-upgrade.

## Surse oficiale

1. Oracle Database Upgrade Guide 19c — [Upgrading Oracle Database](https://docs.oracle.com/en/database/oracle/oracle-database/19/upgrd/index.html)
2. Oracle MOS Note 2471245.1 — V4 Reduce Transportable Tablespace Downtime using Incremental Backups (referință internă MOS, accesibilă con account My Oracle Support)
3. Oracle Database SQL Language Reference 19c — [DBMS_WORKLOAD_REPOSITORY](https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_WORKLOAD_REPOSITORY.html)
4. Oracle AutoUpgrade Tool — [AutoUpgrade Documentation](https://docs.oracle.com/en/database/oracle/oracle-database/19/upgrd/using-autoupgrade-oracle-database-upgrades.html)
