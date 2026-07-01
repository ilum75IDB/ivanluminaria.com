---
categories:
- mysql
date: 2099-12-31
description: 'Swap al 100% su un cluster MySQL InnoDB 3 nodi in produzione: diagnosi,
  la matematica dei buffer per thread, fix e rolling restart a zero downtime.'
draft: true
image: articolo-mysql-saturazione-swap-su-innodb-cluster-3-nodi-analisi-e-fix-dei-param.cover.jpg
seoTitle: 'InnoDB Cluster 3 nodi: swap 100% e fix dei buffer per thread'
tags:
- mysql
- innodb-cluster
- memory-tuning
- group-replication
- performance-schema
title: 'Swap al 100% su InnoDB Cluster: quando join_buffer_size moltiplica il problema'
translationKey: articolo_mysql_saturazione_swap_su_innodb_cluster_3_nodi_analisi_e_fix_dei_param
webo_generated_at: 2026-07-01
webo_status: da_approvare
---

## La telefonata del martedì mattina

Martedì mattina, poco dopo le nove. Caffè ancora caldo sulla scrivania, la giornata sembrava una di quelle tranquille in cui si riesce finalmente a chiudere le cose rimaste sospese dal venerdì. Poi è arrivata la chiamata.

Dall'altra parte il team infrastrutture di una casa di GDO alimentare italiana: il backend di monitoring era diventato lentissimo, le dashboard interne non caricavano più, alcuni alert non arrivavano. Un nodo del cluster MySQL era praticamente fermo. "Non abbiamo toccato niente, è successo così."

Sotto il cofano c'era una query di aggregazione, apparentemente innocua. Qualcosa del tipo:

```sql
SELECT itemid, MIN(clock), MAX(clock), COUNT(*)
FROM history_log
GROUP BY itemid;
```

Su una tabella da 1,3 miliardi di righe, senza partizionamento, senza filtro temporale, senza `LIMIT`. Il nodo secondary del cluster ha iniziato a swappare in modo aggressivo, poi si è fermato.

Il contesto: la GDO in questione usa un cluster MySQL InnoDB Cluster a 3 nodi come backend per la propria piattaforma di monitoring interna, quella che tiene sotto controllo i sistemi di cassa, i magazzini, la logistica dei punti vendita. I nodi — `mysql-node-01`, `mysql-node-02`, `mysql-node-03` — gestiscono la raccolta e la consultazione di metriche storiche. La tabella `history_log` è il cuore del sistema: ogni evento di monitoring finisce lì, accumulato nel tempo senza una policy di retention attiva e senza partizionamento per data.

Quando la query è partita in produzione — qualcuno stava evidentemente cercando di rispondere a una domanda di business su tutta la storia degli item — il nodo secondary non aveva abbastanza RAM libera per reggere il full scan. La situazione, però, non si esauriva in quella query. Era la configurazione di memoria sottostante, che rendeva il cluster strutturalmente fragile a qualsiasi carico aggregato non banale.

## `free -h` e la prima sorpresa

Il primo segnale era arrivato dalla dashboard di monitoring del cliente, condivisa in call pochi minuti dopo la chiamata: il grafico dello swap su `mysql-node-01` e `mysql-node-02` mostrava una linea piatta al massimo da ore. Su `mysql-node-03` invece tutto sembrava normale.

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

La differenza tra i nodi era netta. `mysql-node-03` era il nodo che aveva ricevuto meno carico di query in quel periodo — era il secondary "freddo", per così dire. I primi due reggevano il traffico principale di lettura e scrittura, e la memoria era esaurita.

`vmstat 1 5` confermava: swap in uso attivo, non solo occupato staticamente.

```bash
# vmstat 1 5 su mysql-node-01
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 3  2 6291456  52428  18432 1572864  142  198  2840  3120 4821 9234 28  8 58  6  0
 2  1 6291456  48120  18432 1572864  156  212  3012  3340 5102 9876 31  9 54  6  0
```

`si` e `so` (swap-in e swap-out) attivi: il kernel stava spostando pagine tra RAM e disco continuamente. Con un database relazionale sotto carico, questo è il modo più rapido per degradare le performance in modo irreversibile.

## La matematica che non tornava

Guardando la configurazione attiva sul cluster, il parametro che saltava subito all'occhio era questo:

```sql
SHOW VARIABLES LIKE 'join_buffer_size';
-- join_buffer_size = 2147483648  (2 GB)

SHOW VARIABLES LIKE 'max_connections';
-- max_connections = 151

SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
-- innodb_buffer_pool_size = 133143986176  (124 GB)
```

Il `join_buffer_size` a 2 GB è un parametro **per thread**, non globale. Ogni connessione MySQL che esegue un join senza indice può allocare fino a 2 GB di memoria aggiuntiva. Con `max_connections = 151`, il potenziale teorico di allocazione è:

```
2 GB × 151 connessioni = 302 GB
```

Su macchine con 157 GB di RAM totale, di cui 124 GB già impegnati nell'`innodb_buffer_pool_size`.

Ovviamente 302 GB non vengono allocati tutti insieme in condizioni normali — i buffer per thread vengono allocati solo quando servono, e non tutte le connessioni eseguono join contemporaneamente. In un momento di carico aggregato, però, con query full-scan su `history_log` in esecuzione su più connessioni, anche una frazione di quel potenziale è sufficiente a saturare la RAM disponibile.

Anche `tmp_table_size` e `max_heap_table_size` erano sovrastimati, contribuendo alla pressione sulle tabelle temporanee in memoria.

## Quello che diceva il `performance_schema`

Per capire quali query stessero effettivamente consumando risorse, la consultazione di `events_statements_summary_by_digest` ha dato il quadro completo:

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

I numeri che emergevano erano significativi [1]:

- `Select_full_join` accumulato: fino a **22.631.693** — join eseguiti senza indice
- `Created_tmp_disk_tables`: oltre **200.000** — tabelle temporanee riversate su disco perché la memoria non bastava

Non erano numeri di un singolo evento. Erano il risultato di settimane di query mal ottimizzate che si accumulavano silenziosamente, finché un full scan su `history_log` non aveva fatto traboccare il sistema.

## La struttura di `history_log` e il nodo senza via d'uscita

```sql
SHOW CREATE TABLE history_log\G
-- Engine: InnoDB
-- Rows (approx): 1.312.847.203
-- Partitions: none
-- Indexes: PRIMARY KEY (id), KEY idx_itemid_clock (itemid, clock)

SELECT COUNT(*) FROM history_log;
-- 1312847203
```

La tabella aveva un indice su `(itemid, clock)`, ma la query di aggregazione che aveva causato il crash non usava il filtro su `clock`. MySQL non riusciva a usare l'indice in modo efficiente per una `GROUP BY itemid` su tutta la tabella — il piano di esecuzione sceglieva un full scan, allocava strutture temporanee in memoria, e quando la memoria finiva, riversava tutto su disco. Su `mysql-node-02`, con lo swap già al 100%, non c'era disco virtuale disponibile: il nodo si è fermato [2].

Senza partizionamento per data su `history_log`, qualsiasi query aggregata sull'intera storia è strutturalmente pericolosa. È una scelta architetturale che andava affrontata, e al tempo stesso non nell'immediato — il fix urgente era sui parametri di memoria.

## I valori nuovi e il ragionamento dietro

Il piano di intervento era diretto. I parametri per thread andavano ridimensionati a valori ragionevoli per il workload reale:

```ini
# my.cnf — modifiche applicate
[mysqld]

# Buffer per thread: da 2G a 64M
join_buffer_size        = 64M
tmp_table_size          = 64M
max_heap_table_size     = 64M

# InnoDB redo log: capacità aumentata per ridurre la frequenza dei checkpoint
innodb_redo_log_capacity = 8G

# Parametri InnoDB mantenuti invariati
innodb_buffer_pool_size  = 124G   # già dimensionato correttamente per il dataset
innodb_buffer_pool_instances = 8  # invariato
```

La scelta di mantenere `innodb_buffer_pool_size` a 124 GB era deliberata: il buffer pool è memoria globale, non per thread, e il suo dimensionamento era corretto rispetto alla dimensione del dataset attivo. Ridurlo avrebbe peggiorato le performance di I/O senza risolvere la causa reale.

Il `join_buffer_size` a 64 MB è un valore standard per workload OLTP misti. Con 151 connessioni massime, il potenziale di allocazione scende a:

```
64 MB × 151 = 9,6 GB
```

Sommato ai 124 GB del buffer pool e all'overhead del sistema operativo, si rientra ampiamente nei 157 GB disponibili con margine sufficiente per i picchi [3].

L'`innodb_redo_log_capacity` a 8 GB (da un valore precedente più basso) serve a ridurre la frequenza dei checkpoint InnoDB, che in presenza di write intensive generano I/O aggiuntivo — un contributo secondario alla pressione sul sistema.

## Il rolling restart e perché funziona su InnoDB Cluster

InnoDB Cluster con Group Replication permette di riavviare i nodi in sequenza senza interrompere il servizio, a condizione che il quorum sia mantenuto [4]. Con 3 nodi, si può portare offline un nodo alla volta: gli altri due mantengono il quorum e continuano a servire le richieste.

La sequenza applicata, concordata al telefono con il team del cliente:

```bash
# Step 1: riavvio mysql-node-03 (il nodo con swap minima, meno rischio)
# Verifica stato cluster prima di procedere
mysqlsh -- cluster status

# Su mysql-node-03: stop, modifica my.cnf, start
systemctl stop mysqld
# -- modifica /etc/my.cnf con i nuovi parametri --
systemctl start mysqld

# Attesa rejoin automatico al cluster
# Verifica: SECONDARY tornato ONLINE

# Step 2: riavvio mysql-node-02
# Step 3: riavvio mysql-node-01 (PRIMARY per ultimo)
# Prima del riavvio del PRIMARY: switchover manuale se necessario
mysqlsh -- cluster setPrimaryInstance mysql-node-02:3306
```

Il riavvio del nodo PRIMARY per ultimo è una precauzione: se il PRIMARY viene riavviato mentre gli altri due non sono ancora completamente sincronizzati, Group Replication elegge automaticamente un nuovo PRIMARY, e al tempo stesso è più pulito gestire il switchover manualmente.

Tempo totale dell'operazione: circa 40 minuti dalla prima call, zero interruzioni di servizio per le applicazioni client. Le casse dei punti vendita non se ne sono accorte.

## Da 100% a 11%: i numeri dopo il fix

Il grafico dello swap nelle ore successive al rolling restart mostrava la curva attesa: discesa rapida su `mysql-node-01` e `mysql-node-02`, stabilizzazione intorno al 10-11%.

```bash
# mysql-node-01 — 6 ore dopo il rolling restart
              total        used        free      shared  buff/cache   available
Mem:           157Gi       132Gi        18Gi       0.8Gi       6.2Gi        23Gi
Swap:            6Gi       672Mi       5.4Gi

# mysql-node-02
              total        used        free      shared  buff/cache   available
Mem:           157Gi       129Gi        21Gi       0.7Gi       6.8Gi        25Gi
Swap:            6Gi       614Mi       5.4Gi
```

Il carico CPU si era stabilizzato: i picchi legati allo swap I/O erano spariti. Le metriche del `performance_schema` mostravano una riduzione netta dei `Created_tmp_disk_tables` — non a zero, perché alcune query continuavano a fare full scan, e al tempo stesso il sistema non era più in pressione strutturale.

`Select_full_join` continuava ad accumularsi: quella metrica richiede interventi sulle query e sugli indici, non solo sui parametri di memoria. Il cluster, però, reggeva il carico senza saturare lo swap.

## Quello che resta da fare su `history_log`

Il fix sui parametri di memoria era necessario e sufficiente per stabilizzare il cluster nell'immediato. La causa strutturale, però — una tabella da 1,3 miliardi di righe senza partizionamento e senza retention policy — rimane aperta.

Le azioni raccomandate al cliente per il medio termine:

**Partizionamento per data su `history_log`**

```sql
-- Schema target (da applicare con migrazione pianificata)
ALTER TABLE history_log
    PARTITION BY RANGE (clock) (
        PARTITION p_2023 VALUES LESS THAN (UNIX_TIMESTAMP('2024-01-01')),
        PARTITION p_2024 VALUES LESS THAN (UNIX_TIMESTAMP('2025-01-01')),
        PARTITION p_2025 VALUES LESS THAN (UNIX_TIMESTAMP('2026-01-01')),
        PARTITION p_future VALUES LESS THAN MAXVALUE
    );
```

Con il partizionamento, le query con filtro su `clock` possono usare il partition pruning ed evitare il full scan sull'intera tabella. La query di aggregazione che ha causato il crash, con un filtro temporale ragionevole, diventerebbe gestibile [2].

**Retention policy attiva**

Definire una finestra di retention (es. 12 mesi) e implementare una procedura di purge periodica. Su 1,3 miliardi di righe, anche una retention di 6 mesi riduce significativamente il dataset attivo.

**Query tuning**

Le query di aggregazione senza filtro temporale su `history_log` vanno considerate operazioni di manutenzione, non query operative. Andrebbero eseguite su repliche dedicate, in finestre di manutenzione, con `MAX_EXECUTION_TIME` impostato.

```sql
-- Versione sicura della query incriminata
SELECT /*+ MAX_EXECUTION_TIME(30000) */ itemid, MIN(clock), MAX(clock), COUNT(*)
FROM history_log
WHERE clock >= UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 30 DAY))
GROUP BY itemid;
```

## La regola base che si dimentica

Il fix è stato quello che era: diagnosi corretta, valori ragionevoli, rolling restart. Nessuna magia, nessun eroismo — una call durata qualche ora con un team che sapeva cosa aveva sul tavolo, e un paio di occhi esterni che hanno guardato la matematica dei buffer.

La cosa che colpisce, guardando indietro, è quanto spesso la configurazione dei buffer per thread venga trascurata rispetto al dimensionamento del buffer pool. L'`innodb_buffer_pool_size` è il parametro che tutti guardano per primo — ed è giusto così, è il più impattante. I buffer per thread come `join_buffer_size`, `sort_buffer_size`, `read_buffer_size` hanno però una caratteristica insidiosa: vengono allocati per connessione, e il loro impatto reale dipende dal numero di connessioni concorrenti attive.

La formula è semplice:

```
memoria_per_thread × max_connections = pressione potenziale massima
```

Va calcolata esplicitamente quando si dimensiona un server MySQL, e va confrontata con la RAM disponibile al netto del buffer pool e dell'overhead OS. Se il risultato supera la RAM fisica, il sistema è strutturalmente fragile — non "potrebbe avere situazioni critiche", ma **le avrà**, quando il carico sarà quello giusto.

In questo caso il carico giusto è stato una query aggregata su una tabella da 1,3 miliardi di righe, un martedì mattina qualsiasi. Poteva essere qualsiasi altra cosa, in qualsiasi altro momento.

## Fonti ufficiali

1. MySQL 8.0 Reference Manual — [Performance Schema Statement Digests](https://dev.mysql.com/doc/refman/8.0/en/performance-schema-statement-digests.html)
2. MySQL 8.0 Reference Manual — [RANGE Partitioning](https://dev.mysql.com/doc/refman/8.0/en/partitioning-range.html)
3. MySQL 8.0 Reference Manual — [Memory Use in MySQL](https://dev.mysql.com/doc/refman/8.0/en/memory-use.html)
4. MySQL 8.0 Reference Manual — [InnoDB Cluster — Rolling Restart](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-innodb-cluster-working-with-cluster.html)

## Glossario
- **[join_buffer_size](/it/glossary/join-buffer-size/)** (MySQL) — Buffer allocato per thread per ogni join eseguito senza indice. A differenza del buffer pool, viene allocato per ogni connessione attiva: il suo impatto sulla memoria totale dipende dal numero di connessioni concorrenti.

- **[innodb_buffer_pool_size](/it/glossary/group-replication/)** (MySQL/InnoDB) — Parametro globale che definisce la dimensione della cache principale di InnoDB per dati e indici. È il parametro di memoria più impattante su MySQL: tipicamente si dimensiona al 70-80% della RAM disponibile su server dedicati.

- **[Group Replication](/it/glossary/join-buffer-size/)** (MySQL) — Meccanismo di replica sincrona multi-master integrato in MySQL, base di InnoDB Cluster. Garantisce consistenza tra i nodi tramite un protocollo di consenso distribuito; permette rolling restart senza perdita di quorum con 3+ nodi.

- **[performance_schema](/it/glossary/innodb-buffer-pool-size/)** (MySQL) — Schema di sistema che raccoglie metriche di esecuzione in tempo reale: statistiche per query digest, wait events, memoria allocata per thread. Base per la diagnostica delle performance senza strumenti esterni.

- **[rolling restart](/it/glossary/group-replication/)** — Procedura di riavvio sequenziale dei nodi di un cluster che mantiene il servizio attivo durante l'operazione. Su InnoDB Cluster con 3 nodi, permette di applicare modifiche alla configurazione senza downtime, riavviando un nodo alla volta mentre gli altri mantengono il quorum.
