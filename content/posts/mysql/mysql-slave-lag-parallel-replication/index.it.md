---
categories:
- mysql
date: '2026-08-25'
description: Replica MySQL con 4 ore di lag e nessun alert. Come funziona il binlog,
  perché Seconds_Behind_Master mente, e come il parallel replication risolve davvero.
draft: false
image: mysql-slave-lag-parallel-replication.cover.jpg
seoTitle: 'MySQL replica lag: diagnosi, GTID e parallel replication'
tags:
- replication
- slave-lag
- gtid
- monitoring
- mysql
title: 'MySQL slave lag: Seconds_Behind_Master mente, GTID no — diagnosi e fix con
  parallel replication'
translationKey: mysql_slave_lag_parallel_replication
webo_generated_at: 2026-08-08
webo_status: scheduled
---

## Il report del lunedì mattina

Era un lunedì mattina. Il responsabile commerciale di un grande operatore postale e logistico nazionale aveva appena aperto il report settimanale delle spedizioni e stava guardando numeri che non tornava. Le consegne del venerdì pomeriggio risultavano ancora "in transito". I KPI di sabato erano a zero. Qualcosa non andava, e la prima ipotesi era stata un bug nell'applicazione di reportistica.

Quando siamo arrivati a guardare, il bug non c'era. C'era qualcosa di più sottile: il replica MySQL su cui giravano tutte le query di reportistica accumulava quattro ore di ritardo rispetto al master. I dati erano lì, corretti, sul master — ma il replica li stava ancora applicando con ore di ritardo. E nessun alert aveva scattato.

Quattro ore di lag in un sistema logistico significano decisioni operative prese su numeri sbagliati. Significa che il responsabile del magazzino ha pianificato i turni del weekend su dati che non riflettevano la realtà. Significa che il sistema di prioritizzazione delle spedizioni urgenti stava lavorando su una fotografia vecchia di mezza giornata lavorativa.

Questo articolo racconta come funziona la replica MySQL sotto il cofano, perché il suo strumento di monitoraggio principale è inaffidabile, e cosa abbiamo fatto per risolvere — senza magia, con profiling e qualche decisione architetturale.

---

## Binlog, relay log, e i due thread che non si parlano abbastanza

Per capire perché la replica accumula lag, serve capire come funziona davvero. La replica MySQL asincrona si basa su tre componenti principali: il **binary log** sul master, il **relay log** sullo slave, e due thread che lavorano in sequenza.

Il **IO thread** sullo slave si connette al master e legge gli eventi dal binlog, scrivendoli localmente nel relay log. È una lettura sequenziale, generalmente veloce, raramente il collo di bottiglia.

Il **SQL thread** legge il relay log e applica gli eventi al database locale dello slave. Qui sta il problema: in configurazione classica, questo thread è **single-threaded**. Applica un evento alla volta, in sequenza. Se il master ha dieci sessioni che scrivono in parallelo, lo slave le applica una dopo l'altra.

```text
MASTER
  ├── sessione 1 → INSERT INTO spedizioni (...)
  ├── sessione 2 → UPDATE tracking SET stato = 'consegnato' WHERE ...
  ├── sessione 3 → INSERT INTO eventi_logistici (...)
  └── ... (N sessioni parallele)
         │
         ▼ binlog (serializzato)
SLAVE IO thread → relay log → SQL thread (single-threaded)
         ▼
  applica evento 1, poi evento 2, poi evento 3...
```

Il master scrive in parallelo, lo slave applica in serie. Su un sistema con carico sostenuto, questa asimmetria è la causa principale del lag.

---

## Perché Seconds_Behind_Master mente

La prima cosa che guardi quando sospetti lag è `SHOW SLAVE STATUS\G`. Il campo `Seconds_Behind_Master` sembra esattamente quello che ti serve. Non lo è.

```sql
SHOW SLAVE STATUS\G
-- ...
Seconds_Behind_Master: 14523
-- ...
```

Quattordici mila secondi. Quattro ore. Il numero c'era — ma il problema è che questo valore è calcolato in modo che lo rende inaffidabile in diversi scenari comuni.

`Seconds_Behind_Master` misura la differenza tra il timestamp dell'evento che lo SQL thread sta **attualmente applicando** e l'ora corrente del sistema. Se lo SQL thread è fermo (perché è bloccato su un lock, perché ha avuto un errore, perché il relay log è esaurito e l'IO thread non ha ancora ricevuto nuovi eventi), il valore smette di aggiornarsi o si comporta in modo imprevedibile.

Ancora più insidioso: se la replica si interrompe e poi riparte, `Seconds_Behind_Master` può tornare a zero prima che il lag sia effettivamente recuperato, perché l'IO thread ha scaricato il relay log ma lo SQL thread non ha ancora finito di applicarlo. Il campo riflette lo stato del SQL thread, non il ritardo reale rispetto al master.

In pratica, `Seconds_Behind_Master` è utile come indicatore grossolano, ma non come base per l'alerting. [1]

**Cosa usare al suo posto**: con la **GTID-based replication** attiva, si può calcolare il lag reale confrontando il set di transazioni eseguite sul master (`gtid_executed` sul master) con quello applicato sullo slave (`gtid_executed` sullo slave). La differenza — il numero di transazioni in attesa — è una metrica molto più affidabile.

```sql
-- Sul master
SELECT @@global.gtid_executed;

-- Sullo slave
SELECT @@global.gtid_executed;
-- La differenza tra i due set è il lag reale in termini di transazioni
```

Con strumenti come `pt-heartbeat` di Percona Toolkit si può misurare il lag in modo ancora più preciso: il tool scrive un timestamp sul master a intervalli regolari e misura quanto tempo impiega ad apparire sullo slave. [2]

---

## Le cause più comuni di slave lag

Nel caso specifico, abbiamo identificato tre cause concorrenti:

**1. Query pesanti non ottimizzate sul master**

Il master eseguiva ogni notte un batch di aggiornamento massivo: `UPDATE spedizioni SET stato_elaborazione = 'archiviato' WHERE data_spedizione < DATE_SUB(NOW(), INTERVAL 90 DAY)`. Nessun indice su `data_spedizione`. La query faceva un full table scan su una tabella da 180 milioni di righe, produceva un singolo evento binlog enorme, e lo slave impiegava 40 minuti ad applicarlo — durante i quali non applicava nient'altro.

**2. SQL thread single-threaded sotto carico sostenuto**

Durante le ore di punta (dalle 14 alle 18), il master riceveva circa 800 write/secondo distribuite su decine di sessioni parallele. Lo SQL thread non riusciva a stare al passo: ogni ora di produzione intensa aggiungeva circa 20-30 minuti di lag accumulato.

**3. I/O lento sullo slave**

Lo slave era su storage condiviso con altri servizi. Nelle ore di punta, la latenza di scrittura su disco saliva a valori che rallentavano ulteriormente l'applicazione degli eventi. Il relay log veniva scritto e letto con latenze che moltiplicavano il problema del single-thread.

---

## GTID: perché vale la pena migrare subito

La **Global Transaction ID** (GTID) è un identificatore univoco assegnato a ogni transazione committata sul master. [3] Ogni transazione ha un GTID nel formato `source_id:transaction_id`, dove `source_id` è l'UUID del server master.

```sql
-- Abilitare GTID sul master (richiede restart o SET PERSIST su MySQL 8.0+)
SET PERSIST gtid_mode = ON;
SET PERSIST enforce_gtid_consistency = ON;

-- Verificare lo stato
SHOW VARIABLES LIKE 'gtid_mode';
-- gtid_mode | ON
```

I vantaggi rispetto alla replica basata su posizione binlog sono concreti:

- **Failover più semplice**: con GTID, un nuovo slave sa esattamente da dove ricominciare senza dover calcolare manualmente la posizione nel binlog
- **Monitoraggio del lag reale**: come descritto sopra, confrontare i set GTID è molto più affidabile di `Seconds_Behind_Master`
- **Rilevamento di transazioni mancanti**: se una transazione è stata applicata sul master ma non sullo slave, il gap è immediatamente visibile nel set GTID

Nel contesto di questo progetto, la migrazione a GTID era già pianificata ma non ancora eseguita. Averla completata prima di affrontare il problema del lag avrebbe reso la diagnosi molto più rapida.

---

## Da single-thread a parallel replication

La soluzione al collo di bottiglia dello SQL thread è la **parallel replication**, disponibile in MySQL 5.7+ e MariaDB 10.0+. [4]

L'idea di base: invece di applicare gli eventi in sequenza con un singolo thread, si usano più worker thread che applicano transazioni in parallelo — rispettando i vincoli di consistenza.

MySQL offre due modalità di parallelizzazione:

- **`DATABASE`**: transazioni che modificano database diversi vengono applicate in parallelo. Semplice, ma inutile se tutte le scritture vanno sullo stesso database.
- **`LOGICAL_CLOCK`** (la modalità corretta per la maggior parte dei casi): sfrutta le informazioni di commit timestamp nel binlog per identificare transazioni che erano in esecuzione contemporaneamente sul master e possono quindi essere applicate in parallelo sullo slave.

```sql
-- Configurazione sullo slave
STOP SLAVE SQL_THREAD;

SET GLOBAL slave_parallel_type = 'LOGICAL_CLOCK';
SET GLOBAL slave_parallel_workers = 8;
SET GLOBAL slave_preserve_commit_order = ON;

START SLAVE SQL_THREAD;
```

Il parametro `slave_preserve_commit_order = ON` garantisce che le transazioni vengano committate sullo slave nello stesso ordine in cui lo erano sul master — fondamentale per la consistenza delle letture. [4]

Per sfruttare al meglio `LOGICAL_CLOCK`, il master deve avere `binlog_group_commit_sync_delay` configurato in modo da raggruppare più transazioni nello stesso commit group. Questo aumenta leggermente la latenza di commit sul master, ma aumenta significativamente il parallelismo disponibile sullo slave.

```sql
-- Sul master: aumentare la finestra di group commit
-- (valore in microsecondi, 1000 = 1ms)
SET GLOBAL binlog_group_commit_sync_delay = 1000;
SET GLOBAL binlog_group_commit_sync_no_delay_count = 10;
```

---

## Quello che ha funzionato davvero

Abbiamo lavorato su tre fronti in parallelo, e il risultato finale è stato una riduzione del lag da quattro ore a meno di trenta secondi in condizioni normali.

**Fronte 1: parallel replication con 8 worker**

Dopo aver abilitato `LOGICAL_CLOCK` con 8 worker thread, il throughput dello slave è aumentato in modo significativo. Il lag accumulato si è ridotto nel giro di poche ore. Il DBA del cliente aveva già valutato questa opzione in precedenza ma aveva avuto resistenza interna perché "funzionava così da anni" — la crisi ha sbloccato la conversazione.

**Fronte 2: ottimizzazione della query batch**

La query di archiviazione notturna è stata riscritta per operare in batch più piccoli, con un indice aggiunto su `data_spedizione`:

```sql
-- Prima: un unico UPDATE enorme
UPDATE spedizioni
SET stato_elaborazione = 'archiviato'
WHERE data_spedizione < DATE_SUB(NOW(), INTERVAL 90 DAY);

-- Dopo: batch da 10.000 righe con pausa tra un batch e l'altro
-- (eseguito da uno script Python con loop + sleep)
UPDATE spedizioni
SET stato_elaborazione = 'archiviato'
WHERE data_spedizione < DATE_SUB(NOW(), INTERVAL 90 DAY)
  AND stato_elaborazione != 'archiviato'
LIMIT 10000;
```

```sql
-- Indice aggiunto
ALTER TABLE spedizioni
ADD INDEX idx_data_elaborazione (data_spedizione, stato_elaborazione);
```

Questo ha eliminato il picco di lag notturno: invece di un singolo evento da 40 minuti, lo slave applicava migliaia di piccoli eventi distribuiti nell'arco di un'ora, senza mai bloccarsi.

**Fronte 3: storage dedicato per lo slave**

Lo slave è stato spostato su storage dedicato con latenze di scrittura coerenti. Questo da solo non avrebbe risolto il problema, ma ha eliminato la variabilità che rendeva il lag imprevedibile nelle ore di punta.

---

## Monitoraggio che non mente

Dopo aver risolto il lag, abbiamo costruito un sistema di alerting che non si basasse su `Seconds_Behind_Master`.

La soluzione adottata è stata `pt-heartbeat` di Percona Toolkit, configurato per scrivere un timestamp sul master ogni secondo e misurare il ritardo sullo slave:

```bash
# Sul master: avviare il daemon che scrive il heartbeat
pt-heartbeat \
  --user=monitor_user \
  --password=*** \
  --host=mysql-master-01 \
  --database=monitoring \
  --create-table \
  --daemonize \
  --update

# Sullo slave: misurare il lag reale
pt-heartbeat \
  --user=monitor_user \
  --password=*** \
  --host=mysql-replica-01 \
  --database=monitoring \
  --monitor \
  --master-server-id=1
```

Il valore restituito da `pt-heartbeat --monitor` è il lag reale in secondi, calcolato sulla base di timestamp effettivi — non sulla posizione nel binlog né su `Seconds_Behind_Master`.

Abbiamo configurato alert su due soglie:

- **Warning a 60 secondi**: notifica al team, nessuna azione automatica
- **Critical a 300 secondi (5 minuti)**: notifica urgente + blocco automatico delle query di reportistica (redirect temporaneo al master con query in sola lettura)

Il blocco automatico era la parte più delicata: meglio restituire un errore esplicito all'utente ("dati temporaneamente non disponibili, riprovare tra qualche minuto") che restituire dati vecchi di ore senza alcun avviso.

---

## Quattro ore diventano trenta secondi

Il lag da quattro ore era il sintomo visibile di tre problemi sovrapposti: architettura single-thread, query batch non ottimizzata, storage condiviso. Nessuno dei tre, da solo, avrebbe causato quattro ore di ritardo — insieme, si amplificavano a vicenda.

La parte più interessante di questa storia non è tecnica: è che il problema esisteva da mesi, probabilmente, e nessuno se n'era accorto perché `Seconds_Behind_Master` non era monitorato sistematicamente, e quando veniva controllato manualmente dava valori che sembravano ragionevoli nelle ore di bassa attività.

Il monitoraggio del lag di replica non è un nice-to-have. È una metrica operativa che impatta direttamente sulla qualità dei dati che il business usa per prendere decisioni. Se le query di reportistica girano su un replica, il lag di quel replica è parte integrante della qualità del dato — e va trattato come tale, con alert, soglie, e un piano di risposta.

`Seconds_Behind_Master` è un punto di partenza, non una risposta. `pt-heartbeat` o il confronto dei set GTID sono strumenti molto più affidabili. E il parallel replication, su MySQL 5.7+ con `LOGICAL_CLOCK`, è oggi la configurazione di default ragionevole per qualsiasi replica che riceva carico sostenuto.

---

## Fonti ufficiali

1. MySQL 8.0 Reference Manual — [Replication Slave Status Variables: Seconds_Behind_Master](https://dev.mysql.com/doc/refman/8.0/en/show-replica-status.html)
2. Percona Toolkit Documentation — [pt-heartbeat](https://docs.percona.com/percona-toolkit/pt-heartbeat.html)
3. MySQL 8.0 Reference Manual — [GTID-Based Replication](https://dev.mysql.com/doc/refman/8.0/en/replication-gtids.html)
4. MySQL 8.0 Reference Manual — [Replication with Multithreaded Appliers](https://dev.mysql.com/doc/refman/8.0/en/replication-threads-applier.html)

---

## Glossario
- **[Binlog](/it/glossary/binlog/)** (MySQL binary log) — registro sequenziale di tutte le modifiche ai dati sul master MySQL. Base della replica: lo slave legge il binlog per sapere cosa applicare. Formato ROW, STATEMENT o MIXED.

- **[Relay log](/it/glossary/gtid/)** — copia locale del binlog del master, scritta dall'IO thread sullo slave. Lo SQL thread legge il relay log per applicare le transazioni. È il buffer tra ricezione e applicazione degli eventi.

- **[GTID](/it/glossary/binlog/)** (Global Transaction Identifier) — identificatore univoco assegnato a ogni transazione committata su un server MySQL. Formato `source_uuid:transaction_id`. Permette failover semplificato e monitoraggio preciso del lag di replica.

- **[Parallel replication](/it/glossary/relay-log/)** — modalità di applicazione degli eventi di replica che usa più worker thread invece di un singolo SQL thread. In MySQL, la modalità `LOGICAL_CLOCK` identifica transazioni eseguibili in parallelo basandosi sui commit timestamp nel binlog.

- **[pt-heartbeat](/it/glossary/gtid/)** — tool di Percona Toolkit che misura il lag di replica MySQL scrivendo timestamp sul master e confrontandoli con i valori letti sullo slave. Più affidabile di `Seconds_Behind_Master` per l'alerting in produzione.
