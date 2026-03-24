---
title: "mysqldump vs mysqlpump vs mydumper: il backup che non ti fa dormire la notte"
description: "Un database da 60 GB, un mysqldump che ci metteva tre ore e bloccava le scritture. Ho testato mysqlpump e mydumper sullo stesso ambiente, con tempi reali di dump e restore. Ecco cosa ho trovato — e perché la scelta dello strumento di backup è una decisione architetturale, non operativa."
date: "2026-04-14T08:03:00+01:00"
draft: false
translationKey: "mysqldump_mysqlpump_mydumper"
tags: ["backup", "mysqldump", "mydumper", "restore", "mariadb"]
categories: ["mysql"]
image: "mysqldump-mysqlpump-mydumper.cover.jpg"
---

La chiamata è arrivata un venerdì pomeriggio — perché queste cose succedono sempre di venerdì. Il DBA di un cliente nel settore logistico mi scrive su Teams: "Il backup notturno ha impiegato tre ore e mezza. Stamattina gli utenti si sono trovati l'applicazione lenta alle 8. Possiamo parlarne?"

Potevamo parlarne, sì. Anzi, dovevamo parlarne da un pezzo.

Il setup era un classico: un MySQL 8.0 su Rocky Linux, database da circa 60 GB, un gestionale con una trentina di tabelle InnoDB di cui quattro o cinque davvero grosse — la tabella degli ordini, quella dei movimenti di magazzino, la storicizzazione dei tracking. Il backup veniva fatto ogni notte con un mysqldump lanciato da cron alle 2:00. Aveva funzionato per anni. Il problema è che il database nel frattempo era cresciuto.

Tre ore di mysqldump significano tre ore di `--lock-all-tables` — o nel migliore dei casi tre ore di transazione consistente con `--single-transaction` che comunque tiene aperta una snapshot InnoDB per tutto il tempo. E quando il dump finisce alle 5:00 e il restore di test (che nessuno faceva) avrebbe richiesto altre quattro ore, la finestra di backup semplicemente non esiste più.

---

## Il problema vero: mysqldump è single-threaded

La prima cosa da capire su {{< glossary term="mysqldump" >}}mysqldump{{< /glossary >}} è che fa una cosa sola alla volta. Una tabella dopo l'altra, una riga dopo l'altra, un file SQL in output. Punto.

Non c'è parallelismo. Non c'è compressione nativa. Non c'è modo di dire "usa 4 thread e fai prima". È un programma nato nel 2000 — letteralmente — e il suo design riflette un'epoca in cui 60 GB erano una quantità impensabile per un database MySQL.

Il dump del cliente produceva un file SQL da 45 GB. Un singolo file monolitico che conteneva tutte le tabelle, tutte le stored procedure, tutti i trigger. Per fare un restore bastava dare in pasto quel file a `mysql` — ma ci volevano quattro ore, perché anche il restore è sequenziale.

```bash
# Il backup classico — funziona, ma scala malissimo
mysqldump --single-transaction --routines --triggers --events \
  --all-databases > /backup/full_backup.sql
```

La cosa paradossale è che mysqldump ha un vantaggio enorme: è ovunque. È incluso in ogni installazione MySQL, non richiede nulla di aggiuntivo, produce SQL leggibile. Se devi spostare una tabellina da 500 righe tra due ambienti, è perfetto. Se devi fare il backup di un database da 60 GB in produzione — no.

Ho spiegato al cliente che avevamo due alternative: mysqlpump e mydumper. Due strumenti con filosofie diverse, limiti diversi, e performance che sulla carta promettono molto ma che nella realtà vanno testate.

---

## mysqlpump: la promessa non mantenuta di Oracle

{{< glossary term="mysqlpump" >}}mysqlpump{{< /glossary >}} è arrivato con MySQL 5.7 come evoluzione ufficiale di mysqldump. La promessa era chiara: parallelismo nel dump, compressione nativa, gestione degli utenti. Sulla carta, tutto quello che mancava a mysqldump.

L'ho installato — anzi, era già lì perché è incluso nella distribuzione MySQL — e ho lanciato un primo test sul database del cliente:

```bash
mysqlpump --single-transaction --default-parallelism=4 \
  --compress-output=zlib --all-databases > /backup/full_backup.sql.zlib
```

Il risultato? 48 minuti per il dump, contro le tre ore e mezza di mysqldump. Un miglioramento importante. Ma poi ho guardato meglio.

Il parallelismo di mysqlpump funziona a livello di tabella: se hai 4 thread, dumpa 4 tabelle contemporaneamente. Il problema è che quando hai una tabella da 30 GB e tre tabelle da 50 MB, tre thread finiscono in trenta secondi e poi un thread solo si trascina per quaranta minuti sulla tabella grande. Il parallelismo è tanto efficace quanto bilanciato è il tuo database — e i database di produzione non sono mai bilanciati.

Ma il problema più serio è un altro. mysqlpump con `--single-transaction` non garantisce un backup consistente tra tabelle diverse. Lo dice la documentazione stessa, in una nota che la maggior parte delle persone non legge:

> *mysqlpump does not guarantee consistency of the dumped data across tables when using parallelism. Tables dumped in different threads may be at different points in time.*

Rileggete questa frase. Se usi il parallelismo — che è l'unico motivo per usare mysqlpump — perdi la garanzia di consistenza tra tabelle. In un database relazionale. Dove le tabelle hanno foreign key tra di loro.

Per un ambiente di sviluppo o test, può andare bene. Per un backup di produzione da cui potresti dover fare un restore in caso di disastro? No. Assolutamente no.

Un'altra nota: Oracle ha dichiarato mysqlpump **deprecato in MySQL 8.0.34** e lo ha rimosso in MySQL 8.4. Il che la dice lunga sulla fiducia che Oracle stessa aveva in questo strumento.

---

## mydumper: il tool che fa quello che promette

{{< glossary term="mydumper" >}}mydumper{{< /glossary >}} è un progetto open source nato nel 2009 dalla comunità MySQL — in particolare dal lavoro di Domas Mituzas, Andrew Hutchings e poi mantenuto da Max Bubenick. Non è un tool Oracle. Non è incluso nella distribuzione MySQL. Va installato separatamente. Ma fa una cosa che né mysqldump né mysqlpump fanno: parallelismo vero, a livello di chunk all'interno della stessa tabella.

```bash
# Installazione su Rocky Linux / CentOS
yum install https://github.com/mydumper/mydumper/releases/download/v0.16.9-1/mydumper-0.16.9-1.el8.x86_64.rpm
```

mydumper prende una tabella grande, la divide in chunk (per default basandosi sulla primary key), e assegna ogni chunk a un thread diverso. Quindi quella tabella da 30 GB non viene dumpata da un singolo thread — viene spezzata in pezzi e scaricata in parallelo.

Il dump che ho lanciato sul database del cliente:

```bash
mydumper --threads 8 --compress --trx-consistency-only \
  --outputdir /backup/mydumper_full/ \
  --logfile /var/log/mydumper.log
```

22 minuti. Contro le tre ore e mezza di mysqldump e i 48 minuti di mysqlpump.

Ma il vero vantaggio di mydumper non è solo la velocità del dump — è la velocità del restore. mydumper produce un file per ogni tabella (o per ogni chunk), e il suo compagno `myloader` li carica in parallelo:

```bash
myloader --threads 8 --directory /backup/mydumper_full/ \
  --overwrite-tables --compress-protocol
```

Il restore che con mysqldump avrebbe richiesto quattro ore, con myloader ne ha richieste una e venti. Su un database da 60 GB. Con otto thread.

---

## I numeri: test su ambiente reale

Ho fatto i test sullo stesso server del cliente — non su un ambiente di laboratorio con dischi NVMe e RAM infinita. Server reale, carico reale, dischi SATA in RAID 10.

| Operazione | mysqldump | mysqlpump (4 thread) | mydumper (8 thread) |
|------------|-----------|----------------------|---------------------|
| **Dump** | 3h 25min | 48 min | 22 min |
| **Dimensione output** | 45 GB (SQL) | 12 GB (compresso) | 9.8 GB (compresso) |
| **Restore** | ~4h (stimato) | ~3h (stimato) | 1h 20min |
| **Consistenza tra tabelle** | Sì | No (con parallelismo) | Sì |
| **Lock sulle scritture** | No* | No* | No* |

*Con `--single-transaction` su InnoDB.

Qualche nota sui numeri:
- Il restore di mysqldump e mysqlpump è stimato perché non ho fatto il test completo in produzione — troppo rischioso. I tempi sono calcolati da test parziali su un subset delle tabelle
- La compressione di mydumper (`--compress`) usa zstd di default, che comprime meglio e più velocemente di zlib
- Il restore con myloader disabilita i check delle foreign key e ricostruisce gli indici alla fine, il che accelera enormemente il caricamento

---

## Le opzioni critiche che non devi dimenticare

Qualunque strumento tu scelga, ci sono opzioni che devi includere sempre. Le ho viste dimenticate troppe volte, con conseguenze che vanno dal fastidio al disastro.

### --single-transaction

Obbligatorio su InnoDB. Senza questa opzione, il dump acquisisce lock che bloccano le scritture. Con `--single-transaction`, il dump usa una transazione con isolation level REPEATABLE READ per ottenere una snapshot consistente senza bloccare nessuno.

Attenzione: funziona solo su tabelle InnoDB. Se hai tabelle MyISAM (e sì, nel 2026 ne trovo ancora), quelle verranno comunque lockate.

### --routines --triggers --events

Stored procedure, trigger e scheduled events non vengono inclusi nel dump di default. Li devi chiedere esplicitamente. Ho visto restore che "funzionavano perfettamente" — tranne che mancavano tutti i trigger di audit e l'applicazione scriveva dati senza tracciamento.

### --set-gtid-purged (MySQL) o --gtid (mydumper)

Se usi la replica basata su GTID — e dovresti — il dump deve gestire correttamente i GTID. Se non lo fa, il restore su uno slave genera conflitti di replica che ti faranno impazzire.

### Verifica del restore

Questa non è un'opzione — è una pratica. Il backup che non verifichi è il backup che non hai. Ho un cliente che faceva backup ogni notte da tre anni. Il giorno che ha dovuto fare un restore, ha scoperto che il file era corrotto dalla settimana prima. Tre anni di backup, nessun test di restore.

```bash
# Verifica minima con mydumper: restore su istanza di test
myloader --threads 4 --directory /backup/mydumper_full/ \
  --host test-mysql-server --overwrite-tables

# Conta le righe delle tabelle principali
mysql -h test-mysql-server -e "
  SELECT table_name, table_rows
  FROM information_schema.tables
  WHERE table_schema = 'production_db'
  ORDER BY table_rows DESC LIMIT 10;"
```

---

## Quando usare cosa

Dopo trent'anni di database, la mia regola è semplice:

**mysqldump** — per database sotto i 5 GB, per migrazioni una tantum, per dump di singole tabelle, per ambienti di sviluppo dove la velocità non è critica. È il coltellino svizzero: fa tutto, lentamente, ma lo fa.

**mysqlpump** — non lo consiglio più. Deprecato da Oracle, consistenza non garantita con il parallelismo, e mydumper fa tutto quello che mysqlpump prometteva ma meglio. Se lo stai usando, pianifica la migrazione a mydumper.

**mydumper/myloader** — per qualsiasi database sopra i 10 GB in produzione. Il parallelismo vero, la consistenza garantita, il restore veloce. Richiede un'installazione separata, ma il tempo che risparmi al primo backup ripaga abbondantemente.

---

## La strategia completa: non solo logical backup

Una cosa che dico sempre ai clienti: il logical backup (mysqldump, mydumper) è **una** componente della strategia, non la strategia intera.

Per il cliente della logistica abbiamo messo in piedi questo schema:

1. **mydumper ogni notte** — backup logico completo, 8 thread, compressione zstd, retention 7 giorni
2. **Binary log continuo** — con `binlog_expire_logs_seconds` a 7 giorni, per il {{< glossary term="pitr" >}}point-in-time recovery{{< /glossary >}}
3. **Percona XtraBackup settimanale** — backup fisico a caldo, per il restore più veloce possibile in caso di disastro totale
4. **Test di restore automatico** — uno script che ogni domenica fa il restore del backup di mydumper su un'istanza di test e verifica il conteggio delle righe

Il backup logico è comodo perché è portabile — puoi fare il restore su qualsiasi versione di MySQL, su qualsiasi architettura. Ma per un database da 60 GB, un backup fisico con XtraBackup ti permette un restore in 15-20 minuti invece di un'ora e mezza. Quando il database di produzione è giù e il telefono squilla, quell'ora di differenza conta.

Il venerdì successivo, il DBA del cliente mi ha scritto di nuovo su Teams. Ma questa volta il messaggio era diverso: "Backup finito in 23 minuti. Nessun impatto sugli utenti. Grazie."

Non c'è di che. Ma la prossima volta, non aspettare che il backup ci metta tre ore per chiedermi aiuto.

------------------------------------------------------------------------

## Glossario

**[mysqldump](/it/glossary/mysqldump/)** — Utility di backup logico inclusa in ogni installazione MySQL. Produce un file SQL sequenziale con tutte le istruzioni per ricreare schema e dati. Single-threaded, affidabile ma lenta su database grandi.

**[mysqlpump](/it/glossary/mysqlpump/)** — Evoluzione di mysqldump introdotta in MySQL 5.7, con supporto per il parallelismo a livello di tabella e compressione nativa. Deprecato da Oracle in MySQL 8.0.34 per problemi di consistenza.

**[mydumper](/it/glossary/mydumper/)** — Tool open source di backup logico per MySQL/MariaDB con parallelismo reale a livello di chunk. Divide le tabelle grandi in pezzi e li esporta con thread multipli, con restore parallelo tramite myloader.

**[PITR](/it/glossary/pitr/)** — Point-in-Time Recovery: tecnica che combina un backup completo con i binary log per riportare il database a un qualsiasi momento nel tempo, non solo all'ora del backup.

**[GTID](/it/glossary/gtid/)** — Global Transaction Identifier: identificativo univoco assegnato a ogni transazione in MySQL, che semplifica la gestione della replica e il tracking delle transazioni tra master e slave.
