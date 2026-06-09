---
title: "ORA-00205 alle tre di notte: capire i file critici Oracle prima di averne bisogno"
date: 2099-12-31
draft: true
section: oracle
webo_status: da_tradurre
webo_generated_at: 2026-06-09
---

## Apelul

[3:08] Telefonul vibrează pe noptieră. E Paolo, DBA-ul clientului farmaceutic — Oracle 19c, trasabilitate loturi, conformitate reglementară. Fereastra de mentenanță storage se închisese la 2:30. El încercase startup-ul. Instanța nu pornise.

Îmi citește mesajul de pe telefon, cu voce plată, dar cu acea tensiune subtilă a celui care știe că sistemul e oprit și nu știe încă de ce:

```text
ORA-00205: error in identifying control file
  '/u01/app/oracle/oradata/PHARMDB/control01.ctl'
```

E prima urgență reală pe care o gestionează ca persoană de gardă. Nu e nepregătit: cunoaște Oracle, știe să folosească comenzile, a citit documentația clientului. Problema e că acea documentație e scrisă ca referință, nu ca metodă. Și în acel moment are nevoie de o metodă.

---

## Faza MOUNT

[3:09] Primul lucru pe care îl întreb nu e „ai verificat permisiunile?" sau „listener-ul e pornit?". Îl întreb: „în ce fază de startup s-a oprit Oracle?".

Nu e o întrebare retorică. E punctul de plecare al oricărui diagnostic pe o instanță care nu pornește.

Oracle pornește un database în trei faze distincte [1]:

**`NOMOUNT`** — Oracle alocă SGA și pornește procesele de fundal citind **parameter file**-ul (SPFILE sau PFILE). În această fază nu cunoaște încă baza de date fizică: știe doar cum să configureze instanța în memorie.

**`MOUNT`** — Oracle citește **control file**-ul. Aici instanța „descoperă" structura fizică a bazei de date: ce datafile-uri există, unde se află, care e SCN-ul curent, care e starea redo log-urilor. Abia după MOUNT Oracle știe ce gestionează.

**`OPEN`** — Oracle verifică consistența **online redo log file**-urilor și a datafile-urilor, aplică recovery dacă e necesar și deschide baza de date utilizatorilor.

Consecința practică e directă: dacă parameter file-ul e corupt sau lipsește, Oracle nu ajunge nici măcar la NOMOUNT. Dacă control file-ul e inaccesibil, instanța se oprește la MOUNT. Dacă redo log-urile sunt corupte, blocajul apare în OPEN.

A cunoaște această secvență înseamnă a ști, citind un cod ORA, în ce fază s-a oprit totul — și deci ce fișier să cauți primul, fără ipoteze în orb.

Paolo se gândește o secundă. „ORA-00205 e în MOUNT. Deci e control file-ul."

Exact.

---

## Control file-ul și remontarea

[3:11] Îi dictez cele trei verificări de făcut în secvență, în această ordine:

**(a)** dă-mi path-ul exact din mesajul ORA-00205
**(b)** `ls -la` pe acel path și spune-mi proprietarul și permisiunile
**(c)** compară cu runbook-ul de pre-mentenanță pe care îl scriserăm împreună cu un an înainte

În timp ce Paolo deschide terminalul, îi explic de ce control file-ul e punctul critic al acelei faze.

Control file-ul e un fișier binar pe care Oracle îl actualizează continuu în timpul funcționării. Conține informații pe care niciun alt fișier nu le poate furniza [3]:

- numele bazei de date (`db_name`)
- lista tuturor datafile-urilor cu path-urile și statusul lor
- lista online redo log file-urilor
- SCN-ul (System Change Number) curent — „timestamp-ul logic" al bazei de date
- informațiile de checkpoint
- catalogul backup-urilor RMAN, când se folosește RMAN cu control file-ul ca repository

Oracle nu poate monta baza de date fără control file: i-ar lipsi modalitatea de a ști ce datafile-uri aparțin instanței, care e starea lor și dacă baza de date e consistentă. E o dependență structurală.

Pentru a verifica control file-urile pe o instanță activă [4]:

```sql
SELECT name FROM v$controlfile;
```

Pe `oracle-node-01` cu SID-ul `PHARMDB`, output-ul cu o configurație multiplexată e:

```text
NAME
--------------------------------------------------
/u01/app/oracle/oradata/PHARMDB/control01.ctl
/u02/app/oracle/fast_recovery_area/PHARMDB/control02.ctl
```

Două copii, pe path-uri fizic separate. Multiplexarea nu e opțională: dacă control file-ul trăiește pe un singur disc și acel disc are o problemă, baza de date nu se deschide și recovery-ul devine semnificativ mai complex. Se configurează în parameter file:

```text
control_files = '/u01/app/oracle/oradata/PHARMDB/control01.ctl',
                '/u02/app/oracle/fast_recovery_area/PHARMDB/control02.ctl'
```

Oracle scrie sincron pe toate copiile. Dacă una devine inaccesibilă, înregistrează eroarea și continuă să funcționeze cu copiile rămase — atât timp cât cel puțin una e disponibilă.

**Notă despre ASM**: în mediile care folosesc Automatic Storage Management, path-urile fizice sunt înlocuite cu path-uri logice de tipul `+DATA/PHARMDB/CONTROLFILE/current.260.1234567890`. Conceptul rămâne identic — sunt tot aceleași trei tipuri de fișiere critice — se schimbă doar gestionarea fizică, delegată ASM-ului. Comenzile SQL de verificare sunt aceleași; se schimbă doar output-ul.

[3:14] Paolo face `ls -la`. Permisiunile s-au schimbat: înainte de mentenanță proprietarul era `oracle:oinstall`, acum e `root:root`. Oracle nu poate citi fișierul.

Control file-ul era fizic intact. Echipa de storage remontase filesystem-ul `/u01` cu permisiuni diferite după mentenanță, iar Oracle nu reușea să îl deschidă.

Îi spun imediat: „ok, sunăm storage. Nu atinge nimic tu, niciun `chmod` manual." Nu pentru că n-ar ști să o facă — ar ști — ci pentru că într-un sistem de conformitate reglementară orice modificare manuală în afara procedurii devine o problemă documentară pe lângă cea tehnică. Fix-ul trebuie să treacă prin echipa de storage, cu ticket deschis și urmărit.

În timp ce așteptăm ca storage să se conecteze, îi atrag atenția asupra unui lucru: dacă `ls -la` ar fi arătat fișierul intact și accesibil, pasul următor ar fi fost să urcăm o fază, la parameter file. Eroare diferită, fază diferită: tipic `ORA-01078` (failure in processing system parameters) sau `LRM-00109` (could not open parameter file), și în acel caz Oracle nu ar fi ajuns nici măcar la NOMOUNT.

Parameter file-ul e punctul de plecare absolut: Oracle îl citește înaintea oricărui alt lucru pentru a ști cum să configureze instanța în memorie, și mai ales pentru a ști unde se află control file-urile. Parametrul `control_files` care indică path-urile e conținut tocmai acolo.

Există două variante [2]:

**PFILE** (`init<SID>.ora`) — fișier text, modificabil cu orice editor. Necesită un restart pentru a aplica modificările. Util în medii de dezvoltare sau ca backup lizibil al parametrilor.

**SPFILE** (`spfile<SID>.ora`) — fișier binar, gestionat de Oracle. Permite modificări la cald cu `ALTER SYSTEM SET` fără a reporni instanța. În producție se folosește aproape întotdeauna SPFILE.

Ordinea de căutare Oracle e precisă: caută mai întâi SPFILE-ul în path-ul implicit, apoi PFILE-ul. Pe Linux/Unix:

```bash
# SPFILE (implicit)
$ORACLE_HOME/dbs/spfilePHARMDB.ora

# PFILE (fallback)
$ORACLE_HOME/dbs/initPHARMDB.ora
```

Pentru a verifica ce parameter file e în uz pe o instanță activă:

```sql
-- Dacă VALUE e gol, Oracle folosește un PFILE
SHOW PARAMETER spfile;
```

Paolo notează. În cazul nostru parameter file-ul era în regulă — problema era o fază mai departe — și modelul mental e acum complet.

---

## Startup-ul complet

[3:23] Storage aplică `chmod 640` și restaurează `oracle:oinstall` ca proprietar pe fișierele din `/u01`. Paolo repornește instanța.

[3:38] Instanța trece de MOUNT. Apoi se oprește în OPEN cu un warning pe redo log-uri.

Îi explic ce vede.

Online redo log file-urile sunt ultimul element al triadei critice. Fiecare modificare care are loc în baza de date — un `INSERT`, un `UPDATE`, un `DELETE` — e scrisă mai întâi în redo log-uri, și abia ulterior (asincron) pe datafile-uri. Acest mecanism se numește **write-ahead logging**: dacă sistemul cade înainte ca datele să fie scrise pe datafile-uri, Oracle poate reconstrui modificările citind redo log-urile. Fără redo log-uri, Oracle nu poate garanta consistența bazei de date în caz de crash — și de aceea, dacă sunt corupte sau lipsesc, baza de date nu se deschide [5].

Redo log-urile sunt organizate în **grupuri**. Oracle scrie circular: umple grupul 1, trece la 2, apoi la 3, apoi revine la grupul 1. Fiecare grup poate conține unul sau mai mulți **membri** — copii identice ale log-ului pe path-uri diferite, pentru redundanță.

```sql
-- Starea grupurilor redo log
SELECT group#, members, status, bytes/1024/1024 AS mb
FROM v$log;

-- Path-urile fizice ale membrilor
SELECT group#, member
FROM v$logfile
ORDER BY group#;
```

Output-ul pentru `PHARMDB` cu trei grupuri de 200MB:

```text
GROUP#  MEMBERS  STATUS    MB
------  -------  --------  ---
     1        1  INACTIVE  200
     2        1  CURRENT   200
     3        1  INACTIVE  200
```

`CURRENT` e grupul pe care Oracle scrie în acel moment. `INACTIVE` indică grupuri deja ciclate, care nu mai sunt necesare pentru recovery-ul instanței curente. `ACTIVE` ar semnala un grup încă necesar pentru recovery dar nu mai curent — o stare care necesită atenție înainte de orice operațiune pe log-uri.

Path-urile fizice pe `oracle-node-01`:

```bash
/u01/app/oracle/oradata/PHARMDB/redo01.log   # GROUP 1, 200MB
/u01/app/oracle/oradata/PHARMDB/redo02.log   # GROUP 2, 200MB
/u01/app/oracle/oradata/PHARMDB/redo03.log   # GROUP 3, 200MB
```

Erorile tipice când redo log-urile sunt inaccesibile sau corupte:

```text
ORA-00313: open failed for members of log group 1 of thread 1
ORA-00312: online log 1 thread 1: '/u01/app/oracle/oradata/PHARMDB/redo01.log'
```

În acest caz nu era o problemă reală. Remontarea lui `/u01` atinsese și directorul redo log-urilor, iar Oracle înregistrase un warning în timpul primei tentative de deschidere. Paolo verifică statusul grupurilor cu `v$log`, controlează permisiunile fișierelor fizice: totul în regulă după `chmod`-ul aplicat de storage. Warning-ul dispăruse deja.

[3:42] Database OPEN. Trasabilitatea loturilor revine online.

---

## Fișa de referință

Paolo mă sună imediat după. „Ivan, mulțumesc mult, singur nu aș fi ajuns la timp. Am citit documentația clientului, dar e scrisă ca referință, nu ca metodă. Acum am înțeles secvența și am înțeles de ce e nevoie de runbook."

Îi spun să noteze două tabele în caiet — cele pe care ar fi trebuit să le punem în runbook de la bun început.

**Path-uri standard și convențiile OFA**

Oracle recomandă o convenție de layout numită **OFA** (Optimal Flexible Architecture) care organizează fișierele instanței în mod previzibil. Urmarea ei nu e obligatorie, și în producție face mentenanța curentă și recovery-ul semnificativ mai ușor de gestionat.

| Fișier | Path tipic Linux (OFA) | Comandă de verificare |
|---|---|---|
| SPFILE | `/u01/app/oracle/product/19.0.0/dbhome_1/dbs/spfilePHARMDB.ora` | `SHOW PARAMETER spfile` |
| Control file 1 | `/u01/app/oracle/oradata/PHARMDB/control01.ctl` | `SELECT name FROM v$controlfile` |
| Control file 2 | `/u02/app/oracle/fast_recovery_area/PHARMDB/control02.ctl` | `SELECT name FROM v$controlfile` |
| Redo log group 1 | `/u01/app/oracle/oradata/PHARMDB/redo01.log` | `SELECT group#, member FROM v$logfile` |
| Redo log group 2 | `/u01/app/oracle/oradata/PHARMDB/redo02.log` | `SELECT group#, member FROM v$logfile` |
| Redo log group 3 | `/u01/app/oracle/oradata/PHARMDB/redo03.log` | `SELECT group#, member FROM v$logfile` |

**Hartă de diagnostic: ce blochează ce**

Când o instanță Oracle nu pornește, prima întrebare e: în ce fază s-a oprit? Răspunsul e aproape întotdeauna în alert log, iar codul ORA indică direct ce fișier critic e implicat.

| Fișier lipsă/corupt | Fază blocată | Eroare ORA tipică | Prima acțiune |
|---|---|---|---|
| SPFILE/PFILE | Pre-NOMOUNT | `ORA-01078`, `LRM-00109` | Verificați existența și permisiunile în `$ORACLE_HOME/dbs/` |
| Control file | MOUNT | `ORA-00205` | Verificați path-ul în `control_files`, permisiunile filesystem, disponibilitatea copiilor multiplexate |
| Online redo log | OPEN | `ORA-00313`, `ORA-00312` | Verificați `v$logfile`, statusul grupurilor în `v$log`, integritatea fizică a fișierelor |

Aceasta nu e un ghid de recovery — acela e un subiect separat, care necesită să distingem între control file corupt și control file lipsă, între redo log CURRENT și redo log INACTIVE, între recovery cu RMAN și recovery manual. E o hartă de diagnostic: servește la a nu merge în direcții greșite în primele faze ale unei urgențe.

---

## Ce rămâne din apel

Paolo nu era nepregătit din incompetență. Cunoștea sintaxa — știa ce face `SHOW PARAMETER spfile`, știa să interogheze `v$controlfile`. Ceea ce nu interiorizase încă era secvența de startup ca metodă de diagnostic: ce fișier citește Oracle în fiecare fază, și deci ce fișier să cauți primul când ceva nu merge.

Diferența dintre douăzeci de minute petrecute pe rețea, listener și OS și trei verificări directe la țintă nu e experiență acumulată în ani. E a avea un model mental al secvenței — NOMOUNT, MOUNT, OPEN — și a ști ce se mapează pe ce.

Valoarea acelui apel n-a fost să rezolvăm problema în locul lui. A fost să transferăm acel model în treizeci de minute, cu un caz real în față. Acum Paolo știe ce să întrebe echipa de storage data viitoare („permisiunile pe `/u01` au fost modificate în timpul mentenanței?"), știe ce rânduri din alert log contează, știe în ce ordine să excludă ipotezele.

DBA-ul senior care nu mai e sunat în miez de noapte a investit în două lucruri: în runbook-ul scris bine împreună cu echipa clientului, și în capacitatea de a ghida de la distanță pe cel de gardă dând cele trei verificări corecte în loc să îl pună să facă treizeci în orb.

---

## Surse oficiale

1. Oracle Database Concepts 19c — Startup and Shutdown: secvența NOMOUNT/MOUNT/OPEN și rolul fișierelor critice — `<TODO: scout URL exact pentru Oracle 19c Concepts, capitolul "Starting Up a Database">`

2. Oracle Database Administrator's Guide 19c — Managing Initialization Parameters: SPFILE, PFILE, ordinea de căutare, `ALTER SYSTEM SET` — `<TODO: scout URL exact pentru capitolul "Managing Initialization Parameters Using a Server Parameter File">`

3. Oracle Database Administrator's Guide 19c — [Managing the Online Redo Log](https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-the-online-redo-log.html) — grupuri, membri, status, `v$log`, `v$logfile`, erori ORA-00313/ORA-00312

4. Oracle Database Reference 19c — [V$CONTROLFILE](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/V-CONTROLFILE.html) — structură și query de verificare a control file-urilor

5. Oracle Database Reference 19c — [V$LOG](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/V-LOG.html) — coloanele `GROUP#`, `MEMBERS`, `STATUS`, `BYTES`; interpretarea statusurilor CURRENT/ACTIVE/INACTIVE

6. oracle-base.com (Tim Hall) — `<TODO: scout URL specific pentru "Oracle Database Startup and Shutdown" pe oracle-base.com>` — secvența de startup, erori comune, exemple practice

---

## Glosar candidat

- **SPFILE** (Oracle) — Server Parameter File: fișier binar citit de Oracle la pornire care conține parametrii de configurare ai instanței (`db_name`, `control_files`, `memory_target` etc.). Modificabil la cald cu `ALTER SYSTEM SET` fără a reporni baza de date.

- **Control File** (Oracle) — Fișier binar actualizat continuu de Oracle care înregistrează structura fizică a bazei de date: path-urile datafile-urilor și redo log-urilor, SCN-ul curent, informațiile de checkpoint. Indispensabil pentru faza de MOUNT; trebuie multiplexat pe path-uri fizic separate.

- **Online Redo Log** (Oracle) — Fișier circular care înregistrează în secvență toate modificările aduse bazei de date (redo entries) înainte ca acestea să fie scrise pe datafile-uri. Organizat în grupuri cu posibili membri multipli pentru redundanță; baza mecanismului de recovery în caz de crash.

- **SCN** (System Change Number) — Număr secvențial monoton crescător pe care Oracle îl folosește pentru a identifica un punct precis în viața bazei de date. Prezent în control file și în datafile-uri; folosit pentru a determina consistența și punctul de recovery.

- **OFA** (Optimal Flexible Architecture) — Convenție de denumire și layout al path-urilor recomandată de Oracle pentru a organiza fișierele unei instanțe (datafile-uri, control file-uri, redo log-uri, backup-uri) în mod previzibil, ușor de întreținut și portabil între medii diferite.
