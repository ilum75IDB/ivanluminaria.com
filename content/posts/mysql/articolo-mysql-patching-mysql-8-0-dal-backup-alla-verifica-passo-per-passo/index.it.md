---
categories:
- mysql
date: '2026-08-18'
description: 'View rotte, GTID warning, check replica prima dello stop: il workflow
  reale di un patching MySQL 8.0 su RHEL 8.3, con query riutilizzabili e tutti gli
  errori del campo.'
draft: false
image: articolo-mysql-patching-mysql-8-0-dal-backup-alla-verifica-passo-per-passo.cover.jpg
seoTitle: 'Patching MySQL 8.0.34→8.0.45 su RHEL 8: workflow completo'
tags:
- mysql-8
- patching
- mysqldump
- gtid
- rhel
title: 'MySQL 8.0.34→8.0.45: workflow di patching reale con errori inclusi'
translationKey: articolo_mysql_patching_mysql_8_0_dal_backup_alla_verifica_passo_per_passo
webo_generated_at: 2026-08-08
webo_status: scheduled
---

## Il ticket diceva "aggiorna MySQL e spegni il servizio"

Il ticket è arrivato la mattina: aggiornare MySQL Community da 8.0.34 a 8.0.45 su un server RHEL 8.3, poi spegnere il servizio applicativo per una finestra di manutenzione. Quattro righe, nessun dettaglio.

"Sembra semplice" è la frase più pericolosa che un DBA possa pensare prima di toccare un sistema in produzione. Ogni volta che ci siamo fidati di quella sensazione abbiamo trovato qualcosa di inaspettato. Questa volta non è andata diversamente: view rotte che bloccavano il dump, GTID abilitati, una replica configurata ma ferma che nessuno sapeva spiegare. Niente di drammatico, tutto da gestire nell'ordine giusto.

Quello che segue è il workflow reale, con le query usate e gli errori incontrati. Non la documentazione ufficiale MySQL — quella è su `dev.mysql.com` e la conoscono tutti. Qui c'è il campo.

---

## Quanto spazio occupa davvero questo database?

Prima di fare qualsiasi cosa, capire con cosa si ha a che fare. Il database in questione era piccolo — circa 135 MB, 58 tabelle, un solo schema applicativo — e "piccolo" non significa "senza sorprese".

Le query su `information_schema` che uso sempre come primo passo:

```sql
-- Dimensione totale dello schema
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
-- Le tabelle più grandi, con stima righe e spazio liberabile
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

In questo caso le tre tabelle più grandi erano tutte di monitoraggio: `event_log` (~43 MB, ~500K righe), `metric_snapshot` (~41 MB, ~320K righe), `alert_history` (~28 MB, ~290K righe). Nessun BLOB, nessun TEXT di grandi dimensioni — il dump sarebbe stato veloce.

Verifico anche se ci sono colonne di tipo BLOB o MEDIUMBLOB che potrebbero gonfiare i tempi:

```sql
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'app_monitoring'
  AND data_type IN ('blob','mediumblob','longblob','text','mediumtext','longtext')
ORDER BY table_name;
```

Zero risultati. Bene. Si procede con il backup.

---

## mysqldump si blocca: errore 1356 e le view rotte

Lancio il dump. Trenta secondi di silenzio, poi:

```text
mysqldump: Got error: 1356: View 'app_monitoring.v_active_alerts' references
invalid table(s) or column(s) or function(s) or definer/invoker of view
lack rights to use them when using LOCK TABLES
```

Il dump si è fermato su una view. Non è raro: qualcuno modifica una tabella sottostante — rinomina una colonna, la elimina, ne cambia il tipo — e la view che la referenzia diventa invalida senza che nessuno se ne accorga finché non si prova a fare un dump o una query diretta su quella view.

La prima cosa è mappare tutte le view invalide dello schema. Non solo quelle che restituiscono errore 1356 esplicito — anche quelle con `last_altered` o `created` NULL in `information_schema`, che spesso indicano oggetti corrotti o non compilabili [1]:

```sql
-- Metadati delle view: definer, security_type, updatabilità
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
-- Verifica diretta: elenco delle view per iterare con SELECT * LIMIT 1 su ognuna
-- (utile in uno script per schema grandi)
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'app_monitoring'
  AND table_type = 'VIEW';
```

In questo caso ho trovato 6 view problematiche: 2 con errore 1356 esplicito, 4 con `created` NULL in `information_schema` — segno che MySQL non riusciva a compilarle al momento della query.

La strategia è escluderle dal dump principale e salvarne la sola DDL a parte con `--force`, per non perdere traccia della loro definizione:

```bash
# Dump principale senza le view rotte
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

# DDL delle view rotte (solo struttura, con --force per non bloccarsi)
mysqldump \
  --no-data \
  --force \
  app_monitoring \
  v_active_alerts v_alert_summary v_metric_daily \
  v_metric_hourly v_event_open v_event_closed \
  > /backup/app_monitoring_broken_views_$(date +%Y%m%d_%H%M).sql
```

Il secondo dump con `--force` produce la DDL delle view anche se invalide — utile per ricrearle a posteriori, una volta sistemate le tabelle sottostanti. Non risolve il problema delle view rotte, ma almeno resta traccia di cosa c'era.

---

## Il warning GTID e quando usare `--set-gtid-purged=OFF`

Durante il dump principale compare questo avviso:

```text
Warning: A partial dump from a server that has GTIDs will by default include
the GTIDs of all transactions, even those that changed suppressed parts of
the database. If you don't want to restore the GTIDs, pass
--set-gtid-purged=OFF. To make a complete dump, pass --all-databases
--triggers --routines --events.
```

I GTID — *Global Transaction Identifiers* — sono identificatori univoci assegnati da MySQL a ogni transazione quando `gtid_mode=ON` [2]. Servono principalmente alla replica: ogni server tiene traccia di quali GTID ha già eseguito, e la replica usa questa informazione per sapere da dove riprendere.

Il warning dice: stai facendo un dump parziale (solo uno schema, non `--all-databases`), e il dump includerà comunque il set di GTID dell'intero server. Se poi importi questo dump su un altro server, quel server penserà di aver già eseguito tutte quelle transazioni — condizione che può rompere una replica appena impostata.

In questo caso il dump serve solo come backup pre-upgrade, non per replicare su un altro server. Aggiungo `--set-gtid-purged=OFF`:

```bash
mysqldump \
  --single-transaction \
  --routines \
  --triggers \
  --events \
  --set-gtid-purged=OFF \
  --ignore-table=app_monitoring.v_active_alerts \
  [... altre --ignore-table ...] \
  app_monitoring > /backup/app_monitoring_$(date +%Y%m%d_%H%M).sql
```

Regola pratica: se il dump è per backup/restore sullo stesso server o su un server standalone, `--set-gtid-purged=OFF` è quasi sempre la scelta corretta. Se stai costruendo una replica o facendo point-in-time recovery su un server con GTID, la situazione è più articolata — argomento per un altro articolo.

---

## Prima di spegnere: questo server è master, replica o standalone?

Il backup è fatto. Adesso viene il passaggio che molti saltano: capire il ruolo del server nel cluster prima di spegnerlo.

Spegnere un master senza promuovere una replica causa downtime. Spegnere un nodo Galera senza verificare il quorum può corrompere il cluster. Anche in questo caso, dove il server sembrava standalone, la verifica è obbligatoria.

Le query da eseguire nell'ordine:

```sql
-- 1. Stato della replica (se questo server è replica di qualcuno)
SHOW REPLICA STATUS\G
```

```sql
-- 2. Stato come sorgente (se questo server ha repliche)
SHOW BINARY LOG STATUS\G
SHOW REPLICAS\G
```

```sql
-- 3. Group Replication o cluster InnoDB
SELECT * FROM performance_schema.replication_group_members;
```

```sql
-- 4. Parametri chiave
SHOW VARIABLES LIKE 'server_id';
SHOW VARIABLES LIKE 'read_only';
SHOW VARIABLES LIKE 'gtid_mode';
SHOW VARIABLES LIKE 'group_replication%';
```

Risultato in questo caso: `SHOW REPLICA STATUS` restituisce una riga con `Replica_IO_Running: No` e `Replica_SQL_Running: No` — la replica era configurata ma ferma da tempo. `SHOW REPLICAS` restituisce zero righe. `replication_group_members` è vuota. `server_id=1`, `read_only=OFF`.

Di fatto un server standalone con i resti di una configurazione di replica mai completata o abbandonata. Nessun rischio di downtime a cascata. Si procede.

---

## L'upgrade RPM: tutti i pacchetti, nell'ordine giusto

Stop del servizio:

```bash
systemctl stop mysqld
systemctl status mysqld   # verifica che sia davvero fermo
```

L'errore più comune in questa fase è aggiornare solo `mysql-community-server` dimenticando i pacchetti dipendenti. Su RHEL 8 con i repo MySQL Community, i pacchetti da aggiornare insieme sono [3]:

```bash
# Verifica versione corrente
rpm -qa | grep mysql | sort

# Upgrade di tutti i pacchetti MySQL in un colpo solo
dnf upgrade \
  mysql-community-server \
  mysql-community-client \
  mysql-community-libs \
  mysql-community-common \
  mysql-community-client-plugins \
  mysql-community-icu-data-files
```

Aggiornando solo `mysql-community-server` e lasciando `mysql-community-libs` alla versione precedente si ottengono errori di linking al riavvio che non sono immediati da diagnosticare. Meglio aggiornare tutto insieme.

Riavvio e verifica:

```bash
systemctl start mysqld
systemctl status mysqld

# Verifica versione
mysql -u root -p -e "SELECT VERSION();"
```

```text
+-----------+
| VERSION() |
+-----------+
| 8.0.45    |
+-----------+
```

In MySQL 8.0 l'upgrade dello schema interno — quello che nelle versioni precedenti richiedeva `mysql_upgrade` manuale — è automatico al primo avvio [4]. Il server esegue le migrazioni necessarie e scrive nel log:

```text
[System] [MY-013381] [Server] Server upgrade from '80034' to '80045' started.
[System] [MY-013381] [Server] Server upgrade from '80034' to '80045' completed.
```

Se quelle due righe non compaiono, qualcosa non è andato come previsto. Verifica sempre:

```bash
grep -i "upgrade" /var/log/mysqld.log | tail -5
```

---

## Verifica post-upgrade: non basta che parta

Il server è partito e mostra la versione corretta. Non è ancora finita.

```sql
-- Verifica tabelle di sistema
CHECK TABLE mysql.user;
CHECK TABLE mysql.db;

-- Verifica che le tabelle applicative siano accessibili
SELECT COUNT(*) FROM app_monitoring.event_log;
SELECT COUNT(*) FROM app_monitoring.metric_snapshot;

-- Verifica variabili critiche post-upgrade
SHOW VARIABLES LIKE 'gtid_mode';
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
SHOW VARIABLES LIKE 'max_connections';
```

Le view rotte esistevano già prima dell'upgrade e restano rotte dopo — l'upgrade non le aggiusta, ovviamente. Vanno sistemate separatamente, una volta chiarito con il team applicativo quali tabelle sottostanti sono cambiate e come.

Un ultimo check sul log per errori silenziosi:

```bash
grep -i "error\|warning\|corrupt" /var/log/mysqld.log | grep -v "^#" | tail -20
```

In questo caso tutto pulito. Il patching è completato.

---

## Un ticket da quattro righe non chiarisce la complessità dell'attività

Il patching MySQL non è complicato. I comandi sono pochi e la documentazione ufficiale è buona. La parte difficile non è eseguire i passi — è sapere quali domande fare prima di iniziare.

Quanto è grande il database? Ci sono oggetti invalidi? Questo server ha un ruolo nel cluster? I GTID sono abilitati e cosa comporta per il dump? Ogni domanda saltata è un rischio che si materializza nel momento peggiore: durante la finestra di manutenzione, con qualcuno che aspetta.

La differenza tra un approccio junior e uno senior non sta nei comandi — sta nel tempo speso prima di lanciarli. Le query su `information_schema`, il check della replica, la verifica del log post-upgrade: sono tutti passi che sembrano ridondanti finché non lo sono.

Le view rotte in questo caso erano già rotte prima del patching. L'upgrade non le ha create, le ha solo rese visibili perché qualcuno ha provato a fare un dump per la prima volta in mesi. È il tipo di scoperta che ripaga il tempo di un'analisi pre-backup accurata: non per bloccare il patching, ma per non essere sorpresi a metà strada.

---

## Fonti ufficiali

1. MySQL 8.0 Reference Manual — [INFORMATION_SCHEMA VIEWS Table](https://dev.mysql.com/doc/refman/8.0/en/information-schema-views-table.html)
2. MySQL 8.0 Reference Manual — [Replication with Global Transaction Identifiers](https://dev.mysql.com/doc/refman/8.0/en/replication-gtids.html)
3. MySQL 8.0 Reference Manual — [Installing MySQL on Linux Using the MySQL Yum Repository](https://dev.mysql.com/doc/refman/8.0/en/linux-installation-yum-repo.html)
4. MySQL 8.0 Reference Manual — [Upgrading MySQL](https://dev.mysql.com/doc/refman/8.0/en/upgrading.html)

---

## Glossario candidato

- **GTID** (MySQL) — *Global Transaction Identifier*: identificatore univoco assegnato a ogni transazione quando `gtid_mode=ON`. Composto da `server_uuid:numero_sequenza`, permette alla replica di tracciare esattamente quali transazioni ha già applicato, indipendentemente dalla posizione nel binlog.

- **mysqldump** — utility di backup logico inclusa in MySQL. Produce un file SQL con le istruzioni `CREATE` e `INSERT` per ricreare il database. Adatto per database di piccole e medie dimensioni; per volumi elevati si preferiscono strumenti come mydumper o backup fisici con xtrabackup.

- **View invalida** (MySQL) — vista il cui corpo SQL fa riferimento a oggetti non più esistenti o non accessibili (tabelle rinominate, colonne eliminate, permessi revocati). MySQL non invalida automaticamente le view alla modifica della tabella sottostante: l'errore emerge solo alla prima esecuzione o durante un dump.

- **`--single-transaction`** (mysqldump) — flag che avvia una transazione `REPEATABLE READ` prima del dump, garantendo consistenza senza acquisire lock sulle tabelle InnoDB. Non applicabile a tabelle MyISAM, che richiedono `--lock-tables`.

- **`replication_group_members`** (MySQL Performance Schema) — tabella di sistema che elenca i nodi attivi in un cluster Group Replication, con stato (`ONLINE`, `RECOVERING`, `UNREACHABLE`) e ruolo (`PRIMARY`, `SECONDARY`). Vuota su server standalone o con replica tradizionale.
