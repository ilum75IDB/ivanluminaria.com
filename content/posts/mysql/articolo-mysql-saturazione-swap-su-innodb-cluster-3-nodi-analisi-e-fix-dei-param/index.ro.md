---
categories:
- mysql
date: '2026-07-28'
description: Un full scan pe 1,3 miliarde de rânduri a saturat swap-ul pe două noduri
  MySQL. Diagnostic cu performance_schema, reconfigurare buffere per-thread și rolling
  restart fără downtime.
draft: false
image: articolo-mysql-saturazione-swap-su-innodb-cluster-3-nodi-analisi-e-fix-dei-param.cover.jpg
seoTitle: 'MySQL join_buffer_size: diagnostic și fix pe InnoDB Cluster 3 noduri'
tags:
- mysql
- innodb-cluster
- performance-tuning
- memory-configuration
- incident-response
title: 'Apelul de marți dimineața: cum un join_buffer_size de 2 GB a blocat un cluster
  MySQL de 157 GB'
translationKey: articolo_mysql_saturazione_swap_su_innodb_cluster_3_nodi_analisi_e_fix_dei_param
webo_generated_at: 2026-07-01
webo_status: scheduled
---

## Apelul de marți dimineața

Marți dimineața, puțin după nouă. Cafeaua încă fierbinte pe birou, ziua părea una dintre acelea liniștite în care reușești în sfârșit să închizi lucrurile rămase suspendate de vineri. Apoi a venit apelul.

De cealaltă parte era echipa de infrastructură a unui lanț de retail alimentar italian: backend-ul de monitoring devenise extrem de lent, dashboard-urile interne nu mai încărcau, unele alerte nu mai ajungeau. Un nod din clusterul MySQL era practic blocat. „N-am atins nimic, s-a întâmplat așa."

Sub capotă era o interogare de agregare, aparent inofensivă. Ceva de genul:

```sql
SELECT itemid, MIN(clock), MAX(clock), COUNT(*)
FROM history_log
GROUP BY itemid;
```

Pe un tabel cu 1,3 miliarde de rânduri, fără partiționare, fără filtru temporal, fără `LIMIT`. Nodul secondary al clusterului a început să facă swap agresiv, apoi s-a oprit.

Contextul: lanțul de retail în cauză folosea un cluster MySQL InnoDB Cluster cu 3 noduri ca backend pentru propria platformă internă de monitoring — cea care ținea sub control sistemele de casă, depozitele, logistica punctelor de vânzare. Nodurile — `mysql-node-01`, `mysql-node-02`, `mysql-node-03` — gestionau colectarea și consultarea metricilor istorice. Tabelul `history_log` era inima sistemului: fiecare eveniment de monitoring ajungea acolo, acumulat în timp fără o politică de retenție activă și fără partiționare pe dată.

Când interogarea a pornit în producție — cineva căuta evident să răspundă la o întrebare de business pe toată istoria item-urilor — nodul secondary nu avea suficientă RAM liberă pentru a susține full scan-ul. Situația, însă, nu se rezuma la acea interogare. Era configurația de memorie de dedesubt, care făcea clusterul structural fragil la orice sarcină agregată non-trivială.

## `free -h` și prima surpriză

Primul semnal venise din dashboard-ul de monitoring al clientului, partajat în call la câteva minute după apel: graficul swap-ului pe `mysql-node-01` și `mysql-node-02` arăta o linie plată la maximum de ore. Pe `mysql-node-03` în schimb totul părea normal.

```bash
# mysql-node-01
              total        used        free      shared  buff/cache   available
Mem:           157Gi       155Gi       512Mi       1.2Gi       1.5Gi       400Mi
Swap:            6Gi         6Gi         0Bi

# mysql-node-02
              total        used        free      shared  buff/cache   available
Mem:           157Gi       150Gi       2.1Gi       1.1Gi       4.8Gi       1.2Gi
Swap:            6Gi         6Gi         0Bi

# mysql-node-03
              total        used        free      shared  buff/cache   available
Mem:           157Gi        21Gi       130Gi       0.3Gi       5.9Gi       134Gi
Swap:            6Gi       512Mi       5.5Gi
```

Diferența dintre noduri era clară. `mysql-node-03` era nodul care primise mai puțin trafic de interogări în acea perioadă — era secondary-ul „rece", ca să spunem așa. Primele două susțineau traficul principal de citire și scriere, iar memoria era epuizată.

`vmstat 1 5` confirma: swap în uz activ, nu doar ocupat static.

```bash
# vmstat 1 5 pe mysql-node-01
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 3  2 6291456  52428  18432 1572864  142  198  2840  3120 4821 9234 28  8 58  6  0
 2  1 6291456  48120  18432 1572864  156  212  3012  3340 5102 9876 31  9 54  6  0
```

`si` și `so` (swap-in și swap-out) active: kernel-ul muta pagini între RAM și disc în mod continuu. Cu un database relațional sub sarcină, acesta este cel mai rapid mod de a degrada performanțele în mod ireversibil.

## Matematica care nu se potrivea

Uitându-ne la configurația activă pe cluster, parametrul care sărea imediat în ochi era acesta:

```sql
SHOW VARIABLES LIKE 'join_buffer_size';
-- join_buffer_size = 2147483648  (2 GB)

SHOW VARIABLES LIKE 'max_connections';
-- max_connections = 151

SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
-- innodb_buffer_pool_size = 133143986176  (124 GB)
```

`join_buffer_size` la 2 GB este un parametru **per thread**, nu global. Fiecare conexiune MySQL care execută un join fără index poate aloca până la 2 GB de memorie suplimentară. Cu `max_connections = 151`, potențialul teoretic de alocare este:

```
2 GB × 151 conexiuni = 302 GB
```

Pe mașini cu 157 GB RAM total, din care 124 GB deja angajați în `innodb_buffer_pool_size`.

Evident, 302 GB nu se alocă toți deodată în condiții normale — bufferele per thread se alocă doar când sunt necesare, și nu toate conexiunile execută join-uri simultan. Într-un moment de sarcină agregată, însă, cu interogări full-scan pe `history_log` în execuție pe mai multe conexiuni, chiar și o fracțiune din acel potențial este suficientă pentru a satura RAM-ul disponibil.

Și `tmp_table_size` și `max_heap_table_size` erau supradimensionate, contribuind la presiunea pe tabelele temporare în memorie.

## Ce spunea `performance_schema`

Pentru a înțelege care interogări consumau efectiv resurse, consultarea `events_statements_summary_by_digest` a oferit imaginea completă:

```sql
SELECT
    DIGEST_TEXT,
    COUNT_STAR,
    SUM_ROWS_EXAMINED,
    SUM_CREATED_TMP_DISK_TABLES,
    SUM_NO_INDEX_USED,
    ROUND(SUM_TIMER_WAIT / 1e12, 2) AS total_wait_sec
FROM performance_schema.events_statements_summary_by_digest
WHERE SUM_NO_INDEX_USED > 0
   OR SUM_CREATED_TMP_DISK_TABLES > 0
ORDER BY SUM_ROWS_EXAMINED DESC
LIMIT 10;
```

Numerele care ieșeau la suprafață erau semnificative [1]:

- `Select_full_join` acumulat: până la **22.631.693** — join-uri executate fără index
- `Created_tmp_disk_tables`: peste **200.000** — tabele temporare deversate pe disc pentru că memoria nu era suficientă

Nu erau numerele unui singur eveniment. Erau rezultatul unor săptămâni de interogări slab optimizate care se acumulau în tăcere, până când un full scan pe `history_log` nu a făcut să se reverse sistemul.

## Structura lui `history_log` și nodul fără ieșire

```sql
SHOW CREATE TABLE history_log\G
-- Engine: InnoDB
-- Rows (approx): 1.312.847.203
-- Partitions: none
-- Indexes: PRIMARY KEY (id), KEY idx_itemid_clock (itemid, clock)

SELECT COUNT(*) FROM history_log;
-- 1312847203
```

Tabelul avea un index pe `(itemid, clock)`, dar interogarea de agregare care cauzase crash-ul nu folosea filtrul pe `clock`. MySQL nu reușea să folosească indexul eficient pentru un `GROUP BY itemid` pe întregul tabel — planul de execuție alegea un full scan, aloca structuri temporare în memorie, iar când memoria se termina, deversa totul pe disc. Pe `mysql-node-02`, cu swap-ul deja la 100%, nu mai era disc virtual disponibil: nodul s-a oprit [2].

Fără partiționare pe dată pe `history_log`, orice interogare agregată pe întreaga istorie este structural periculoasă. Este o alegere arhitecturală care trebuia abordată, și în același timp nu în regim de urgență — fix-ul urgent era pe parametrii de memorie.

## Valorile noi și raționamentul din spate

Planul de intervenție era direct. Parametrii per thread trebuiau redimensionați la valori rezonabile pentru workload-ul real:

```ini
# my.cnf — modificări aplicate
[mysqld]

# Buffer per thread: de la 2G la 64M
join_buffer_size        = 64M
tmp_table_size          = 64M
max_heap_table_size     = 64M

# InnoDB redo log: capacitate mărită pentru a reduce frecvența checkpoint-urilor
innodb_redo_log_capacity = 8G

# Parametri InnoDB menținuți neschimbați
innodb_buffer_pool_size  = 124G   # deja dimensionat corect pentru dataset
innodb_buffer_pool_instances = 8  # neschimbat
```

Decizia de a menține `innodb_buffer_pool_size` la 124 GB era deliberată: buffer pool-ul este memorie globală, nu per thread, iar dimensionarea sa era corectă față de dimensiunea dataset-ului activ. Reducerea lui ar fi înrăutățit performanțele de I/O fără a rezolva cauza reală.

`join_buffer_size` la 64 MB este o valoare standard pentru workload-uri OLTP mixte. Cu 151 conexiuni maxime, potențialul de alocare scade la:

```
64 MB × 151 = 9,6 GB
```

Adăugat la cei 124 GB ai buffer pool-ului și la overhead-ul sistemului de operare, se încadrează confortabil în cei 157 GB disponibili cu marjă suficientă pentru vârfuri [3].

`innodb_redo_log_capacity` la 8 GB (față de o valoare anterioară mai mică) servește la reducerea frecvenței checkpoint-urilor InnoDB, care în prezența unui trafic intens de scriere generează I/O suplimentar — o contribuție secundară la presiunea pe sistem.

## Rolling restart-ul și de ce funcționează pe InnoDB Cluster

InnoDB Cluster cu Group Replication permite repornirea nodurilor în secvență fără a întrerupe serviciul, cu condiția menținerii quorum-ului [4]. Cu 3 noduri, se poate scoate offline câte un nod pe rând: celelalte două mențin quorum-ul și continuă să servească cererile.

Secvența aplicată, stabilită telefonic cu echipa clientului:

```bash
# Pasul 1: repornire mysql-node-03 (nodul cu swap minim, risc mai mic)
# Verificare stare cluster înainte de a proceda
mysqlsh -- cluster status

# Pe mysql-node-03: stop, modificare my.cnf, start
systemctl stop mysqld
# -- modificare /etc/my.cnf cu noii parametri --
systemctl start mysqld

# Așteptare rejoin automat în cluster
# Verificare: SECONDARY revenit ONLINE

# Pasul 2: repornire mysql-node-02
# Pasul 3: repornire mysql-node-01 (PRIMARY ultimul)
# Înainte de repornirea PRIMARY: switchover manual dacă e necesar
mysqlsh -- cluster setPrimaryInstance mysql-node-02:3306
```

Repornirea nodului PRIMARY ultimul este o măsură de precauție: dacă PRIMARY-ul este repornit în timp ce celelalte două nu sunt complet sincronizate, Group Replication alege automat un nou PRIMARY, și în același timp este mai curat să gestionezi switchover-ul manual.

Timp total al operațiunii: aproximativ 40 de minute de la primul apel, zero întreruperi de serviciu pentru aplicațiile client. Casele de marcat din punctele de vânzare nu au simțit nimic.

## De la 100% la 11%: numerele după fix

Graficul swap-ului în orele următoare rolling restart-ului arăta curba așteptată: scădere rapidă pe `mysql-node-01` și `mysql-node-02`, stabilizare în jurul valorii de 10-11%.

```bash
# mysql-node-01 — 6 ore după rolling restart
              total        used        free      shared  buff/cache   available
Mem:           157Gi       132Gi        18Gi       0.8Gi       6.2Gi        23Gi
Swap:            6Gi       672Mi       5.4Gi

# mysql-node-02
              total        used        free      shared  buff/cache   available
Mem:           157Gi       129Gi        21Gi       0.7Gi       6.8Gi        25Gi
Swap:            6Gi       614Mi       5.4Gi
```

Sarcina CPU se stabilizase: vârfurile legate de swap I/O dispăruseră. Metricile din `performance_schema` arătau o reducere netă a `Created_tmp_disk_tables` — nu la zero, pentru că unele interogări continuau să facă full scan, și în același timp sistemul nu mai era sub presiune structurală.

`Select_full_join` continua să se acumuleze: acea metrică necesită intervenții pe interogări și indecși, nu doar pe parametrii de memorie. Clusterul, însă, susținea sarcina fără a satura swap-ul.

## Ce rămâne de făcut pe `history_log`

Fix-ul pe parametrii de memorie era necesar și suficient pentru a stabiliza clusterul în regim de urgență. Cauza structurală, însă — un tabel cu 1,3 miliarde de rânduri fără partiționare și fără politică de retenție — rămâne deschisă.

Acțiunile recomandate clientului pe termen mediu:

**Partiționare pe dată pe `history_log`**

```sql
-- Schema țintă (de aplicat cu migrare planificată)
ALTER TABLE history_log
    PARTITION BY RANGE (clock) (
        PARTITION p_2023 VALUES LESS THAN (UNIX_TIMESTAMP('2024-01-01')),
        PARTITION p_2024 VALUES LESS THAN (UNIX_TIMESTAMP('2025-01-01')),
        PARTITION p_2025 VALUES LESS THAN (UNIX_TIMESTAMP('2026-01-01')),
        PARTITION p_future VALUES LESS THAN MAXVALUE
    );
```

Cu partiționarea, interogările cu filtru pe `clock` pot folosi partition pruning și evita full scan-ul pe întregul tabel. Interogarea de agregare care a cauzat crash-ul, cu un filtru temporal rezonabil, ar deveni gestionabilă [2].

**Politică de retenție activă**

Definirea unei ferestre de retenție (ex. 12 luni) și implementarea unei proceduri de purge periodic. Pe 1,3 miliarde de rânduri, chiar și o retenție de 6 luni reduce semnificativ dataset-ul activ.

**Query tuning**

Interogările de agregare fără filtru temporal pe `history_log` trebuie considerate operațiuni de mentenanță, nu interogări operative. Ar trebui executate pe replici dedicate, în ferestre de mentenanță, cu `MAX_EXECUTION_TIME` setat.

```sql
-- Versiunea sigură a interogării incriminate
SELECT /*+ MAX_EXECUTION_TIME(30000) */ itemid, MIN(clock), MAX(clock), COUNT(*)
FROM history_log
WHERE clock >= UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 30 DAY))
GROUP BY itemid;
```

## Regula de bază care se uită

Fix-ul a fost ceea ce era: diagnostic corect, valori rezonabile, rolling restart. Nicio magie, niciun eroism — un apel de câteva ore cu o echipă care știa ce avea pe masă, și câteva priviri din exterior care au verificat matematica bufferelor.

Ceea ce frapează, privind înapoi, este cât de des configurarea bufferelor per thread este neglijată față de dimensionarea buffer pool-ului. `innodb_buffer_pool_size` este parametrul pe care toată lumea îl verifică primul — și e corect, este cel mai impactant. Bufferele per thread precum `join_buffer_size`, `sort_buffer_size`, `read_buffer_size` au însă o caracteristică insidioasă: se alocă per conexiune, iar impactul lor real depinde de numărul de conexiuni concurente active.

Formula este simplă:

```
memorie_per_thread × max_connections = presiune potențială maximă
```

Trebuie calculată explicit când se dimensionează un server MySQL, și trebuie comparată cu RAM-ul disponibil net de buffer pool și de overhead-ul OS. Dacă rezultatul depășește RAM-ul fizic, sistemul este structural fragil — nu „ar putea avea situații critice", ci **le va avea**, când sarcina va fi cea potrivită.

În acest caz sarcina potrivită a fost o interogare agregată pe un tabel cu 1,3 miliarde de rânduri, într-o marți dimineață oarecare. Putea fi orice altceva, în orice alt moment.

## Fonti ufficiali

1. MySQL 8.0 Reference Manual — [Performance Schema Statement Digests](https://dev.mysql.com/doc/refman/8.0/en/performance-schema-statement-digests.html)
2. MySQL 8.0 Reference Manual — [RANGE Partitioning](https://dev.mysql.com/doc/refman/8.0/en/partitioning-range.html)
3. MySQL 8.0 Reference Manual — [Memory Use in MySQL](https://dev.mysql.com/doc/refman/8.0/en/memory-use.html)
4. MySQL 8.0 Reference Manual — [InnoDB Cluster — Rolling Restart](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-innodb-cluster-working-with-cluster.html)

## Glosar candidat

- **join_buffer_size** (MySQL) — Buffer alocat per thread pentru fiecare join executat fără index. Spre deosebire de buffer pool, se alocă pentru fiecare conexiune activă: impactul său asupra memoriei totale depinde de numărul de conexiuni concurente.

- **innodb_buffer_pool_size** (MySQL/InnoDB) — Parametru global care definește dimensiunea cache-ului principal InnoDB pentru date și indecși. Este parametrul de memorie cu cel mai mare impact în MySQL: în mod tipic se dimensionează la 70-80% din RAM-ul disponibil pe servere dedicate.

- **Group Replication** (MySQL) — Mecanism de replicare sincronă multi-master integrat în MySQL, baza InnoDB Cluster. Garantează consistența între noduri printr-un protocol de consens distribuit; permite rolling restart fără pierderea quorum-ului cu 3+ noduri.

- **performance_schema** (MySQL) — Schema de sistem care colectează metrici de execuție în timp real: statistici per query digest, wait events, memorie alocată per thread. Baza pentru diagnosticarea performanțelor fără instrumente externe.

- **rolling restart** — Procedură de repornire secvențială a nodurilor unui cluster care menține serviciul activ în timpul operațiunii. Pe InnoDB Cluster cu 3 noduri, permite aplicarea modificărilor de configurație fără downtime, repornind câte un nod pe rând în timp ce celelalte mențin quorum-ul.
