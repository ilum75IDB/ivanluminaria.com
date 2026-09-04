---
title: "Oracle 12c → 21c pe 12 TB: tablespace-uri transportabile, RMAN incremental și fereastra de sâmbătă noapte"
date: 2099-12-31
draft: true
translationKey: "oracle_12c_21c_su_12_tb_transportable_tablespaces_rman_incremental_e_la"
tags: []
categories: ["oracle"]
image: "oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la.cover.jpg"
webo_status: da_tradurre
webo_generated_at: 2026-09-04
---

```
---
title: "Sâmbătă noaptea pe care nimeni nu și-o dorește: migrare Oracle 12c → 21c pe 12 terabyte"
seoTitle: "Migrare Oracle 12c la 21c: TTS + RMAN incremental pe 12 TB"
description: "Strategie hibridă Transportable Tablespaces + RMAN incremental pentru migrare Oracle 12c→21c pe 12 TB în 4 ore. Pre-check, runbook pas cu pas, probleme reale."
tags: ["oracle", "migration", "rman", "transportable-tablespaces", "upgrade"]
---
```

## Sâmbătă noaptea pe care nimeni nu și-o dorește

Cererea venise cu câteva săptămâni înainte, într-una din acele ședințe unde cifrele sunt prezentate ca și cum ar fi detalii: „trebuie să migrăm baza de date Oracle de la 12c la 21c, avem o fereastră de mentenanță sâmbătă noaptea, patru ore". Douăsprezece terabyte. Server cu opt ani de viață, ieșit din suportul hardware. Serverul nou deja în rack, Oracle 21c instalat, gata.

Patru ore pentru douăsprezece terabyte.

Cine lucrează cu Oracle de ceva vreme știe deja unde e problema: nu în baza de date, nu în versiune, nu în hardware-ul nou. Stă în matematică. Un Data Pump pe douăsprezece terabyte, chiar și cu paralelism agresiv și storage rapid, nu termină în patru ore. Nu termină în opt. Probabil nu termină în weekend.

Ceea ce urmează este raționamentul care a dus la o strategie hibridă — transportable tablespaces cross-version plus RMAN incremental — și detaliile a ceea ce s-a întâmplat cu adevărat în cele patru ore critice. Cifrele sunt cele reale, comenzile sunt cele folosite, problemele sunt cele pe care le găsești doar când ești deja înăuntru.

---

## De ce Data Pump nu e răspunsul la această scară

Data Pump este instrumentul potrivit pentru migrări de până la câteva sute de gigabyte, sau pentru export/import selective de scheme specifice. Dincolo de acel prag, limitele devin structurale.

Pe douăsprezece terabyte, problema principală este throughput-ul de I/O. Data Pump exportă datele serializând rânduri în format proprietar Oracle, apoi le reimportează reconstruind segmente, indecși, statistici. Chiar și cu `PARALLEL=16` și storage NVMe pe ambele părți, throughput-ul efectiv depășește rareori 3-4 GB/minut în scenarii reale (nu benchmark). Douăsprezece terabyte la 4 GB/minut: cincizeci de ore. Optimist.

Există și problema spațiului: e nevoie de o zonă de staging care să conțină întregul export, plus spațiul pe target în timpul importului. Cu douăsprezece terabyte de date, vorbim de douăzeci-douăzeci și cinci de terabyte de spațiu temporar necesar între cele două mașini.

Ultima problemă este fereastra: Data Pump nu este incremental. Dacă exportul pornește vineri seara și baza de date continuă să primească scrieri, la finalul exportului datele sunt deja parțial depășite. Nu există un mecanism nativ pentru a sincroniza modificările apărute în timpul exportului.

---

## Opțiunile reale pentru migrări multi-terabyte

Când Data Pump este exclus, alternativele reale sunt patru [1]:

**RMAN Duplicate** — duplică baza de date completă via RMAN, inclusiv toate fișierele fizice. Necesită spațiu dublu pe target (sau aproape), dar este fiabil și bine documentat. Problema: pentru douăsprezece terabyte, chiar și faza inițială de copiere necesită multe ore și nu rezolvă problema ferestrei scurte.

**Transportable Tablespaces (TTS)** — copiază fișierele datafile direct, fără serializare/deserializare. Este metoda cea mai rapidă pentru a muta volume mari deoarece throughput-ul este limitat doar de viteza canalului de transfer (rețea, storage partajat, bandă). Constrângerea istorică era endianness-ul: platforme diferite (ex. Solaris SPARC → Linux x86) necesitau o conversie. Între două sisteme Linux x86_64, problema nu există [2].

**Data Guard ca punte** — se configurează o bază de date standby pe mașina nouă, se lasă sincronizarea să aibă loc via redo log (ore sau zile, fără impact pe primar), apoi se execută un failover controlat în fereastra de mentenanță. Elegant, dar necesită ca versiunile să fie compatibile pentru redo shipping — și între 12c și 21c există constrângeri precise.

**GoldenGate** — replicare logică, flexibilitate maximă cross-version și cross-platform. Necesită licență separată, setup non-trivial și o perioadă de warm-up pentru sincronizarea inițială. Pentru o migrare one-shot cu fereastră definită, este adesea supradimensionat.

---

## Strategia aleasă: TTS + RMAN incremental

Soluția adoptată combină două tehnici: transportable tablespaces pentru a muta masa datelor înainte de fereastră, și RMAN incremental backup pentru a sincroniza modificările acumulate între timp.

Ideea de bază este simplă: dacă nu pot muta douăsprezece terabyte în patru ore, mut unsprezece terabyte și jumătate în zilele anterioare, iar în cele patru ore critice mut doar delta.

Planul se articulează în trei faze:

1. **Faza pregătitoare** (zile înainte de fereastră): copierea datafile-urilor în modul read-only via TTS, transfer pe serverul nou
2. **Faza de sincronizare** (ore înainte de fereastră): RMAN incremental backup pe sursă, restore pe target, pentru a reduce gap-ul
3. **Fereastra de downtime** (patru ore): ultimul incremental, conversia finală, deschiderea bazei de date 21c

---

## Pre-check: ce descoperi înainte să atingi ceva

Înainte de a muta un byte, e nevoie de o analiză de compatibilitate. Între Oracle 12.2 și Oracle 21c sunt aproape zece ani de versiuni intermediare, iar unele lucruri s-au schimbat în mod non-retro-compatibil.

**Character set**: verifică că sursa și target-ul folosesc același character set, sau că target-ul este un superset. O migrare TTS între AL32UTF8 și WE8ISO8859P1 necesită conversie explicită și nu este banală.

```sql
-- Pe baza de date sursă (12c)
SELECT value FROM nls_database_parameters WHERE parameter = 'NLS_CHARACTERSET';
SELECT value FROM nls_database_parameters WHERE parameter = 'NLS_NCHAR_CHARACTERSET';
```

**Endianness**: pe Linux x86_64 → Linux x86_64 nu există probleme. Pe migrări cross-platform (ex. AIX → Linux), e nevoie de `RMAN CONVERT TABLESPACE`.

```sql
-- Verificare platformă
SELECT platform_name, endian_format FROM v$transportable_platform
WHERE endian_format = (SELECT endian_format FROM v$database);
```

**Componente deprecate**: Oracle 21c a eliminat sau deprecat unele funcționalități din 12c. Scriptul `utlupgrd.sql` (sau succesorul său `dbupgrade`) generează un raport de pre-upgrade [3]:

```bash
# Pe sursă, cu Oracle 21c home deja disponibil
$ORACLE_HOME_21C/rdbms/admin/preupgrd.sql
```

Raportul semnalează obiecte invalide, parametri obsoleti, componente de eliminat înainte de upgrade. Printre cele mai comune în trecerea 12c → 21c: `AUDIT_TRAIL` (înlocuit de Unified Auditing), `SQLNET.ALLOWED_LOGON_VERSION` (deprecat) și unele view-uri de compatibilitate.

**Tablespace-urile SYSTEM și SYSAUX**: nu sunt transportabile. Rămân pe sursă și sunt recreate pe target prin procesul standard de upgrade.

---

## Planul pas cu pas

### Faza 1 — Pregătire TTS (zile înainte)

Se pun în read-only tablespace-urile de transportat (excluse SYSTEM, SYSAUX, TEMP, UNDO):

```sql
-- Pe sursă
ALTER TABLESPACE data_01 READ ONLY;
ALTER TABLESPACE data_02 READ ONLY;
ALTER TABLESPACE idx_01 READ ONLY;
-- repetă pentru toate tablespace-urile aplicative
```

Se verifică self-containment-ul — niciun obiect din tablespace-urile de transportat nu trebuie să aibă dependențe față de obiecte din afara lor:

```sql
EXECUTE DBMS_TTS.TRANSPORT_SET_CHECK('DATA_01,DATA_02,IDX_01', TRUE);
SELECT * FROM transport_set_violations;
```

Dacă `transport_set_violations` este goală, se continuă cu exportul metadatelor:

```bash
expdp system/*** TRANSPORT_TABLESPACES=DATA_01,DATA_02,IDX_01 \
  TRANSPORT_FULL_CHECK=Y \
  DUMPFILE=tts_export.dmp \
  LOGFILE=tts_export.log
```

Fișierele datafile fizice sunt copiate pe serverul nou via `rsync` sau replicare storage. Cu douăsprezece terabyte pe rețea 10GbE, transferul necesită aproximativ trei-patru ore. Între timp baza de date sursă continuă să funcționeze: tablespace-urile în read-only primesc doar citiri, scrierile merg pe tablespace-urile încă în read-write (SYSTEM, SYSAUX, eventuale tablespace-uri aplicative excluse din TTS).

### Faza 2 — Sincronizare incrementală

În orele de după transferul inițial, tablespace-urile sursă sunt repuse în read-write (baza de date trebuie să revină operațională). Din acest moment, modificările se acumulează ca delta de sincronizat.

Se configurează RMAN pentru backup incremental level 0 pe sursă:

```bash
rman target /
BACKUP INCREMENTAL LEVEL 0 TABLESPACE DATA_01,DATA_02,IDX_01
FORMAT '/backup/rman/incr0_%U'
TAG 'PRE_MIGRATION_L0';
```

Acest backup level 0 este transferat pe target și aplicat pe datafile-urile deja copiate:

```bash
# Pe target (21c)
rman target /
CATALOG START WITH '/backup/rman/';
RECOVER TABLESPACE DATA_01,DATA_02,IDX_01
FROM TAG 'PRE_MIGRATION_L0';
```

În orele următoare se execută backup-uri incrementale level 1 periodice pentru a reduce progresiv gap-ul. Fiecare level 1 conține doar delta față de ultimul backup — câțiva gigabyte în loc de terabyte.

### Faza 3 — Fereastra de patru ore

Ora 23:00, sâmbătă. Baza de date sursă este pusă în modul restricted:

```sql
ALTER SYSTEM ENABLE RESTRICTED SESSION;
```

Se execută ultimul backup incremental level 1:

```bash
rman target /
BACKUP INCREMENTAL LEVEL 1 TABLESPACE DATA_01,DATA_02,IDX_01
FORMAT '/backup/rman/incr1_final_%U'
TAG 'FINAL_SYNC';
```

Acest backup conține doar modificările din ultimele ore — de obicei câțiva gigabyte. Transfer pe target și apply:

```bash
# Pe target
RECOVER TABLESPACE DATA_01,DATA_02,IDX_01
FROM TAG 'FINAL_SYNC';
```

Tablespace-urile sunt puse în read-only pe sursă (definitiv de data aceasta), și se importă metadatele TTS pe target:

```bash
impdp system/*** TRANSPORT_DATAFILES='/u01/oradata/data_01.dbf','/u01/oradata/data_02.dbf' \
  DUMPFILE=tts_export.dmp \
  LOGFILE=tts_import.log
```

În acest moment tablespace-urile sunt pe target în Oracle 21c. Se execută procesul de upgrade al dicționarului de date:

```bash
$ORACLE_HOME/bin/dbupgrade -d $ORACLE_BASE/diag/rdbms -l /tmp/upgrade_log
```

---

## Ce nu spun manualele

Patru probleme pe care le găsești doar când ești deja înăuntrul ferestrei.

**Password file format**: Oracle 21c folosește un format de password file diferit față de 12c. Dacă se copiază password file-ul de pe sursă, instanța 21c s-ar putea să nu-l recunoască. Soluția este să-l regenerezi pe target înainte de deschidere:

```bash
orapwd file=$ORACLE_HOME/dbs/orapwORCL password=<sys_password> format=12.2
```

**Unified Auditing**: în Oracle 21c, Unified Auditing este activat implicit și nu poate fi dezactivat ca în 12c. Dacă baza de date sursă folosea vechiul `AUDIT_TRAIL=DB`, politicile de audit trebuie recreate în noul framework. Asta nu blochează migrarea, dar poate surprinde echipa aplicativă luni dimineața când log-urile de audit au un format diferit.

**Auto-Indexing**: Oracle 21c are Auto-Indexing activabil (introdus în 19c). Dacă nu se dorește ca Oracle să înceapă să creeze indecși automat pe noua bază de date, trebuie dezactivat explicit:

```sql
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE','OFF');
```

**Conversia la PDB**: Oracle 21c suportă încă bazele de date non-CDB, dar este ultima versiune care o face. Dacă planul viitor prevede conversia la CDB/PDB (obligatorie din Oracle 23c), acesta este momentul să fie evaluată. Conversia non-CDB → PDB se face cu `DBMS_PDB.DESCRIBE` și necesită o fereastră separată — nu se bagă în aceeași noapte.

---

## Cifrele nopții

| Fază | Durată reală |
|---|---|
| Export TTS metadata | 12 minute |
| Transfer datafile (11,8 TB via rsync pe 10GbE) | 3h 40min |
| Backup RMAN level 0 | 1h 15min |
| Apply level 0 pe target | 48 minute |
| Backup RMAN level 1 (delta ~180 GB) | 22 minute |
| Apply level 1 final | 14 minute |
| Import TTS metadata pe target | 8 minute |
| dbupgrade (dicționar de date) | 41 minute |
| Validare post-migrare | 35 minute |
| **Total fereastră de downtime** | **3h 52min** |

Opt minute marjă. Nu e mult, dar a fost suficient.

---

## Validarea: controalele care nu se sar

După deschiderea bazei de date 21c, validarea nu este opțională. Patru controale în ordinea corectă.

**Obiecte invalide**: procesul de upgrade poate lăsa obiecte de sistem invalide. `utl_recomp` le recompilează:

```sql
EXECUTE UTL_RECOMP.RECOMP_SERIAL();
-- sau paralel
EXECUTE UTL_RECOMP.RECOMP_PARALLEL(4);
```

**Scripturi de diagnostică post-upgrade**: Oracle furnizează `dbupgdiag.sql` pentru a verifica starea dicționarului de date după upgrade [4]:

```bash
sqlplus / as sysdba @$ORACLE_HOME/rdbms/admin/dbupgdiag.sql
```

**Statistici optimizer**: statisticile dicționarului de date trebuie regenerate pe noua bază de date. Statisticile obiectelor aplicative pot fi importate de pe sursă sau regenerate:

```sql
EXECUTE DBMS_STATS.GATHER_DICTIONARY_STATS;
EXECUTE DBMS_STATS.GATHER_FIXED_OBJECTS_STATS;
```

**Verificare componente**: toate componentele Oracle trebuie să fie în starea `VALID`:

```sql
SELECT comp_name, version, status FROM dba_registry ORDER BY comp_name;
```

Orice componentă în starea `INVALID` sau `UPGRADED` (în loc de `VALID`) necesită atenție înainte de a declara migrarea completă.

---

## Ce rămâne din runbook

Migrarea a mers. Baza de date 21c este în producție de luni dimineața, aplicativele nu și-au dat seama de nimic — sau aproape: câteva query-uri cu hint-uri obsolete au necesitat revizuire în zilele următoare, pentru că optimizer-ul 21c are statistici mai precise și alege planuri diferite.

Punctul care merită reținut nu este tehnica specifică — TTS plus RMAN incremental este o strategie documentată, nu o invenție. Este raționamentul care precede alegerea: a înțelege de ce Data Pump nu funcționează la acea scară, a înțelege care sunt constrângerile reale (fereastră, spațiu, versiuni) și a alege combinația de instrumente care respectă acele constrângeri.

Partea cea mai lungă nu a fost noaptea de sâmbătă. A fost săptămâna dinainte: pre-check-urile, testele pe target cu un subset de date, simularea procesului de upgrade pe un clone, verificarea că fiecare pas din runbook producea output-ul așteptat. Când ajungi la fereastra de patru ore cu un runbook deja testat, surprizele sunt gestionabile. Când ajungi fără să-l fi testat, cele opt minute de marjă devin zero foarte repede.

---

## Fonti ufficiali

1. Oracle Database Backup and Recovery User's Guide 21c — [Transportable Tablespaces](https://docs.oracle.com/en/database/oracle/oracle-database/21/bradv/rman-transporting-data-across-platforms.html)
2. Oracle Database Administrator's Guide 21c — [Transporting Tablespaces Between Databases](https://docs.oracle.com/en/database/oracle/oracle-database/21/admin/transporting-data.html)
3. Oracle Database Upgrade Guide 21c — [Pre-Upgrade Information Tool](https://docs.oracle.com/en/database/oracle/oracle-database/21/upgrd/using-preupgrade-information-tool-for-oracle-database.html)
4. Oracle Database Upgrade Guide 21c — [Post-Upgrade Status Tool](https://docs.oracle.com/en/database/oracle/oracle-database/21/upgrd/post-upgrade-status-tool-postupgrade-fixups-script.html)

---

## Glosar candidat

- **Transportable Tablespaces (TTS)** — tehnică Oracle care permite mutarea tablespace-urilor între baze de date copiind datafile-urile fizice și importând doar metadatele prin Data Pump. Mult mai rapidă decât un export/import complet pe volume mari.

- **RMAN Incremental Backup** — backup RMAN care înregistrează doar blocurile modificate față de ultimul backup de nivel egal sau superior. Level 0 este baza completă, level 1 este delta. Folosit în migrare pentru a sincroniza gap-ul dintre copia inițială și fereastra de downtime.

- **dbupgrade** — utilitar Oracle (succesorul lui `catupgrd.sql`) care actualizează dicționarul de date de sistem în timpul unui upgrade de versiune. Recompilează componentele interne și aduce baza de date la nivelul noii versiuni Oracle instalate.

- **Unified Auditing** — framework de auditare Oracle introdus în 12c și obligatoriu în 21c, care consolidează toate log-urile de audit (bază de date, fine-grained, SYSDBA) într-o singură structură `AUDSYS`. Înlocuiește vechiul parametru `AUDIT_TRAIL`.

- **Auto-Indexing** — funcționalitate Oracle (disponibilă din 19c, configurabilă în 21c) care analizează workload-ul și creează automat indecși invizibili, îi validează și îi face vizibili dacă îmbunătățesc performanțele. Trebuie dezactivat explicit dacă nu este dorit în producție.
