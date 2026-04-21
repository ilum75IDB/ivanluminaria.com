---
title: "Înainte de a face upgrade la MySQL: cifrele pe care clientul ți le cere și cum să le găsești cu adevărat"
description: "Patru servere MySQL 8.0 în producție, un responsabil de infrastructură care planifică fereastra de mentenanță și patru întrebări directe: cât de mari sunt, cât de repede cresc, cât durează un backup complet, cât durează un restore complet. Cum să răspunzi cu cifre măsurate în loc de estimări aproximative."
date: "2026-05-05T08:03:00+01:00"
draft: false
translationKey: "mysql_pre_upgrade_assessment"
tags: ["mysql", "upgrade", "backup", "restore", "assessment", "information-schema", "mysqldump", "mydumper", "xtrabackup"]
categories: ["MySQL"]
image: "mysql-pre-upgrade-assessment.cover.jpg"
---

Mail-ul de la responsabilul de infrastructură a sosit într-o luni dimineață, trei rânduri seci. *"Salut, până vineri am nevoie de patru cifre pentru a planifica fereastra de mentenanță pe MySQL-uri: cât de mari sunt astăzi, cât de mult cresc pe lună, cât durează un backup complet, cât ne ia să le reconstruim de la zero dacă ceva merge prost. Mulțumesc."*

Scenariu clasic într-o direcție IT a unei Administrații Publice italiene. Patru servere MySQL 8.0 care susțin aplicații interne și un portal pentru utilizatori, cu versiuni ușor diferite (8.0.32, 8.0.33, 8.0.34) pentru că au fost patch-uite în momente diferite. Upgrade de infrastructură planificat: noi host-uri, sistem de operare actualizat, aceeași versiune major de MySQL, cu fereastră de mentenanță nocturnă de șase ore.

PM-ul nu voia un assessment academic. Voia patru cifre reale de pus în planul de rollback. Iar tentația, când ai grabă, este să răspunzi după ureche: *"Or fi vreo 300 GB, backup-ul durează vreo două ore, restore-ul poate trei."* Cifre plauzibile, poate chiar corecte, dar nemăsurate — iar dacă greșești estimarea restore-ului cu un factor de doi, fereastra nu mai este suficientă și cutover-ul pică.

Mi-am luat o jumătate de zi. Iată metoda pe care am folosit-o.

## 📏 1. Cât cântăresc cu adevărat — `information_schema`

Prima cifră este cea mai simplă de găsit și cea mai înșelătoare de interpretat. În MySQL 8.0 {{< glossary term="information-schema" >}}`information_schema`{{< /glossary >}} expune tot ce este necesar, dar trebuie să știi ce să ceri.

```sql
-- Dimensiuni totale pe schemă (date + indecși)
SELECT
    table_schema                            AS schema_name,
    ROUND(SUM(data_length)  / 1024 / 1024 / 1024, 2) AS data_gb,
    ROUND(SUM(index_length) / 1024 / 1024 / 1024, 2) AS index_gb,
    ROUND(SUM(data_length + index_length) / 1024 / 1024 / 1024, 2) AS total_gb,
    COUNT(*)                                AS num_tables
FROM information_schema.TABLES
WHERE table_schema NOT IN ('mysql', 'sys', 'performance_schema', 'information_schema')
GROUP BY table_schema
ORDER BY total_gb DESC;
```

Rezultat tipic pe unul dintre cele patru servere:

| schema_name            | data_gb | index_gb | total_gb | num_tables |
|------------------------|--------:|---------:|---------:|-----------:|
| portal_utilizatori     |   58,34 |    21,07 |    79,41 |        142 |
| gestiune_dosare        |   31,12 |    14,88 |    46,00 |         97 |
| audit_log              |   28,45 |     9,20 |    37,65 |         12 |
| master_partajat        |    4,18 |     1,32 |     5,50 |         24 |
| *(alte scheme)*        |    2,70 |     0,90 |     3,60 |         38 |
| **Total server**       |**124,79**|**47,37**|**172,16**|       313 |

Pare un rezultat închis, dar nu este. Două lucruri importante:

- **`data_length` și `index_length` sunt estimări** pe care InnoDB le actualizează periodic și care depind de ultimul `ANALYZE TABLE`. Pe tabele foarte volatile pot subestima cu 10-15%. Pentru date critice merită să verificăm cu dimensiunea fizică a fișierelor `.ibd` din datadir (`du -sh /var/lib/mysql/portal_utilizatori/*.ibd`).
- **Totalul serverului nu este dimensiunea backup-ului.** Fișierul de dump (logic) este mai compact pentru că nu replică fragmentarea InnoDB, dar conține `INSERT`-uri textuale care cântăresc mai mult decât datele binare. În practică, dump-ul necomprimat cântărește 70-90% din `data_length + index_length`. Cu `gzip` standard se coboară la 15-25%, cu `zstd -3` în jur de 18-28% dar mult mai rapid.

Rulând interogarea pe cele patru servere, sizing-ul total pe care l-am prezentat PM-ului a fost:

| Server    | MySQL  | Scheme | Total data + index | Fișiere .ibd pe disc |
|-----------|:------:|-------:|-------------------:|---------------------:|
| mysql-01  | 8.0.34 |      7 |           172,2 GB |              181 GB  |
| mysql-02  | 8.0.33 |      5 |            94,7 GB |               98 GB  |
| mysql-03  | 8.0.32 |      9 |           218,5 GB |              229 GB  |
| mysql-04  | 8.0.34 |      4 |            46,1 GB |               49 GB  |
| **Total** |        |     25 |         **531,5 GB** |         **557 GB** |

Diferența dintre "data + index" și "fișiere fizice" este costul fragmentării și al tablespace-ului `ibtmp1`. Merită evidențiat pentru PM pentru că pe noul mediu se poate planifica un `OPTIMIZE TABLE` post-migrare care recuperează acel 5-6% de spațiu.

## 📈 2. Cât cresc — snapshot-uri periodice și citire din binary log

Cifra creșterii este mai delicată. PM-ul întreabă "cât pe lună", dar răspunsul util este: *cât prevezi să crească în următoarele trei-șase luni, adică până la următorul assessment?* Există două abordări, ambele valide, pe care le folosesc împreună.

**Abordarea 1 — snapshot-uri periodice.** Dacă ai istoricul monitorizării (Prometheus + `mysqld_exporter`, Zabbix sau chiar doar folderul cu backup-urile istorice), poți reconstrui curba dimensiunilor. Dacă nu ai nimic, începe acum: un cron săptămânal care execută interogarea de mai sus și scrie rezultatul într-un tabel `ops.sizing_history` — după 6-8 săptămâni ai un rezultat solid.

```sql
-- Tabel de istoricizare (de rulat o singură dată)
CREATE TABLE ops.sizing_history (
    captured_at   TIMESTAMP NOT NULL,
    server_name   VARCHAR(50) NOT NULL,
    schema_name   VARCHAR(64) NOT NULL,
    data_bytes    BIGINT,
    index_bytes   BIGINT,
    num_tables    INT,
    PRIMARY KEY (captured_at, server_name, schema_name)
);

-- Snapshot săptămânal via cron
INSERT INTO ops.sizing_history (captured_at, server_name, schema_name, data_bytes, index_bytes, num_tables)
SELECT
    NOW(),
    @@hostname,
    table_schema,
    SUM(data_length),
    SUM(index_length),
    COUNT(*)
FROM information_schema.TABLES
WHERE table_schema NOT IN ('mysql', 'sys', 'performance_schema', 'information_schema', 'ops')
GROUP BY table_schema;
```

**Abordarea 2 — estimare din {{< glossary term="binary-log" >}}binary log{{< /glossary >}}.** Acesta este trucul pe care mulți nu îl folosesc. Binlog-ul înregistrează fiecare scriere, iar dimensiunea sa zilnică este un proxy excelent pentru rata de creștere a datelor (scăzând update-urile și delete-urile, care generează trafic dar nu creștere netă). Cu `expire_logs_days=7` ai o săptămână de istoric gata de citit.

```bash
# Volum zilnic binlog (ultimele 7 zile)
ls -la /var/lib/mysql/binlog.* | awk '{print substr($6" "$7,1,6), $5}' | \
    sort | awk '{a[$1]+=$2} END {for (k in a) printf "%s  %.2f GB\n", k, a[k]/1024/1024/1024}'
```

Rezultat tipic pe unul dintre servere:

```
Apr 14   3,87 GB
Apr 15   4,12 GB
Apr 16   3,95 GB
Apr 17   4,44 GB
Apr 18   2,18 GB   # sâmbătă
Apr 19   1,02 GB   # duminică
Apr 20   3,78 GB
```

Media în zile lucrătoare ~4 GB/zi de trafic de scriere. Rata de creștere netă a tablespace-ului este tipic între 20% și 40% din volumul binlog, în funcție de mix-ul insert/update/delete. În cazul nostru, combinând cu puținele snapshot-uri disponibile, am ajuns la o estimare de **+8-12 GB pe lună per server**, cu vârfuri pe `mysql-03` (cel al portalului utilizatori, mai dinamic).

## 💾 3. Cât durează backup-ul — `mysqldump`, `mydumper`, `xtrabackup`

Aici PM-ul așteaptă o singură cifră. Răspunsul onest este: depinde de ce instrument folosești, iar timpii pot diferi cu un ordin de mărime.

Pe același server (`mysql-03`, 218 GB de date + indecși, tabele InnoDB cu câteva MyISAM reziduale pe care nimeni nu le-a atins din 2014), am măsurat empiric patru strategii.

**`{{< glossary term="mysqldump" >}}mysqldump{{< /glossary >}}` (logic, single-threaded):**

```bash
time mysqldump --single-transaction --quick --routines --triggers --events \
    --default-character-set=utf8mb4 --hex-blob \
    --all-databases > /backup/mysql-03-full.sql
```

Rezultat: 2 ore și 47 minute. Fișier SQL necomprimat: 189 GB. Cu pipe în timp real pe `gzip` (`| gzip -3 > ...gz`): 3 ore și 22 minute, fișier comprimat 38 GB.

**`mysqldump` + `zstd` (preferatul meu pentru serverele PA unde timpul de CPU contează mai puțin decât fereastra):**

```bash
time mysqldump --single-transaction --quick --routines --triggers --events \
    --default-character-set=utf8mb4 --hex-blob --all-databases | \
    zstd -3 -T4 > /backup/mysql-03-full.sql.zst
```

Rezultat: 2 ore și 58 minute, fișier comprimat 42 GB. Puțin mai mare decât gzip dar **aproximativ de două ori mai rapid** la decompresie la restore — care este momentul când viteza contează cu adevărat.

**`{{< glossary term="mydumper" >}}mydumper{{< /glossary >}}` (logic, paralel):**

```bash
time mydumper --host=localhost --user=backup --socket=/var/lib/mysql/mysql.sock \
    --threads=8 --compress --rows=500000 \
    --outputdir=/backup/mysql-03-mydumper \
    --logfile=/backup/mysql-03-mydumper.log
```

Rezultat: 47 minute. Output: director cu 312 fișiere comprimate, total 41 GB. De aproape 4x mai rapid decât `mysqldump` datorită paralelismului la nivel de chunk de tabelă.

**`xtrabackup` (fizic, hot backup):**

```bash
time xtrabackup --backup --target-dir=/backup/mysql-03-xtra \
    --user=backup --password=*** --parallel=4 --compress --compress-threads=4
```

Rezultat: 22 minute. Output: 179 GB necomprimat / 48 GB comprimat. Este cel mai rapid pentru că copiază fișierele InnoDB la nivel fizic în loc să regenereze `INSERT`-uri, dar are o restricție importantă: **tabelele MyISAM reziduale sunt blocate** pe durata copiei lor. Din fericire pe `mysql-03` erau reziduale și citite doar de un batch nocturn, deci nu impactează.

Rezumat prezentat PM-ului:

| Instrument              | Timp backup | Dim. output | Note                                          |
|-------------------------|------------:|------------:|-----------------------------------------------|
| `mysqldump` + gzip      | 3h 22m      | 38 GB       | baseline, single-thread, disponibil peste tot |
| `mysqldump` + zstd      | 2h 58m      | 42 GB       | mai rapid la restore                          |
| `mydumper` + compress   | 47m         | 41 GB       | paralel, excelent compromis timp/spațiu       |
| `xtrabackup` + compress | 22m         | 48 GB       | fizic, cel mai rapid, restricții pe MyISAM    |

În assessment am propus standardizarea pe **`mydumper` pentru backup-ul periodic** (zilnic, ocupă puțin spațiu, restore flexibil per schemă) și **`xtrabackup` pentru snapshot-ul pre-upgrade** (foarte rapid, ideal pentru fereastra de mentenanță strânsă).

## ⏱️ 4. Cât durează restore-ul — cifra pe care PM-ul uită să o ceară

Restore-ul este locul unde assessment-urile făcute prost eșuează. Un backup poate dura 47 minute, dar reconstrucția aceluiași dataset poate cere ore — iar în fereastra de mentenanță, asta contează.

Tot pe `mysql-03`, măsurare empirică a cât durează reconstruirea de la zero a bazei de date pornind de la backup-urile de mai sus, pe un host geamăn (același CPU, același storage NVMe):

**Din `mysqldump.sql.gz`:**

```bash
time gunzip -c /backup/mysql-03-full.sql.gz | \
    mysql --default-character-set=utf8mb4
```

Rezultat: **5 ore și 12 minute**. Este lent pentru că restore-ul logic regenerează fiecare rând cu `INSERT`-uri individuale, actualizează indecșii tranzacțional și nu poate paraleliza pe o singură tabelă.

**Din `mysqldump.sql.zst`:**

```bash
time zstd -dc /backup/mysql-03-full.sql.zst | \
    mysql --default-character-set=utf8mb4
```

Rezultat: **4 ore și 38 minute**. Aici se vede avantajul decompresiei zstd (aproximativ 2x mai rapidă decât gzip), care este singurul element ce diferă de testul anterior.

**Din `mydumper` cu `myloader`:**

```bash
time myloader --host=localhost --user=root --socket=/var/lib/mysql/mysql.sock \
    --threads=8 --directory=/backup/mysql-03-mydumper \
    --disable-redo-log --overwrite-tables
```

Rezultat: **1 oră și 52 minute**. Flag-ul `--disable-redo-log` (MySQL 8.0.21+) este adevăratul game-changer: sare peste generarea {{< glossary term="redo-log-mysql" >}}redo log{{< /glossary >}}-ului în timpul încărcării inițiale, reducând overhead-ul de I/O. De folosit DOAR pe o instanță goală în faza de import, niciodată în producție.

**Din `xtrabackup`:**

```bash
time xtrabackup --decompress --target-dir=/backup/mysql-03-xtra --parallel=4
time xtrabackup --prepare --target-dir=/backup/mysql-03-xtra
# apoi rsync al fișierelor pe noul datadir + pornire mysqld
```

Rezultat: **34 minute** (decompress) + **12 minute** (prepare) + **6 minute** (copiere + restart) = **52 minute total**. Restore fizic: copie binară + crash recovery, fără SQL regenerat. Este singura opțiune care se apropie de timpul backup-ului însuși.

Rezumat restore:

| Strategie              | Timp restore | Note                                                   |
|------------------------|-------------:|--------------------------------------------------------|
| `mysqldump` + gzip     | 5h 12m       | de evitat pentru dataset-uri > 50 GB                   |
| `mysqldump` + zstd     | 4h 38m       | doar dacă nu ai alternative                            |
| `mydumper` + myloader  | 1h 52m       | cu `--disable-redo-log`, logic rapid                   |
| `xtrabackup`           | 52m          | fizic, singura opțiune compatibilă cu ferestre strâmte |

## 📋 5. Template-ul de răspuns pentru PM

După măsurătorile pe cele patru servere, am consolidat totul într-un singur tabel, pentru că PM-ul are nevoie de o pagină de atașat la planul de cutover, nu de treizeci de slide-uri.

| Server    | Dim. actuală | Creștere estimată | Backup (`xtrabackup`) | Restore (`xtrabackup`) | Restore worst-case (`mysqldump+gz`) |
|-----------|-------------:|------------------:|----------------------:|-----------------------:|------------------------------------:|
| mysql-01  |     172 GB   | +8 GB/lună        |               18 min  |                45 min  |                          4h 10m     |
| mysql-02  |      95 GB   | +3 GB/lună        |               11 min  |                28 min  |                          2h 25m     |
| mysql-03  |     219 GB   | +12 GB/lună       |               22 min  |                52 min  |                          5h 12m     |
| mysql-04  |      46 GB   | +2 GB/lună        |                6 min  |                15 min  |                          1h 20m     |
| **Total** |  **532 GB** | **+25 GB/lună**   |          **57 min**   |         **2h 20m**     |                    **13h 07m**      |

Pe baza acestui tabel, fereastra de mentenanță de șase ore este **compatibilă cu un rollback bazat pe `xtrabackup`** (snapshot 57 minute + restore 2h 20m = 3h 17m, cu marjă de 2h 43m pentru debug și verificări), dar **incompatibilă cu un rollback bazat pe `mysqldump`** (peste 13 ore). Decizie operațională: `xtrabackup` ca strategie principală de rollback, `mydumper` ca fallback pentru restore-uri selective per schemă dacă apar probleme punctuale în timpul cutover-ului.

PM-ul mi-a cerut patru cifre. I-am dat douăzeci și patru. Dar sunt douăzeci și patru de cifre măsurate — nu estimări aproximative — iar diferența este toată acolo.

## Ce am învățat

Un pre-upgrade assessment nu este un document tehnic, este un instrument de guvernare a riscului. Clientul care întreabă "cât durează backup-ul" de fapt întreabă *"dacă totul o ia razna în fereastra de mentenanță, reușim să repunem serviciile în funcțiune înainte de ora 6 dimineața?"*. Dacă răspunsul tău este "vreo trei ore, cred", întrebarea aceea rămâne fără răspuns și riscul nu a fost măsurat.

Partea tehnică — interogările, instrumentele, măsurătorile — este partea ușoară. Partea dificilă este să faci ca cifrele măsurate să ajungă în planul de cutover, ca PM-ul să le citească, ca echipa ops să le folosească pentru a calibra fereastra. În cazul nostru PM-ul a vrut să adauge un slide în plus la întâlnirea cu vendor-ul noului storage: *"uite, astea sunt cifrele de referință; dacă array-ul vostru nu susține aceste throughput-uri de restore, planul nu funcționează"*. Și este exact ce ar trebui să facă un PM bun.

În final upgrade-ul a trecut în patru ore, nu șase. Fără rollback. Clientul ne-a mulțumit nu pentru fereastra scurtă, ci pentru faptul că **știuseseră mereu ce s-ar întâmpla dacă ceva mergea prost**. Care este adevăratul obiectiv al unui pre-upgrade assessment bine făcut.

------------------------------------------------------------------------

## Glosar

**[information_schema](/ro/glossary/information-schema/)** — Schema de sistem MySQL (read-only) care expune metadate despre baze de date, tabele, indecși, utilizatori și starea serverului. Punct de plecare pentru orice assessment, sizing sau analiză structurală.

**[xtrabackup](/ro/glossary/xtrabackup/)** — Instrument de backup fizic hot pentru MySQL/MariaDB dezvoltat de Percona. Copiază direct fișierele InnoDB în timp ce baza de date rulează, gestionând tranzacțiile în curs prin redo log. Semnificativ mai rapid decât backup-urile logice pe dataset-uri mari.

**[Pre-upgrade assessment](/ro/glossary/pre-upgrade-assessment/)** — Măsurare structurată a dimensiunilor, ratei de creștere, timpilor de backup și timpilor de restore ai unei baze de date înainte de un upgrade. Servește la dimensionarea ferestrei de mentenanță și la definirea unei strategii de rollback realiste.

**[mysqldump](/ro/glossary/mysqldump/)** — Utilitar de backup logic inclus în orice instalație MySQL. Produce un fișier SQL secvențial cu toate instrucțiunile pentru a recrea schema și datele. Single-threaded, fiabil dar lent pe baze de date mari.

**[mydumper](/ro/glossary/mydumper/)** — Instrument open source de backup logic pentru MySQL/MariaDB cu paralelism real la nivel de chunk. Împarte tabelele mari în bucăți și le exportă cu thread-uri multiple, cu restore paralel prin myloader.
