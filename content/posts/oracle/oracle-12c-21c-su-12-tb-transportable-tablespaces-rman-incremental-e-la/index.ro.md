---
title: "Sâmbătă noaptea pe care nimeni nu și-o dorește: migrare Oracle 12c → 21c pe 12 TB cu transportable tablespaces și RMAN incremental"
seoTitle: "Migrare Oracle 12.2 → 21c: 12 TB în 4 ore de downtime"
description: "Cum am mutat 12 TB Oracle de la 12.2 la 21c într-o fereastră de 4 ore: strategie TTS + RMAN incremental, pași detaliați și cifrele reale din noaptea migrării."
date: 2099-12-31
draft: true
translationKey: "oracle_12c_21c_su_12_tb_transportable_tablespaces_rman_incremental_e_la"
tags: ["oracle", "migration", "rman", "transportable-tablespaces", "multitenant"]
categories: ["oracle"]
image: "oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la.cover.jpg"
webo_status: da_tradurre
webo_generated_at: 2026-09-04
---

## Sâmbătă noaptea pe care nimeni nu și-o dorește

Cererea venise cu câteva săptămâni înainte, într-una din acele ședințe în care cifrele sunt prezentate ca și cum ar fi detalii: „trebuie să migrăm baza de date Oracle de la 12.2 la 21c, avem o fereastră de mentenanță sâmbătă noaptea, patru ore". Doisprezece terabytes. Server cu opt ani de viață, ieșit din suportul hardware. Noul server deja în rack, Oracle 21c instalat — un CDB, pentru că în 21c nu există altă opțiune, și la asta revenim puțin mai târziu.

Patru ore pentru doisprezece terabytes.

Cine lucrează cu Oracle de ceva vreme știe deja unde e problema: nu în baza de date, nu în versiune, nu în hardware-ul nou. Stă în matematică. Un Data Pump pe doisprezece terabytes, chiar și cu paralelism agresiv și storage rapid, nu termină în patru ore. Nu termină în opt. Probabil nu termină în weekend.

Ceea ce urmează este raționamentul care a dus la o strategie hibridă — transportable tablespaces cross-version plus RMAN incremental — și detaliile a ceea ce s-a întâmplat cu adevărat în cele patru ore critice. Cifrele sunt cele reale, comenzile sunt cele folosite, problemele sunt cele care se descoperă doar când ești deja înăuntru.

---

## De ce Data Pump nu e răspunsul la această scară

Data Pump este instrumentul potrivit pentru migrări de până la câteva sute de gigabytes, sau pentru export/import selective pe scheme specifice. Dincolo de acea limită, constrângerile devin structurale.

Pe doisprezece terabytes, problema principală este throughput-ul de I/O. Data Pump exportă datele serializând rânduri în format proprietar Oracle, apoi le reimportează reconstruind segmente, indecși, statistici. Chiar și cu `PARALLEL=16` și storage NVMe pe ambele părți, throughput-ul efectiv depășește rareori 3-4 GB/minut în scenarii reale (nu benchmark). Doisprezece terabytes la 4 GB/minut: cincizeci de ore. Optimist.

Există și problema spațiului: e nevoie de o zonă de staging care să conțină întregul export, plus spațiul pe target în timpul importului. Cu doisprezece terabytes de date, vorbim de douăzeci-douăzeci și cinci de terabytes de spațiu temporar necesar între cele două mașini.

Ultima problemă este fereastra: Data Pump nu este incremental. Dacă exportul pornește vineri seara și baza de date continuă să primească scrieri, la finalul exportului datele sunt deja parțial depășite. Nu există un mecanism nativ pentru a sincroniza modificările apărute în timpul exportului.

---

## Opțiunile reale pentru migrări multi-terabyte

Când Data Pump este exclus, alternativele reale sunt patru [1]:

**RMAN Duplicate** — duplică baza de date completă via RMAN, inclusiv toate fișierele fizice. Necesită spațiu dublu pe target (sau aproape), dar este fiabil și bine documentat. Problema: pentru doisprezece terabytes, chiar și faza inițială de copiere necesită multe ore și nu rezolvă problema ferestrei scurte.

**Transportable Tablespaces (TTS)** — copiază fișierele datafile direct, fără serializare/deserializare. Este metoda cea mai rapidă pentru a muta volume mari deoarece throughput-ul este limitat doar de viteza canalului de transfer (rețea, storage partajat, bandă). Constrângerea istorică era endianness-ul: platforme diferite (ex. Solaris SPARC → Linux x86) necesitau conversie. Între două sisteme Linux x86_64, problema nu există [2].

**Data Guard ca punte** — se configurează o bază de date standby pe mașina nouă, se lasă sincronizarea să aibă loc via redo log (ore sau zile, fără impact pe primar), apoi se execută un failover controlat în fereastra de mentenanță. Elegant, dar necesită ca versiunile să fie compatibile pentru redo shipping — și între 12c și 21c există constrângeri precise.

**GoldenGate** — replicare logică, flexibilitate maximă cross-version și cross-platform. Necesită licență separată, setup non-trivial și o perioadă de warm-up pentru sincronizarea inițială. Pentru o migrare one-shot cu fereastră definită, este adesea supradimensionat.

---

## Strategia aleasă: TTS + RMAN incremental

Soluția adoptată combină două tehnici: transportable tablespaces pentru a muta masa de date înainte de fereastră, și RMAN incremental backup pentru a sincroniza modificările acumulate între timp.

Ideea de bază este simplă: dacă nu pot muta doisprezece terabytes în patru ore, mut unsprezece terabytes și jumătate în zilele anterioare, iar în cele patru ore critice mut doar delta.

Planul se articulează în trei faze:

1. **Faza pregătitoare** (zile înainte de fereastră): backup RMAN level 0 transportabil **cu baza de date deschisă și în scriere**, transfer pe noul server, restore ca foreign datafile copy
2. **Faza de sincronizare** (zile și ore înainte de fereastră): level 1 incrementale, tot cu baza de date operațională, pentru a reduce progresiv gap-ul
3. **Fereastra de downtime** (patru ore): tablespace în read-only, ultimul incremental, plug-in-ul metadatelor în PDB, deschidere

Diferența dintre acest plan și cel care ar veni instinctiv — a pune tablespace-urile în read-only, a le copia cu calm, apoi a le alinia — stă toată în primul punct, și este motivul pentru care clauza `ALLOW INCONSISTENT` există.

---

## Pre-check: ce se descoperă înainte de a atinge ceva

Înainte de a muta un byte, este necesară o analiză de compatibilitate. Între Oracle 12.2 și Oracle 21c sunt aproape zece ani de versiuni intermediare, iar unele lucruri s-au schimbat în mod non-retrocompatibil.

**Character set**: verifică că sursa și target-ul folosesc același character set, sau că target-ul este un superset. O migrare TTS între AL32UTF8 și WE8ISO8859P1 necesită conversie explicită și nu este banală.

```sql
-- Pe baza de date sursă (12c)
SELECT value FROM nls_database_parameters WHERE parameter = 'NLS_CHARACTERSET';
SELECT value FROM nls_database_parameters WHERE parameter = 'NLS_NCHAR_CHARACTERSET';
```

**Endianness**: pe Linux x86_64 → Linux x86_64 nu există probleme. Pe migrări cross-platform (ex. AIX → Linux), este necesar `RMAN CONVERT TABLESPACE`.

```sql
-- Verificare platformă
SELECT platform_name, endian_format FROM v$transportable_platform
WHERE endian_format = (SELECT endian_format FROM v$database);
```

**Arhitectura de destinație**: este constrângerea care decide forma întregii migrări, și merită descoperită înainte de a comanda serverul, nu cu o săptămână înainte de fereastră. **În Oracle 21c arhitectura non-CDB nu mai este suportată**: multitenant este singura arhitectură suportată [3]. Un 12.2 non-CDB nu devine un 21c non-CDB, pentru că acea destinație nu mai există — devine o **PDB într-un CDB 21c**. Nu e un detaliu de packaging: schimbă unde aterizează tablespace-urile, cum se deschide baza de date și ce comenzi se folosesc în fereastră.

**Componente deprecate**: raportul de pre-upgrade nu se mai generează cu un script SQL. Din Oracle 21c Pre-Upgrade Information Tool (`preupgrade.jar`) nu mai este distribuit, iar funcțiile sale au fost integrate în **AutoUpgrade** [4]:

```bash
# Cu home-ul 21c disponibil — doar analiză, nu modifică nimic
java -jar $ORACLE_HOME_21C/rdbms/admin/autoupgrade.jar \
  -preupgrade "target_version=21,dir=/tmp/preupg" -mode analyze
```

Raportul semnalează obiecte invalide, parametri obsoleti, componente de eliminat înainte de upgrade. Printre cele mai frecvente în tranziția 12.2 → 21c: `SQLNET.ALLOWED_LOGON_VERSION` (deprecat), unele view-uri de compatibilitate și politicile de audit — la auditing revenim mai târziu, pentru că este punctul cu cea mai multă dezinformare în circulație.

`-mode analyze` este read-only: poate fi lansat în producție, în orele de lucru, cu săptămâni înainte. Este primul lucru de făcut, și este cel care aproape întotdeauna se face prea târziu.

**Tablespace-urile SYSTEM și SYSAUX**: nu sunt transportabile. Rămân pe sursă; pe target dicționarul este cel al PDB-ului, creat de CDB-ul care o găzduiește.

---

## Planul pas cu pas

Punctul de care depinde totul: **tablespace-urile rămân în citire și scriere până la ultimul pas**. Acesta este exact motivul pentru care există backup-ul incremental `FOR TRANSPORT`: read-only este necesar doar pentru backup-ul final, cel care închide fereastra. Cine pune tablespace-urile în read-only de la început, pentru a le copia cu calm în zilele anterioare, tocmai a mutat downtime-ul — nu l-a redus: o aplicație care nu poate scrie este oprită, indiferent dacă baza de date este deschisă sau nu.

### Faza 1 — Copiere inițială la cald (zile înainte)

Mai întâi self-containment-ul: niciun obiect din tablespace-urile de transportat nu trebuie să depindă de obiecte din afara lor.

```sql
-- Pe sursă
EXECUTE DBMS_TTS.TRANSPORT_SET_CHECK('DATA_01,DATA_02,IDX_01', TRUE);
SELECT * FROM transport_set_violations;
```

Dacă `transport_set_violations` este goală, se continuă. Backup-ul level 0 se ia **cu baza de date deschisă și în scriere**, cu `FOR TRANSPORT ALLOW INCONSISTENT` [1]: este clauza care autorizează RMAN să producă un backset transportabil din tablespace-uri inconsistente între ele, care vor fi realiniate de incrementalele ulterioare.

```bash
rman target /
BACKUP INCREMENTAL LEVEL 0
  FOR TRANSPORT ALLOW INCONSISTENT
  TABLESPACE DATA_01, DATA_02, IDX_01
  FORMAT '/backup/rman/xtts_l0_%U';
```

Backset-ul este transferat pe noul server via `rsync` sau replicare storage. Cu doisprezece terabytes pe rețea 10GbE, transferul necesită aproximativ trei-patru ore. **Între timp baza de date sursă lucrează normal**: nicio tablespace nu este în read-only, aplicațiile scriu, iar modificările care se acumulează sunt exact delta-ul pe care incrementalele îl vor recupera.

Pe target, datafile-urile se materializează ca *foreign datafile copy*:

```bash
# Pe target (CDB 21c, conectat la PDB de destinație)
rman target /
RESTORE FOREIGN TABLESPACE DATA_01, DATA_02, IDX_01 TO NEW
  FROM BACKUPSET '/backup/rman/xtts_l0_1_1';
```

### Faza 2 — Sincronizare incrementală

În zilele care separă copia inițială de fereastră se execută unul sau mai multe level 1, tot cu baza de date în scriere. Fiecare ciclu reduce gap-ul: primul incremental poate valora câteva sute de gigabytes, ultimul înainte de fereastră tipic câteva zeci.

```bash
# Pe sursă — baza de date mereu operațională
BACKUP INCREMENTAL LEVEL 1
  FOR TRANSPORT ALLOW INCONSISTENT
  TABLESPACE DATA_01, DATA_02, IDX_01
  FORMAT '/backup/rman/xtts_l1_%U';
```

Pe target, fiecare backset se aplică la foreign datafile copy-urile deja prezente, **unul câte unul și în ordinea în care a fost produs**:

```bash
# Pe target — un singur backupset per RECOVER
RECOVER FOREIGN DATAFILECOPY '/u02/oradata/pdb1/data_01.dbf',
                             '/u02/oradata/pdb1/data_02.dbf',
                             '/u02/oradata/pdb1/idx_01.dbf'
  FROM BACKUPSET '/backup/rman/xtts_l1_2_1';
```

Atenție la o limitare care nu se descoperă citind, ci dând cu capul de ea: **nu se pot aplica mai multe backupset-uri într-un singur `RECOVER`**. Fiecare incremental este o comandă separată, în secvență. Un script care le înlănțuie într-o singură comandă eșuează, și o face în cel mai prost moment.

### Faza 3 — Fereastra de patru ore

Ora 23:00, sâmbătă. Sursa este închisă aplicațiilor:

```sql
ALTER SYSTEM ENABLE RESTRICTED SESSION;
```

**Abia acum** tablespace-urile intră în read-only — este pasul care îngheață datele și deschide fereastra:

```sql
ALTER TABLESPACE data_01 READ ONLY;
ALTER TABLESPACE data_02 READ ONLY;
ALTER TABLESPACE idx_01 READ ONLY;
-- repetă pentru toate tablespace-urile aplicative
```

Ultimul incremental se ia acum, **fără** `ALLOW INCONSISTENT` (tablespace-urile sunt acum consistente) și cu `DATAPUMP FORMAT`, care face ca RMAN să producă și dump-ul metadatelor împreună cu backset-ul:

```bash
rman target /
BACKUP INCREMENTAL LEVEL 1
  FOR TRANSPORT
  DATAPUMP FORMAT '/backup/rman/xtts_meta.bck'
  TABLESPACE DATA_01, DATA_02, IDX_01
  FORMAT '/backup/rman/xtts_l1_final_%U';
```

Conține doar modificările din ultimele ore — tipic câțiva gigabytes. Transfer pe target și apply final:

```bash
# Pe target
RECOVER FOREIGN DATAFILECOPY '/u02/oradata/pdb1/data_01.dbf',
                             '/u02/oradata/pdb1/data_02.dbf',
                             '/u02/oradata/pdb1/idx_01.dbf'
  FROM BACKUPSET '/backup/rman/xtts_l1_final_3_1';
```

Rămâne plug-in-ul metadatelor în PDB-ul de destinație. Data Pump vrea un *directory object* — nu un path de filesystem — și lista completă a datafile-urilor:

```sql
-- Pe target, în interiorul PDB-ului
CREATE DIRECTORY dump_dir AS '/backup/rman';
```

```bash
impdp system/***@pdb1 \
  DIRECTORY=dump_dir \
  DUMPFILE=tts_export.dmp \
  LOGFILE=tts_import.log \
  TRANSPORT_TABLESPACES=DATA_01,DATA_02,IDX_01 \
  TRANSPORT_DATAFILES='/u02/oradata/pdb1/data_01.dbf','/u02/oradata/pdb1/data_02.dbf','/u02/oradata/pdb1/idx_01.dbf'
```

`DUMPFILE` este cel produs pe sursă cu exportul metadatelor TTS, care se lansează după ce tablespace-urile sunt în read-only:

```bash
# Pe sursă, cu tablespace-urile deja read-only
expdp system/*** \
  DIRECTORY=dump_dir \
  DUMPFILE=tts_export.dmp \
  LOGFILE=tts_export.log \
  TRANSPORT_TABLESPACES=DATA_01,DATA_02,IDX_01 \
  TRANSPORT_FULL_CHECK=Y
```

La acest punct tablespace-urile sunt în PDB, care se deschide și revine în scriere:

```sql
ALTER PLUGGABLE DATABASE pdb1 OPEN;
ALTER TABLESPACE data_01 READ WRITE;
ALTER TABLESPACE data_02 READ WRITE;
ALTER TABLESPACE idx_01 READ WRITE;
```

Niciun `dbupgrade` pe acest traseu: dicționarul de date nu este migrat, pentru că este cel al PDB-ului — creat deja la nivel 21c de CDB-ul care îl găzduiește. Este o diferență care merită reținută când se compară timpii cu cei ai unui upgrade in place, unde în schimb upgrade-ul dicționarului este faza dominantă.

---

## Ce manualele nu spun

Patru probleme care se descoperă doar când ești deja înăuntrul ferestrei.

**Password file**: formatul în sine nu se schimbă — `12.2` este default-ul atât în 12.2 cât și în 21c. Ceea ce se schimbă este toleranța: în 21c parametrul `IGNORECASE` nu mai este suportat și password file-urile sunt întotdeauna case-sensitive [6]. Un password file moștenit dintr-un mediu care convieția cu parole case-insensitive nu mai lasă să intre utilizatorii administrativi, și se întâmplă la primul `sqlplus sys as sysdba` de la distanță — adică în cel mai prost moment. Se regenerează pe target înainte de deschidere:

```bash
orapwd file=$ORACLE_HOME/dbs/orapwCDB1 password=<sys_password> format=12.2
```

**Auditing, și ce circulă pe internet**: versiunea care circulă este „în 21c auditing-ul tradițional a dispărut". Nu este așa, și diferența contează când planifici. În 21c default-ul rămâne **mixed mode** — unified auditing activ împreună cu auditing-ul tradițional — exact ca din 12c încoace; auditing-ul tradițional este **deprecat** în 21c și **scos din suport** abia din 23c [5]. *Pure* unified auditing nu este un parametru: se obține relinkând binarul Oracle cu `uniaud_on` și repornind instanța. Tradus în practică: migrarea nu obligă la refacerea politicilor de audit în acea noapte, dar nota de plată vine la release-ul următor — și merită pusă conversia în plan, nu descoperită când devine obligatorie.

**Auto-Indexing**: Oracle 21c are Auto-Indexing activabil (introdus în 19c). Dacă nu se dorește ca Oracle să înceapă să creeze indecși automat pe noua bază de date, trebuie dezactivat explicit:

```sql
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE','OFF');
```

**CDB-ul nu este o decizie de amânat**: cine vine din 12.2 tinde să trateze multitenant ca o decizie arhitecturală de luat cu calm, poate la release-ul următor. În 21c acel calm nu există: non-CDB nu mai este suportat, deci destinația este o PDB și atât. Consecința operațională este că CDB-ul trebuie creat și testat **înainte** de fereastră, cu `db_name`-ul său, parametrii de memorie, serviciile — și trebuie aduse în PDB obiectele care în vechea bază de date trăiau în afara tablespace-urilor transportate: profiluri, roluri, utilizatori, directory object-uri, DB link-uri, job-uri din scheduler. Nu călătoresc cu TTS, și sunt elementul care cel mai des se descoperă lipsă luni dimineața.

---

## Cifrele nopții

Distincția care contează este între ce s-a întâmplat **înainte**, cu baza de date în producție, și ce s-a întâmplat **înăuntrul** ferestrei. Doar a doua tabelă reprezintă downtime.

**În afara ferestrei — baza de date deschisă, aplicații operative**

| Fază | Durată |
|---|---|
| Backup RMAN level 0 `FOR TRANSPORT ALLOW INCONSISTENT` | 1h 15min |
| Transfer backset (11,8 TB via rsync pe 10GbE) | 3h 40min |
| `RESTORE FOREIGN TABLESPACE` pe target | 48 min |
| Level 1 intermediare din zilele următoare + apply | 1h 05min |
| **Total lucru pregătitor** | **6h 48min** |

**Înăuntrul ferestrei — downtime aplicativ**

| Fază | Durată |
|---|---|
| Restricted session + tablespace-uri în read-only | 9 min |
| Ultimul level 1 `FOR TRANSPORT` + `DATAPUMP` (delta ~180 GB) | 22 min |
| Export metadate TTS pe sursă | 12 min |
| Transfer delta + dump pe target | 25 min |
| `RECOVER FOREIGN DATAFILECOPY` final | 18 min |
| `impdp` plug-in metadate în PDB | 12 min |
| Deschidere PDB + tablespace-uri în read-write | 4 min |
| Recreare obiecte netransportate (utilizatori, roluri, DB link-uri, job-uri) | 35 min |
| Statistici dicționar + recompilare obiecte invalide | 45 min |
| Validare și smoke test aplicativ | 50 min |
| **Total fereastră de downtime** | **3h 52min** |

Opt minute marjă față de patru ore. Nu e mult, dar a fost suficient.

Merită privite cele două tabele împreună: munca totală a fost aproape unsprezece ore, din care mai puțin de patru vizibile utilizatorului. Nu am făcut migrarea mai rapidă — am mutat-o aproape în întregime în afara ferestrei. Este singurul lucru pe care această metodă știe să-l facă, și era tot ce era necesar.

---

## Validare: controalele care nu se sar

După deschiderea PDB-ului, validarea nu este opțională. Patru controale în ordinea corectă — toate de executat **înăuntrul PDB-ului**, nu în root-ul CDB-ului, altfel se privește baza de date greșită:

```sql
ALTER SESSION SET CONTAINER = pdb1;
```

**Obiecte invalide**: plug-in-ul metadatelor poate lăsa obiecte aplicative invalide, tipic din cauza dependențelor față de obiecte încă nerecreate. `utl_recomp` le recompilează:

```sql
EXECUTE UTL_RECOMP.RECOMP_SERIAL();
-- sau paralel
EXECUTE UTL_RECOMP.RECOMP_PARALLEL(4);
```

**Violări ale plug-in-ului**: este controlul specific acestui traseu, fără echivalent într-un upgrade in place. `PDB_PLUG_IN_VIOLATIONS` listează ce a găsit CDB-ul incompatibil când a primit PDB-ul — opțiuni neinstalate, parametri sub prag, componente lipsă:

```sql
SELECT name, cause, type, status, message
FROM pdb_plug_in_violations
WHERE status <> 'RESOLVED'
ORDER BY time;
```

Rândurile de tip `ERROR` trebuie rezolvate înainte de a declara migrarea închisă; cele `WARNING` se citesc una câte una, nu se arhivează în bloc.

**Statistici optimizer**: statisticile dicționarului trebuie regenerate. Statisticile obiectelor aplicative pot fi importate de pe sursă sau regenerate:

```sql
EXECUTE DBMS_STATS.GATHER_DICTIONARY_STATS;
EXECUTE DBMS_STATS.GATHER_FIXED_OBJECTS_STATS;
```

**Verificare componente**: toate componentele Oracle trebuie să fie în starea `VALID`:

```sql
SELECT comp_name, version, status FROM dba_registry ORDER BY comp_name;
```

Orice componentă în starea `INVALID` sau `UPGRADED` (în loc de `VALID`) necesită atenție înainte de a declara migrarea completă. Într-un PDB proaspăt populat via TTS, registrul reflectă CDB-ul care îl găzduiește: dacă ceva este invalid acolo, problema aparține containerului, nu transportului.

---

## Ce rămâne din runbook

Migrarea a mers. PDB-ul este în producție de luni dimineața, aplicațiile nu au observat nimic — sau aproape: câteva query-uri cu hint-uri obsolete au necesitat revizuire în zilele următoare, pentru că optimizer-ul 21c are statistici mai precise și alege planuri diferite.

Punctul care merită reținut nu este tehnica specifică — TTS plus RMAN incremental este o strategie documentată, nu o invenție. Este raționamentul care precede alegerea: a înțelege de ce Data Pump nu funcționează la acea scară, a înțelege care sunt constrângerile reale (fereastră, spațiu, arhitectura de destinație), și a alege combinația de instrumente care le respectă. Constrângerea care a cântărit cel mai mult nu a fost nici măcar tehnică în sens strict: a fost descoperirea la timp că non-CDB nu mai exista ca destinație. A o descoperi târziu nu prelungește fereastra — schimbă proiectul.

Partea cea mai lungă nu a fost noaptea de sâmbătă. A fost săptămâna dinaintea: pre-check-urile cu AutoUpgrade, testele pe target cu un subset de date, proba plug-in-ului pe un PDB de colaudare, verificarea că fiecare pas din runbook producea output-ul așteptat. Când ajungi la fereastra de patru ore cu un runbook deja testat, surprizele sunt gestionabile. Când ajungi fără să-l fi testat, acele opt minute de marjă devin zero foarte repede.

---

## Fonti ufficiali

1. Oracle Database Backup and Recovery User's Guide 21c — [Transporting Data Across Platforms](https://docs.oracle.com/en/database/oracle/oracle-database/21/bradv/rman-transporting-data-across-platforms.html) (`BACKUP … FOR TRANSPORT ALLOW INCONSISTENT`, `RESTORE FOREIGN TABLESPACE`, `RECOVER FOREIGN DATAFILECOPY`)
2. Oracle Database Administrator's Guide 21c — [Transporting Tablespaces Between Databases](https://docs.oracle.com/en/database/oracle/oracle-database/21/admin/transporting-data.html)
3. Oracle Database Upgrade Guide 21c — [Manual Non-CDB Release Upgrades to Multitenant Architecture](https://docs.oracle.com/en/database/oracle/oracle-database/21/upgrd/upgrade-scenarios-non-cdb-oracle-databases.html) (renunțarea la suportul pentru arhitectura non-CDB)
4. Oracle Database Upgrade Guide 21c — [Using the Pre-Upgrade Information Tool](https://docs.oracle.com/en/database/oracle/oracle-database/21/upgrd/using-preupgrade-information-tool-for-oracle-database.html) (`preupgrade.jar` non più distribuito, funzioni confluite in AutoUpgrade)
5. Oracle Database Security Guide 21c — [Introduction to Auditing](https://docs.oracle.com/en/database/oracle/oracle-database/21/dbseg/introduction-to-auditing.html) (mixed mode di default, `uniaud_on` per il pure unified auditing)
6. Oracle Database Administrator's Reference 21c — [Creating and Populating Password Files](https://docs.oracle.com/en/database/oracle/oracle-database/21/ntqrf/creating-and-populating-password-files.html) (`format`, renunțarea la suportul pentru `IGNORECASE`)

---

## Glosar candidat

- **Transportable Tablespaces (TTS)** — tehnică Oracle care permite mutarea tablespace-urilor între baze de date copiind datafile-urile fizice și importând doar metadatele via Data Pump. Mult mai rapidă decât un export/import complet pe volume mari.

- **RMAN Incremental Backup** — backup RMAN care înregistrează doar blocurile modificate față de ultimul backup de nivel egal sau superior. Level 0 este baza completă, level 1 este delta. Folosit în migrare pentru a sincroniza gap-ul dintre copia inițială și fereastra de downtime.

- **AutoUpgrade** — utilitar Java (`autoupgrade.jar`) care din Oracle 21c este instrumentul unic pentru analiza pre-upgrade, corecții și upgrade-ul propriu-zis. Cu `-preupgrade … -mode analyze` produce în mod read-only raportul care anterior se obținea cu `preupgrade.jar`, care nu mai este distribuit.

- **Foreign datafile copy** — datafile pe care RMAN îl materializează pe baza de date de destinație pornind de la un backset transportabil, înainte ca tablespace-urile să fie conectate. Este obiectul pe care acționează `RESTORE FOREIGN TABLESPACE` și `RECOVER FOREIGN DATAFILECOPY` în transportul incremental.

- **Unified Auditing** — framework de auditing introdus în 12c care consolidează log-urile (database, fine-grained, SYSDBA) în structura `AUDSYS`. În 21c coexistă cu auditing-ul tradițional în *mixed mode*, care rămâne default-ul; *pure* unified auditing necesită relink-ul binarului cu `uniaud_on`.

- **Auto-Indexing** — funcționalitate Oracle (disponibilă din 19
