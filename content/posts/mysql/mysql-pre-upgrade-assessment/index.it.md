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