---
categories:
- mysql
date: '2026-08-25'
description: 'Cum am redus lag-ul de replicare MySQL de la patru ore la treizeci de
  secunde: GTID, parallel replication cu LOGICAL_CLOCK și monitorizare reală cu pt-heartbeat.'
draft: false
image: replica-mysql-quando-lo-slave-resta-indietro-e-nessuno-se-ne-accorge.cover.jpg
seoTitle: 'MySQL replica lag: GTID, parallel replication și pt-heartbeat'
tags:
- mysql
- replication
- gtid
- performance-tuning
- monitoring
title: 'Raportul de luni dimineața: patru ore de lag pe replica MySQL'
translationKey: replica_mysql_quando_lo_slave_resta_indietro_e_nessuno_se_ne_accorge
webo_generated_at: 2026-08-08
webo_status: scheduled
---

## Raportul de luni dimineața

Era o luni dimineața. Responsabilul comercial al unui mare operator poștal și logistic național tocmai deschisese raportul săptămânal al expedierilor și se uita la niște cifre care nu se potriveau. Livrările de vineri după-amiază apăreau încă „în tranzit". KPI-urile de sâmbătă erau la zero. Ceva nu mergea, iar prima ipoteză fusese un bug în aplicația de raportare.

Când am ajuns să ne uităm, bug-ul nu exista. Era ceva mai subtil: replica MySQL pe care rulau toate interogările de raportare acumula patru ore de întârziere față de master. Datele erau acolo, corecte, pe master — dar replica le aplica cu ore în urmă. Și niciun alert nu se declanșase.

Patru ore de lag într-un sistem logistic înseamnă decizii operaționale luate pe cifre greșite. Înseamnă că responsabilul de depozit a planificat turele de weekend pe date care nu reflectau realitatea. Înseamnă că sistemul de prioritizare a expedierilor urgente lucra pe o fotografie veche de jumătate de zi lucrătoare.

Articolul de față povestește cum funcționează replicarea MySQL sub capotă, de ce instrumentul său principal de monitorizare este nesigur și ce am făcut pentru a rezolva — fără magie, cu profiling și câteva decizii arhitecturale.

---

## Binlog, relay log și cele două thread-uri care nu se înțeleg îndeajuns

Ca să înțelegi de ce replica acumulează lag, trebuie să înțelegi cum funcționează cu adevărat. Replicarea asincronă MySQL se bazează pe trei componente principale: **binary log**-ul pe master, **relay log**-ul pe slave și două thread-uri care lucrează în secvență.

**IO thread**-ul de pe slave se conectează la master și citește evenimentele din binlog, scriindu-le local în relay log. Este o citire secvențială, în general rapidă, rareori gâtuiala sistemului.

**SQL thread**-ul citește relay log-ul și aplică evenimentele în baza de date locală a slave-ului. Aici stă problema: în configurația clasică, acest thread este **single-threaded**. Aplică un eveniment pe rând, în secvență. Dacă masterul are zece sesiuni care scriu în paralel, slave-ul le aplică una după alta.

```text
MASTER
  ├── sesiune 1 → INSERT INTO spedizioni (...)
  ├── sesiune 2 → UPDATE tracking SET stato = 'consegnato' WHERE ...
  ├── sesiune 3 → INSERT INTO eventi_logistici (...)
  └── ... (N sesiuni paralele)
         │
         ▼ binlog (serializat)
SLAVE IO thread → relay log → SQL thread (single-threaded)
         ▼
  aplică evenimentul 1, apoi evenimentul 2, apoi evenimentul 3...
```

Masterul scrie în paralel, slave-ul aplică în serie. Pe un sistem cu încărcare susținută, această asimetrie este cauza principală a lag-ului.

---

## De ce Seconds_Behind_Master minte

Primul lucru pe care îl verifici când suspectezi lag este `SHOW SLAVE STATUS\G`. Câmpul `Seconds_Behind_Master` pare exact ce ai nevoie. Nu este.

```sql
SHOW SLAVE STATUS\G
-- ...
Seconds_Behind_Master: 14523
-- ...
```

Paisprezece mii de secunde. Patru ore. Numărul era acolo — dar problema e că această valoare este calculată într-un mod care o face nesigură în mai multe scenarii comune.

`Seconds_Behind_Master` măsoară diferența dintre timestamp-ul evenimentului pe care SQL thread-ul îl **aplică în acel moment** și ora curentă a sistemului. Dacă SQL thread-ul este blocat (din cauza unui lock, a unei erori, sau pentru că relay log-ul s-a epuizat și IO thread-ul nu a primit încă noi evenimente), valoarea încetează să se actualizeze sau se comportă imprevizibil.

Și mai insidios: dacă replicarea se întrerupe și repornește, `Seconds_Behind_Master` poate reveni la zero înainte ca lag-ul să fie recuperat efectiv, deoarece IO thread-ul a descărcat relay log-ul, dar SQL thread-ul nu a terminat încă de aplicat. Câmpul reflectă starea SQL thread-ului, nu întârzierea reală față de master.

În practică, `Seconds_Behind_Master` este util ca indicator grosier, dar nu ca bază pentru alerting. [1]

**Ce să folosești în loc**: cu **replicarea bazată pe GTID** activă, poți calcula lag-ul real comparând setul de tranzacții executate pe master (`gtid_executed` pe master) cu cel aplicat pe slave (`gtid_executed` pe slave). Diferența — numărul de tranzacții în așteptare — este o metrică mult mai fiabilă.

```sql
-- Pe master
SELECT @@global.gtid_executed;

-- Pe slave
SELECT @@global.gtid_executed;
-- Diferența dintre cele două seturi reprezintă lag-ul real în termeni de tranzacții
```

Cu instrumente precum `pt-heartbeat` din Percona Toolkit se poate măsura lag-ul cu și mai multă precizie: tool-ul scrie un timestamp pe master la intervale regulate și măsoară cât timp îi ia să apară pe slave. [2]

---

## Cauzele cele mai frecvente de slave lag

În cazul specific, am identificat trei cauze concurente:

**1. Interogări grele neoptimizate pe master**

Masterul executa în fiecare noapte un batch de actualizare masivă: `UPDATE spedizioni SET stato_elaborazione = 'archiviato' WHERE data_spedizione < DATE_SUB(NOW(), INTERVAL 90 DAY)`. Niciun index pe `data_spedizione`. Interogarea făcea un full table scan pe un tabel de 180 de milioane de rânduri, producea un singur eveniment binlog uriaș, iar slave-ul avea nevoie de 40 de minute să îl aplice — timp în care nu aplica nimic altceva.

**2. SQL thread single-threaded sub încărcare susținută**

În orele de vârf (între 14 și 18), masterul primea aproximativ 800 de scrieri/secundă distribuite pe zeci de sesiuni paralele. SQL thread-ul nu reușea să țină pasul: fiecare oră de producție intensă adăuga aproximativ 20-30 de minute de lag acumulat.

**3. I/O lent pe slave**

Slave-ul se afla pe storage partajat cu alte servicii. În orele de vârf, latența de scriere pe disc urca la valori care încetineau și mai mult aplicarea evenimentelor. Relay log-ul era scris și citit cu latențe care amplificau problema single-thread.

---

## GTID: de ce merită să migrezi acum

**Global Transaction ID** (GTID) este un identificator unic atribuit fiecărei tranzacții committate pe master. [3] Fiecare tranzacție are un GTID în formatul `source_id:transaction_id`, unde `source_id` este UUID-ul serverului master.

```sql
-- Activarea GTID pe master (necesită restart sau SET PERSIST pe MySQL 8.0+)
SET PERSIST gtid_mode = ON;
SET PERSIST enforce_gtid_consistency = ON;

-- Verificarea stării
SHOW VARIABLES LIKE 'gtid_mode';
-- gtid_mode | ON
```

Avantajele față de replicarea bazată pe poziție în binlog sunt concrete:

- **Failover mai simplu**: cu GTID, un slave nou știe exact de unde să reia fără a calcula manual poziția în binlog
- **Monitorizarea lag-ului real**: după cum am descris mai sus, compararea seturilor GTID este mult mai fiabilă decât `Seconds_Behind_Master`
- **Detectarea tranzacțiilor lipsă**: dacă o tranzacție a fost aplicată pe master dar nu pe slave, golul este imediat vizibil în setul GTID

În contextul acestui proiect, migrarea la GTID era deja planificată, dar neexecutată. Finalizarea ei înainte de a aborda problema lag-ului ar fi făcut diagnosticarea mult mai rapidă.

---

## De la single-thread la parallel replication

Soluția pentru gâtuiala SQL thread-ului este **parallel replication**, disponibilă în MySQL 5.7+ și MariaDB 10.0+. [4]

Ideea de bază: în loc să aplice evenimentele în secvență cu un singur thread, se folosesc mai multe worker thread-uri care aplică tranzacțiile în paralel — respectând constrângerile de consistență.

MySQL oferă două moduri de paralelizare:

- **`DATABASE`**: tranzacțiile care modifică baze de date diferite sunt aplicate în paralel. Simplu, dar inutil dacă toate scrierile merg pe aceeași bază de date.
- **`LOGICAL_CLOCK`** (modul corect pentru majoritatea cazurilor): exploatează informațiile de commit timestamp din binlog pentru a identifica tranzacțiile care rulau simultan pe master și pot fi aplicate în paralel pe slave.

```sql
-- Configurare pe slave
STOP SLAVE SQL_THREAD;

SET GLOBAL slave_parallel_type = 'LOGICAL_CLOCK';
SET GLOBAL slave_parallel_workers = 8;
SET GLOBAL slave_preserve_commit_order = ON;

START SLAVE SQL_THREAD;
```

Parametrul `slave_preserve_commit_order = ON` garantează că tranzacțiile sunt committate pe slave în aceeași ordine în care erau pe master — esențial pentru consistența citirilor. [4]

Pentru a valorifica la maximum `LOGICAL_CLOCK`, masterul trebuie să aibă `binlog_group_commit_sync_delay` configurat astfel încât să grupeze mai multe tranzacții în același commit group. Acest lucru crește ușor latența de commit pe master, dar crește semnificativ paralelismul disponibil pe slave.

```sql
-- Pe master: mărirea ferestrei de group commit
-- (valoare în microsecunde, 1000 = 1ms)
SET GLOBAL binlog_group_commit_sync_delay = 1000;
SET GLOBAL binlog_group_commit_sync_no_delay_count = 10;
```

---

## Ce a funcționat cu adevărat

Am lucrat pe trei fronturi în paralel, iar rezultatul final a fost o reducere a lag-ului de la patru ore la mai puțin de treizeci de secunde în condiții normale.

**Frontul 1: parallel replication cu 8 worker-i**

După activarea `LOGICAL_CLOCK` cu 8 worker thread-uri, throughput-ul slave-ului a crescut semnificativ. Lag-ul acumulat s-a redus în câteva ore. DBA-ul clientului evaluase deja această opțiune anterior, dar se lovise de rezistență internă pentru că „mergea așa de ani de zile" — criza a deblocat conversația.

**Frontul 2: optimizarea interogării batch**

Interogarea de arhivare nocturnă a fost rescrisă pentru a opera în batch-uri mai mici, cu un index adăugat pe `data_spedizione`:

```sql
-- Înainte: un singur UPDATE uriaș
UPDATE spedizioni
SET stato_elaborazione = 'archiviato'
WHERE data_spedizione < DATE_SUB(NOW(), INTERVAL 90 DAY);

-- După: batch-uri de 10.000 de rânduri cu pauză între ele
-- (executat dintr-un script Python cu loop + sleep)
UPDATE spedizioni
SET stato_elaborazione = 'archiviato'
WHERE data_spedizione < DATE_SUB(NOW(), INTERVAL 90 DAY)
  AND stato_elaborazione != 'archiviato'
LIMIT 10000;
```

```sql
-- Index adăugat
ALTER TABLE spedizioni
ADD INDEX idx_data_elaborazione (data_spedizione, stato_elaborazione);
```

Aceasta a eliminat vârful de lag nocturn: în loc de un singur eveniment de 40 de minute, slave-ul aplica mii de evenimente mici distribuite pe parcursul unei ore, fără să se blocheze niciodată.

**Frontul 3: storage dedicat pentru slave**

Slave-ul a fost mutat pe storage dedicat cu latențe de scriere coerente. Singur, acest lucru nu ar fi rezolvat problema, dar a eliminat variabilitatea care făcea lag-ul imprevizibil în orele de vârf.

---

## Monitorizare care nu minte

După rezolvarea lag-ului, am construit un sistem de alerting care să nu se bazeze pe `Seconds_Behind_Master`.

Soluția adoptată a fost `pt-heartbeat` din Percona Toolkit, configurat să scrie un timestamp pe master în fiecare secundă și să măsoare întârzierea pe slave:

```bash
# Pe master: pornirea daemon-ului care scrie heartbeat-ul
pt-heartbeat \
  --user=monitor_user \
  --password=*** \
  --host=mysql-master-01 \
  --database=monitoring \
  --create-table \
  --daemonize \
  --update

# Pe slave: măsurarea lag-ului real
pt-heartbeat \
  --user=monitor_user \
  --password=*** \
  --host=mysql-replica-01 \
  --database=monitoring \
  --monitor \
  --master-server-id=1
```

Valoarea returnată de `pt-heartbeat --monitor` este lag-ul real în secunde, calculat pe baza timestamp-urilor efective — nu pe poziția în binlog și nici pe `Seconds_Behind_Master`.

Am configurat alerte pe două praguri:

- **Warning la 60 de secunde**: notificare către echipă, nicio acțiune automată
- **Critical la 300 de secunde (5 minute)**: notificare urgentă + blocarea automată a interogărilor de raportare (redirect temporar către master cu interogări în read-only)

Blocarea automată era partea cea mai delicată: mai bine să returnezi o eroare explicită utilizatorului („date temporar indisponibile, încearcă din nou în câteva minute") decât să returnezi date vechi de ore fără niciun avertisment.

---

## Patru ore devin treizeci de secunde

Lag-ul de patru ore era simptomul vizibil al trei probleme suprapuse: arhitectură single-thread, interogare batch neoptimizată, storage partajat. Niciuna dintre ele, singură, nu ar fi cauzat patru ore de întârziere — împreună, se amplificau reciproc.

Partea cea mai interesantă a acestei povești nu este tehnică: este că problema exista probabil de luni de zile, și nimeni nu o observase pentru că `Seconds_Behind_Master` nu era monitorizat sistematic, iar când era verificat manual dădea valori care păreau rezonabile în orele de activitate scăzută.

Monitorizarea lag-ului de replicare nu este un nice-to-have. Este o metrică operațională care impactează direct calitatea datelor pe care business-ul le folosește pentru a lua decizii. Dacă interogările de raportare rulează pe o replică, lag-ul acelei replici face parte integrantă din calitatea datelor — și trebuie tratat ca atare, cu alerte, praguri și un plan de răspuns.

`Seconds_Behind_Master` este un punct de plecare, nu un răspuns. `pt-heartbeat` sau compararea seturilor GTID sunt instrumente mult mai fiabile. Iar parallel replication, pe MySQL 5.7+ cu `LOGICAL_CLOCK`, este astăzi configurația implicită rezonabilă pentru orice replică ce primește încărcare susținută.

---

## Fontes oficiale

1. MySQL 8.0 Reference Manual — [Replication Slave Status Variables: Seconds_Behind_Master](https://dev.mysql.com/doc/refman/8.0/en/show-replica-status.html)
2. Percona Toolkit Documentation — [pt-heartbeat](https://docs.percona.com/percona-toolkit/pt-heartbeat.html)
3. MySQL 8.0 Reference Manual — [GTID-Based Replication](https://dev.mysql.com/doc/refman/8.0/en/replication-gtids.html)
4. MySQL 8.0 Reference Manual — [Replication with Multithreaded Appliers](https://dev.mysql.com/doc/refman/8.0/en/replication-threads-applier.html)

---

## Glosar candidat

- **Binlog** (MySQL binary log) — registru secvențial al tuturor modificărilor de date pe masterul MySQL. Baza replicării: slave-ul citește binlog-ul pentru a ști ce să aplice. Format ROW, STATEMENT sau MIXED.

- **Relay log** — copie locală a binlog-ului masterului, scrisă de IO thread pe slave. SQL thread-ul citește relay log-ul pentru a aplica tranzacțiile. Este buffer-ul dintre recepția și aplicarea evenimentelor.

- **GTID** (Global Transaction Identifier) — identificator unic atribuit fiecărei tranzacții committate pe un server MySQL. Format `source_uuid:transaction_id`. Permite failover simplificat și monitorizarea precisă a lag-ului de replicare.

- **Parallel replication** — mod de aplicare a evenimentelor de replicare care folosește mai multe worker thread-uri în loc de un singur SQL thread. În MySQL, modul `LOGICAL_CLOCK` identifică tranzacțiile executabile în paralel pe baza commit timestamp-urilor din binlog.

- **pt-heartbeat** — tool din Percona Toolkit care măsoară lag-ul de replicare MySQL scriind timestamp-uri pe master și comparându-le cu valorile citite pe slave. Mai fiabil decât `Seconds_Behind_Master` pentru alerting în producție.
