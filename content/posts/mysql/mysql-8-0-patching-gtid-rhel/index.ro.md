---
categories:
- mysql
date: '2026-08-18'
description: 'Upgrade MySQL Community 8.0.34→8.0.45 pe RHEL 8: view-uri invalide,
  GTID, verificarea replicii și pașii corecți de patching. Workflow real, cu query-urile
  folosite.'
draft: false
image: mysql-8-0-patching-gtid-rhel.cover.jpg
seoTitle: 'Upgrade MySQL 8.0 pe RHEL 8: ghid practic pentru DBA'
tags:
- mysql
- upgrade
- rhel
- gtid
- mysqldump
title: Tichetul spunea «actualizează MySQL și oprește serviciul»
translationKey: mysql_8_0_patching_gtid_rhel
webo_generated_at: 2026-08-08
webo_status: scheduled
---

## Tichetul spunea «actualizează MySQL și oprește serviciul»

Tichetul a sosit dimineața: actualizare MySQL Community de la 8.0.34 la 8.0.45 pe un server RHEL 8.3, apoi oprirea serviciului aplicativ pentru o fereastră de mentenanță. Patru rânduri, niciun detaliu.

„Pare simplu" este cea mai periculoasă frază pe care un DBA o poate gândi înainte să atingă un sistem în producție. De fiecare dată când ne-am încrezut în acea senzație am găsit ceva neașteptat. De data aceasta nu a fost diferit: view-uri invalide care blocau dump-ul, GTID activat, o replică configurată dar oprită pe care nimeni nu o putea explica. Nimic dramatic, totul de gestionat în ordinea corectă.

Ceea ce urmează este workflow-ul real, cu query-urile folosite și erorile întâlnite. Nu documentația oficială MySQL — aceea e pe `dev.mysql.com` și o știe toată lumea. Aici e terenul.

---

## Cât spațiu ocupă cu adevărat această bază de date?

Înainte de orice, trebuie să înțelegi cu ce ai de-a face. Baza de date în cauză era mică — aproximativ 135 MB, 58 tabele, un singur schema aplicativ — și „mică" nu înseamnă „fără surprize".

Query-urile pe `information_schema` pe care le folosesc întotdeauna ca prim pas:

```sql
-- Dimensiunea totală a schemei
SELECT
    table_schema                                    AS schema_name,
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS size_mb,
    COUNT(*)                                        AS table_count
FROM information_schema.tables
WHERE table_schema NOT IN ('mysql','information_schema','performance_schema','sys')
GROUP BY table_schema
ORDER BY size_mb DESC;
```

```sql
-- Cele mai mari tabele, cu estimare rânduri și spațiu eliberabil
SELECT
    table_name,
    ROUND((data_length + index_length) / 1024 / 1024, 2) AS size_mb,
    table_rows                                            AS estimated_rows,
    data_free / 1024 / 1024                               AS free_mb
FROM information_schema.tables
WHERE table_schema = 'app_monitoring'
ORDER BY (data_length + index_length) DESC
LIMIT 10;
```

În acest caz, cele trei tabele mai mari erau toate de monitorizare: `event_log` (~43 MB, ~500K rânduri), `metric_snapshot` (~41 MB, ~320K rânduri), `alert_history` (~28 MB, ~290K rânduri). Niciun BLOB, niciun TEXT de dimensiuni mari — dump-ul ar fi fost rapid.

Verific și dacă există coloane de tip BLOB sau MEDIUMBLOB care ar putea umfla timpii:

```sql
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'app_monitoring'
  AND data_type IN ('blob','mediumblob','longblob','text','mediumtext','longtext')
ORDER BY table_name;
```

Zero rezultate. Bine. Se continuă cu backup-ul.

---

## mysqldump se blochează: eroarea 1356 și view-urile invalide

Lansez dump-ul. Treizeci de secunde de liniște, apoi:

```text
mysqldump: Got error: 1356: View 'app_monitoring.v_active_alerts' references
invalid table(s) or column(s) or function(s) or definer/invoker of view
lack rights to use them when using LOCK TABLES
```

Dump-ul s-a oprit pe un view. Nu e rar: cineva modifică o tabelă de bază — redenumește o coloană, o șterge, îi schimbă tipul — iar view-ul care o referențiază devine invalid fără ca nimeni să observe, până când nu se încearcă un dump sau o interogare directă pe acel view.

Primul lucru este să mapezi toate view-urile invalide din schemă. Nu doar cele care returnează eroarea 1356 explicit — și cele cu `last_altered` sau `created` NULL în `information_schema`, care indică adesea obiecte corupte sau care nu pot fi compilate [1]:

```sql
-- Metadate ale view-urilor: definer, security_type, updatabilitate
SELECT
    table_name     AS view_name,
    definer,
    security_type,
    is_updatable,
    check_option
FROM information_schema.views
WHERE table_schema = 'app_monitoring'
ORDER BY table_name;
```

```sql
-- Verificare directă: lista view-urilor pentru a itera cu SELECT * LIMIT 1 pe fiecare
-- (util într-un script pentru scheme mari)
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'app_monitoring'
  AND table_type = 'VIEW';
```

În acest caz am găsit 6 view-uri problematice: 2 cu eroarea 1356 explicită, 4 cu `created` NULL în `information_schema` — semn că MySQL nu reușea să le compileze în momentul interogării.

Strategia este să le excludem din dump-ul principal și să salvăm separat doar DDL-ul lor cu `--force`, pentru a nu pierde urma definiției lor:

```bash
# Dump principal fără view-urile invalide
mysqldump \
  --single-transaction \
  --routines \
  --triggers \
  --events \
  --ignore-table=app_monitoring.v_active_alerts \
  --ignore-table=app_monitoring.v_alert_summary \
  --ignore-table=app_monitoring.v_metric_daily \
  --ignore-table=app_monitoring.v_metric_hourly \
  --ignore-table=app_monitoring.v_event_open \
  --ignore-table=app_monitoring.v_event_closed \
  app_monitoring > /backup/app_monitoring_$(date +%Y%m%d_%H%M).sql

# DDL-ul view-urilor invalide (doar structura, cu --force pentru a nu se bloca)
mysqldump \
  --no-data \
  --force \
  app_monitoring \
  v_active_alerts v_alert_summary v_metric_daily \
  v_metric_hourly v_event_open v_event_closed \
  > /backup/app_monitoring_broken_views_$(date +%Y%m%d_%H%M).sql
```

Al doilea dump cu `--force` produce DDL-ul view-urilor chiar dacă sunt invalide — util pentru a le recrea ulterior, odată rezolvate tabelele de bază. Nu rezolvă problema view-urilor invalide, dar cel puțin rămâne o urmă a ce exista.

---

## Avertismentul GTID și când să folosești `--set-gtid-purged=OFF`

În timpul dump-ului principal apare acest avertisment:

```text
Warning: A partial dump from a server that has GTIDs will by default include
the GTIDs of all transactions, even those that changed suppressed parts of
the database. If you don't want to restore the GTIDs, pass
--set-gtid-purged=OFF. To make a complete dump, pass --all-databases
--triggers --routines --events.
```

GTID-urile — *Global Transaction Identifiers* — sunt identificatori unici asignați de MySQL fiecărei tranzacții când `gtid_mode=ON` [2]. Servesc în principal replicii: fiecare server ține evidența GTID-urilor pe care le-a executat deja, iar replica folosește această informație pentru a ști de unde să reia.

Avertismentul spune: faci un dump parțial (doar o schemă, nu `--all-databases`), iar dump-ul va include totuși setul de GTID al întregului server. Dacă apoi imporți acest dump pe un alt server, acel server va crede că a executat deja toate acele tranzacții — condiție care poate strica o replică tocmai configurată.

În acest caz dump-ul servește doar ca backup pre-upgrade, nu pentru a replica pe un alt server. Adaug `--set-gtid-purged=OFF`:

```bash
mysqldump \
  --single-transaction \
  --routines \
  --triggers \
  --events \
  --set-gtid-purged=OFF \
  --ignore-table=app_monitoring.v_active_alerts \
  [... alte --ignore-table ...] \
  app_monitoring > /backup/app_monitoring_$(date +%Y%m%d_%H%M).sql
```

Regulă practică: dacă dump-ul e pentru backup/restore pe același server sau pe un server standalone, `--set-gtid-purged=OFF` este aproape întotdeauna alegerea corectă. Dacă construiești o replică sau faci point-in-time recovery pe un server cu GTID, situația e mai complexă — subiect pentru un alt articol.

---

## Înainte de oprire: serverul acesta e master, replică sau standalone?

Backup-ul e gata. Acum vine pasul pe care mulți îl sar: înțelegerea rolului serverului în cluster înainte de a-l opri.

Oprirea unui master fără a promova o replică provoacă downtime. Oprirea unui nod Galera fără a verifica quorum-ul poate corupe clusterul. Chiar și în acest caz, unde serverul părea standalone, verificarea este obligatorie.

Query-urile de executat în ordine:

```sql
-- 1. Starea replicii (dacă acest server este replica cuiva)
SHOW REPLICA STATUS\G
```

```sql
-- 2. Starea ca sursă (dacă acest server are replici)
SHOW BINARY LOG STATUS\G
SHOW REPLICAS\G
```

```sql
-- 3. Group Replication sau cluster InnoDB
SELECT * FROM performance_schema.replication_group_members;
```

```sql
-- 4. Parametri cheie
SHOW VARIABLES LIKE 'server_id';
SHOW VARIABLES LIKE 'read_only';
SHOW VARIABLES LIKE 'gtid_mode';
SHOW VARIABLES LIKE 'group_replication%';
```

Rezultat în acest caz: `SHOW REPLICA STATUS` returnează un rând cu `Replica_IO_Running: No` și `Replica_SQL_Running: No` — replica era configurată dar oprită de mult timp. `SHOW REPLICAS` returnează zero rânduri. `replication_group_members` este goală. `server_id=1`, `read_only=OFF`.

De fapt un server standalone cu rămășițele unei configurații de replică niciodată finalizate sau abandonate. Niciun risc de downtime în cascadă. Se continuă.

---

## Upgrade-ul RPM: toate pachetele, în ordinea corectă

Oprirea serviciului:

```bash
systemctl stop mysqld
systemctl status mysqld   # verificare că e cu adevărat oprit
```

Cea mai frecventă greșeală în această fază este actualizarea doar a `mysql-community-server`, uitând pachetele dependente. Pe RHEL 8 cu repo-urile MySQL Community, pachetele de actualizat împreună sunt [3]:

```bash
# Verificare versiune curentă
rpm -qa | grep mysql | sort

# Upgrade al tuturor pachetelor MySQL dintr-o singură comandă
dnf upgrade \
  mysql-community-server \
  mysql-community-client \
  mysql-community-libs \
  mysql-community-common \
  mysql-community-client-plugins \
  mysql-community-icu-data-files
```

Dacă actualizezi doar `mysql-community-server` și lași `mysql-community-libs` la versiunea anterioară, obții erori de linking la repornire care nu sunt ușor de diagnosticat. Mai bine actualizezi totul împreună.

Repornire și verificare:

```bash
systemctl start mysqld
systemctl status mysqld

# Verificare versiune
mysql -u root -p -e "SELECT VERSION();"
```

```text
+-----------+
| VERSION() |
+-----------+
| 8.0.45    |
+-----------+
```

În MySQL 8.0 upgrade-ul schemei interne — cel care în versiunile anterioare necesita `mysql_upgrade` manual — este automat la prima pornire [4]. Serverul execută migrările necesare și scrie în log:

```text
[System] [MY-013381] [Server] Server upgrade from '80034' to '80045' started.
[System] [MY-013381] [Server] Server upgrade from '80034' to '80045' completed.
```

Dacă acele două rânduri nu apar, ceva nu a mers cum trebuia. Verifică întotdeauna:

```bash
grep -i "upgrade" /var/log/mysqld.log | tail -5
```

---

## Verificare post-upgrade: nu e suficient că pornește

Serverul a pornit și afișează versiunea corectă. Nu s-a terminat încă.

```sql
-- Verificare tabele de sistem
CHECK TABLE mysql.user;
CHECK TABLE mysql.db;

-- Verificare că tabelele aplicative sunt accesibile
SELECT COUNT(*) FROM app_monitoring.event_log;
SELECT COUNT(*) FROM app_monitoring.metric_snapshot;

-- Verificare variabile critice post-upgrade
SHOW VARIABLES LIKE 'gtid_mode';
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
SHOW VARIABLES LIKE 'max_connections';
```

View-urile invalide existau deja înainte de upgrade și rămân invalide după — upgrade-ul nu le repară, evident. Trebuie rezolvate separat, odată clarificat cu echipa aplicativă ce tabele de bază s-au modificat și cum.

O ultimă verificare în log pentru erori silențioase:

```bash
grep -i "error\|warning\|corrupt" /var/log/mysqld.log | grep -v "^#" | tail -20
```

În acest caz totul curat. Patching-ul este finalizat.

---

## Un tichet de patru rânduri nu clarifică complexitatea activității

Patching-ul MySQL nu e complicat. Comenzile sunt puține și documentația oficială e bună. Partea dificilă nu e executarea pașilor — e să știi ce întrebări să pui înainte de a începe.

Cât de mare e baza de date? Există obiecte invalide? Serverul acesta are un rol în cluster? GTID-urile sunt activate și ce implică asta pentru dump? Fiecare întrebare sărită este un risc care se materializează în cel mai prost moment: în timpul ferestrei de mentenanță, cu cineva care așteaptă.

Diferența dintre o abordare junior și una senior nu stă în comenzi — stă în timpul petrecut înainte de a le lansa. Query-urile pe `information_schema`, verificarea replicii, controlul log-ului post-upgrade: sunt toți pași care par redundanți până când nu mai sunt.

View-urile invalide în acest caz erau deja invalide înainte de patching. Upgrade-ul nu le-a creat, le-a făcut doar vizibile pentru că cineva a încercat să facă un dump pentru prima dată în luni de zile. E tipul de descoperire care răsplătește timpul unei analize pre-backup atente: nu pentru a bloca patching-ul, ci pentru a nu fi surprins la jumătatea drumului.

---

## Fonti ufficiali

1. MySQL 8.0 Reference Manual — [INFORMATION_SCHEMA VIEWS Table](https://dev.mysql.com/doc/refman/8.0/en/information-schema-views-table.html)
2. MySQL 8.0 Reference Manual — [Replication with Global Transaction Identifiers](https://dev.mysql.com/doc/refman/8.0/en/replication-gtids.html)
3. MySQL 8.0 Reference Manual — [Installing MySQL on Linux Using the MySQL Yum Repository](https://dev.mysql.com/doc/refman/8.0/en/linux-installation-yum-repo.html)
4. MySQL 8.0 Reference Manual — [Upgrading MySQL](https://dev.mysql.com/doc/refman/8.0/en/upgrading.html)

---

## Glosar candidat

- **GTID** (MySQL) — *Global Transaction Identifier*: identificator unic asignat fiecărei tranzacții când `gtid_mode=ON`. Compus din `server_uuid:număr_secvență`, permite replicii să urmărească exact ce tranzacții a aplicat deja, independent de poziția în binlog.

- **mysqldump** — utilitar de backup logic inclus în MySQL. Produce un fișier SQL cu instrucțiunile `CREATE` și `INSERT` pentru a recrea baza de date. Potrivit pentru baze de date de dimensiuni mici și medii; pentru volume mari se preferă instrumente precum mydumper sau backup-uri fizice cu xtrabackup.

- **View invalid** (MySQL) — vedere al cărei corp SQL face referire la obiecte care nu mai există sau nu sunt accesibile (tabele redenumite, coloane șterse, permisiuni revocate). MySQL nu invalidează automat view-urile la modificarea tabelei de bază: eroarea apare doar la prima execuție sau în timpul unui dump.

- **`--single-transaction`** (mysqldump) — flag care inițiază o tranzacție `REPEATABLE READ` înainte de dump, garantând consistența fără a achiziționa lock-uri pe tabelele InnoDB. Nu se aplică tabelelor MyISAM, care necesită `--lock-tables`.

- **`replication_group_members`** (MySQL Performance Schema) — tabelă de sistem care listează nodurile active într-un cluster Group Replication, cu starea (`ONLINE`, `RECOVERING`, `UNREACHABLE`) și rolul (`PRIMARY`, `SECONDARY`). Goală pe servere standalone sau cu replică tradițională.
