---
title: "Prima di aggiornare MySQL: le cifre che il cliente ti chiede e come trovarle davvero"
description: "Quattro server MySQL 8.0 in produzione, un responsabile infrastruttura che prepara la finestra di manutenzione e quattro domande dirette: quanto pesano, quanto crescono, quanto dura il backup, quanto dura il restore. Come rispondere con numeri misurati invece che stime a occhio."
date: "2026-05-05T08:03:00+01:00"
draft: false
translationKey: "mysql_pre_upgrade_assessment"
tags: ["mysql", "upgrade", "backup", "restore", "assessment", "information-schema", "mysqldump", "mydumper", "xtrabackup"]
categories: ["MySQL"]
image: "mysql-pre-upgrade-assessment.cover.jpg"
---

La mail dal responsabile infrastruttura è arrivata un lunedì mattina, tre righe secche. *"Ciao, entro venerdì ho bisogno di quattro numeri per pianificare la finestra di manutenzione sui MySQL: quanto pesano oggi, quanto crescono al mese, quanto dura un backup completo, quanto ci mettiamo a rimetterli su da zero se qualcosa va storto. Grazie."*

Scenario classico in una direzione IT della Pubblica Amministrazione italiana. Quattro server MySQL 8.0 a supporto di applicazioni interne e di un portale utenti, versioni leggermente disallineate (8.0.32, 8.0.33, 8.0.34) perché sono stati patchati in momenti diversi. Upgrade infrastrutturale previsto: nuovi host, sistema operativo aggiornato, stesso major di MySQL, con finestra di manutenzione notturna di sei ore.

Il PM non voleva un assessment accademico. Voleva quattro cifre vere da mettere nel piano di rollback. E la tentazione, quando si ha fretta, è di rispondere a occhio: *"Saranno sui 300 GB, il backup dura un paio d'ore, il restore forse tre."* Numeri plausibili, magari anche corretti, ma non misurati — e se sbagli la stima del restore di un fattore due, la finestra non basta e il cutover salta.

Mi sono preso mezza giornata. Ecco il metodo che ho usato.

## 📏 1. Quanto pesano davvero — `information_schema`

La prima cifra è la più semplice da trovare e la più ingannevole da interpretare. In MySQL 8.0 l'{{< glossary term="information-schema" >}}`information_schema`{{< /glossary >}} espone tutto quello che serve, ma bisogna sapere cosa chiedere.

```sql
-- Dimensioni totali per schema (dati + indici)
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

Risultato tipico su uno dei quattro server:

| schema_name           | data_gb | index_gb | total_gb | num_tables |
|-----------------------|--------:|---------:|---------:|-----------:|
| portale_utenti        |   58,34 |    21,07 |    79,41 |        142 |
| gestione_pratiche     |   31,12 |    14,88 |    46,00 |         97 |
| audit_log             |   28,45 |     9,20 |    37,65 |         12 |
| anagrafica_condivisa  |    4,18 |     1,32 |     5,50 |         24 |
| *(altri schemi)*      |    2,70 |     0,90 |     3,60 |         38 |
| **Totale server**     |**124,79**|**47,37**|**172,16**|       313 |

Sembra un dato chiuso, ma non lo è. Due cose importanti:

- **`data_length` e `index_length` sono stime** che InnoDB aggiorna periodicamente e che dipendono dall'ultima `ANALYZE TABLE`. Su tabelle molto volatili possono sottostimare del 10-15%. Per dati critici conviene incrociare con la dimensione fisica dei file `.ibd` nel datadir (`du -sh /var/lib/mysql/portale_utenti/*.ibd`).
- **Il total del server non è la dimensione del backup.** Il file di dump (logical) è più compatto perché non replica la frammentazione InnoDB, ma contiene `INSERT` testuali che pesano più dei dati binari. Nella pratica il dump non compresso pesa il 70-90% del `data_length + index_length`. Con `gzip` standard si scende al 15-25%, con `zstd -3` intorno al 18-28% ma molto più veloce.

Ripetendo la query sui quattro server, il sizing complessivo che ho portato al PM era:

| Server    | MySQL  | Schemi | Totale data + index | File .ibd su disco |
|-----------|:------:|-------:|--------------------:|-------------------:|
| mysql-01  | 8.0.34 |      7 |            172,2 GB |            181 GB  |
| mysql-02  | 8.0.33 |      5 |             94,7 GB |             98 GB  |
| mysql-03  | 8.0.32 |      9 |            218,5 GB |            229 GB  |
| mysql-04  | 8.0.34 |      4 |             46,1 GB |             49 GB  |
| **Totale**|        |     25 |          **531,5 GB** |       **557 GB** |

Il gap tra "data + index" e "file fisici" è il costo della frammentazione e del tablespace `ibtmp1`. Vale la pena evidenziarlo al PM perché sul nuovo ambiente si può pianificare un `OPTIMIZE TABLE` post-migrazione che recupera quel 5-6% di spazio.

## 📈 2. Quanto cresce — snapshot periodici e letture dal binary log

La cifra della crescita è più delicata. Il PM chiede "quanto al mese", ma la risposta utile è: *quanto prevedi che cresca nei prossimi tre-sei mesi, cioè fino al prossimo assessment?* Ci sono due approcci, entrambi validi, che io uso insieme.

**Approccio 1 — snapshot periodici.** Se hai a disposizione la cronologia del monitoraggio (Prometheus + `mysqld_exporter`, Zabbix, o anche solo la cartella dei backup storicizzati), puoi ricostruire la curva delle dimensioni. Se non hai niente, parti adesso: un cron job settimanale che fa la query qui sopra e scrive il risultato in una tabella `ops.sizing_history`, dopo 6-8 settimane hai un dato solido.

```sql
-- Tabella di storicizzazione (da eseguire una volta)
CREATE TABLE ops.sizing_history (
    captured_at   TIMESTAMP NOT NULL,
    server_name   VARCHAR(50) NOT NULL,
    schema_name   VARCHAR(64) NOT NULL,
    data_bytes    BIGINT,
    index_bytes   BIGINT,
    num_tables    INT,
    PRIMARY KEY (captured_at, server_name, schema_name)
);

-- Snapshot da lanciare via cron weekly
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

**Approccio 2 — stima dal {{< glossary term="binary-log" >}}binary log{{< /glossary >}}.** Questo è il trucco che molti non usano. Il binlog registra ogni scrittura, e la sua dimensione giornaliera è un proxy eccellente del tasso di crescita dei dati (al netto di update e delete, che generano traffico ma non crescita netta). Con `expire_logs_days=7` hai una settimana di storico pronta da leggere.

```bash
# Volume giornaliero del binlog (ultimi 7 giorni)
ls -la /var/lib/mysql/binlog.* | awk '{print substr($6" "$7,1,6), $5}' | \
    sort | awk '{a[$1]+=$2} END {for (k in a) printf "%s  %.2f GB\n", k, a[k]/1024/1024/1024}'
```

Tipico risultato su uno dei server:

```
Apr 14   3.87 GB
Apr 15   4.12 GB
Apr 16   3.95 GB
Apr 17   4.44 GB
Apr 18   2.18 GB   # sabato
Apr 19   1.02 GB   # domenica
Apr 20   3.78 GB
```

Media feriale ~4 GB/giorno di write traffic. Il tasso di crescita netto della tablespace è tipicamente tra il 20% e il 40% del volume binlog, a seconda del mix insert/update/delete. Nel nostro caso, incrociando con i pochi snapshot disponibili, siamo arrivati a una stima di **+8-12 GB al mese per server**, con punte sul `mysql-03` (quello del portale utenti, più dinamico).

## 💾 3. Quanto dura il backup — `mysqldump`, `mydumper`, `xtrabackup`

Qui il PM si aspetta un numero solo. La risposta onesta è: dipende da quale strumento usi, e i tempi possono differire di un ordine di grandezza.

Sullo stesso server (`mysql-03`, 218 GB di data + index, tabelle InnoDB con qualche MyISAM residuo che nessuno ha mai toccato dal 2014), ho misurato empiricamente quattro strategie.

**`{{< glossary term="mysqldump" >}}mysqldump{{< /glossary >}}` (logical, single-threaded):**

```bash
time mysqldump --single-transaction --quick --routines --triggers --events \
    --default-character-set=utf8mb4 --hex-blob \
    --all-databases > /backup/mysql-03-full.sql
```

Risultato: 2 ore e 47 minuti. File SQL non compresso: 189 GB. Con pipe su `gzip` in tempo reale (`| gzip -3 > ...gz`): 3 ore e 22 minuti, file compresso 38 GB.

**`mysqldump` + `zstd` (il mio preferito per i server PA dove il tempo CPU conta meno della finestra):**

```bash
time mysqldump --single-transaction --quick --routines --triggers --events \
    --default-character-set=utf8mb4 --hex-blob --all-databases | \
    zstd -3 -T4 > /backup/mysql-03-full.sql.zst
```

Risultato: 2 ore e 58 minuti, file compresso 42 GB. Leggermente più grande del gzip ma circa **il doppio più veloce** in decompressione al restore — che è il momento in cui la velocità conta davvero.

**`{{< glossary term="mydumper" >}}mydumper{{< /glossary >}}` (logical, parallelo):**

```bash
time mydumper --host=localhost --user=backup --socket=/var/lib/mysql/mysql.sock \
    --threads=8 --compress --rows=500000 \
    --outputdir=/backup/mysql-03-mydumper \
    --logfile=/backup/mysql-03-mydumper.log
```

Risultato: 47 minuti. Output: directory con 312 file compressi, totale 41 GB. Quasi 4x più veloce di `mysqldump` grazie al parallelismo a livello di chunk di tabella.

**`xtrabackup` (physical, hot backup):**

```bash
time xtrabackup --backup --target-dir=/backup/mysql-03-xtra \
    --user=backup --password=*** --parallel=4 --compress --compress-threads=4
```

Risultato: 22 minuti. Output: 179 GB non compressi / 48 GB compressi. È il più veloce perché copia i file InnoDB a livello fisico invece di rigenerare gli `INSERT`, ma ha un vincolo importante: **le tabelle MyISAM residue vengono lockate** per la durata della loro copia. Per fortuna sul `mysql-03` erano residuali e lette solo da un batch notturno, quindi non impatta.

Riepilogo che ho presentato al PM:

| Strumento              | Tempo backup | Dim. output | Note                                           |
|------------------------|-------------:|------------:|------------------------------------------------|
| `mysqldump` + gzip     | 3h 22m       | 38 GB       | baseline, single-thread, disponibile ovunque   |
| `mysqldump` + zstd     | 2h 58m       | 42 GB       | più veloce su restore                          |
| `mydumper` + compress  | 47m          | 41 GB       | parallelo, ottimo compromesso tempo/spazio     |
| `xtrabackup` + compress| 22m          | 48 GB       | physical, il più veloce, vincoli su MyISAM     |

Nell'assessment ho proposto di standardizzare su **`mydumper` per il backup periodico** (giornaliero, occupa poco disco, restore flessibile schema-per-schema) e **`xtrabackup` per lo snapshot pre-upgrade** (velocissimo, ideale per la finestra di manutenzione stretta).

## ⏱️ 4. Quanto dura il restore — la cifra che il PM dimentica di chiedere

Il restore è dove gli assessment fatti male falliscono. Un backup può impiegare 47 minuti, ma il ripristino sullo stesso dataset può richiedere ore — e sulla finestra di manutenzione è quello che conta.

Sempre su `mysql-03`, misurazione empirica di quanto ci si mette a ricostruire da zero il database partendo dai backup di cui sopra, su un host gemello (stessa CPU, stesso storage NVMe):

**Da `mysqldump.sql.gz`:**

```bash
time gunzip -c /backup/mysql-03-full.sql.gz | \
    mysql --default-character-set=utf8mb4
```

Risultato: **5 ore e 12 minuti**. È lento perché il logical restore rigenera ogni riga con `INSERT` individuali, aggiorna gli indici transazionalmente, e non può parallelizzare su singola tabella.

**Da `mysqldump.sql.zst`:**

```bash
time zstd -dc /backup/mysql-03-full.sql.zst | \
    mysql --default-character-set=utf8mb4
```

Risultato: **4 ore e 38 minuti**. Qui si vede il vantaggio della decompressione zstd (circa 2x più veloce di gzip), che è l'unico elemento che differisce dal test precedente.

**Da `mydumper` con `myloader`:**

```bash
time myloader --host=localhost --user=root --socket=/var/lib/mysql/mysql.sock \
    --threads=8 --directory=/backup/mysql-03-mydumper \
    --disable-redo-log --overwrite-tables
```

Risultato: **1 ora e 52 minuti**. Il flag `--disable-redo-log` (MySQL 8.0.21+) è il vero game-changer: salta la generazione del {{< glossary term="redo-log-mysql" >}}redo log{{< /glossary >}} durante il caricamento iniziale, riducendo l'overhead di I/O. Da usare SOLO su un'istanza vuota in fase di import, mai in produzione.

**Da `xtrabackup`:**

```bash
time xtrabackup --decompress --target-dir=/backup/mysql-03-xtra --parallel=4
time xtrabackup --prepare --target-dir=/backup/mysql-03-xtra
# poi rsync dei file sul nuovo datadir + avvio mysqld
```

Risultato: **34 minuti** (decompress) + **12 minuti** (prepare) + **6 minuti** (copia + restart) = **52 minuti totali**. Physical restore: copia binaria + crash recovery, nessun SQL rigenerato. È l'unica opzione che si avvicina al tempo del backup stesso.

Riepilogo restore:

| Strategia              | Tempo restore | Note                                                    |
|------------------------|--------------:|---------------------------------------------------------|
| `mysqldump` + gzip     | 5h 12m        | da evitare per dataset > 50 GB                          |
| `mysqldump` + zstd     | 4h 38m        | solo se non hai alternative                             |
| `mydumper` + myloader  | 1h 52m        | con `--disable-redo-log`, logical veloce                |
| `xtrabackup`           | 52m           | physical, l'unica opzione compatibile con finestre strette |

## 📋 5. Il template di risposta al PM

Dopo le misurazioni sui quattro server, ho sintetizzato tutto in una tabella singola, perché al PM serve una pagina da allegare al piano di cutover, non trenta slide.

| Server    | Dim. attuale | Crescita stimata | Backup (`xtrabackup`) | Restore (`xtrabackup`) | Restore worst-case (`mysqldump+gz`) |
|-----------|-------------:|-----------------:|----------------------:|-----------------------:|------------------------------------:|
| mysql-01  |     172 GB   | +8 GB/mese       |               18 min  |                45 min  |                          4h 10m     |
| mysql-02  |      95 GB   | +3 GB/mese       |               11 min  |                28 min  |                          2h 25m     |
| mysql-03  |     219 GB   | +12 GB/mese      |               22 min  |                52 min  |                          5h 12m     |
| mysql-04  |      46 GB   | +2 GB/mese       |                6 min  |                15 min  |                          1h 20m     |
| **Totale**|  **532 GB** | **+25 GB/mese**  |          **57 min**   |         **2h 20m**     |                    **13h 07m**      |

Sulla base di questa tabella, la finestra di manutenzione di sei ore è **compatibile con un rollback basato su `xtrabackup`** (snapshot 57 minuti + restore 2h 20m = 3h 17m, con margine di 2h 43m per debug e verifiche), ma **incompatibile con un rollback basato su `mysqldump`** (più di 13 ore). Decisione operativa: `xtrabackup` come strategia di rollback primaria, `mydumper` come fallback per restore selettivi schema-per-schema se emergono problemi mirati durante il cutover.

Il PM mi ha chiesto solo quattro numeri. Gliene ho dati ventiquattro. Ma sono ventiquattro numeri misurati — non stime a occhio — e la differenza è tutta lì.

## Quello che ho imparato

Un pre-upgrade assessment non è un documento tecnico, è uno strumento di governance del rischio. Il cliente che chiede "quanto dura il backup" in realtà sta chiedendo *"se va tutto in vacca nella finestra di manutenzione, ce la facciamo a rimettere in piedi i servizi prima delle 6 del mattino?"*. Se la tua risposta è "circa tre ore, credo", quella domanda resta senza risposta e il rischio non è stato misurato.

La parte tecnica — le query, gli strumenti, le misurazioni — è la parte facile. La parte difficile è fare in modo che le cifre misurate finiscano nel piano di cutover, che il PM le legga, che il team ops le usi per calibrare la finestra. Nel nostro caso il PM ha voluto aggiungere una slide in più nella riunione con il vendor del nuovo storage: *"guardate, queste sono le cifre di riferimento, se il vostro array non regge questi throughput di restore il piano non funziona"*. Ed è esattamente quello che dovrebbe fare un PM bravo.

Alla fine l'upgrade è passato in quattro ore, non sei. Nessun rollback. Il cliente ci ha ringraziato non per la finestra breve, ma per il fatto che avevano **sempre saputo cosa sarebbe successo se qualcosa fosse andato storto**. Che è poi il vero obiettivo di un pre-upgrade assessment ben fatto.

------------------------------------------------------------------------

## Glossario

**[information_schema](/it/glossary/information-schema/)** — Schema di sistema MySQL (in sola lettura) che espone metadati su database, tabelle, indici, utenti e stato del server. Punto di partenza per qualunque assessment, sizing o analisi strutturale.

**[xtrabackup](/it/glossary/xtrabackup/)** — Strumento di backup fisico hot per MySQL/MariaDB sviluppato da Percona. Copia direttamente i file InnoDB mentre il database è in esecuzione, gestendo transazioni in corso tramite il redo log. Nettamente più veloce dei backup logici su dataset grandi.

**[Pre-upgrade assessment](/it/glossary/pre-upgrade-assessment/)** — Misurazione strutturata di dimensioni, crescita, tempi di backup e tempi di restore di un database prima di un upgrade. Serve a dimensionare la finestra di manutenzione e a definire una strategia di rollback realistica.

**[mysqldump](/it/glossary/mysqldump/)** — Utility di backup logico inclusa in ogni installazione MySQL. Produce un file SQL sequenziale con tutte le istruzioni per ricreare schema e dati. Single-threaded, affidabile ma lenta su database grandi.

**[mydumper](/it/glossary/mydumper/)** — Tool open source di backup logico per MySQL/MariaDB con parallelismo reale a livello di chunk. Divide le tabelle grandi in pezzi e li esporta con thread multipli, con restore parallelo tramite myloader.