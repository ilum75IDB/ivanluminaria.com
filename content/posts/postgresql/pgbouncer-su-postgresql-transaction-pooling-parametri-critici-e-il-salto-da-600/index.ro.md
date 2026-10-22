---
categories:
- postgresql
date: '2026-11-17'
description: 12 microservicii, 600 conexiuni simultane, PostgreSQL la pământ. Cum
  PgBouncer a redus conexiunile reale la 80 îmbunătățind throughput și stabilitate.
  Transaction pooling, prepared statements, parametri critici.
draft: false
image: pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600.cover.jpg
seoTitle: 'PgBouncer: de la 600 la 80 conexiuni PostgreSQL fără pierderi'
tags:
- pgbouncer
- connection-pooling
- postgresql
- performance
- scalability
title: De la 600 la 80 de conexiuni PostgreSQL cu PgBouncer, fără să pierzi throughput
translationKey: pgbouncer_su_postgresql_transaction_pooling_parametri_critici_e_il_salto_da_600
webo_generated_at: 2026-10-22
webo_status: scheduled
---

## Șase sute de conexiuni și o luni dimineața

Monitorul de sistem afișa numere care nu se potriveau. O aplicație distribuită pe douăsprezece microservicii, fiecare configurat cu propriul pool intern de cincizeci de conexiuni către PostgreSQL. Pe hârtie: cincizeci înmulțit cu doisprezece face șase sute, dar în producție instanțele scalau orizontal și vârfurile de trafic împingeau totalul și mai sus.

PostgreSQL nu mai ținea pasul. Interogările care în mod normal se terminau în câțiva milisecunde așteptau slot-uri libere zeci de secunde. Load average-ul serverului era constant peste zece. Memoria era aproape epuizată — nu din cauza datelor, ci a proceselor backend ale PostgreSQL înseși.

Echipa încercase deja să reducă pool-urile din aplicație, dar fiecare microserviciu era dezvoltat de o echipă diferită, cu dependențe și constrângeri proprii. Coordonarea unei reduceri uniforme ar fi durat săptămâni. Era nevoie de o soluție la nivel infrastructural.

Acea soluție era PgBouncer.

## De ce PostgreSQL suferă cu sute de conexiuni

Înainte de a înțelege de ce PgBouncer ajută, merită să înțelegem de ce PostgreSQL suferă cu multe conexiuni simultane — nu e o problemă de configurare, e arhitectură.

PostgreSQL folosește un model **process-per-connection**: fiecare conexiune client este servită de un proces OS separat, cu propriul stack, propria memorie privată și propriul overhead de context switch. Pe Linux, fiecare backend PostgreSQL ocupă tipic între 5 și 10 MB de memorie privată (plus memoria partajată). Cu șase sute de conexiuni active, vorbim de 3-6 GB de RAM dedicați exclusiv proceselor backend — înainte de a executa vreo interogare.

Problema se agravează cu **context switching**. Scheduler-ul kernelului trebuie să gestioneze sute de procese care concurează pentru core-urile CPU. Când majoritatea acestor procese așteaptă I/O sau lock-uri, kernelul petrece timp făcând scheduling în loc să execute muncă utilă. Rezultatul e vizibil în load average: un server cu opt core-uri care afișează load average de doisprezece sau cincisprezece nu face de doisprezece ori mai multă muncă — irosește cicluri CPU în overhead de scheduling.

Există și problema **lock-urilor și a statisticilor**. Fiecare conexiune, chiar și când e idle, menține structuri de date în memoria partajată. Cu șase sute de conexiuni, operații precum `VACUUM`, `ANALYZE` și gestionarea lock-urilor devin mai costisitoare pentru că trebuie să parcurgă structuri mai mari.

Parametrul `max_connections` din PostgreSQL există tocmai din acest motiv: nu e o limită arbitrară, e o protecție împotriva colapsului sistemului [1].

## Ce face PgBouncer și cum se poziționează în arhitectură

PgBouncer este un connection pooler ușor care se poziționează între clienți (microserviciile) și PostgreSQL. Clienții se conectează la PgBouncer ca și cum ar fi PostgreSQL — același port, același protocol. PgBouncer menține un pool redus de conexiuni reale către baza de date și le reutilizează între clienți.

Punctul cheie este că PgBouncer e scris în C, e single-threaded cu I/O asincron (bazat pe `libevent`), și gestionează mii de conexiuni client cu un overhead minim. O singură instanță PgBouncer poate susține confortabil o mie de conexiuni client folosind câteva zeci de MB de RAM.

Arhitectura rezultată arată astfel:

```text
[Microserviciu A] ──┐
[Microserviciu B] ──┤                    ┌──────────────────┐
[Microserviciu C] ──┼──► [PgBouncer] ───►│  PostgreSQL      │
[Microserviciu D] ──┤    (port 5432)     │  (80 conexiuni)  │
[Microserviciu E] ──┘                    └──────────────────┘
  (600 conexiuni client)
```

PgBouncer primește cele șase sute de conexiuni client, dar către PostgreSQL menține doar optzeci de conexiuni reale. Când un client trimite o interogare, PgBouncer alocă o conexiune backend disponibilă, execută interogarea și — în funcție de modul de pooling — eliberează acea conexiune pentru alți clienți.

## Transaction pooling vs session pooling: alegerea care schimbă totul

PgBouncer suportă trei moduri de pooling. Cele două relevante în producție sunt **session pooling** și **transaction pooling**.

**Session pooling**: o conexiune backend este alocată unui client pe toată durata sesiunii sale. Backend-ul este eliberat doar când clientul se deconectează. E modul cel mai compatibil — funcționează cu orice — dar oferă cel mai mic câștig: dacă un client ține sesiunea deschisă fără să execute interogări, backend-ul e tot ocupat.

**Transaction pooling**: o conexiune backend este alocată clientului doar pe durata unei tranzacții. Imediat ce tranzacția se termină (COMMIT sau ROLLBACK), backend-ul revine în pool și poate fi alocat altui client. Acesta e modul care permite să servești șase sute de clienți cu optzeci de backend-uri reale, pentru că în practică majoritatea clienților e idle între o tranzacție și alta.

Alegerea între cele două nu e banală. Transaction pooling are constrângeri importante:

- **Variabilele de sesiune** (`SET search_path`, `SET timezone`, etc.) nu persistă între tranzacții diferite
- **Prepared statements** cu nume explicit nu funcționează transparent (discutăm în secțiunea dedicată)
- **Advisory lock**-urile la nivel de sesiune nu funcționează
- `LISTEN/NOTIFY` nu e suportat în transaction pooling

Session pooling e mai sigur, dar necesită ca clienții să se deconecteze când nu mai au nevoie — lucru pe care pool-urile aplicative îl fac deja. În acel caz, câștigul e real dar mai puțin dramatic.

În cazul nostru, microserviciile foloseau un ORM standard fără prepared statements cu nume explicit, fără advisory lock-uri, fără `LISTEN/NOTIFY`. Transaction pooling era alegerea corectă.

## Instalare și configurare de bază

Pe o distribuție Debian/Ubuntu recentă, instalarea e directă [2]:

```bash
apt install pgbouncer
```

Configurația trăiește în două fișiere: `pgbouncer.ini` și `userlist.txt`.

### `pgbouncer.ini`

```ini
[databases]
; "appdb" este numele bazei de date virtuale expuse de PgBouncer
; clienții se conectează la acest nume
appdb = host=127.0.0.1 port=5432 dbname=appdb

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 5432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt

; modul de pooling
pool_mode = transaction

; conexiuni reale către PostgreSQL per pool
default_pool_size = 80

; numărul maxim de conexiuni client acceptate de PgBouncer
max_client_conn = 1000

; pool de rezervă pentru vârfuri de trafic
reserve_pool_size = 10
reserve_pool_timeout = 5

; timeout conexiuni idle pe partea serverului
server_idle_timeout = 600

; log
logfile = /var/log/pgbouncer/pgbouncer.log
pidfile = /var/run/pgbouncer/pgbouncer.pid

; statistici
stats_period = 60
```

### `userlist.txt`

Fișierul conține credențialele în formatul `"username" "password_hash"`. PgBouncer suportă hash-uri MD5 în formatul PostgreSQL (`md5` + md5(parolă + username)):

```text
"app_user" "md5a1b2c3d4e5f6..."
"pgbouncer_admin" "md5..."
```

Pentru a genera hash-ul corect:

```bash
echo -n "passwordusername" | md5sum
# prefixează "md5" la rezultat
```

După configurare, pornește PgBouncer și verifică că se conectează corect:

```bash
systemctl start pgbouncer
systemctl enable pgbouncer

# verifică conexiunea admin
psql -h 127.0.0.1 -p 5432 -U pgbouncer pgbouncer
```

## De la șase sute la optzeci: cifrele înainte și după

După deploy-ul PgBouncer în transaction pooling, cifrele s-au schimbat substanțial. Câteva măsurători reprezentative, colectate în primele săptămâni:

| Metrică | Înainte | După |
|---|---|---|
| Conexiuni reale la PostgreSQL | 580-620 | 65-80 |
| RAM ocupată de backend-urile PG | ~4,2 GB | ~600 MB |
| Load average (8 core-uri) | 12-18 | 3-5 |
| Latență medie interogare (p50) | 180 ms | 22 ms |
| Latență p99 | 4,2 s | 310 ms |
| Timeout-uri de conexiune | frecvente | absente |

Reducerea latenței nu se datorează doar mai puțin contention pe conexiuni. Cu mai puține procese backend active, kernelul face mai puțin context switching, PostgreSQL gestionează structuri de date mai mici, iar `VACUUM` reușește să-și termine ciclurile fără să fie continuu întrerupt. E un efect în cascadă.

Throughput-ul total — interogări pe secundă — a crescut cu aproximativ 40%, deși numărul de conexiuni reale scăzuse cu aproape un ordin de mărime. Acesta e punctul care surprinde adesea: mai puține conexiuni nu înseamnă mai puțin lucru efectuat, înseamnă mai puțin overhead per unitate de muncă.

## Prepared statements și transaction pooling: nodul de dezlegat

Cea mai frecventă problemă la migrarea la PgBouncer în transaction pooling privește **prepared statements**.

În PostgreSQL, prepared statements cu nume explicit (`PREPARE nume AS ...`) sunt legate de sesiune. În transaction pooling, fiecare tranzacție poate ajunge pe un backend diferit — deci un prepared statement creat într-o tranzacție anterioară nu există pe noul backend.

Rezultatul e o eroare de tipul:

```text
ERROR: prepared statement "s1" does not exist
```

Există trei abordări pentru a gestiona situația:

**1. Folosirea prepared statements anonime (la nivel de protocol)**

Driver-ele moderne precum `libpq`, `asyncpg`, `psycopg3` și JDBC suportă prepared statements la nivel de protocol fără nume explicit. PgBouncer le gestionează transparent în transaction pooling. Dacă framework-ul folosește acest mecanism (majoritatea ORM-urilor moderne o fac), nu există nicio problemă.

**2. Dezactivarea prepared statements din aplicație**

Dacă driver-ul sau ORM-ul folosește prepared statements cu nume explicit, soluția cea mai simplă e să le dezactivezi. În SQLAlchemy, de exemplu:

```python
engine = create_engine(
    "postgresql+psycopg2://user:pass@pgbouncer-host/appdb",
    execution_options={"no_parameters": True},
    # sau cu psycopg2:
    connect_args={"options": "-c statement_timeout=30000"}
)
```

Cu JDBC și driver-ul PostgreSQL:

```text
jdbc:postgresql://pgbouncer-host/appdb?prepareThreshold=0
```

`prepareThreshold=0` îi spune driver-ului să nu folosească niciodată prepared statements server-side.

**3. Folosirea `DEALLOCATE ALL` între tranzacții**

Mai puțin elegant, dar funcționează: configurează PgBouncer cu `server_reset_query = DEALLOCATE ALL` pentru a curăța prepared statements când un backend revine în pool. Atenție: adaugă latență la fiecare eliberare de conexiune.

În cazul nostru, microserviciile foloseau SQLAlchemy cu psycopg2 și prepared statements cu nume explicit. Soluția a fost adăugarea echivalentului `prepareThreshold=0` în configurația driver-ului — o modificare de două rânduri per serviciu, deployată într-o după-amiază.

## Parametrii critici de înțeles înainte de a merge în producție

Trei parametri din `pgbouncer.ini` merită atenție specială [3]:

**`default_pool_size`**: numărul de conexiuni reale către PostgreSQL menținute de PgBouncer pentru fiecare pereche (bază de date, utilizator). E parametrul cel mai important. Cum îl alegi? O regulă empirică: `num_cores * 2` ca punct de plecare, apoi măsoară. Cu opt core-uri, începi de la șaisprezece și urci până găsești punctul de saturație. În cazul nostru, optzeci de conexiuni pe un server cu șaisprezece core-uri și SSD NVMe era punctul de echilibru.

**`max_client_conn`**: numărul maxim de conexiuni client pe care PgBouncer le acceptă în total. Trebuie să fie mai mare decât numărul de conexiuni pe care clienții le pot deschide. Dacă cei șase sute de clienți deschid câte o conexiune fiecare, `max_client_conn` trebuie să fie cel puțin șase sute, mai bine o mie pentru a avea marjă. Când se depășește această limită, PgBouncer refuză conexiuni noi — mai bine o eroare explicită decât un timeout silențios.

**`reserve_pool_size`** și **`reserve_pool_timeout`**: pool-ul de rezervă e un set de conexiuni suplimentare pe care PgBouncer le poate deschide când pool-ul principal e epuizat. Dacă un client așteaptă mai mult de `reserve_pool_timeout` secunde pentru o conexiune, PgBouncer apelează la reserve pool. E o plasă de siguranță pentru vârfuri de trafic, nu o soluție structurală: dacă reserve pool-ul se epuizează regulat, `default_pool_size` trebuie crescut.

Un parametru adesea neglijat e **`server_idle_timeout`**: după câte secunde de inactivitate PgBouncer închide o conexiune backend. Valoarea implicită e șase sute de secunde (zece minute). În medii cu trafic foarte variabil — ridicat ziua, aproape nul noaptea — reducerea la o sută cincizeci sau două sute de secunde scade numărul de conexiuni idle pe care PostgreSQL le menține deschise în orele de activitate redusă.

## Citind cifrele: SHOW STATS și SHOW POOLS

PgBouncer expune o consolă de administrare accesibilă conectându-se la baza de date virtuală `pgbouncer`:

```bash
psql -h 127.0.0.1 -p 5432 -U pgbouncer_admin pgbouncer
```

Comanda cea mai utilă pentru monitorizarea zilnică e `SHOW STATS` [4]:

```sql
SHOW STATS;
```

```text
 database | total_xact_count | total_query_count | total_received | total_sent | total_xact_time | total_query_time | total_wait_time | avg_xact_count | avg_query_count | avg_recv | avg_sent | avg_xact_time | avg_query_time | avg_wait_time
----------+------------------+-------------------+----------------+------------+-----------------+------------------+-----------------+----------------+-----------------+----------+----------+---------------+----------------+---------------
 appdb    |        284721043 |         284721043 |   182043219872 | 9823041928 |    492831029183 |     492831029183 |      1823041928 |            312 |             312 |   199823 |    10782 |          1732 |           1732 |             6
```

Coloanele cheie: `avg_wait_time` (timpul mediu de așteptare pentru o conexiune backend — dacă depășește câțiva milisecunde, pool-ul e prea mic) și `avg_xact_time` (durata medie a tranzacțiilor).

`SHOW POOLS` afișează starea în timp real a pool-urilor:

```sql
SHOW POOLS;
```

```text
 database | user     | cl_active | cl_waiting | sv_active | sv_idle | sv_used | sv_tested | sv_login | maxwait | maxwait_us | pool_mode
----------+----------+-----------+------------+-----------+---------+---------+-----------+----------+---------+------------+-----------
 appdb    | app_user |       412 |          0 |        78 |       2 |       0 |         0 |        0 |       0 |          0 | transaction
```

- `cl_active`: clienți cu o conexiune backend alocată
- `cl_waiting`: clienți care așteaptă o conexiune backend — dacă acest număr e constant > 0, pool-ul e saturat
- `sv_active`: backend-uri ocupate
- `sv_idle`: backend-uri libere în pool
- `maxwait`: timpul maxim de așteptare al unui client (în secunde) — indicatorul principal de alarmă

Pentru monitorizarea automată, aceste valori se extrag ușor cu orice sistem de metrici. Prometheus are un exporter dedicat (`pgbouncer_exporter`) care expune toate metricile din `SHOW STATS` și `SHOW POOLS` în format scrape [5].

## Ce rămâne după deploy

PgBouncer nu e o soluție magică și nu elimină necesitatea de a proiecta bine layer-ul de acces la date. Dacă interogările sunt lente, PgBouncer nu le accelerează. Dacă baza de date are probleme de lock-uri, PgBouncer nu le rezolvă. Ceea ce face e să elimine un bottleneck specific — overhead-ul de gestionare a conexiunilor — care în arhitecturile cu microservicii devine rapid problema dominantă.

Ceea ce izbitoare, privind cifrele retrospectiv, e cât de simplă era diagnosticarea: serverul avea memorie suficientă pentru date, CPU suficient pentru interogări, I/O suficient pentru scrieri. Suferea din cauza overhead-ului pur de a gestiona șase sute de procese OS simultan. PgBouncer a mutat acea problemă în afara PostgreSQL, unde poate fi gestionată mult mai eficient.

Un punct care merită reținut pentru arhitecturi viitoare: într-un sistem cu multe microservicii, connection pooling-ul nu ar trebui să fie o adăugire ulterioară. Ar trebui să fie parte din design-ul inițial, la fel ca load balancer-ul sau service mesh-ul. Costul adăugării lui după — coordonarea echipelor, gestionarea migrării, testarea compatibilității prepared statements — e real, chiar dacă în final gestionabil.

Echipa a adăugat ulterior PgBouncer ca și componentă standard în template-ul de deploy pentru toate serviciile noi. Nu mai e o decizie de luat caz cu caz.

## Surse oficiale

1. PostgreSQL Documentation — [Connections and Authentication: max_connections](https://www.postgresql.org/docs/current/runtime-config-connection.html)
2. PgBouncer Documentation — [Installation](https://www.pgbouncer.org/install.html)
3. PgBouncer Documentation — [Configuration file pgbouncer.ini](https://www.pgbouncer.org/config.html)
4. PgBouncer Documentation — [Usage: SHOW commands](https://www.pgbouncer.org/usage.html)
5. prometheus-community — [pgbouncer_exporter](https://github.com/prometheus-community/pgbouncer_exporter)

## Glosar
- **[PgBouncer](/ro/glossary/pgbouncer/)** — Connection pooler ușor pentru PostgreSQL, scris în C cu I/O asincron. Se poziționează între clienți și baza de date, menținând un pool redus de conexiuni reale către PostgreSQL și reutilizându-le între mulți clienți.

- **[Transaction pooling](/ro/glossary/pgbouncer/)** — Mod de pooling în care o conexiune backend este alocată clientului doar pe durata unei tranzacții. Imediat ce tranzacția se termină, backend-ul revine în pool disponibil pentru alți clienți. Permite servirea multor clienți cu puține conexiuni reale.

- **[Session pooling](/ro/glossary/transaction-pooling/)** — Mod de pooling în care o conexiune backend rămâne alocată unui client pe toată durata sesiunii sale. Mai compatibil decât transaction pooling, dar mai puțin eficient deoarece backend-ul e ocupat chiar și când clientul e idle.

- **[`max_connections`](/ro/glossary/pgbouncer/)** (PostgreSQL) — Parametru de configurare care limitează numărul maxim de conexiuni simultane acceptate de PostgreSQL. Nu e o limită arbitrară: reflectă costul real în memorie și overhead de scheduling al fiecărui proces backend.

- **[`default_pool_size`](/ro/glossary/transaction-pooling/)** (PgBouncer) — Numărul de conexiuni reale către PostgreSQL menținute de PgBouncer pentru fiecare pereche (bază de date, utilizator). E parametrul principal pentru dimensionarea pool-ului: prea mic cauzează așteptări, prea mare readuce problema conexiunilor excesive pe PostgreSQL.
